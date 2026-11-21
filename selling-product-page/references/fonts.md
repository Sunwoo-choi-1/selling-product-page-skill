# 상세페이지 폰트 카탈로그 (분위기별)

목차: 고르는 법 (3초) · 분위기별 조합 (fonts.css의 data-font 값) · 전체 목록 (CDN 확인됨) · 라이선스 주의 · 출처

조사일 2026-10-27. **전부 무료 상업용**이고, 전부 CDN 링크가 살아있는 걸 확인했다(fonts-archive 66종, Google Fonts 34종 응답 200).
폰트 파일은 동봉하지 않는다 — 한글 폰트는 하나에 2~10MB라 zip이 터지고, 재배포 조건이 폰트마다 다르다. 링크 한 줄이면 브라우저가 알아서 받아오고, 캡처하면 이미지에 박힌다.

사용법은 `assets/fonts.css`에 분위기별 블록이 있다. **블록 하나만 골라 `template.html`의 `<style>` 맨 위에 붙이면 끝.** 여러 블록을 다 넣으면 로딩이 느려진다.

## 고르는 법 (3초)

1. `design-presets.md`에서 카테고리 기본 조합을 본다 → 대부분 그걸로 끝.
2. 사용자가 Q9에서 분위기를 고르거나 "귀엽게/고급스럽게" 같은 말을 했으면 아래 표에서 그 분위기 블록으로 바꾼다.
3. 사용자가 폰트 이름을 직접 말하면 그걸 쓴다. 이 목록에 없으면 라이선스(상업용 가능?)만 확인하고 쓴다.

**원칙:** 제목 폰트 1 + 본문 폰트 1. 세 번째 폰트는 손글씨 강조 한 줄 정도만. 본문은 항상 고딕 계열(명조 본문은 폰에서 작게 보이면 읽기 힘들다). 제목용 개성 폰트는 **짧은 카피·상품명에만**, 본문에 쓰면 피곤하다.

---

## 분위기별 조합 (`fonts.css`의 `data-font` 값)

| data-font | 분위기 | 제목 | 본문 | 어울리는 상품 |
|---|---|---|---|---|
| `clean` | 깔끔·전문적·믿음직 | **Pretendard** 800 | Pretendard 400 | 뷰티, 주방, 건강식품, 가전 — 뭐든 안전한 기본값 |
| `modern` | 세련·트렌디·요즘 | **Paperlogy** 800 | Paperlogy 400 | 패션, 홈인테리어, 문구, 브랜드 있는 뷰티 |
| `round` | 귀여운·친근·부드러운 | **Cafe24 Ssurround** | Nanum Square Round 400 | 유아동, 반려동물, 문구, 간식, 캐릭터 상품 |
| `kids` | 아동·장난감·명랑 | **BM JUA** | Nanum Square Round 400 | 완구, 유아 식품, 키즈 의류 |
| `warm` | 따뜻·정겨운·손맛 | **Cafe24 Simplehae** | Nanum Square Neo 400 | 농수산물, 수제 식품, 공방 제품, 선물 |
| `bold` | 강한 임팩트·프로모션 | **Jalnan** | Pretendard 500 | 생활용품(쿠팡 스타일), 할인 행사, 간편식, 스포츠 |
| `luxe` | 고급·우아·명조 | **Maru Buri** 600 | Pretendard 400 | 고가 뷰티, 프리미엄 식품(한우·과일 선물세트), 주얼리, 홈인테리어 고급선 |
| `editorial` | 지적·차분·읽는 맛 | **Noto Serif KR** 700 | Gowun Batang 400 | 도서, 브랜드 스토리형, 차·커피, 문구 |
| `tech` | 기술·정확·숫자 | **Gmarket Sans** 700 | Spoqa Han Sans Neo 400 | 가전디지털, 자동차용품, 스포츠 장비 |
| `sport` | 역동·강함·속도 | **Giants** 700 | Pretendard 500 | 스포츠/레저, 운동 보조식품, 아웃도어 |
| `retro` | 레트로·뉴트로·간판 | **BM EULJIRO** | Pretendard 400 | 전통 식품, 막걸리·전통주, 복고 굿즈, 노포 느낌 |

### 각 분위기의 대체 폰트 (조합이 안 맞을 때 바꿔 끼우기)

**깔끔·전문 (clean)** — SUIT, Freesentation, Nanum Square Neo, Noto Sans KR, IBM Plex Sans KR, LINE Seed KR
**세련·트렌디 (modern)** — SUITE, Freesentation, The Jamsil(굵기 다양), Seoul Namsan
**귀여운 (round)** — Tmoney Round Wind, Hakgyoansim Dunggeunmiso, Cafe24 Ssurround Air(가벼운 버전), Cafe24 Dangdanghae, Google: Hi Melody, Gaegu, Dongle
**아동 (kids)** — Cafe24 Syongsyong, Cafe24 Shiningstar, Cafe24 Moyamoya, Google: Jua, Cute Font, Gamja Flower, Bagel Fat One
**따뜻·손맛 (warm)** — Cafe24 Oneprettynight, Hakgyoansim Allimjang, BM YEONSUNG, Nanum Pen(강조 한 줄만), Google: Nanum Pen Script, Poor Story, Single Day
**강한 임팩트 (bold)** — BM DOHYEON, Jalnan Gothic, Gmarket Sans 700, Cafe24 Ohsquare, Google: Black Han Sans, Do Hyeon
**고급·명조 (luxe)** — RIDI Batang, Bookk Myungjo, Chosun Centennial, Hahmlet(굵기 9단), Nanum Myeongjo, Google: Song Myung, Diphylleia
**지적·차분 (editorial)** — Gowun Dodum(고딕인데 차분), RIDI Batang, Nanum Myeongjo, Hahmlet
**기술 (tech)** — IBM Plex Sans KR, SUIT, NEXON Lv1 Gothic, Orbit(숫자 포인트용), Google: Gothic A1
**역동 (sport)** — Jalnan Gothic, Seoul Namsan 800, Gmarket Sans 700, Google: Black Han Sans
**레트로 (retro)** — KCC Ganpan, Cafe24 Classic Type, Gyeonggi Title, Chosun Centennial, Google: East Sea Dokdo, Kirang Haerang, Stylish

---

## 전체 목록 (CDN 확인됨)

### fonts-archive (jsdelivr) — `https://cdn.jsdelivr.net/gh/fonts-archive/{저장소명}/{저장소명}.css`
용량 아끼려면 `/subsets/{저장소명}-dynamic-subset.css` 경로 (쓰는 글자만 받음).

| 저장소명 | font-family | 굵기 | 분류 | 비고 |
|---|---|---|---|---|
| Pretendard | 'Pretendard' | 100~900 | 고딕 | 본문 기본값. 가변폰트 |
| Paperlogy | 'Paperlogy' | 100~900 | 고딕 | 2024~ 급상승, 모던 |
| SUIT | 'SUIT' | 100~900 | 고딕 | 깔끔, 숫자 예쁨 |
| SUITE | 'SUITE' | 300~900 | 고딕 | SUIT의 네모난 버전 |
| Freesentation | 'Freesentation' | 100~900 | 고딕 | 프레젠테이션용, 제목 좋음 |
| GmarketSans | 'Gmarket Sans' | 300/500/700 | 고딕 | 쇼핑몰 단골, 임팩트 |
| SpoqaHanSansNeo | "Spoqa Han Sans Neo" | 100~700 | 고딕 | 숫자·영문 가독성 최고 |
| NanumSquareNeo | 'Nanum Square Neo' | 300~900 | 고딕 | 네모 정갈 |
| NanumSquareRound | 'Nanum Square Round' | 300~800 | 둥근고딕 | 부드러운 본문 |
| NanumGothic / NanumBarunGothic | 'Nanum Gothic' 등 | — | 고딕 | 무난, 약간 구형 느낌 |
| IBMPlexSansKR | 'IBM Plex Sans KR' | 100~700 | 고딕 | 기술적·정확 |
| LINESeedKR | 'LINE Seed KR' | 100/400/700 | 고딕 | 앱 느낌, 친근 |
| NEXONLv1Gothic | 'NEXON Lv1 Gothic' | 300/400/700 | 고딕 | 게임·테크 |
| TheJamsil | 'The Jamsil' | 100~800 | 고딕 | 롯데, 굵기 다양 |
| SeoulHangang / SeoulNamsan | "Seoul Hangang" / "Seoul Namsan" | 300~800 | 고딕 | 서울서체, 남산이 더 굵직 |
| Cafe24Ssurround | 'Cafe24 Ssurround' | 1종 | 둥근 제목 | **귀여운 제목 1순위** |
| Cafe24SsurroundAir | 'Cafe24 Ssurround Air' | 1종 | 둥근 제목 | 써라운드 가벼운 버전 |
| Cafe24Dangdanghae | 'Cafe24 Dangdanghae' | 1종 | 둥근 제목 | 당당, 또렷 |
| Cafe24Ohsquare / Air | 'Cafe24 Ohsquare' | 1종 | 각진 제목 | 임팩트 |
| Cafe24Simplehae | 'Cafe24 Simplehae' | 1종 | 손글씨풍 | **따뜻한 제목 1순위** |
| Cafe24Oneprettynight | 'Cafe24 Oneprettynight' | 1종 | 손글씨 | 감성, 밤 |
| Cafe24ClassicType | 'Cafe24 Classic Type' | 1종 | 타자기풍 | 레트로 |
| Cafe24Moyamoya | 'Cafe24 Moyamoya' | 1종 | 귀여운 | 몽글몽글 |
| Cafe24Danjunghae | 'Cafe24 Danjunghae' | 1종 | 명조풍 손글씨 | 단정 |
| Cafe24Syongsyong | 'Cafe24 Syongsyong' | 1종 | 귀여운 | 아동 |
| Cafe24Shiningstar | 'Cafe24 Shiningstar' | 1종 | 귀여운 | 반짝 |
| Cafe24Supermagic | 'Cafe24 Supermagic' | 400/700 | 제목 | 마법·판타지 |
| Cafe24Decobox | 'Cafe24 Decobox' | 1종 | 장식 | 포인트 한 단어만 |
| BMJUA | 'BM JUA' | 1종 | 둥근 제목 | **아동 1순위**, 배민 주아 |
| BMDOHYEON | 'BM DOHYEON' | 1종 | 각진 제목 | 배민 도현, 임팩트 |
| BMHANNAPro / Air | 'BM HANNA Pro' / 'BM HANNA Air' | 1종 | 제목 | 배민 한나 |
| BMYEONSUNG | 'BM YEONSUNG' | 1종 | 손글씨 | 배민 연성, 정겨움 |
| BMEULJIRO | 'BM EULJIRO' | 1종 | 간판체 | **레트로 1순위** |
| BMKIRANGHAERANG | 'BM KIRANGHAERANG' | 1종 | 붓글씨 | 전통 |
| Jalnan | 'Jalnan' | 1종 | 제목 | **임팩트 1순위**, 여기어때 잘난체 |
| JalnanGothic | 'Jalnan Gothic' | 1종 | 제목 | 잘난체 고딕 버전 |
| Giants | 'Giants' | 400/700 | 제목 | 롯데자이언츠, 역동 |
| TmoneyRoundWind | 'Tmoney Round Wind' | 400/800 | 둥근고딕 | 친근 |
| HakgyoansimDunggeunmiso | 'Hakgyoansim Dunggeunmiso' | 400/700 | 둥근 | 학교안심, 귀여움 |
| HakgyoansimAllimjang | 'Hakgyoansim Allimjang' | 400/700 | 손글씨 | 알림장 |
| MaruBuri | 'Maru Buri' | 200~700 | 명조 | **고급 제목 1순위**, 네이버 |
| RIDIBatang | 'RIDI Batang' | 1종 | 명조 | 리디, 읽기 좋음 |
| BookkMyungjo | 'Bookk Myungjo' | 400/700 | 명조 | 부크크 |
| ChosunCentennial | 'Chosun Centennial' | 1종 | 명조 | 신문, 클래식 |
| NanumMyeongjo | 'Nanum Myeongjo' | 400~800 | 명조 | 무난 |
| Hahmlet | 'Hahmlet' | 100~900 | 명조 | 굵기 다양한 명조 |
| NanumPen | 'Nanum Pen' | 400 | 손글씨 | 강조 한 줄용 |
| KCCGanpan | 'KCC Ganpan' | 1종 | 간판체 | 레트로 |
| KCCChassam | 'KCC Chassam' | 1종 | 손글씨 | 차쌤 |
| GyeonggiTitle | 'Gyeonggi Title' | 300~700 | 제목 | 경기천년, 공공 느낌 |
| Recipekorea | 'Recipekorea' | 1종 | 제목 | 레시피코리아, 식품 |
| InkLipquid | 'InkLipquid' | 1종 | 붓 | 잉크 |
| EliceDigitalBaeum | 'Elice Digital Baeum' | 400/700 | 고딕 | 교육 |
| DNFBitBit | 'bitbit' | 1종 | 픽셀 | 게임·레트로 포인트 |
| Bazzi | 'Bazzi' | 1종 | 제목 | 카트라이더, 발랄 |
| Yeongdo | 'Yeongdo' | 1종 | 제목 | 영도, 바다 |
| Orbit | 'Orbit' | 1종 | 숫자 | 숫자 포인트 |
| HSYuji | 'HSYuji' | 1종 | 손글씨 | 유지체 |

### Google Fonts — `https://fonts.googleapis.com/css2?family={이름}&display=swap`
이름의 공백은 `+`. 굵기 지정은 `:wght@400;700`.

| 이름 | 분류 | 분위기 |
|---|---|---|
| Noto Sans KR | 고딕 | 기본 본문 |
| Noto Serif KR | 명조 | 지적·고급 제목 |
| Nanum Gothic / Nanum Myeongjo | 고딕/명조 | 무난 |
| Gothic A1 | 고딕 | 굵기 9단, 테크 |
| IBM Plex Sans KR | 고딕 | 기술 |
| Gowun Dodum / Gowun Batang | 고딕/명조 | **차분·읽기 좋음** (브랜드 스토리) |
| Do Hyeon / Jua / Yeon Sung / Kirang Haerang | 배민 서체 | 도현(임팩트) 주아(아동) 연성(손글씨) |
| Black Han Sans | 극굵 제목 | 할인·임팩트 |
| Song Myung | 명조 | 고급 |
| Hahmlet | 명조 | 굵기 다양 |
| Nanum Pen Script / Nanum Brush Script | 손글씨 | 강조 한 줄 |
| Gaegu / Hi Melody / Poor Story / Single Day / Gamja Flower / Cute Font | 손글씨·귀여운 | 아동·감성 |
| Dongle / Bagel Fat One / Moirai One / Grandiflora One | 둥근·디스플레이 | 귀여운·트렌디 |
| Sunflower / Stylish / Gugi / East Sea Dokdo / Diphylleia / Orbit | 디스플레이 | 레트로·개성 |

---

## 라이선스 주의

- 위 목록은 전부 **개인·기업 상업적 사용 무료**. 단 공통 금지: 폰트 파일 자체를 팔기, 폰트를 BI/CI(로고)에 쓰기(일부), 폰트 이름 바꿔 재배포.
- **29CM 에디토리얼, 산돌·윤디자인 유료 폰트, 어도비 폰트(구독 끊기면 사용 불가)** 는 쓰지 않는다. 사용자가 요청하면 "이건 상업용 유료예요" 알려주고 비슷한 무료 폰트를 제안한다.
- 손글씨 폰트는 최근 AI 생성 도용 검수 이슈가 있어(눈누 공지) 출처 불명 폰트는 피한다. 위 목록은 전부 배포처가 명확하다.
- 라이선스는 바뀔 수 있다. 상세페이지는 "이미지로 캡처해서 올리는" 경우가 대부분이라 폰트 임베딩 문제가 없지만, HTML 그대로 쓰는 자사몰은 웹폰트 사용 허용 여부를 한 번 더 본다 (위 목록은 전부 웹폰트 허용).

## 출처
- [fonts-archive (GitHub)](https://github.com/fonts-archive) — CDN 호스팅, 라이선스 원문 동봉
- [눈누](https://noonnu.cc) — 상업용 무료 한글 폰트 모음
- [Google Fonts 한국어](https://fonts.google.com/?subset=korean)
- [무료 한글 폰트 총정리 2026 — AWEZARD](https://awz.kr/free-korean-fonts-commercial-use/)
- [무료 폰트 추천 11선과 라이선스 — flowworks](https://flowworks.io/blog/free-commercial-fonts)
- [웹 디자인에 적합한 무료 상업용 한글 폰트 — designkits](https://www.designkits.co.kr/blog/web-design/web-font)
