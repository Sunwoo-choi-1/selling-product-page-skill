# 이미지 만들기 가이드

목차: 원칙 · 도구 고르기 · 섹션별 이미지 스펙 · 프롬프트 쓰는 법 · 누끼 소품 세트 (기본, 2026-11-04) · 질감 바탕 · "디테일" 섹션 (기본 포함) — 실물 사진 콜라주 · 사용자 사진 다루기 · 플랫폼별 최종 규격

## 원칙

1. **본문 사진은 질문지 Q2-1 답대로 (2026-11-21).** ① 실제 사진만 → 생성하지 않고 사용자 사진을 정리해서(밝기·수평·크롭, 필요하면 누끼) 그대로. ② 섞기 → 상품·실물은 실제 사진, 사용 장면·분위기만 생성. ③ AI 위주 → 아래 방식. 생성할 때는 SKILL.md "이미지 도구 연결"에서 고른 도구로. 단, 손님이 받아보는 물건이 사진과 다르면 반품·악플·신고로 돌아오니 두 가지를 지킨다: ① 사용자 사진을 누끼 따서 참조로 넣어 상품 생김새가 실제와 같게 유지한다(원칙 2). ② 하단 "디테일" 섹션에 실물 사진 콜라주를 기본으로 넣는다. 다 만든 뒤 사용자에게 원본 사진으로 교체하고 싶은 부분이 있는지 한 번 묻는다(SKILL.md "끝낼 때").
2. **상품 사진을 참조로 쓸 땐 누끼부터.** 배경 제거(힉스필드 `remove_background`)로 상품만 남긴 결과를 참조로 넣는다. 원본 사진을 통째로 넣으면 집 조명·누런 테이블·벽지가 생성 결과에 따라 들어와 페이지 톤이 탁해진다. 배경은 프롬프트로 새로 지정한다. **항상 이 순서다.**
3. **연출컷의 배경은 세트 2종으로 통일한다.** 스튜디오 컷(히어로·클로즈업·크기감)은 페이지 색에 맞춘 파스텔 단색 seamless, 생활 컷(책상·사용·선물)은 밝은 흰 책상 + 자연광. 섹션마다 배경이 다르면 싸구려로 보인다.
4. **글자는 이미지 "위"에 HTML로 얹는 게 기본.** 이미지 생성 땐 글자를 넣지 않고(한글 깨짐 + 문구 수정 때마다 재생성), 카피는 HTML 텍스트를 이미지 위에 오버레이한다(`template.html`의 `.imgtext`). "이미지 따로 + 아래 캡션 따로"는 페이지만 길어지고 기획안처럼 보이니 단독 이미지 섹션에선 쓰지 않는다. 그래서 **카피가 앉을 빈 공간을 프롬프트에 미리 지정**한다 — 상단 하늘·벽면·단색 배경 등, `negative space at top for text, clean copy space`. 이미지에 올리는 글자는 헤드라인+한 줄까지 — 긴 설명은 이미지 밖에.
   - **예외 — 텍스트까지 디자인하는 배너 (페이지당 1~2개):** 히어로 배너와 비주얼/아트 배너는 텍스트까지 이미지 안에 디자인해도 된다. 특히 비주얼이 곧 상품인 카테고리(홈인테리어·문구·패션 등 — `categories.md` 히어로 배너 가이드)의 히어로는 AI 텍스트 생성도 OK. 단 한글은 짧게(2~8자 단어 위주), 깨지면 재생성하고, 두 번 깨지면 HTML 합성으로 전환한다.
4-1. **AI 표기와 AI 인물 (2026-11-20).** AI로 만든 연출컷 아래 `.cap`은 "연출 이미지(AI 활용)". 네이버·카카오가 표기를 요구한다(`research.md`). AI로 만든 사람이 나오는 컷에 "써 봤어요" 같은 후기 말풍선·추천 문구를 붙이지 않는다 — 가상인물 추천·보증은 "가상인물" 표시가 필요하고(공정위 지침, 2026-06-01), 식품·건강기능식품·화장품에 의사·약사·연구원처럼 보이는 AI 인물은 표시를 해도 금지다(2026-11-27 시행). 이 카테고리의 사용 장면엔 손·뒷모습·소품 위주로 뽑는다.
5. **같은 상품이면 같은 톤.** 섹션마다 조명·색감이 다르면 싸구려로 보인다. 한 페이지는 색감 하나(Q9 분위기)로 통일.
6. **비율은 블록이 정한다 — 정사각 기본 금지.** 쿠팡·컬리·무신사 상위 페이지 15개를 보면(`layout-refs.md`) 단독 이미지는 전부 가로 4:3·3:2 또는 세로 4:5·5:6이고, 1:1은 색상·옵션·디테일 2장처럼 **여러 장 나열할 때만** 쓴다. 생성할 때부터 아래 표의 블록 비율로 뽑는다. 폰에서 가로형이 작아 보이는 건 글을 사진 위에 안 얹고 **글(위) → 사진(아래)** 로 두면 해결된다.

## 도구 고르기

순서: 힉스필드 → 연결된 다른 이미지 서비스(매그니픽 등) → ChatGPT 프롬프트 → 자리만. 연결 여부는 도구 목록이나 ToolSearch("generate image", "remove background")로 **직접 확인**하고, 유료 크레딧이면 만들기 전에 장수·예상 크레딧을 알린다.

### 1순위: 힉스필드 (Higgsfield)
MCP 도구 `mcp__claude_ai_Higgsfield__generate_image` / `generate_image_batch`가 있으면 쓴다. 장수가 많으면 `estimate_image_cost`로 먼저 견적.

- 상품 사진이 있으면 **업로드 후 누끼부터**: `media_upload` → `media_confirm` → `remove_background` → 그 job_id를 참조로 넣고, 프롬프트에 "keep the product exactly as the reference" 류를 넣는다. 원본 사진을 바로 참조로 넣지 않는다.
- 배경만 바꾸고 싶으면 `remove_background` → 새 배경 생성 → 합성 순서. 또는 Marketing Studio 상품샷 프리셋(`get_presets source:'marketing_studio', category:'product-shot'`)이 빠르다.
- 여러 섹션 이미지는 `generate_image_batch`로 한 번에 → `jobs_wait` → `show_generation_by_ids`.
- 어떤 모델이 맞는지 모르겠으면 `models_explore(action:'recommend')`.
- 결과 파일은 `images/01_hook.png` 식으로 저장.

### 1-1순위: 다른 이미지 생성 서비스 (연결돼 있을 때)
- **매그니픽(Magnific):** 처음에 `magnific_start` → 누끼 `images_remove_background` → 생성 `images_generate`(참조 이미지 넣기) → `creations_wait` → `creations_read`로 결과를 눈으로 확인. 여러 장이면 `simulate_cost`로 견적.
- **그 밖(Adobe Firefly·Figma `generate_image` 등):** 그 서비스 안내대로. 공통 원칙은 같다 — 누끼 먼저, 참조로 상품 유지, 글자 없는 이미지, 섹션 비율대로.
- 여러 서비스가 연결돼 있으면 사용자가 평소 쓰는 걸 한 줄로 묻고, 답이 없으면 힉스필드.

### 2순위: GPT 이미지 (ChatGPT)
연결된 생성 도구가 없으면 GPT 이미지를 쓴다. 이 환경에서 직접 호출 못 하면:
- 사용자가 ChatGPT로 직접 만들어야 할 때만 `1_기획안.md` 끝 "이미지 만들기" 섹션에 섹션별 프롬프트를 **한글 설명 + 영문 프롬프트** 두 벌로 정리한다(따로 파일을 만들지 않는다).
- 사용자에게 안내: "ChatGPT에 상품 사진을 첨부하고, 아래 프롬프트를 붙여넣으세요. 만들어진 이미지는 `images/` 폴더에 번호 순서대로 저장하면 HTML에 자동으로 들어가요."
- HTML에는 `images/01_hook.png` 경로를 미리 박아두고, 파일이 없을 때 보이는 회색 placeholder(`.ph`)를 둔다.

### 3순위: 아무것도 없을 때
Placeholder + 프롬프트만. 사용자 사진이 있으면 그걸로 전부 채운다(연출 없이도 깨끗한 실사진이 AI 합성보다 낫다). 사용자에게 연결 방법을 한 번 안내한다: "claude.ai → 설정 → 커넥터에서 힉스필드(또는 쓰시는 이미지 서비스)를 연결하고 대화를 다시 열어주세요."

## 섹션별 이미지 스펙

블록·비율은 `layout-refs.md`의 카테고리 레시피가 우선이다. 아래는 레시피에 없을 때의 기본값.

| 섹션 | 블록 → 비율 | 장수 | 뭘 찍나 | 프롬프트 키워드 |
|---|---|---|---|---|
| 1 첫 화면 | `.hero` 4:5 (식품 3:2, 가전·인테리어 4:3, 패션 5:6, 완구·반려 1:1, 도서 2:3) | 1 | **상품이 가장 또렷하게.** 글은 사진 위(HTML)에 두므로 사진 자체엔 카피 공간 불필요. 배너형(`.imgtext`)일 때만 상단 여백 | hero shot, soft natural light, clean background, product centered |
| 2 신뢰 | — (옵션 나열이면 `.lineup` 1:1) | 0~6 | 배지는 HTML. 옵션·색상은 흰 배경 누끼 1:1 | product only, white background, front view |
| 3 공감 | `.ask` 원형 틀 1:1 | 2 | 고민 장면 — **밝게.** 원형으로 잘리니 피사체를 가운데. 답답함은 문구(말풍선)가 만든다. 사람 얼굴은 안 보이게 | bright airy daylight, centered composition, lifestyle, no people, warm cream tones, 1:1 |
| 4 해결 | `.split` 3:4 | 1 | 상품 밝은 컷, 세로. 3번과 대비 | bright, airy, relief, clean, vertical |
| 5 장점 | 장점 1 `.wide` 4:3 + 장점 2·3 `.pair` 1:1 (가전은 `.split` 1:1 ×3, 식품은 `.wide` ×3) | 3 | 장점별 클로즈업·디테일 | macro, detail, texture |
| 6 증거 | `.pair.contain` 1:1 (시험성적서·비포/애포 실사진만, AI 금지) | 0~2 | 비교표·숫자는 HTML | — |
| 7 사용 장면 | `.wide` 4:3 + `.split.rev` 3:4 + `.pair` 1:1 | 2~4 | 일상 속 사용. 손·식탁·싱크대·화장대. 첫 장은 가로 와이드 | lifestyle, in-use, hands, Korean home interior |
| 8 후기 | — | 0 | 텍스트. 고객 사진 후기 있으면 `.pair` | — |
| 9 실물 디테일 | `.mosaic`(세로 1 + 1:1 2) + `.pair.contain`(패키지·치수) | 3~5 | **실물 사진만.** 정면·측면·뒷면, 패키지, 자·손 대고 찍은 크기 비교 | real photo, front view, measurement reference |
| 10 추천/FAQ | — | 0 | 텍스트 | — |
| 11 구매 유도 | `.wide` 4:3 | 1 | 구성품 전체 펼친 샷(플랫레이) | flat lay, all items, top view, 4:3 |
| 12 고지 | — | 0 | 텍스트 | — |

이미지 총 10~14장 목표. 쿠팡은 6~8장으로 줄인다. **연속 두 블록이 같은 비율이면 하나를 바꾼다.**

## 프롬프트 쓰는 법

기본 틀:
```
[무엇] + [어디서/어떤 장면] + [조명·분위기] + [카메라] + [금지]
```
예 (식품, 따뜻한 분위기):
```
A bowl of freshly steamed Korean dumplings, steam rising, on a wooden dining table in a cozy Korean home kitchen, warm morning sunlight from the window, shallow depth of field, 50mm, photorealistic, no text, no watermark, no people's faces
```
예 (생활용품, 공감 섹션):
```
Close-up of a worn, discolored kitchen sponge on a wet sink edge, bright natural daylight, clean airy Korean apartment kitchen, soft shadows, realistic, no text, no faces  (공감도 밝게 — 어두운 딤·moody 금지, design.md 0항 5)
```

분위기(Q9)별 공통 키워드:
- 깔끔·믿음직: `white background, studio lighting, minimal, clean`
- 따뜻·정겨운: `warm sunlight, wooden, linen, cozy Korean home, soft`
- 고급: `dark background, dramatic rim light, matte, luxury, negative space`
- 발랄·트렌디: `pastel colors, playful, bright, pop, high saturation`
- 알뜰한 선택: `bright even lighting, white background, product clearly visible, quantity and contents laid out, clean` (구성품·용량이 한눈에 보이게)

항상 끝에: `photorealistic, no text, no watermark, no logo`
사람이 들어가면: 얼굴은 가급적 `no face visible` 또는 뒷모습.
**손 컷 필터 요령:** "a person's hand" 류는 안전 필터에 걸릴 수 있다. 손을 장면의 부속으로 묘사하면 통과된다 — "held between a thumb and index finger entering from the upper edge of the frame, no face".

## 누끼 소품 세트 (기본, 2026-11-04)

`design.md` 0항 연출(`.scene` `.feat` `.duo`)의 재료. 사진 한 장 대신 이걸로 장면을 조립한다.

- **고르는 법:** 주인공 1(상품 누끼 — 사용자 사진 배경 제거본) + 상품이 담긴/쓰이는 모습 1~2(그릇·착용·사용 중 결과물) + 원재료·소품 3~5(곡물·과일·꽃·도구·포장재 등 상품 세계의 물건). 카테고리 예: 식품=그릇·재료·숟가락·우유잔, 뷰티=제형 한 방울·원료 식물·물방울, 주방=조리 결과·식재료, 생활=쓰는 물건·결과물, 반려=간식 낱개·장난감, 문구=펜·종이·클립.
- **생성:** 소품마다 따로, `isolated on a plain pure white background, top-down (또는 three-quarter) view, soft even studio light, very soft contact shadow, photorealistic product cutout photo, no text`. 내용물은 01번 연출컷을 참조로 넣어 상품과 같은 생김새 유지. → 각각 `remove_background` → `images/cut/이름.png`로 저장하고 투명 여백을 잘라낸다. 긴 변 1300px 이하로.
- **흰 내용물 주의:** 우유·요거트·크림 같은 흰 부분은 배경 제거기가 배경으로 지운다. 받은 누끼를 초록 바탕에 얹어 확인하고, 구멍이 있으면 그릇 외곽 원(타원)을 그려 그 안은 원본 픽셀·불투명으로 메운다.
- **포장 글씨 주의:** AI가 포장을 다시 그리면 작은 글씨를 지어낸다(없는 알레르기 문구까지). 포장은 사용자 사진 누끼를 그대로 쓰고, AI 연출컷에 포장이 크게 보이면 진짜 포장 누끼를 원근 변환해 덮는다.

## 질감 바탕

- **생성 2종:** 상품 세계의 재질로. 예: `Flat straight-on full-frame texture of warm off-white lime plaster wall, very subtle mottling and speckles, perfectly even lighting, no vignette, no shadows, no objects, uniform tone`, 그리고 종이·린넨·나무결 중 하나. 1:1.
- **이음매:** 원본·좌우반전·상하반전·180° 회전 4장을 2×2로 붙여 이음매 없는 타일을 만들고, 1200px JPG(품질 80 안팎)로 `images/tex_a.jpg` `tex_b.jpg`. CSS가 페이지 폭으로 반복한다.
- **톤:** 글자가 얹히니 아주 옅게. 무늬가 글자보다 눈에 띄면 다시 뽑는다.

## "디테일" 섹션 (기본 포함) — 실물 사진 콜라주

본문(히어로·장점·사용 장면)이 AI 연출컷이므로, 하단(FAQ 뒤·상품정보 앞)에 **"디테일" 섹션**을 만들어 직접 찍은 실물 사진을 콜라주로 넣는다. 사용자 사진이 있으면 항상 넣는다.
- 구성: `.mosaic` — 세로 1장(정면, 왼쪽 2칸 높이) + 정사각 2장(측면·뒷면) + `.pair.contain` 패키지·치수 2장. 흐릿한 컷은 뺀다. 템플릿 9번 섹션에 자리가 있다.
- 실물 컷에도 같은 밝기 보정(누런 끼 중화 + 밝기)을 걸어 본문과 톤을 맞춘다.
- 고지(12번)에 "사용 장면은 연출 이미지, 실물은 디테일 섹션 기준" 한 줄을 넣는다. "사진과 다르다" 반품을 막는 장치다.

## 사용자 사진 다루기

- 폴더 경로를 받으면 jpg/png/webp/heic 파일을 전부 읽어서 각각 뭐가 찍혔는지 한 줄씩 메모한다 (정면/뒷면/포장/사용샷/단면…).
- 사용자 사진의 기본 용도는 두 가지: ① 누끼 따서 AI 생성 참조로, ② 디테일 섹션 실물 콜라주로. 본문에 바로 넣지 않는다.
- 다 만든 뒤 사용자가 원본 교체를 원하면 이 매핑으로 바꾼다: 가장 잘 나온 컷 → 1번 첫 화면. 디테일 컷 → 5번. 사용샷 → 7번. 포장·구성 → 11번.
- 배경이 지저분하면 힉스필드 `remove_background`로 누끼 → 흰 배경 또는 연출 배경.
- 사진이 흐리거나 작으면 `upscale_image`.
- HEIC는 PNG로 변환해서 `images/`에 복사.

## 플랫폼별 최종 규격

| 플랫폼 | 가로 | 글자 최소 | 장수 | 특이사항 |
|---|---|---|---|---|
| 스마트스토어 | 860px | 16px | 10장↑ | 이미지 대체텍스트(alt)에 키워드 |
| 쿠팡 | 780px | 25pt | 5~7장 | GIF 불가, 대표이미지는 흰배경 상품만·글자 금지 |
| 카페24 | 860px | 16px | 자유 | HTML 그대로 삽입 가능 |
| 인스타/블로그 | 1080px | 32px | 카드 6~10장 | 4:5, 첫 장이 썸네일 |
