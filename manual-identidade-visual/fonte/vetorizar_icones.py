"""Vetoriza as pranchas de ícones geradas no Canva.

Uso: python vectorize.py <prancha.png> <saida_dir> <nomes separados por vírgula> [line_px] [close_px]
"""
import sys, os
import numpy as np, cv2, potrace
from skimage.morphology import skeletonize

AZUL, VERDE = "#1D2756", "#70EF8E"
src, out, names = sys.argv[1], sys.argv[2], sys.argv[3].split(",")
LINE_W = float(sys.argv[4]) if len(sys.argv) > 4 else 15.0   # espessura final da linha, em px da prancha
CLOSE = int(sys.argv[5]) if len(sys.argv) > 5 else 9          # emenda das falhas
os.makedirs(out, exist_ok=True)

img = cv2.imread(src)[:, :, ::-1].astype(np.float32)   # RGB
R, G, B = img[..., 0], img[..., 1], img[..., 2]
lum = 0.299 * R + 0.587 * G + 0.114 * B
fg = ((255 - R) + (255 - B) > 70).astype(np.uint8)         # mancha + linhas (não branco)
line = (lum < 150).astype(np.uint8)                         # linhas azuis, incluindo as mais fracas

def ell(k): return cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (k, k))

# separa os ícones pelos blocos de mancha
fgc = cv2.morphologyEx(fg, cv2.MORPH_CLOSE, ell(15))
n, lab, stats, cent = cv2.connectedComponentsWithStats(fgc)
allb = [i for i in range(1, n) if stats[i, cv2.CC_STAT_AREA] > 1500]
med = np.median([stats[i, cv2.CC_STAT_AREA] for i in allb])
blobs = [i for i in allb if stats[i, cv2.CC_STAT_AREA] > med * .3]
groups = {i: [i] for i in blobs}
for i in allb:
    if i in blobs: continue
    near = min(blobs, key=lambda b: np.hypot(*(cent[b] - cent[i])))
    groups[near].append(i)
mid = np.median([cent[i][1] for i in blobs])
top = sorted([i for i in blobs if cent[i][1] < mid], key=lambda i: cent[i][0])
bot = sorted([i for i in blobs if cent[i][1] >= mid], key=lambda i: cent[i][0])
order = top + bot
assert len(order) == len(names), (len(order), names)

def trace(mask, alphamax=1.1, turd=40):
    bm = potrace.Bitmap(~mask.astype(bool))   # o potracer considera False como preenchido
    plist = bm.trace(turdsize=turd, turnpolicy=potrace.POTRACE_TURNPOLICY_MINORITY, alphamax=alphamax,
                     opticurve=True, opttolerance=0.3)
    parts = []
    for curve in plist:
        s = curve.start_point
        d = [f"M{s.x:.1f} {s.y:.1f}"]
        for seg in curve:
            if seg.is_corner:
                d.append(f"L{seg.c.x:.1f} {seg.c.y:.1f} L{seg.end_point.x:.1f} {seg.end_point.y:.1f}")
            else:
                d.append(f"C{seg.c1.x:.1f} {seg.c1.y:.1f} {seg.c2.x:.1f} {seg.c2.y:.1f} {seg.end_point.x:.1f} {seg.end_point.y:.1f}")
        d.append("Z")
        parts.append(" ".join(d))
    return " ".join(parts)

for idx, name in zip(order, names):
    g = groups[idx]
    xs = [stats[i, 0] for i in g]; ys = [stats[i, 1] for i in g]
    xe = [stats[i, 0] + stats[i, 2] for i in g]; ye = [stats[i, 1] + stats[i, 3] for i in g]
    x, y = min(xs), min(ys); w, h = max(xe) - x, max(ye) - y
    pad = 30
    x0, y0 = max(0, x - pad), max(0, y - pad)
    x1, y1 = min(img.shape[1], x + w + pad), min(img.shape[0], y + h + pad)
    comp = np.isin(lab[y0:y1, x0:x1], g).astype(np.uint8)
    # normaliza o tamanho: o ícone passa a ter 860 px no maior lado, para a linha ficar igual em todos
    sc = 860.0 / max(w, h)
    def rs(m): return (cv2.resize(m.astype(np.float32), None, fx=sc, fy=sc, interpolation=cv2.INTER_LINEAR) > .5).astype(np.uint8)
    comp = rs(comp); line_c = rs(line[y0:y1, x0:x1])
    # mancha: só este ícone, sem furos, contorno suavizado
    sil = comp.copy()
    cnts, _ = cv2.findContours(sil, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    sil = np.zeros_like(sil); cv2.drawContours(sil, cnts, -1, 1, -1)
    sil = cv2.morphologyEx(sil, cv2.MORPH_OPEN, ell(9))
    sil = (cv2.GaussianBlur(sil.astype(np.float32), (0, 0), 3) > .5).astype(np.uint8)
    # linhas: dentro da mancha, falhas emendadas, eixo central, espessura uniforme
    ln = line_c & cv2.erode(sil, ell(5))
    ln = cv2.morphologyEx(ln, cv2.MORPH_CLOSE, ell(CLOSE))
    nl, llab, lst, _ = cv2.connectedComponentsWithStats(ln)
    keep = np.zeros_like(ln)
    for j in range(1, nl):
        if lst[j, cv2.CC_STAT_AREA] >= 60: keep[llab == j] = 1
    sk = skeletonize(keep.astype(bool)).astype(np.uint8)
    r = int(round(LINE_W / 2))
    ln2 = cv2.dilate(sk, ell(2 * r + 1))
    ln2 = (cv2.GaussianBlur(ln2.astype(np.float32), (0, 0), 1.2) > .5).astype(np.uint8)
    H, W = sil.shape
    BOX = 960
    ox, oy = (BOX - W) / 2, (BOX - H) / 2
    d_sil = trace(sil, alphamax=1.2, turd=200)
    d_ln = trace(ln2, alphamax=1.0, turd=20)
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {BOX} {BOX}" width="512" height="512">'
           f'<g transform="translate({ox:.1f} {oy:.1f})">'
           f'<path fill="{VERDE}" fill-rule="evenodd" d="{d_sil}"/>'
           f'<path fill="{AZUL}" fill-rule="evenodd" d="{d_ln}"/></g></svg>')
    open(os.path.join(out, name + ".svg"), "w").write(svg)
    print(name, W, H, len(svg) // 1024, "KB")
