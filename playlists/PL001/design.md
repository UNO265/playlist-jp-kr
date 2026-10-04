# PL001 설계 — 일요일 오전 10시, 카페 작업 플리

| 항목 | 내용 |
|---|---|
| 라인 | KR |
| 콘셉트 | 일요일 오전 10시, 햇살 드는 카페 창가 자리에서 노트북을 켜고 작업하는 1시간 반 |
| 길이 | 약 90분 / 22곡 (곡당 3:50~4:20) |
| 구성 | 보컬 15곡(여 7·남 7·듀엣 1) + 인스트 7곡(32%) |
| 에너지 | 2~3 유지. 작업 방해 없이, 정점도 "밝아지는 정도"까지만 |
| 제목안 | `일요일 오전 10시, 창가 자리에서 작업할 때 듣는 플리 ☕` / `[Playlist] 햇살 드는 카페 창가, 집중이 잘 되는 일요일 오전` |
| 비주얼 | 햇살 드는 카페 창가, 노트북·커피잔, 바깥 가을 가로수. 1920×1080 |

## 흐름

```
energy
 3 |  ▲  ▲   ▲  ▲▲ ▲  ▲▲▲
 2 | ▲ ▲  ▲▲ ▲▲  ▲  ▲   ▲▲▲▲▲▲▲
   +---------------------------------
    도착·주문  집중1   밝아짐  집중2·여운
    1-4       5-11    12-15   16-22
```

- **1-4 도착·주문**: 따뜻하고 밝은 어쿠스틱. 첫 곡이 콘셉트 대표곡.
- **5-11 집중 1**: 템포를 조금 낮추고 인스트를 섞어 작업 몰입.
- **12-15 밝아짐**: 11시 무렵 햇살이 강해지는 느낌. 템포 98~106, 박수·셰이커.
- **16-22 집중 2·여운**: 다시 차분하게. 22번(G, 84)이 1번(G, 92)으로 자연스럽게 돌아가 반복 재생에 맞춤.
- 이웃 곡 BPM 차이 ≤ 15, 키는 같은 조·5도·나란한조로만 이동.

## ElevenLabs 생성 설정

- 길이: **4:00 전후** (3:50~4:20)
- 모든 프롬프트 끝에 공통 꼬리말:
  `High-fidelity studio mix, warm and natural, intimate cafe atmosphere, no spoken intro, intro under 5 seconds, natural ending.`
- 곡마다 2~3개 생성 → 가장 콘셉트에 맞는 1개 선택. 결과를 듣고 **실제 BPM·키·energy**를 `tracks.csv`에 기록(프롬프트 값과 다를 수 있음).
- 가사 테마는 프롬프트에 넣되, 생성된 가사에 실제 가수·곡명·브랜드가 나오면 버린다.

## 곡별 설계

| # | ID | 구간 | 보컬 | BPM | 키 | E | 가사 테마 / 역할 |
|---|---|---|---|---|---|---|---|
| 1 | T0001 | 도착 | 여 | 92 | G | 2 | 문 열고 들어서는 커피 향 — **대표곡** |
| 2 | T0002 | 도착 | 남 | 96 | D | 3 | 늦잠 없이 일어난 일요일의 작은 뿌듯함 |
| 3 | T0003 | 도착 | 인스트 | 88 | G | 2 | 주문 기다리는 동안 |
| 4 | T0004 | 도착 | 여 | 94 | C | 3 | 창가 자리, 햇살이 키보드 위에 |
| 5 | T0005 | 집중1 | 인스트 | 84 | Am | 2 | 작업 시작 |
| 6 | T0006 | 집중1 | 남 | 90 | C | 2 | 할 일 목록을 하나씩 지우는 기분 |
| 7 | T0007 | 집중1 | 여 | 86 | F | 3 | 식어가는 라떼, 그래도 좋은 오전 |
| 8 | T0008 | 집중1 | 인스트 | 80 | Dm | 2 | 깊은 몰입 |
| 9 | T0009 | 집중1 | 남 | 92 | F | 3 | 창밖 가로수, 천천히 물드는 가을 |
| 10 | T0010 | 집중1 | 여 | 96 | B♭ | 3 | 서두르지 않아도 되는 하루 |
| 11 | T0011 | 집중1 | 인스트 | 88 | F | 2 | 숨 고르기 |
| 12 | T0012 | 밝아짐 | 남 | 98 | C | 3 | 리필한 커피, 다시 힘 내기 |
| 13 | T0013 | 밝아짐 | 여 | 102 | G | 3 | 오늘은 잘 될 것 같은 예감 |
| 14 | T0014 | 밝아짐 | 듀엣 | 106 | D | 3 | 옆자리 사람과 눈이 마주친 순간 — **정점** |
| 15 | T0015 | 밝아짐 | 남 | 104 | G | 3 | 정오가 가까워지는 햇살 |
| 16 | T0016 | 집중2 | 인스트 | 98 | C | 2 | 다시 집중 |
| 17 | T0017 | 집중2 | 여 | 90 | Am | 2 | 조용히 흘러가는 시간이 고마운 |
| 18 | T0018 | 집중2 | 남 | 86 | Em | 2 | 오래 미뤄둔 일을 마무리하며 |
| 19 | T0019 | 집중2 | 인스트 | 82 | G | 2 | 마지막 몰입 |
| 20 | T0020 | 여운 | 여 | 80 | C | 2 | 노트북을 덮고 남은 커피 한 모금 |
| 21 | T0021 | 여운 | 남 | 78 | Am | 2 | 카페를 나서며, 다음 일요일을 기다리는 |
| 22 | T0022 | 여운 | 인스트 | 84 | G | 2 | 엔딩 → 1번으로 이어짐 |

## 프롬프트 (곡별, 공통 꼬리말 붙여서 사용)

```
T0001  Warm Korean acoustic pop, 92 BPM, G major, fingerpicked acoustic guitar, soft piano, brushed drums, light shaker, gentle female vocals in Korean, lyrics about stepping into a sunlit cafe on a Sunday morning and the smell of coffee
T0002  Bright Korean acoustic pop, 96 BPM, D major, strummed acoustic guitar, warm bass, soft claps, relaxed male vocals in Korean, lyrics about waking up early on a quiet Sunday and feeling quietly proud
T0003  Instrumental acoustic cafe music, 88 BPM, G major, nylon guitar melody, soft upright bass, light brushes, calm and cozy
T0004  Korean acoustic pop, 94 BPM, C major, piano and acoustic guitar, light percussion, airy female vocals in Korean, lyrics about a window seat and morning sunlight falling on the keyboard
T0005  Instrumental lo-fi acoustic, 84 BPM, A minor, soft Rhodes, mellow guitar, gentle boom bap drums, warm and focused
T0006  Soft Korean pop, 90 BPM, C major, muted electric guitar, warm Rhodes, light drums, calm male vocals in Korean, lyrics about crossing tasks off a to-do list one by one
T0007  Korean acoustic pop ballad, 86 BPM, F major, piano, cello, brushed drums, tender female vocals in Korean, lyrics about a latte slowly getting cold on a peaceful morning
T0008  Instrumental ambient piano, 80 BPM, D minor, felt piano, soft pads, subtle vinyl texture, deep focus
T0009  Korean indie folk pop, 92 BPM, F major, acoustic guitar, glockenspiel, soft bass, warm male vocals in Korean, lyrics about autumn trees outside the cafe window slowly changing color
T0010  Korean acoustic pop, 96 BPM, B flat major, piano, acoustic guitar, light shaker, gentle female vocals in Korean, lyrics about a day with nothing to rush
T0011  Instrumental jazzy cafe guitar, 88 BPM, F major, clean jazz guitar, upright bass, brushed drums, relaxed
T0012  Upbeat Korean acoustic pop, 98 BPM, C major, strummed guitar, claps, warm bass, friendly male vocals in Korean, lyrics about a coffee refill and getting a second wind
T0013  Bright Korean pop, 102 BPM, G major, acoustic guitar, light synth pad, tambourine, sweet female vocals in Korean, lyrics about a feeling that today will go well
T0014  Bright Korean acoustic pop duet, 106 BPM, D major, strummed guitars, claps, glockenspiel, male and female duet vocals in Korean, lyrics about briefly meeting eyes with a stranger at the next table
T0015  Korean pop, 104 BPM, G major, groovy bass, clean electric guitar, piano, warm male vocals in Korean, lyrics about late morning sunlight as noon approaches
T0016  Instrumental acoustic pop, 98 BPM, C major, acoustic guitar melody, piano, light shaker, cheerful but calm
T0017  Soft Korean pop ballad, 90 BPM, A minor, piano, soft strings, light drums, gentle female vocals in Korean, lyrics about being grateful for quietly passing time
T0018  Mellow Korean R&B pop, 86 BPM, E minor, smooth Rhodes, soft bass, light drums, warm male vocals in Korean, lyrics about finally finishing a long postponed task
T0019  Instrumental lo-fi piano, 82 BPM, G major, soft piano, warm bass, gentle drums, rain-free sunny ambience
T0020  Korean acoustic ballad, 80 BPM, C major, acoustic guitar, piano, soft female vocals in Korean, lyrics about closing the laptop and the last sip of coffee
T0021  Korean acoustic ballad, 78 BPM, A minor, fingerpicked guitar, cello, intimate male vocals in Korean, lyrics about leaving the cafe and looking forward to next Sunday
T0022  Instrumental acoustic outro, 84 BPM, G major, nylon guitar and piano duet, soft and warm, gently resolving
```
