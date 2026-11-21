# -*- coding: utf-8 -*-
"""
export_page.py — 2_상세페이지.html 을 올릴 이미지로 뽑는다. 전체 1장 + 나눈 조각.

  python assets/export_page.py 2_상세페이지.html 3_업로드이미지/ [--platform smartstore|coupang|both|mall] [--max-h 3000] [--q 90]

하는 일
  1. Edge(없으면 Chrome → playwright Chromium)로 폰 화면 폭(스마트스토어·자사몰 430px · 쿠팡 390px)을 2배로 찍는다
     → 가로 860px / 780px. PC 레이아웃으로 찍으면 폰에서 글씨가 반으로 줄어 못 읽는다.
     모션은 끄고(줄이기 모드) 숫자 카운트업은 최종 값으로 찍는다.
     Chromium 스크린샷은 한 번에 16,384px까지라, 3,000 CSS px씩 나눠 찍어 이어 붙인다(긴 상세도 끝까지 찍힌다).
  2. <플랫폼>/상세_전체.jpg — 페이지 전체 한 장.
  3. <플랫폼>/조각_01.jpg … — 섹션 경계에서 자른 조각. 작은 섹션은 이어 붙여 한 장이 --max-h 를 넘지 않게
     (기본 3,000px: 쿠팡 장당 세로 제한이 자료마다 3,000~5,000px 이라 안전한 쪽). 한 섹션이 더 길면 그 안에서 자른다.
  4. 쿠팡은 옵션 구성표(.optable)와 .no-coupang 요소(무료배송·할인 같은 혜택 문구)를 빼고 찍는다
     (쿠팡 상세 이미지 안 가격·할인·무료배송 문구 금지). 빼고도 그런 문구가 남아 있으면 보고서에 적는다.
  5. 점검: 장당 용량(스마트스토어 20MB · 쿠팡 10MB), 전체 높이(스마트스토어는 4,000px 넘으면 앞 3,000px만 보이고 접힘
     → 3번 섹션이 앞 3,000px 안에서 시작하는지), 남은 {{자리표시}}, 빈 이미지 자리(.ph).
     결과는 화면과 <출력폴더>/_export_report.json 한 개(플랫폼별 결과가 그 안에 다 들어간다).
  6. --platform mall: 자사몰(카페24 등)만 쓸 때. 자사몰은 HTML을 그대로 넣는 게 기본이라 이 이미지는 미리보기·카톡 확인용
     (또는 이미지형 업로드용). 스마트스토어 접힘 점검은 하지 않는다.

의존성: pip install playwright pillow  (Windows 는 Edge 가 있어 브라우저 설치 불필요)
"""
import sys, os, io, json, argparse

for _st in (sys.stdout, sys.stderr):          # Windows cp949 콘솔에서 '—' 같은 글자로 죽지 않게
    try:
        _st.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

try:
    from PIL import Image
    Image.MAX_IMAGE_PIXELS = None
except ImportError:
    sys.exit('[필요] Pillow 가 없어요.  pip install pillow  후 다시 실행하세요.')
try:
    from playwright.sync_api import sync_playwright
except ImportError:
    sys.exit('[필요] playwright 가 없어요.  pip install playwright  후 다시 실행하세요.')

PLAT = {
    'smartstore': {'css': 430, 'name': '스마트스토어', 'mb': 20, 'fold': True},
    'coupang':    {'css': 390, 'name': '쿠팡',        'mb': 10, 'fold': False},
    'mall':       {'css': 430, 'name': '자사몰',      'mb': 20, 'fold': False},
}
FOLD_PX = 3000      # 스마트스토어: 4,000px 넘는 상세는 앞 3,000px만 보이고 접힌다
TILE_CSS = 3000     # 한 번에 찍는 높이(CSS px). 2배율이면 6,000px — Chromium 한계 16,384px 아래


def launch(p):
    for kw in ({'channel': 'msedge'}, {'channel': 'chrome'}, {}):
        try:
            return p.chromium.launch(**kw)
        except Exception:
            continue
    sys.exit('[필요] 쓸 수 있는 브라우저가 없어요.  python -m playwright install chromium  을 실행하세요.')


def jpg(img, path, q):
    img.convert('RGB').save(path, 'JPEG', quality=q, optimize=True, progressive=True)
    return os.path.getsize(path) / 1024 / 1024


def capture(pg):
    """.page(.pdp)를 TILE_CSS 높이씩 나눠 찍어 이어 붙인다. 한 번에 찍으면 16,384px 아래가 첫 화면으로 다시 찍힌다."""
    box = pg.evaluate("""() => { const r = (document.querySelector('.pdp') || document.querySelector('.page')).getBoundingClientRect();
        return {x: r.left + scrollX, y: r.top + scrollY, w: r.width, h: r.height}; }""")
    tiles, y0 = [], 0.0
    while y0 < box['h'] - 0.5:
        hh = min(TILE_CSS, box['h'] - y0)
        png = pg.screenshot(full_page=True, animations='disabled',
                            clip={'x': box['x'], 'y': box['y'] + y0, 'width': box['w'], 'height': hh})
        tiles.append(Image.open(io.BytesIO(png)).convert('RGB'))
        y0 += hh
    shot = Image.new('RGB', (tiles[0].size[0], sum(t.size[1] for t in tiles)), 'white')
    yy = 0
    for t in tiles:
        shot.paste(t, (0, yy)); yy += t.size[1]
    return shot


def cut_points(bounds, total, max_h):
    """섹션 경계(bounds: 각 섹션 시작 y, 2배율 px)에서 max_h 를 넘지 않게 자를 위치들."""
    edges = sorted(set([0] + [b for b in bounds if 0 < b < total] + [total]))
    cuts, start = [0], 0
    for i in range(1, len(edges)):
        e = edges[i]
        if e - start <= max_h:
            continue
        prev = edges[i - 1]
        if prev > start:                      # 앞 경계까지 한 장
            cuts.append(prev); start = prev
        while e - start > max_h:              # 한 섹션이 max_h 보다 길면 그 안에서 자른다
            start += max_h; cuts.append(start)
    if cuts[-1] != total:
        cuts.append(total)
    return cuts


def run(pg, src, plat, out, max_h, q):
    cfg = PLAT[plat]
    pg.set_viewport_size({'width': cfg['css'], 'height': 900})
    pg.goto('file:///' + src.replace('\\', '/'))
    pg.wait_for_load_state('networkidle')
    pg.evaluate("Promise.all([...document.images].map(i => i.complete ? 0 : new Promise(r => { i.onload = i.onerror = r; })))")
    pg.evaluate('document.fonts.ready.then(() => true)')
    pg.evaluate("""(plat) => {
        document.querySelectorAll('.big[data-count]').forEach(el => {
            const raw = el.getAttribute('data-count') || '', suf = el.getAttribute('data-suffix') || '';
            const n = parseFloat(raw.replace(/,/g, '')); if (!isNaN(n)) {
                const dec = (raw.split('.')[1] || '').length;
                el.textContent = n.toLocaleString('ko-KR', {minimumFractionDigits: dec, maximumFractionDigits: dec}) + suf; }
            el.classList.add('done'); });
        if (plat === 'coupang') document.querySelectorAll('.optable, .no-coupang').forEach(e => e.remove());
        document.body.style.background = 'transparent';
    }""", plat)
    pg.wait_for_timeout(400)
    page = pg.query_selector('.pdp') or pg.query_selector('.page')
    if page is None:
        sys.exit('[없음] .page(또는 .pdp) 요소를 못 찾았어요.')
    info = pg.evaluate("""() => {
        const root = document.querySelector('.pdp') || document.querySelector('.page');
        const r0 = root.getBoundingClientRect();
        const secs = [...root.querySelectorAll(':scope > section, :scope > div.s, :scope > .s')]
                     .map(s => Math.round(s.getBoundingClientRect().top - r0.top));
        const txt = root.innerText;
        return { w: Math.round(r0.width), h: Math.round(r0.height), secs,
                 left: [...new Set((txt.match(/\\{\\{[^}]+\\}\\}/g) || []))].slice(0, 12),
                 ph: [...root.querySelectorAll('.ph')].filter(p => p.getClientRects().length).length,
                 promo: [...new Set((txt.match(/무료\\s?배송|무배|할인|특가|쿠폰|적립|\\d[\\d,]*\\s?원(?![가-힣])|https?:\\/\\/\\S+/g) || []))].slice(0, 8) };
    }""")
    shot = capture(pg)
    W, H = shot.size
    d = os.path.join(out, cfg['name']); os.makedirs(d, exist_ok=True)
    for old in os.listdir(d):                  # 지난번 조각이 남아 있으면 개수가 줄었을 때 옛 조각이 섞인다
        if old.startswith('조각_') and old.endswith('.jpg'):
            os.remove(os.path.join(d, old))
    rec = {'platform': cfg['name'], 'width': W, 'height': H, 'files': [], 'issues': []}
    if W != cfg['css'] * 2:
        rec['issues'].append(f'가로 {W}px — {cfg["css"] * 2}px 이어야 해요(템플릿 --w 확인)')

    full = os.path.join(d, '상세_전체.jpg')
    mb = jpg(shot, full, q)
    if mb > cfg['mb']:                         # 용량 넘으면 품질을 낮춰 한 번 더
        mb = jpg(shot, full, 78)
    rec['files'].append({'file': os.path.relpath(full, out), 'px': f'{W}x{H}', 'mb': round(mb, 2)})
    if mb > cfg['mb']:
        rec['issues'].append(f'전체 1장이 {mb:.1f}MB > {cfg["mb"]}MB — 이 플랫폼엔 조각으로 올리세요')
    if plat == 'coupang':
        rec['issues'].append('쿠팡은 장당 세로 제한이 있어 전체 1장 대신 조각으로 올리세요 (전체는 확인·보관용)')
    scale = H / max(info['h'], 1)
    bounds = [round(y * scale) for y in info['secs']]
    rec['sections_px'] = bounds
    if cfg['fold'] and H > 4000:
        s3 = bounds[2] if len(bounds) > 2 else None
        rec['note'] = f'전체 높이 {H}px — 스마트스토어는 앞 {FOLD_PX:,}px만 먼저 보이고 나머지는 "펼쳐보기"로 접혀요.'
        if s3 is not None:
            rec['note'] += f' 3번 섹션 시작 {s3:,}px'
            if s3 > FOLD_PX:
                rec['issues'].append(f'3번 섹션이 {s3:,}px에서 시작 — 앞 {FOLD_PX:,}px 안에서 시작하게 1번 첫 화면·2번 신뢰를 줄이세요(SKILL.md "결정 정보는 앞 3,000px 안에")')
            else:
                rec['note'] += ' (OK)'
    cuts = cut_points(bounds, H, max_h)
    for i in range(len(cuts) - 1):
        piece = shot.crop((0, cuts[i], W, cuts[i + 1]))
        p = os.path.join(d, f'조각_{i + 1:02d}.jpg')
        m = jpg(piece, p, q)
        rec['files'].append({'file': os.path.relpath(p, out), 'px': f'{W}x{cuts[i + 1] - cuts[i]}', 'mb': round(m, 2)})
        if m > cfg['mb']:
            rec['issues'].append(f'{os.path.basename(p)} {m:.1f}MB > {cfg["mb"]}MB')
    if info['left']:
        rec['issues'].append('남은 자리표시: ' + ', '.join(info['left']))
    if plat == 'coupang' and info['promo']:
        rec['issues'].append('쿠팡 이미지에 가격·혜택 문구: ' + ', '.join(info['promo']) +
                             ' — 그 문장(요소)에 class="no-coupang"을 붙이면 쿠팡 이미지에서만 빠져요')
    if info['ph']:
        rec['issues'].append(f'빈 이미지 자리(.ph) {info["ph"]}개')
    return rec


def main():
    ap = argparse.ArgumentParser(description='상세페이지 HTML → 업로드 이미지(전체 1장 + 조각)')
    ap.add_argument('html'); ap.add_argument('out')
    ap.add_argument('--platform', default='smartstore', choices=['smartstore', 'coupang', 'both', 'mall'],
                    help='both = 스마트스토어+쿠팡, mall = 자사몰만(미리보기용, 접힘 점검 없음)')
    ap.add_argument('--max-h', type=int, default=3000, help='조각 한 장 최대 세로 px (기본 3000)')
    ap.add_argument('--q', type=int, default=90, help='JPG 품질 (기본 90)')
    a = ap.parse_args()
    src = os.path.abspath(a.html)
    if not os.path.isfile(src):
        sys.exit(f'[없음] {src}')
    os.makedirs(a.out, exist_ok=True)
    plats = ['smartstore', 'coupang'] if a.platform == 'both' else [a.platform]
    report = {'html': src, 'results': []}
    with sync_playwright() as p:
        b = launch(p)
        ctx = b.new_context(device_scale_factor=2, reduced_motion='reduce')
        pg = ctx.new_page()
        for pl in plats:
            report['results'].append(run(pg, src, pl, a.out, a.max_h, a.q))
        b.close()
    rp = os.path.join(a.out, '_export_report.json')   # 출력이 깨져도 보고서는 남게 먼저 쓴다
    with open(rp, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=1)
    for r in report['results']:
        print(f"[{r['platform']}] 가로 {r['width']}px · 전체 높이 {r['height']}px")
        for f in r['files']:
            print(f"  {f['file']:<28} {f['px']:>11}  {f['mb']:>5.2f}MB")
        if r.get('note'):
            print('  * ' + r['note'])
        for i in r['issues']:
            print('  - ' + i)
    print(f'보고서: {rp}')


if __name__ == '__main__':
    main()
