# 02 MUSIC SOURCING — 음원 출처·권리·곡 대장

> 2026-10 기준 정리. 각 서비스 약관은 바뀌므로 **새로 가입·결제할 때마다 약관을 직접 확인**하고 확인한 날짜를 대장에 남긴다.

## 1. 출처별 판단

| 출처 | 사용 | 조건 |
|---|---|---|
| **기존 Suno 곡** | 조건부 O | **유료 플랜(Pro/Premier) 가입 중 생성한 곡만.** 무료 플랜 생성곡은 상업 이용 불가 → `hold`. 생성일·플랜을 확인할 수 없으면 `hold` |
| **ElevenLabs Music** | O (주력 후보) | 유료 플랜의 상업 이용 범위 확인. 생성 시 플랜·날짜 기록 |
| Suno 신규 | △ | 유료 플랜이어도 다운로드 월 20/60곡 제한 → 보조용 |
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
| `source` | `suno` / `elevenlabs` / `collab:이름` / `self` |
| `plan` | 생성 당시 플랜 (`suno-pro`, `eleven-creator` 등) |
| `created` | 생성일 YYYY-MM-DD |
| `rights` | `cleared` / `hold` / `rejected` |
| `rights_note` | 근거(약관 확인일, 계약서 파일명 등) |
| `vocal` | `vocal` / `inst` |
| `bpm`, `key`, `energy` | 흐름 설계용 (energy 1~5) |
| `mood` | 자유 태그 `night;drive;rain` |
| `last_used` | 마지막 사용 플리 ID |

## 4. 기존 Suno 곡 정리 순서

1. Suno 계정의 결제 이력으로 **유료 기간**을 확인한다.
2. 곡별 생성일이 유료 기간 안이면 `cleared`, 아니면 `hold`.
3. 이미 업로드한 영상에 쓴 곡 중 `hold`가 있으면 사용자에게 보고한다(영상 처리 방침은 사용자가 정함).

## 5. 프롬프트

ElevenLabs용 프롬프트 세트: `prompts/elevenlabs-prompts.md`. 생성에 쓴 프롬프트는 `rights_note`나 별도 메모에 남긴다(같은 톤 재생성용).
