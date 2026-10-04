#!/usr/bin/env python3
"""Generate track candidates with the ElevenLabs Music API from a playlist design.md.

  # 후보 생성 (곡당 --takes 개, 이미 있는 파일은 건너뜀)
  python3 scripts/generate_tracks.py playlists/PL001/design.md --takes 2
  python3 scripts/generate_tracks.py playlists/PL001/design.md --ids T0001,T0002 --dry-run

  # 들어보고 고른 후보를 확정 → tracks/audio/T0001.mp3 + tracks.csv 등록(rights=hold)
  python3 scripts/generate_tracks.py playlists/PL001/design.md --pick T0001=2 --title "커피 향" --plan eleven-creator

API key: environment variable ELEVENLABS_API_KEY. See docs/guide/02_MUSIC_SOURCING.md.
"""
import argparse
import csv
import datetime as dt
import json
import os
import re
import shutil
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
AUDIO_DIR = ROOT / "tracks" / "audio"
CAND_DIR = AUDIO_DIR / "candidates"
LEDGER = ROOT / "tracks" / "tracks.csv"
GEN_LOG = ROOT / "tracks" / "generation-log.csv"
API_URL = "https://api.elevenlabs.io/v1/music?output_format=mp3_48000_192"


def fail(msg):
    sys.exit(f"[gen] ERROR: {msg}")


def parse_design(path):
    text = Path(path).read_text(encoding="utf-8")
    tail = re.search(r"공통 꼬리말:\s*\n\s*`([^`]+)`", text)
    if not tail:
        fail("common tail (공통 꼬리말) not found in design.md")
    block = text.split("## 프롬프트", 1)[-1]
    prompts = dict(re.findall(r"^(T\d{4})\s+(.+)$", block, re.M))
    if not prompts:
        fail("no prompts found under '## 프롬프트'")
    # planned bpm/key/energy/line from the design table: | # | ID | 구간 | 보컬 | BPM | 키 | E | 테마 |
    table = {}
    for row in re.findall(r"^\|\s*\d+\s*\|\s*(T\d{4})\s*\|([^\n]+)$", text, re.M):
        cells = [c.strip() for c in row[1].split("|")]
        table[row[0]] = {"vocal": "inst" if cells[1] == "인스트" else "vocal",
                         "bpm": cells[2], "key": cells[3], "energy": cells[4]}
    line = re.search(r"\|\s*라인\s*\|\s*(\w+)\s*\|", text)
    return prompts, tail.group(1), table, line.group(1) if line else ""


def compose(prompt, length_s, instrumental, model, out_path):
    key = os.environ.get("ELEVENLABS_API_KEY")
    if not key:
        fail("ELEVENLABS_API_KEY is not set")
    body = {"prompt": prompt, "music_length_ms": length_s * 1000, "model_id": model,
            "force_instrumental": instrumental}
    req = urllib.request.Request(API_URL, data=json.dumps(body).encode(), method="POST",
                                 headers={"xi-api-key": key, "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=600) as res:
            out_path.write_bytes(res.read())
    except urllib.error.HTTPError as e:
        fail(f"API {e.code}: {e.read().decode(errors='replace')[:500]}")


def log_generation(row):
    new = not GEN_LOG.exists()
    with GEN_LOG.open("a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(row))
        if new:
            w.writeheader()
        w.writerow(row)


def generate(args, prompts, tail):
    ids = args.ids.split(",") if args.ids else sorted(prompts)
    missing = [i for i in ids if i not in prompts]
    if missing:
        fail(f"no prompt for {missing}")
    CAND_DIR.mkdir(parents=True, exist_ok=True)
    for tid in ids:
        prompt = f"{prompts[tid]}. {tail}"
        instrumental = prompts[tid].lower().startswith("instrumental")
        for take in range(1, args.takes + 1):
            out = CAND_DIR / f"{tid}_{take}.mp3"
            if out.exists():
                print(f"[gen] skip {out.name} (exists)")
                continue
            print(f"[gen] {out.name}  inst={instrumental}  {args.length}s")
            if args.dry_run:
                print(f"      {prompt}")
                continue
            compose(prompt, args.length, instrumental, args.model, out)
            log_generation({"file": out.name, "id": tid, "take": take, "model": args.model,
                            "length_s": args.length, "generated_at": dt.datetime.now().isoformat(timespec="seconds"),
                            "prompt": prompt})


def pick(args, table, line):
    tid, take = args.pick.split("=")
    src = CAND_DIR / f"{tid}_{take}.mp3"
    if not src.exists():
        fail(f"{src} not found")
    if not args.title or not args.plan:
        fail("--pick needs --title and --plan")
    shutil.copy2(src, AUDIO_DIR / f"{tid}.mp3")

    with LEDGER.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fields, rows = reader.fieldnames, [r for r in reader if r["id"] != tid]
    plan = table.get(tid, {})
    rows.append({
        "id": tid, "title": args.title, "line": line, "source": "elevenlabs", "plan": args.plan,
        "created": dt.date.today().isoformat(), "rights": "hold",
        "rights_note": f"take {take}; flip to cleared after plan terms check",
        "vocal": plan.get("vocal", ""), "bpm": plan.get("bpm", ""), "key": plan.get("key", ""),
        "energy": plan.get("energy", ""), "mood": "", "last_used": "",
    })
    rows.sort(key=lambda r: r["id"])
    with LEDGER.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)
    print(f"[gen] {src.name} -> tracks/audio/{tid}.mp3, ledger updated (rights=hold)")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("design")
    ap.add_argument("--ids", help="comma-separated, default all")
    ap.add_argument("--takes", type=int, default=2)
    ap.add_argument("--length", type=int, default=240, help="seconds (default 240)")
    ap.add_argument("--model", default="music_v1", help="music_v1 / music_v2 / music_v2_5")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--pick", metavar="ID=TAKE")
    ap.add_argument("--title")
    ap.add_argument("--plan")
    args = ap.parse_args()

    prompts, tail, table, line = parse_design(args.design)
    if args.pick:
        pick(args, table, line)
    else:
        generate(args, prompts, tail)


if __name__ == "__main__":
    main()
