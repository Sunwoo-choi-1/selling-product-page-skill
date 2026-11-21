# -*- coding: utf-8 -*-
"""
export_banners.py — banner.html 의 아트보드(.ab)를 규격 그대로 PNG/JPG 로 내보내고 점검한다.

  python assets/export_banners.py <배너html> <출력폴더> [--look scene|spec|magazine|maker] [--theme ..] [--font ..]
                                  [--only insta_feed,thumb_1000] [--suffix _spec] [--no-check]

하는 일
  1. Edge(없으면 Chrome → playwright 내장 Chromium)로 html 을 열고, html[data-mode="export"] 로 바꿔
     미리보기 축소·라벨·안전 여백 가이드를 끈다. 폰트·이미지가 다 뜰 때까지 기다린다.
  2. 아트보드마다 data-size 와 똑같은 픽셀로 캡처한다 (배율 1). 크기가 1px 이라도 다르면 실패로 알린다.
  3. data-format="jpg" + data-kb="최소-최대" 면 그 용량 안에 들도록 JPG 품질을 자동으로 고른다
     (최대를 넘으면 품질을 낮추고, 최소보다 작으면 품질을 올리고, 그래도 작으면 PNG 로 다시 시도한 뒤 경고).
     data-alpha="true" 는 투명 PNG(배경 없이). 500KB 를 넘으면 256색으로 줄인다.
  4. 점검 (--no-check 로 끔): 아트보드 크기 · 글자 최소 크기(1080 폭 기준 본문 28px · 캡션 24px, 폭에 비례) ·
     글자 대비 4.5:1 (큰 글씨 3:1) · data-safe 안전 영역 밖 글자 · 남은 {{자리표시}} · 이모지 · U+0080~U+009F 제어문자.
     결과는 화면과 <출력폴더>/_export_report.json 에.

의존성
  pip install playwright pillow
  (Windows 는 Edge 가 이미 있어 브라우저 설치가 필요 없다. 다른 OS 면: python -m playwright install chromium)
"""
import sys, os, io, re, json, argparse

try:
    from PIL import Image
except ImportError:
    sys.exit('[필요] Pillow 가 없어요.  pip install pillow  후 다시 실행하세요.')
try:
    from playwright.sync_api import sync_playwright
except ImportError:
    sys.exit('[필요] playwright 가 없어요.  pip install playwright  후 다시 실행하세요.\n'
             '       (Edge·Chrome 이 없는 PC 면 이어서  python -m playwright install chromium)')

EMOJI = re.compile('[\U0001F000-\U0001FAFF\U00002600-\U000027BF\U0001F1E6-\U0001F1FF\u2B50\u2B55\u2705\u274C\u2728\uFE0F]')
CTRL = re.compile('[\u0080-\u009f]')

CHECK_JS = r"""
() => {
  const lum = c => { const v = c.map(x => { x /= 255; return x <= .03928 ? x / 12.92 : Math.pow((x + .055) / 1.055, 2.4); });
                     return .2126 * v[0] + .7152 * v[1] + .0722 * v[2]; };
  const parse = s => { const m = s.match(/rgba?\(([^)]+)\)/); if (!m) return null;
                       const p = m[1].split(/[ ,\/]+/).filter(Boolean).map(Number); return [p[0], p[1], p[2], p.length > 3 ? p[3] : 1]; };
  const ratio = (a, b) => { const l1 = lum(a), l2 = lum(b); return (Math.max(l1, l2) + .05) / (Math.min(l1, l2) + .05); };
  const capSel = '.cap,.cap *,.ai,.fn,.brand span,.swipe,.swipe *,.hint,.hint *,small,.facts dt,.sign span';
  const out = [];
  document.querySelectorAll('.ab').forEach(ab => {
    const name = ab.dataset.name, [W, H] = ab.dataset.size.split('x').map(Number);
    const r0 = ab.getBoundingClientRect();
    const rec = { name, size: ab.dataset.size, real: Math.round(r0.width) + 'x' + Math.round(r0.height), issues: [], minBody: null, minCap: null, imageBg: 0 };
    if (Math.round(r0.width) !== W || Math.round(r0.height) !== H) rec.issues.push('크기 다름: ' + rec.real);
    const k = W / 1080, minBody = 28 * Math.max(k, .999), minCap = 24 * Math.max(k, .999);
    const safe = ab.dataset.safe ? ab.dataset.safe.split(/\s+/).map(Number) : null;
    const walker = document.createTreeWalker(ab, NodeFilter.SHOW_TEXT);
    const seen = new Set();
    while (walker.nextNode()) {
      const t = walker.currentNode; if (!t.textContent.trim()) continue;
      const el = t.parentElement; if (seen.has(el) || el.closest('.ph')) continue; seen.add(el);
      const rects = el.getClientRects(); if (!rects.length) continue;
      const cs = getComputedStyle(el); if (cs.visibility === 'hidden' || +cs.opacity === 0) continue;
      const fs = parseFloat(cs.fontSize), isCap = el.matches(capSel), label = t.textContent.trim().slice(0, 18);
      if (isCap) { rec.minCap = rec.minCap === null ? fs : Math.min(rec.minCap, fs); if (fs < minCap - .01) rec.issues.push(`캡션 ${fs}px < ${minCap.toFixed(1)}: "${label}"`); }
      else { rec.minBody = rec.minBody === null ? fs : Math.min(rec.minBody, fs); if (fs < minBody - .01) rec.issues.push(`본문 ${fs}px < ${minBody.toFixed(1)}: "${label}"`); }
      // 대비 — 조상을 따라 올라가 처음 만나는 불투명 배경색. 배경 이미지(질감·사진) 위면 눈으로 확인할 목록에만
      const fg = parse(cs.color); let bg = null, img = false;
      for (let a = el; a; a = a.parentElement) {
        const s = getComputedStyle(a);
        if (s.backgroundImage && s.backgroundImage.includes('url(')) { img = true; }
        const b = parse(s.backgroundColor); if (b && b[3] > .5) { bg = b; break; }
        if (a === ab) break;
      }
      if (img) rec.imageBg++;
      if (fg && bg) {
        const big = fs >= 48 || (fs >= 37 && +cs.fontWeight >= 700);
        const r = ratio(fg, bg), need = big ? 3 : 4.5;
        if (r < need) rec.issues.push(`대비 ${r.toFixed(2)} < ${need}: "${label}"`);
      }
      if (safe) {
        for (const r of rects) {
          const x0 = r.left - r0.left, y0 = r.top - r0.top, x1 = r.right - r0.left, y1 = r.bottom - r0.top;
          if (y0 < safe[0] - .5 || x1 > W - safe[1] + .5 || y1 > H - safe[2] + .5 || x0 < safe[3] - .5) {
            rec.issues.push(`안전 영역 밖: "${label}" (${Math.round(x0)},${Math.round(y0)})-(${Math.round(x1)},${Math.round(y1)})`); break; }
        }
      }
      if (/\{\{[^}]*\}\}/.test(t.textContent)) rec.issues.push(`자리표시 남음: "${label}"`);
    }
    const imgs = [...ab.querySelectorAll('img')].filter(i => i.getClientRects().length && !i.complete);
    if (imgs.length) rec.issues.push('이미지 로딩 안 됨 ' + imgs.length + '개');
    const phs = [...ab.querySelectorAll('.ph')].filter(p => p.getClientRects().length);
    if (phs.length) rec.issues.push('이미지 자리(.ph) 비어 있음 ' + phs.length + '개');
    out.push(rec);
  });
  return out;
}
"""


def launch(p):
    for kw in ({'channel': 'msedge'}, {'channel': 'chrome'}, {}):
        try:
            return p.chromium.launch(**kw), (kw.get('channel') or 'chromium')
        except Exception:
            continue
    sys.exit('[필요] 쓸 수 있는 브라우저가 없어요.  python -m playwright install chromium  을 실행하세요.')


def save_jpg(img, path, kmin, kmax):
    """용량 범위 안에 드는 가장 높은 품질. 반환: (형식, 품질, KB, 경고)"""
    rgb = img.convert('RGB')
    def enc(q):
        b = io.BytesIO(); rgb.save(b, 'JPEG', quality=q, optimize=True, progressive=True, subsampling=0 if q >= 90 else 2); return b.getvalue()
    best = None
    lo, hi = 40, 95
    while lo <= hi:                       # 최대 용량 안에서 가장 높은 품질
        q = (lo + hi) // 2; d = enc(q)
        if len(d) <= kmax * 1024: best = (q, d); lo = q + 1
        else: hi = q - 1
    if best is None:
        q, d = 40, enc(40)
        open(path, 'wb').write(d); return 'jpg', q, len(d) / 1024, f'품질 40 에서도 {len(d)/1024:.0f}KB > {kmax}KB — 사진을 줄이거나 단순하게'
    q, d = best
    if len(d) < kmin * 1024:              # 너무 작으면(단색 위주) 품질을 끝까지 올려 본다
        d = enc(100); q = 100
        if len(d) < kmin * 1024:
            b = io.BytesIO(); img.convert('RGB').save(b, 'PNG', optimize=False)
            if kmin * 1024 <= len(b.getvalue()) <= kmax * 1024:
                p2 = os.path.splitext(path)[0] + '.png'; open(p2, 'wb').write(b.getvalue())
                return 'png', None, len(b.getvalue()) / 1024, f'JPG 가 {kmin}KB 보다 작아 PNG 로 저장 ({os.path.basename(p2)})'
            open(path, 'wb').write(d)
            return 'jpg', q, len(d) / 1024, f'{len(d)/1024:.0f}KB < 최소 {kmin}KB — 사진(질감·실사)이 들어가면 보통 넘는다. 등록 화면에서 확인'
    open(path, 'wb').write(d); return 'jpg', q, len(d) / 1024, ''


def save_png(img, path, alpha, kmax):
    im = img if alpha else img.convert('RGB')
    im.save(path, 'PNG', optimize=True)
    kb = os.path.getsize(path) / 1024
    if kmax and kb > kmax:
        q = im.quantize(256, method=Image.FASTOCTREE) if alpha else im.quantize(256)
        q.save(path, 'PNG', optimize=True); kb = os.path.getsize(path) / 1024
        return kb, f'{kmax}KB 넘어서 256색으로 줄임'
    return kb, ''


def main():
    ap = argparse.ArgumentParser(description='banner.html 아트보드를 규격 PNG/JPG 로')
    ap.add_argument('html'); ap.add_argument('out')
    ap.add_argument('--look'); ap.add_argument('--theme'); ap.add_argument('--font'); ap.add_argument('--preset')
    ap.add_argument('--only', help='쉼표로 data-name 목록'); ap.add_argument('--suffix', default='')
    ap.add_argument('--no-check', action='store_true')
    a = ap.parse_args()
    src = os.path.abspath(a.html)
    if not os.path.isfile(src): sys.exit(f'[없음] {src}')
    os.makedirs(a.out, exist_ok=True)
    only = set(a.only.split(',')) if a.only else None

    raw = open(src, encoding='utf-8').read()
    file_issues = []
    if EMOJI.search(raw): file_issues.append('이모지 발견: ' + ', '.join(sorted(set(EMOJI.findall(raw))))[:80])
    if CTRL.search(raw): file_issues.append(f'U+0080~U+009F 제어문자 {len(CTRL.findall(raw))}개 (인코딩 깨짐 — CSS 이스케이프는 백슬래시로)')

    report = {'html': src, 'file_issues': file_issues, 'boards': []}
    with sync_playwright() as p:
        browser, used = launch(p)
        pg = browser.new_page(viewport={'width': 1400, 'height': 2100}, device_scale_factor=1)
        pg.goto('file:///' + src.replace('\\', '/'))
        pg.evaluate("""(o) => { document.documentElement.dataset.mode = 'export';
            const r = document.querySelector('.bn'); r.dataset.guides = 'off';
            for (const k of ['look','theme','font','preset']) if (o[k] !== null && o[k] !== undefined) r.dataset[k] = o[k]; }""",
                    {'look': a.look, 'theme': a.theme, 'font': a.font, 'preset': a.preset})
        pg.wait_for_load_state('networkidle')
        pg.evaluate('document.fonts.ready.then(() => true)')
        pg.wait_for_timeout(600)
        pg.evaluate("Promise.all([...document.images].map(i => i.complete ? 0 : new Promise(r => { i.onload = i.onerror = r; })))")
        pg.evaluate('document.fonts.ready.then(() => true)')
        checks = {} if a.no_check else {c['name']: c for c in pg.evaluate(CHECK_JS)}

        for el in pg.query_selector_all('.ab'):
            meta = el.evaluate("e => ({name:e.dataset.name,size:e.dataset.size,fmt:e.dataset.format||'png',kb:e.dataset.kb||'',alpha:e.dataset.alpha==='true'})")
            if only and meta['name'] not in only: continue
            W, H = map(int, meta['size'].split('x'))
            el.scroll_into_view_if_needed()
            shot = Image.open(io.BytesIO(el.screenshot(omit_background=meta['alpha'], animations='disabled')))
            rec = checks.get(meta['name'], {'name': meta['name'], 'issues': []})
            if shot.size != (W, H):
                rec['issues'].append(f'캡처 크기 {shot.size[0]}x{shot.size[1]} ≠ {W}x{H} → 맞춰 자름')
                shot = shot.crop((0, 0, W, H)) if shot.size[0] >= W and shot.size[1] >= H else shot.resize((W, H))
            kmin, kmax = (map(float, meta['kb'].split('-')) if meta['kb'] else (0, 0))
            base = os.path.join(a.out, meta['name'] + a.suffix)
            if meta['fmt'] == 'jpg':
                fmt, q, kb, warn = save_jpg(shot, base + '.jpg', kmin, kmax or 10240)
            else:
                kb, warn = save_png(shot, base + '.png', meta['alpha'], kmax); fmt, q = 'png', None
            if warn: rec['issues'].append(warn)
            if meta['alpha'] and shot.mode == 'RGBA' and shot.getextrema()[3][0] == 255:
                rec['issues'].append('투명 영역이 없어요 — 누끼(배경 없는 PNG)를 넣었는지 확인')
            rec.update({'file': os.path.basename(base) + '.' + fmt, 'kb': round(kb, 1), 'quality': q,
                        'kb_range': meta['kb'], 'pixels': f'{W}x{H}'})
            report['boards'].append(rec)
        browser.close()

    print(f'브라우저: {used} · 파일: {src}')
    for i in file_issues: print('  [파일] ' + i)
    for r in report['boards']:
        q = f" q{r['quality']}" if r.get('quality') else ''
        mins = f" 글자 최소 본문 {r.get('minBody') or '-'}px · 캡션 {r.get('minCap') or '-'}px" if r.get('minBody') or r.get('minCap') else ''
        img = f" · 배경 이미지 위 글자 {r['imageBg']}곳(눈으로 확인)" if r.get('imageBg') else ''
        print(f"  {r['file']:<34} {r['pixels']:>9}  {r['kb']:>7.1f}KB{q}{mins}{img}")
        for i in r['issues']: print('      - ' + i)
    with open(os.path.join(a.out, f'_export_report{a.suffix}.json'), 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=1)
    bad = sum(len(r['issues']) for r in report['boards']) + len(file_issues)
    print(f"끝. {len(report['boards'])}장, 확인할 것 {bad}건 → {os.path.join(a.out, f'_export_report{a.suffix}.json')}")


if __name__ == '__main__':
    main()
