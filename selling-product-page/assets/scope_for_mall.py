# -*- coding: utf-8 -*-
"""2_상세페이지.html → 쇼핑몰 상세설명에 그대로 넣을 수 있는 HTML (<style> + <div class="pdp">…</div>)

쇼핑몰 스킨 CSS는 상세설명 안까지 들어온다. 그대로 붙이면
  - 스킨이 상세 영역 조상에 건 text-align:center 가 상속돼 전부 가운데 정렬되고,
  - h2{color} p{margin} img{border} table{border} 같은 요소 선택자 규칙이 새어 들고,
  - word-break 기본값이 사라져 한국어가 "달라 / 요." 처럼 글자 단위로 끊긴다. (2026-10-29 클림트 키링에서 겪음)
그래서 이 스크립트가 세 가지를 한다.
  1) <style>의 모든 선택자를 래퍼(.pdp) 아래로 가둔다. html/body 전역 규칙은 버리고 *{…}는 "상속값으로 초기화" 규칙으로 바꾼다.
  2) 래퍼 본체에 글 기본값(왼쪽 정렬·keep-all·break-word·줄높이)을 직접 넣고, 글자 속성은 전부 !important 로 만든다.
     (!important 끼리는 특이성으로 겨루므로 내 규칙끼리의 우선순위는 그대로다. 인라인 style 은 !important 에 지니 글자 속성은 인라인으로 쓰지 않는다.)
  3) 이미지 경로를 업로드한 URL로 바꾸고(--img-map), ALT 앞에 브랜드명을 붙인다(--alt-prefix).

사용 (2026-11-21부터 결과물은 한 파일):
  만들 때 마지막 단계 — 템플릿으로 만든 초안을 최종본 2_상세페이지.html 로 (열어 보기·몰 삽입 겸용):
    python scope_for_mall.py 초안.html 2_상세페이지.html --standalone
  자사몰에 올릴 때 — 최종본에서 ▼▲ 표시 사이만 꺼내 이미지 URL 을 바꾼다(붙여넣을 조각):
    python scope_for_mall.py 2_상세페이지.html 몰에_붙일_부분.html --img-map urls.json --alt-prefix 브랜드
  초안에서 바로 몰 조각:
    python scope_for_mall.py 초안.html 몰에_붙일_부분.html --scope .pdp --img-map urls.json --alt-prefix 브랜드
  --img-map : {"images/01_hook.jpg": "https://…/01.jpg", …} 또는 {"01_hook": "https://…"} (파일명 stem 으로도 찾는다)
넣은 뒤에는 반드시 실제 상품 페이지(PC·모바일)에서 정렬·줄바꿈을 확인한다. 프론트 캐시 때문에 PUT 뒤 1~2분 걸릴 수 있다.
"""
import argparse, json, os, re, sys

TEXT_PROPS = (r"(text-align|line-height|word-break|overflow-wrap|letter-spacing|font-size|font-weight|font-family|"
              r"font-style|color|text-wrap|white-space)")


def split_rules(text):
    """최상위 규칙을 (머리, 본문) 쌍으로. @media/@keyframes 본문은 호출 쪽에서 다시 쪼갠다."""
    out, i, n = [], 0, len(text)
    while i < n:
        j = text.find("{", i)
        if j < 0:
            break
        head = text[i:j].strip()
        depth, k = 1, j + 1
        while k < n and depth:
            depth += {"{": 1, "}": -1}.get(text[k], 0)
            k += 1
        out.append((head, text[j + 1:k - 1]))
        i = k
    return out


def scope_selector(sel, scope, root_class):
    sel = sel.strip()
    if not sel:
        return None
    if sel == root_class:
        return scope
    if sel.startswith(root_class):           # .page[data-theme="warm"] 같은 것
        return scope + sel[len(root_class):]
    if sel in ("html", "body", ":root"):
        return None
    return scope + " " + sel


def scope_block(text, scope, root_class, kf_prefix):
    parts = []
    for head, inner in split_rules(text):
        if head.startswith("@keyframes"):
            parts.append("%s{%s}" % (re.sub(r"@keyframes\s+(\S+)", lambda m: "@keyframes %s%s" % (kf_prefix, m.group(1)), head), inner))
        elif head.startswith("@media") or head.startswith("@supports"):
            parts.append("%s{%s}" % (head, scope_block(inner, scope, root_class, kf_prefix)))
        elif head.startswith("@"):
            parts.append("%s{%s}" % (head, inner))
        else:
            sels = [scope_selector(s, scope, root_class) for s in head.split(",")]
            sels = [s for s in sels if s]
            if sels:
                parts.append("%s{%s}" % (",".join(sels), inner))
    return "\n".join(parts)


def convert(html, scope=".pdp", root_class=".page", img_map=None, alt_prefix=None):
    m = re.search(r"<style[^>]*>(.*?)</style>", html, re.S)
    if not m:
        raise SystemExit("<style> 블록이 없어요")
    css = m.group(1)
    # 본문은 </style> 뒤에서 찾는다 (CSS 주석 안의 <div class="page"> 예시에 걸리지 않게)
    body_m = re.search(r'(<div class="%s[^"]*"[^>]*>.*)</body>' % re.escape(root_class[1:]), html[m.end():], re.S)
    if not body_m:
        raise SystemExit('<div class="%s"> 를 못 찾았어요' % root_class[1:])
    body = body_m.group(1).rstrip()
    scope_cls = scope[1:]
    kf_prefix = scope_cls + "-"

    # 1) CSS 스코프
    css_nc = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    imports = "\n".join(l.strip() for l in css_nc.splitlines() if l.strip().startswith("@import"))
    rules = "\n".join(l for l in css_nc.splitlines() if not l.strip().startswith("@import"))
    scoped = scope_block(rules, scope, root_class, kf_prefix)
    kf_names = set(re.findall(r"@keyframes\s+([\w-]+)", rules))
    scoped = re.sub(r"animation(-name)?:\s*([A-Za-z_][\w-]*)",
                    lambda mm: "animation%s:%s%s" % (mm.group(1) or "", kf_prefix if mm.group(2) in kf_names else "", mm.group(2)), scoped)

    # 2) 글 기본값을 래퍼 본체에, 전역 * 규칙은 상속 초기화로
    # 줄높이는 원본 body 값 그대로(없으면 1.65). 다르면 줄마다 1px씩 어긋나 섹션 높이가 달라진다
    bm = re.search(r"(?:^|[\s}])body\s*\{[^}]*?line-height:\s*([\d.]+)", css_nc)
    lh = bm.group(1) if bm else "1.65"
    scoped, n = re.subn(r"(^|\n)%s\{" % re.escape(scope),
                        r"\1%s{line-height:%s;word-break:keep-all;overflow-wrap:break-word;text-align:left;" % (scope, lh), scoped, count=1)
    if n != 1:
        raise SystemExit("래퍼 본체 규칙(%s{…})을 못 찾았어요" % scope)
    reset = ("%s *{box-sizing:border-box;margin:0;padding:0;border:0;background:transparent;color:inherit;"
             "font-family:inherit;font-size:inherit;font-weight:inherit;font-style:inherit;line-height:inherit;"
             "letter-spacing:inherit;text-align:inherit;text-transform:none;text-decoration:none;list-style:none;max-width:none}" % scope)
    # 상속 초기화가 브라우저 기본 굵기까지 지우므로 <b>·<strong> 굵게는 되살린다 (템플릿 규칙은 !important 라 이것보다 이긴다)
    reset += "\n%s b,%s strong{font-weight:700}" % (scope, scope)
    scoped, n = re.subn(r"%s \*\{[^}]*\}" % re.escape(scope), reset, scoped, count=1)
    if n != 1:
        scoped = reset + "\n" + scoped
    scoped = re.sub(TEXT_PROPS + r":([^;}!]+)(;|})", lambda mm: "%s:%s!important%s" % (mm.group(1), mm.group(2).strip(), mm.group(3)), scoped)
    for bad in ("\nhtml{", "\nbody{", root_class + "{", root_class + "["):
        if bad in "\n" + scoped:
            raise SystemExit("스코프 누락: %r" % bad)

    # 3) 본문: 래퍼 클래스, <section> → <div>(스킨이 section 에 규칙을 거는 경우 대비), 이미지 URL, ALT
    body = body.replace('<div class="%s' % root_class[1:], '<div class="%s' % scope_cls, 1)
    body = re.sub(r"<section\b", "<div", body).replace("</section>", "</div>")
    missing = []
    if img_map:
        def swap(mm):
            src = mm.group(1)
            stem = os.path.splitext(os.path.basename(src))[0]
            url = img_map.get(src) or img_map.get(os.path.basename(src)) or img_map.get(stem)
            if not url:
                missing.append(src)
                return mm.group(0)
            return 'src="%s"' % url
        body = re.sub(r'src="((?!https?:|data:)[^"]+)"', swap, body)
    if alt_prefix:
        body = re.sub(r'alt="(?!%s)(?=[^"])' % re.escape(alt_prefix), 'alt="%s ' % alt_prefix, body)
    out = "<style>\n%s\n%s\n</style>\n%s\n" % (imports, scoped, body)
    return out, missing


MARK_A = "<!-- ▼ 쇼핑몰 상세설명(HTML 모드)에 넣을 부분: 여기부터 -->"
MARK_B = "<!-- ▲ 여기까지 -->"


def standalone(snippet, title):
    """변환 결과를 그대로 열어 볼 수 있는 한 파일로 감싼다. 몰에 넣을 땐 표시 사이만 쓴다."""
    return ("<!DOCTYPE html>\n<html lang=\"ko\">\n<head>\n<meta charset=\"UTF-8\">\n"
            "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n<title>%s</title>\n"
            "<style>html,body{margin:0;background:#e9ebee}</style>\n</head>\n<body>\n%s\n%s%s\n</body>\n</html>\n"
            % (title, MARK_A, snippet, MARK_B))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("out")
    ap.add_argument("--scope", default=".pdp", help="래퍼 클래스 (스킨과 겹치지 않는 짧은 이름)")
    ap.add_argument("--root", default=".page", help="원본 래퍼 클래스")
    ap.add_argument("--img-map", help="이미지 경로→URL JSON")
    ap.add_argument("--alt-prefix", help="모든 ALT 앞에 붙일 브랜드명")
    ap.add_argument("--standalone", action="store_true",
                    help="열어 볼 수 있는 한 파일로 저장(2_상세페이지.html 최종본). 몰에 넣을 부분은 ▼▲ 표시 사이")
    a = ap.parse_args()
    img_map = json.load(open(a.img_map, encoding="utf-8")) if a.img_map else None
    html = open(a.src, encoding="utf-8").read()

    if MARK_A in html and a.standalone:
        # 이미 변환된 최종본을 다시 --standalone 으로 돌린 경우(고친 뒤 재실행): 다시 가두면 껍데기가 벗겨지니 그대로 둔다
        if os.path.abspath(a.src) != os.path.abspath(a.out):
            open(a.out, "w", encoding="utf-8").write(html)
        print("%s  이미 변환된 최종본이라 그대로 뒀어요(다시 가둘 필요 없음). 고친 내용은 그대로 살아 있어요." % a.out)
        return
    if MARK_A in html:
        # 이미 변환된 최종본: 표시 사이(몰에 넣을 부분)만 꺼내 이미지 URL·ALT 만 바꾼다
        snippet = html.split(MARK_A, 1)[1].split(MARK_B, 1)[0]
        missing = []
        if img_map:
            def swap(mm):
                src = mm.group(1)
                stem = os.path.splitext(os.path.basename(src))[0]
                url = img_map.get(src) or img_map.get(os.path.basename(src)) or img_map.get(stem)
                if not url:
                    missing.append(src)
                    return mm.group(0)
                return 'src="%s"' % url
            snippet = re.sub(r'src="((?!https?:|data:)[^"]+)"', swap, snippet)
        if a.alt_prefix:
            snippet = re.sub(r'alt="(?!%s)(?=[^"])' % re.escape(a.alt_prefix), 'alt="%s ' % a.alt_prefix, snippet)
        out = snippet.strip() + "\n"
    else:
        out, missing = convert(html, a.scope, a.root, img_map, a.alt_prefix)
        if a.standalone:
            m = re.search(r"<title>(.*?)</title>", html, re.S)
            out = standalone(out, m.group(1).strip() if m else "상세페이지")
    open(a.out, "w", encoding="utf-8").write(out)
    print("%s  %s자 / img %d장 / !important %d개" % (a.out, format(len(out), ","), out.count("<img"), out.count("!important")))
    if missing:
        print("URL 없는 이미지(로컬 경로 그대로 남음): %s" % missing)
    if img_map is None and not a.standalone:
        print("주의: --img-map 없이 변환했어요. 이미지 경로가 로컬(images/…)이면 몰에서 엑박이 나요.")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
