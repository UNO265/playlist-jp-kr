# 03 VIDEO — 비주얼·빌드·렌더링

## 1. 비주얼

- 영상마다 **콘셉트 장면 하나**: 1920×1080 이미지 또는 짧은 루프 영상(5~20초, 처음과 끝이 이어지게).
- JP 시티팝: 밤 도시·차창·네온·80s 애니풍 / 칠팝: 방·창가·노을. KR 팝: 계절감 있는 거리·카페·한강.
- 이미지 출처도 권리 확인(직접 제작, 상업 이용 가능한 생성 도구, 라이선스 확보 사진). 기존 애니·영화 캡처 금지.
- 이전 영상과 같은 그림 재사용 금지. 시리즈 통일감은 로고·글자 위치로 낸다.
- 파일: `assets/visuals/PLxxx.png` 또는 `PLxxx.mp4`.
- 직접 그리는 일러스트는 `assets/visuals/src/PLxxx.svg` 로 만들고 `NODE_PATH=$(npm root -g) node scripts/render_svg.js assets/visuals/src/PLxxx.svg assets/visuals/PLxxx.png` 로 렌더링(Playwright 필요). 권리 문제 없음.

## 2. 빌드

필요: Python 3.9+, `pip install pyyaml`, ffmpeg.

```bash
# 오디오만 먼저 만들어 흐름 확인
python3 scripts/build_playlist.py playlists/PL001/playlist.yaml --audio-only

# 최종 영상
python3 scripts/build_playlist.py playlists/PL001/playlist.yaml

# 앞 3분만 미리보기
python3 scripts/build_playlist.py playlists/PL001/playlist.yaml --preview 180
```

하는 일:
1. `tracks.csv`에서 곡을 찾고 `rights=cleared`가 아니면 **중단**
2. 곡 사이 크로스페이드(`crossfade`초)로 연결, 라우드니스 -14 LUFS 정규화
3. 이미지/루프 영상 + 오디오로 1080p 영상
4. `out/PLxxx/`에 `PLxxx.mp4`, `chapters.txt`(YouTube 타임스탬프), `description.txt`(설명란 초안), `credits.txt`

## 3. 렌더 전 확인

- [ ] 미리보기로 첫 곡 시작·전환 2곳 이상 들어봄
- [ ] 곡 사이 무음·튀는 소리 없음
- [ ] 챕터 시간이 실제 곡 시작과 맞음 (00:00 시작, 곡 3개 이상)
- [ ] 비주얼 해상도 1920×1080, 글자 잘림 없음
