# 02 MUSIC SOURCING — 음원 출처·권리·곡 대장

> 2026-10 기준 정리. 각 서비스 약관은 바뀌므로 **새로 가입·결제할 때마다 약관을 직접 확인**하고 확인한 날짜를 대장에 남긴다.

## 1. 출처별 판단

| 출처 | 사용 | 조건 |
|---|---|---|
| **Suno (기존·신규 모두)** | X | 사용자 결정(2026-10-04): Suno 음원은 쓰지 않는다 |
| **ElevenLabs Music** | O (주력 후보) | 유료 플랜의 상업 이용 범위 확인. 생성 시 플랜·날짜 기록 |
| Udio | X | 플랫폼 밖 반출 제한 |
| 음원 라이브러리(Epidemic·Artlist 등) | X | 대부분 음악 중심 영상·컴필레이션 금지 |
| **인디 프로듀서 의뢰·협업** | O (장기) | 서면 계약: 유튜브 수익화·Content ID·크레디트 표기 범위 명시 |
| 직접 제작(DAW + Synthesizer V 등) | O | 보컬 합성은 상업 이용 가능한 보이스뱅크만 |
| 기존 상업 음원(가수 곡) | X | 권리 없음 |

## 2. Content ID 주의

- AI 생성곡이 다른 채널·유통사에 등록돼 있으면 우리 영상에 클레임이 걸릴 수 있다.
- 우리 곡을 직접 유통(DistroKid 등)해 Content ID를 걸 경우, **자기 채널은 화이트리스트** 등록.
- 업로드 후 저작권 탭 확인은 04_UPLOAD 체크리스트에 있음.

## 3. 곡 대장 `tracks/tracks.csv`

| 열 | 내용 |
|---|---|
| `id` | `T0001` 형식, 파일명과 같게 (`tracks/audio/T0001.wav`) |
| `title` | 곡 제목(표시용) |
| `line` | `JP` / `KR` / `BOTH` |
| `source` | `elevenlabs` / `collab:이름` / `self` |
| `plan` | 생성 당시 플랜 (`eleven-creator`, `eleven-pro` 등) |
| `created` | 생성일 YYYY-MM-DD |
| `rights` | `cleared` / `hold` / `rejected` |
| `rights_note` | 근거(약관 확인일, 계약서 파일명 등) |
| `vocal` | `vocal` / `inst` |
| `bpm`, `key`, `energy` | 흐름 설계용 (energy 1~5) |
| `mood` | 자유 태그 `night;drive;rain` |
| `last_used` | 마지막 사용 플리 ID |

## 4. 프롬프트

ElevenLabs용 프롬프트 세트: `prompts/elevenlabs-prompts.md`. 생성에 쓴 프롬프트는 `rights_note`나 별도 메모에 남긴다(같은 톤 재생성용).

## 5. 생성 자동화 (ElevenLabs API)

`scripts/generate_tracks.py` 가 `playlists/PLxxx/design.md` 의 프롬프트로 곡을 만든다. 키는 환경 변수 `ELEVENLABS_API_KEY`(클라우드 환경 설정에 등록, 채팅에 붙여넣지 않는다).

1. 후보 생성: `python3 scripts/generate_tracks.py playlists/PL001/design.md --takes 2` → `tracks/audio/candidates/T0001_1.mp3` … (git 제외, 생성 기록은 `tracks/generation-log.csv`)
2. 사용자가 듣고 고른다.
3. 확정: `--pick T0001=2 --title "곡 제목" --plan <플랜>` → `tracks/audio/T0001.mp3`(git에 커밋) + 대장 등록(`rights=hold`)
4. 플랜 약관의 상업 이용 범위를 확인하면 `rights=cleared` 로 바꾼다.

음원은 MP3 192kbps(곡당 약 6MB)로 받아 확정본만 커밋한다.
