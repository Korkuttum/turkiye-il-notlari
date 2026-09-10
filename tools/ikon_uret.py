"""Uygulama ikonlarını üretir: açık kitap + içinde renkli Türkiye haritası."""
import colorsys, json, math, os
from PIL import Image, ImageDraw

geo = json.load(open('static/tr-cities.json', encoding='utf-8'))

def proj(lon, lat):
    return (lon * math.pi / 180, math.log(math.tan(math.pi / 4 + lat * math.pi / 360)))

iller = []          # (plaka, [ring, ...])
for f in geo['features']:
    g = f['geometry']
    polys = g['coordinates'] if g['type'] == 'MultiPolygon' else [g['coordinates']]
    iller.append((f['properties']['number'],
                  [[proj(*c[:2]) for c in poly[0]] for poly in polys]))

pts = [p for _, rs in iller for r in rs for p in r]
minx, maxx = min(p[0] for p in pts), max(p[0] for p in pts)
miny, maxy = min(p[1] for p in pts), max(p[1] for p in pts)
GEO_W, GEO_H = maxx - minx, maxy - miny

BG_TOP, BG_BOT = (37, 99, 235), (23, 64, 178)

def il_rengi(plaka):
    """Web arayüzüyle aynı altın-açı renk dağılımı."""
    h = ((plaka * 137.508) % 360) / 360
    s = (55 + (plaka * 7) % 18) / 100
    l = (58 + (plaka * 11) % 14) / 100
    r, g, b = colorsys.hls_to_rgb(h, l, s)
    return (round(r * 255), round(g * 255), round(b * 255))

def render(size, out, content=0.86, ss=4):
    S = size * ss
    img = Image.new('RGB', (S, S), BG_TOP)
    d = ImageDraw.Draw(img)
    for y in range(S):
        t = y / (S - 1)
        d.line([(0, y), (S, y)],
               fill=tuple(round(BG_TOP[i] + (BG_BOT[i] - BG_TOP[i]) * t) for i in range(3)))

    box = S * content
    bw = box                    # kitap genişliği
    bh = bw * 0.62              # kitap yüksekliği
    bx = (S - bw) / 2
    by = (S - bh) / 2 + S * 0.02

    def P(nx, ny):
        return (bx + nx * bw, by + ny * bh)

    # --- kitap gövdesi ---
    golge = [P(0.02, 0.26), P(0.50, 0.10), P(0.98, 0.26), P(0.98, 1.06), P(0.50, 0.92), P(0.02, 1.06)]
    d.polygon(golge, fill=(17, 40, 96))          # alt gölge / cilt
    sol = [P(0.00, 0.20), P(0.487, 0.04), P(0.487, 0.90), P(0.00, 1.00)]
    sag = [P(1.00, 0.20), P(0.513, 0.04), P(0.513, 0.90), P(1.00, 1.00)]
    d.polygon(sol, fill='#ffffff')
    d.polygon(sag, fill='#ffffff')

    # --- sayfaların üzerine renkli harita ---
    m_w = bw * 0.78
    m_scale = m_w / GEO_W
    m_h = GEO_H * m_scale
    mx = bx + (bw - m_w) / 2
    my = by + bh * 0.50 - m_h / 2

    cizgi = max(1, int(S * 0.0035))
    for plaka, ringler in iller:
        renk = il_rengi(plaka)
        for r in ringler:
            poly = [(mx + (x - minx) * m_scale, my + (maxy - y) * m_scale) for x, y in r]
            if len(poly) >= 3:
                d.polygon(poly, fill=renk)
                d.line(poly + [poly[0]], fill='#ffffff', width=cizgi)

    # --- kitap sırtı ---
    d.line([P(0.50, 0.045), P(0.50, 0.915)], fill=(214, 222, 236), width=max(2, int(S * 0.006)))

    img = img.resize((size, size), Image.LANCZOS)
    img.save(out)
    print(out, img.size)

os.makedirs('static/icons', exist_ok=True)
render(180, 'static/icons/apple-touch-icon.png')
render(192, 'static/icons/icon-192.png')
render(512, 'static/icons/icon-512.png')
render(512, 'static/icons/icon-512-maskable.png', content=0.64)
