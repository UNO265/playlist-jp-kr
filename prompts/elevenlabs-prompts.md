# ElevenLabs Music 프롬프트 세트

영어 프롬프트가 장르 제어가 가장 안정적이다. 가사 언어는 `vocals in Japanese` / `vocals in Korean`으로 지정.
**실제 가수·밴드 이름은 프롬프트에 넣지 않는다**(권리·정책 리스크).

## 공통 꼬리말

```
High-fidelity studio mix, warm analog character, clean vocals, no spoken intro, no fade-in longer than 2 seconds, natural ending.
```

## JP — City Pop

| 장면 | 프롬프트 |
|---|---|
| 밤 드라이브 | `1980s Japanese city pop, 112 BPM, slap bass, Rhodes electric piano, bright brass stabs, gated reverb drums, female vocals in Japanese, nostalgic night highway mood` |
| 바닷가 오후 | `Japanese city pop with AOR influence, 98 BPM, clean funk guitar cutting, lush string pads, saxophone solo, male vocals in Japanese, sunny seaside afternoon` |
| 도시의 새벽 | `mellow Japanese city pop ballad, 84 BPM, fretless bass, soft synth pads, DX7 electric piano, breathy female vocals in Japanese, quiet city at dawn` |
| 인스트 | `instrumental 1980s city pop fusion, 108 BPM, synth lead melody, slap bass, Rhodes, tight drums, neon night city` |

## JP — Chill Pop

| 장면 | 프롬프트 |
|---|---|
| 비 오는 카페 | `Japanese chill pop, 88 BPM, lo-fi drums, acoustic guitar, soft Rhodes, gentle female vocals in Japanese, rainy cafe window` |
| 방 안 노을 | `bedroom chill pop, 92 BPM, warm bass, muted guitar, vinyl texture, airy female vocals in Japanese, sunset in a small apartment` |
| 작업용 인스트 | `instrumental chillhop with city pop chords, 80 BPM, jazzy Rhodes, soft boom bap drums, calm focus` |

## KR — Pop

| 장면 | 프롬프트 |
|---|---|
| 퇴근길 | `modern Korean pop, 104 BPM, groovy bass, clean electric guitar, light synths, warm male vocals in Korean, evening commute by the river` |
| 카페 작업 | `acoustic Korean pop, 90 BPM, acoustic guitar, piano, light percussion, soft female vocals in Korean, cozy cafe morning` |
| 봄 산책 | `bright Korean indie pop, 116 BPM, jangly guitars, claps, sweet female vocals in Korean, spring walk` |
| 밤 감성 | `R&B tinged Korean pop ballad, 76 BPM, smooth keys, sub bass, intimate male vocals in Korean, late night city lights` |

## 기록

생성할 때마다 `tracks.csv`에 `source=elevenlabs`, `plan`, `created`, `bpm`(프롬프트 값이 아니라 결과를 듣고), `energy`를 채운다.
