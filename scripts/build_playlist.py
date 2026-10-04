#!/usr/bin/env python3
"""Build a long-form playlist video from playlists/PLxxx/playlist.yaml.

Steps: rights check -> crossfade + loudness-normalize audio -> mux with visual
-> chapters.txt / description.txt / credits.txt. See docs/guide/03_VIDEO.md.
"""
import argparse
import csv
import json
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
AUDIO_DIR = ROOT / "tracks" / "audio"
LEDGER = ROOT / "tracks" / "tracks.csv"
AUDIO_EXTS = (".wav", ".flac", ".mp3", ".m4a")
IMAGE_EXTS = (".png", ".jpg", ".jpeg")

AI_NOTICE = {
    "JP": "本チャンネルの楽曲はAIツールを用いて制作し、選曲・曲順は人の手でキュレーションしています。",
    "KR": "이 채널의 음원은 AI 도구를 활용해 제작했으며, 선곡과 곡 순서는 직접 큐레이션했습니다.",
}
LABELS = {
    "JP": {"tracklist": "Tracklist", "credits": "Credits"},
    "KR": {"tracklist": "Tracklist", "credits": "Credits"},
}


def fail(msg):
    sys.exit(f"[build] ERROR: {msg}")


def run(cmd):
    print("[build] $ " + " ".join(str(c) for c in cmd[:6]) + (" ..." if len(cmd) > 6 else ""))
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        fail(f"ffmpeg failed:\n{res.stderr[-2000:]}")


def duration(path):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json", str(path)],
        capture_output=True, text=True, check=True,
    ).stdout
    return float(json.loads(out)["format"]["duration"])


def fmt_ts(sec, long_form):
    sec = int(sec)
    h, m, s = sec // 3600, sec % 3600 // 60, sec % 60
    return f"{h}:{m:02d}:{s:02d}" if long_form else f"{m:02d}:{s:02d}"


def load_ledger():
    if not LEDGER.exists():
        fail(f"{LEDGER} not found")
    with LEDGER.open(newline="", encoding="utf-8") as f:
        return {row["id"]: row for row in csv.DictReader(f)}


def find_audio(track_id):
    for ext in AUDIO_EXTS:
        p = AUDIO_DIR / f"{track_id}{ext}"
        if p.exists():
            return p
    fail(f"audio file for {track_id} not found in {AUDIO_DIR}")


def resolve_tracks(pl, ledger):
    ids = [t["id"] for t in pl["tracks"]]
    if len(ids) != len(set(ids)):
        fail("same track appears twice in this playlist")
    problems, tracks = [], []
    for t in pl["tracks"]:
        row = ledger.get(t["id"])
        if row is None:
            problems.append(f"{t['id']}: not in tracks.csv")
            continue
        if row["rights"] != "cleared":
            problems.append(f"{t['id']} ({row['title']}): rights={row['rights'] or 'empty'}")
            continue
        tracks.append({**row, "note": t.get("note", ""), "path": find_audio(t["id"])})
    if problems:
        fail("rights check failed, build stopped:\n  " + "\n  ".join(problems))
    if len(tracks) < 3:
        fail("need at least 3 tracks (YouTube chapters require 3+)")
    return tracks


def build_audio(tracks, xf, out_path, preview):
    durs = [duration(t["path"]) for t in tracks]
    if min(durs) <= 2 * xf:
        fail(f"a track is shorter than 2x crossfade ({xf}s)")
    cmd = ["ffmpeg", "-y", "-hide_banner"]
    for t in tracks:
        cmd += ["-i", str(t["path"])]
    if xf > 0:
        chain, prev = [], "[0:a]"
        for i in range(1, len(tracks)):
            label = f"[x{i}]"
            chain.append(f"{prev}[{i}:a]acrossfade=d={xf}:c1=tri:c2=tri{label}")
            prev = label
    else:
        chain = ["".join(f"[{i}:a]" for i in range(len(tracks))) + f"concat=n={len(tracks)}:v=0:a=1[x0]"]
        prev = "[x0]"
    chain.append(f"{prev}loudnorm=I=-14:TP=-1:LRA=11,aresample=48000[out]")
    cmd += ["-filter_complex", ";".join(chain), "-map", "[out]"]
    if preview:
        cmd += ["-t", str(preview)]
    cmd += ["-c:a", "aac", "-b:a", "320k", str(out_path)]
    run(cmd)

    # Chapter = middle of each crossfade (where the new track becomes dominant).
    starts, t = [], 0.0
    for i, d in enumerate(durs):
        starts.append(0.0 if i == 0 else t + xf / 2)
        t += d - xf
    total = sum(durs) - xf * (len(durs) - 1)
    return starts, total


def build_video(visual, audio, out_path):
    if not visual.exists():
        fail(f"visual not found: {visual}")
    scale = "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,format=yuv420p"
    if visual.suffix.lower() in IMAGE_EXTS:
        vin = ["-loop", "1", "-framerate", "2", "-i", str(visual)]
        venc = ["-c:v", "libx264", "-tune", "stillimage", "-preset", "medium", "-crf", "18", "-r", "2"]
    else:
        vin = ["-stream_loop", "-1", "-i", str(visual)]
        venc = ["-c:v", "libx264", "-preset", "medium", "-crf", "18", "-r", "30"]
    run(["ffmpeg", "-y", "-hide_banner", *vin, "-i", str(audio), "-map", "0:v", "-map", "1:a",
         "-vf", scale, *venc, "-c:a", "copy", "-shortest", "-movflags", "+faststart", str(out_path)])


def write_texts(pl, tracks, starts, total, out_dir):
    line = pl.get("line", "JP")
    long_form = total >= 3600
    chapters = [f"{fmt_ts(s, long_form)} {t['title']}" for s, t in zip(starts, tracks)]
    credits = [f"{t['id']} {t['title']} — {t['source']} ({t['plan']}, {t['created']})" for t in tracks]

    (out_dir / "chapters.txt").write_text("\n".join(chapters) + "\n", encoding="utf-8")
    (out_dir / "credits.txt").write_text("\n".join(credits) + "\n", encoding="utf-8")
    desc = [
        pl.get("concept", ""),
        "",
        pl.get("curation_note", "").strip(),
        "",
        f"■ {LABELS[line]['tracklist']}",
        *chapters,
        "",
        f"■ {LABELS[line]['credits']}",
        AI_NOTICE[line],
        "",
        " ".join(pl.get("hashtags", [])),
    ]
    (out_dir / "description.txt").write_text("\n".join(desc).strip() + "\n", encoding="utf-8")
    print(f"[build] total {fmt_ts(total, True)} / {len(tracks)} tracks")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("playlist", help="playlists/PLxxx/playlist.yaml")
    ap.add_argument("--audio-only", action="store_true", help="skip video render")
    ap.add_argument("--preview", type=int, metavar="SEC", help="render only the first SEC seconds")
    args = ap.parse_args()

    pl = yaml.safe_load(Path(args.playlist).read_text(encoding="utf-8"))
    if pl.get("line") not in AI_NOTICE:
        fail("line must be JP or KR")
    tracks = resolve_tracks(pl, load_ledger())

    out_dir = ROOT / "out" / pl["id"]
    out_dir.mkdir(parents=True, exist_ok=True)
    suffix = "_preview" if args.preview else ""
    audio = out_dir / f"{pl['id']}{suffix}.m4a"
    starts, total = build_audio(tracks, float(pl.get("crossfade", 3)), audio, args.preview)
    write_texts(pl, tracks, starts, total, out_dir)

    if not args.audio_only:
        build_video(ROOT / pl["visual"], audio, out_dir / f"{pl['id']}{suffix}.mp4")
    print(f"[build] done -> {out_dir.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
