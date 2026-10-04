# playlist-jp-kr

일본 칠팝·시티팝 / 한국 팝 롱폼 플레이리스트 영상 제작 레포.

- 지침: [`CLAUDE.md`](CLAUDE.md) → `docs/guide/00~04`
- 곡 대장: `tracks/tracks.csv` (음원 파일은 `tracks/audio/T0001.wav`, git에는 올리지 않음)
- 플리 정의: `playlists/PLxxx/playlist.yaml` (양식 `docs/templates/playlist.yaml`)
- 빌드: `pip install pyyaml` + ffmpeg 후 `python3 scripts/build_playlist.py playlists/PL001/playlist.yaml`
- ElevenLabs 프롬프트: `prompts/elevenlabs-prompts.md`
