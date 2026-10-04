# playlist-jp-kr

일본 칠팝·시티팝 / 한국 팝 **롱폼 플레이리스트 영상** 채널 제작 레포.

## 지침

| 문서 | 언제 |
|---|---|
| **[00_CORE](docs/guide/00_CORE.md)** | 항상. 원칙·정책·제작 순서 |
| [01_CURATION](docs/guide/01_CURATION.md) | 콘셉트·곡 선정·곡 순서 |
| [02_MUSIC_SOURCING](docs/guide/02_MUSIC_SOURCING.md) | 음원 출처·권리·곡 대장 |
| [03_VIDEO](docs/guide/03_VIDEO.md) | 비주얼·빌드·렌더링 |
| [04_UPLOAD](docs/guide/04_UPLOAD.md) | 제목·설명·태그·업로드·성과 기록 |

양식: `docs/templates/`. 곡 대장: `tracks/tracks.csv`. 플리: `playlists/PLxxx/playlist.yaml`. 빌드: `scripts/build_playlist.py`.

## 꼭 기억할 것

- **권리 확인 안 된 곡은 쓰지 않는다.** `tracks.csv`의 `rights`가 `cleared`가 아니면 빌드가 거부한다.
- 일반 음원 라이브러리(Epidemic·Artlist 등)는 대부분 "음악이 주인공인 영상"을 금지 → 플리에 쓰지 않는다.
- **사람이 큐레이션한 흔적**(콘셉트·장면·곡 순서 이유·고유 비주얼)이 모든 영상에 있어야 한다. AI 곡 나열 영상 금지(YouTube inauthentic content 정책).
- AI로 만든 음원은 업로드 시 **변경·합성 콘텐츠 공개**를 켜고 설명란에 표기한다.
- 단계마다 사용자 확정: 콘셉트 → 트랙리스트 → 비주얼 → 렌더링 → 업로드 문구.
- 일본 채널 문구는 일본어, 한국 채널 문구는 한국어. 사용자와의 대화는 한국어.
