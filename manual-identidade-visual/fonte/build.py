import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from colorlib import hx, cmyk, cr, mix

TPL, OUT = sys.argv[1], sys.argv[2]
AZUL, VERDE, BRANCO = "#1D2756", "#70EF8E", "#FFFFFF"

# ---------- cores ----------
C = {
    "Azul Noite": "#0E1433", "Azul Inah": AZUL, "Azul Céu": "#2F6FD8", "Rio": "#1FB5A5",
    "Verde Inah": VERDE, "Verde Folha": "#C2F06A", "Verde Mata": "#16794A",
    "Amarelo Lanterna": "#FFD447", "Laranja Fogueira": "#FF7A3D", "Terra": "#7A4E2D",
    "Areia": "#F4E8D0", "Névoa": "#EEF5F1", "Branco": BRANCO, "Cinza 333": "#333333",
}

def rgb_s(h): return " · ".join(str(v) for v in hx(h))
def cmyk_s(h): return " · ".join(str(v) for v in cmyk(h))
def on(h):
    """cor de texto legivel sobre h"""
    if cr(h, BRANCO) >= 4.5: return BRANCO
    if cr(h, AZUL) >= 4.5: return AZUL
    return "#000000"

def codes(h):
    return (f'<p class="codes"><button class="code" type="button" data-copy="{h}">{h}</button>'
            f'<span class="code">RGB {rgb_s(h)}</span><span class="code">CMYK {cmyk_s(h)}</span></p>')

def crow(name, h, role=""):
    r = f' <span class="role">{role}</span>' if role else ""
    return (f'<div class="crow"><i style="background:{h}"></i><div class="crow-t">'
            f'<p><b>{name}</b>{r}</p>{codes(h)}</div></div>')

def tile(name, h, role=""):
    r = f'<span class="role">{role}</span>' if role else ""
    return (f'<div class="ctile"><div class="ctile-c" style="background:{h}"></div><div class="ctile-t">'
            f'<b>{name}</b>{r}{codes(h)}</div></div>')

# ---------- escala de cinza ----------
grays = [("Preto", "#000000", "Marca em uma cor, carimbo"), ("Cinza 80", "#333333", "Texto corrido"),
         ("Cinza 60", "#666666", "Legendas e textos secundários"), ("Cinza 40", "#999999", "Ícones e fios. Não em texto"),
         ("Cinza 20", "#CCCCCC", "Fundos, divisórias, flor em P&amp;B")]
GRAYS = '<div class="ctiles">' + "".join(tile(n, h, r) for n, h, r in grays) + "</div>"

# ---------- paletas ----------
palettes = [
    ("Essencial", "Documentos, ofícios, site e tudo o que é institucional. É a paleta padrão.",
     [("Azul Inah", 40), ("Branco", 40), ("Verde Inah", 12), ("Cinza 333", 8)]),
    ("Mata Atlântica", "Acampamentos, trilhas e atividades ao ar livre. Inspirada na mata de Paranapiacaba.",
     [("Verde Mata", 26), ("Verde Inah", 18), ("Verde Folha", 12), ("Azul Inah", 18), ("Terra", 10), ("Areia", 16)]),
    ("Rio e Céu", "Redes sociais e peças para jovens. É a paleta mais luminosa.",
     [("Azul Inah", 26), ("Azul Céu", 22), ("Rio", 18), ("Verde Inah", 16), ("Névoa", 18)]),
    ("Fogo de Conselho", "Festas, Fogo de Conselho, aniversário do grupo e eventos à noite.",
     [("Azul Noite", 34), ("Azul Inah", 20), ("Laranja Fogueira", 18), ("Amarelo Lanterna", 16), ("Verde Inah", 12)]),
]
def pal(name, use, cols):
    strip = "".join(
        f'<div style="flex:{w};background:{C[n]};color:{on(C[n])}">{n if w >= 18 else ""}</div>' for n, w in cols)
    rows = "".join(crow(n if n != "Cinza 333" else "Cinza 80", C[n]) for n, _ in cols)
    return (f'<article class="pal"><div class="pal-strip" role="img" aria-label="Paleta {name}">{strip}</div>'
            f'<div class="pal-body"><h4>{name}</h4><p class="small">{use}</p><div class="crows">{rows}</div></div></article>')
PALETTES = '<div class="grid g2">' + "".join(pal(*p) for p in palettes) + "</div>"

# ---------- escalas ----------
az = [("Azul 900", C["Azul Noite"]), ("Azul 700", AZUL), ("Azul 500", mix(AZUL, BRANCO, .28)),
      ("Azul 300", mix(AZUL, BRANCO, .58)), ("Azul 100", mix(AZUL, BRANCO, .88))]
vd = [("Verde 900", mix(VERDE, "#0B3326", .82)), ("Verde 700", mix(VERDE, "#0B3326", .45)), ("Verde 500", VERDE),
      ("Verde 300", mix(VERDE, BRANCO, .45)), ("Verde 100", mix(VERDE, BRANCO, .82))]
def scale(items):
    return '<div class="ctiles c5">' + "".join(
        tile(n, h, "cor da marca" if h in (AZUL, VERDE) else "") for n, h in items) + "</div>"
SCALES = scale(az) + '<div style="height:12px"></div>' + scale(vd)

# ---------- combinações ----------
pairs = [(AZUL, BRANCO, "Azul sobre branco"), (BRANCO, AZUL, "Branco sobre azul"), (VERDE, AZUL, "Verde sobre azul"),
         (AZUL, VERDE, "Azul sobre verde"), ("#333333", BRANCO, "Cinza 80 sobre branco"), ("#666666", BRANCO, "Cinza 60 sobre branco"),
         (BRANCO, C["Verde Mata"], "Branco sobre Verde Mata"), (BRANCO, C["Azul Céu"], "Branco sobre Azul Céu"),
         (AZUL, C["Laranja Fogueira"], "Azul sobre Laranja Fogueira"), (AZUL, C["Rio"], "Azul sobre Rio"),
         (C["Amarelo Lanterna"], C["Azul Noite"], "Lanterna sobre Azul Noite"), (AZUL, C["Areia"], "Azul sobre Areia"),
         (BRANCO, C["Rio"], "Branco sobre Rio"), (BRANCO, C["Laranja Fogueira"], "Branco sobre Laranja"),
         ("#999999", BRANCO, "Cinza 40 sobre branco"), (VERDE, BRANCO, "Verde sobre branco")]
def pair(fg, bg, label):
    r = cr(fg, bg)
    if r >= 4.5: cls, ic, note = "yes", "i-yes", ""
    elif r >= 3: cls, ic, note = "warn", "i-warn", " · só títulos grandes"
    else: cls, ic, note = "no", "i-no", ""
    rs = f"{r:.1f}".replace(".", ",")
    return (f'<div class="pair"><div class="pair-demo" style="background:{bg};color:{fg}"><b>Aa</b><span>Sempre Alerta</span></div>'
            f'<div class="pair-info"><span class="mono">{rs} : 1{note}</span><span class="verdict {cls}"><svg width="16" height="16"><use href="#{ic}"/></svg>{label}</span></div></div>')
PAIRS = '<div class="pairs">' + "".join(pair(*p) for p in pairs) + "</div>"

# ---------- degradês ----------
def rgba(h, a):
    r, g, b = hx(h); return f"rgba({r},{g},{b},{a})"
def sample(stops, n=24):
    """cores ao longo do degradê (interpolação simples em sRGB)"""
    out = []
    for i in range(n + 1):
        t = 100 * i / n
        for (a, pa), (b, pb) in zip(stops, stops[1:]):
            if pa <= t <= pb:
                out.append(mix(C[a], C[b], (t - pa) / (pb - pa) if pb > pa else 0)); break
    return out
def text_rule(colors):
    if min(cr(AZUL, c) for c in colors) >= 4.5: return "azul", AZUL
    if min(cr(BRANCO, c) for c in colors) >= 4.5: return "branco", BRANCO
    return "misto", AZUL
TAG = {"azul": f'<p class="tag-txt"><i style="background:{AZUL}"></i>Texto azul em qualquer ponto</p>',
       "branco": f'<p class="tag-txt"><i style="background:{BRANCO}"></i>Texto branco em qualquer ponto</p>',
       "misto": f'<p class="tag-txt"><i style="background:{AZUL}"></i><i style="background:{BRANCO}"></i>Texto azul na parte clara, branco na escura</p>'}

grads = [
    ("Lis", "O degradê principal. Capas, banners e fundos de redes sociais.", 135,
     [("Verde Inah", 0), ("Rio", 38), ("Azul Céu", 70), ("Azul Inah", 100)]),
    ("Mata", "Natureza, acampamentos e atividades ao ar livre.", 135,
     [("Verde Folha", 0), ("Verde Inah", 42), ("Verde Mata", 100)]),
    ("Amanhecer", "Peças leves e alegres, convites para famílias.", 135,
     [("Amarelo Lanterna", 0), ("Verde Folha", 50), ("Verde Inah", 100)]),
    ("Fogueira", "Festas, Fogo de Conselho e eventos.", 135,
     [("Amarelo Lanterna", 0), ("Laranja Fogueira", 100)]),
    ("Noite", "Fundos escuros, apresentações e telas.", 160,
     [("Azul Céu", 0), ("Azul Inah", 55), ("Azul Noite", 100)]),
    ("Mata Profunda", "Fundo escuro com cara de mata fechada, para acampamentos e jornadas.", 160,
     [("Verde Mata", 0), ("Azul Inah", 60), ("Azul Noite", 100)]),
]
def css_grad(angle, stops):
    return f"linear-gradient({angle}deg," + ",".join(f"{C[n]} {p}%" for n, p in stops) + ")"
def grad(name, use, angle, stops):
    kind, txt = text_rule(sample(stops))
    rows = "".join(crow(n, C[n], f"{p}%") for n, p in stops)
    return (f'<article class="grad"><div class="grad-demo" style="background:{css_grad(angle, stops)};color:{txt}">'
            f'<b>{name}</b><span class="mono">{angle}°</span></div>'
            f'<div class="grad-body">{TAG[kind]}<p class="small">{use}</p><div class="crows">{rows}</div></div></article>')
GRADIENTS = '<div class="grid g3">' + "".join(grad(*g) for g in grads) + "</div>"
GRAD_CSS = {g[0]: css_grad(g[2], g[3]) for g in grads}

# ---------- malhas ----------
def rad(size, at, name, a, stop):
    return f"radial-gradient({size} at {at},{rgba(C[name], a)} 0%,{rgba(C[name], 0)} {stop}%)"
MESH = {
    "lis": ",".join([rad("110% 80%", "0% 0%", "Verde Folha", 1, 50), rad("90% 90%", "100% 100%", "Azul Inah", 1, 62),
                     "linear-gradient(135deg,#70EF8E 0%,#1FB5A5 48%,#2F6FD8 100%)"]),
    "noite": ",".join([rad("75% 65%", "88% 12%", "Azul Céu", .85, 62), rad("70% 60%", "6% 100%", "Verde Inah", .45, 60),
                       "linear-gradient(160deg,#1D2756 0%,#0E1433 100%)"]),
    "fogueira": ",".join([rad("90% 55%", "50% 108%", "Amarelo Lanterna", 1, 55), rad("110% 70%", "50% 110%", "Laranja Fogueira", .95, 70),
                          "linear-gradient(180deg,#0E1433 0%,#1D2756 70%)"]),
    "mataprofunda": ",".join([rad("80% 70%", "0% 0%", "Verde Mata", .95, 62), rad("70% 60%", "100% 100%", "Azul Céu", .6, 60),
                              "linear-gradient(160deg,#1D2756 0%,#0E1433 100%)"]),
    "rio": ",".join([rad("80% 70%", "0% 0%", "Verde Inah", .9, 55), rad("85% 80%", "100% 100%", "Azul Inah", .95, 60),
                     "linear-gradient(135deg,#1FB5A5 0%,#2F6FD8 100%)"]),
}
meshes = [
    ("Malha Lis", "lis", "misto", ["Verde Folha", "Verde Inah", "Rio", "Azul Céu", "Azul Inah"], "Texto azul na área clara do canto superior."),
    ("Malha Rio", "rio", "misto", ["Verde Inah", "Rio", "Azul Céu", "Azul Inah"], "Texto azul no canto verde; branco no canto azul."),
    ("Malha Noite", "noite", "branco", ["Azul Noite", "Azul Inah", "Azul Céu", "Verde Inah"], "Escura. Apresentações e stories."),
    ("Malha Mata Profunda", "mataprofunda", "branco", ["Azul Noite", "Azul Inah", "Verde Mata", "Azul Céu"], "Escura, com um brilho de mata."),
    ("Malha Fogueira", "fogueira", "misto", ["Azul Noite", "Azul Inah", "Laranja Fogueira", "Amarelo Lanterna"], "Texto branco na parte de cima, longe do brilho."),
]
MESH_TAG = {"azul": TAG["azul"], "branco": TAG["branco"],
            "misto": '<p class="tag-txt"><i style="background:#1D2756"></i><i style="background:#FFFFFF"></i>Texto conforme a região</p>'}
def mesh(name, key, kind, cols, rule):
    txt = BRANCO if kind == "branco" or key == "fogueira" else AZUL
    rows = "".join(crow(n, C[n]) for n in cols)
    return (f'<article class="grad"><div class="grad-demo tall" style="background:{MESH[key]};color:{txt}"><b>{name}</b></div>'
            f'<div class="grad-body">{MESH_TAG[kind]}<p class="small">{rule}</p><div class="crows">{rows}</div></div></article>')
MESHES = '<div class="grid g3">' + "".join(mesh(*m) for m in meshes) + "</div>"

# ---------- texturas (pílulas) ----------
PATHS = ["M-30 70 C 120 30 230 170 100 240 S -60 380 110 440 S 250 540 90 600",
         "M240 150 C 90 190 30 300 150 340 S 270 470 -40 520",
         "M-40 300 C 50 250 160 380 240 330"]
textures = [
    ("Verde Inah", [("Azul Inah", "Azul Céu"), ("Rio", "Azul Inah"), ("Azul Céu", "Rio")]),
    ("Azul Inah", [("Verde Inah", "Rio"), ("Amarelo Lanterna", "Verde Folha"), ("Azul Céu", "Verde Inah")]),
    ("Verde Folha", [("Verde Mata", "Verde Inah"), ("Azul Céu", "Azul Inah"), ("Verde Inah", "Rio")]),
    ("Azul Céu", [("Verde Inah", "Verde Folha"), ("Azul Inah", "Azul Noite"), ("Rio", "Verde Inah")]),
    ("Areia", [("Terra", "Verde Mata"), ("Verde Mata", "Verde Inah"), ("Azul Inah", "Verde Mata")]),
]
def pill(i, base, ribbons):
    defs = "".join(f'<linearGradient id="tx{i}{j}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{C[a]}"/>'
                   f'<stop offset="1" stop-color="{C[b]}"/></linearGradient>' for j, (a, b) in enumerate(ribbons))
    flip = ' transform="translate(200 0) scale(-1 1)"' if i % 2 else ""
    paths = "".join(f'<path d="{PATHS[j]}" stroke="url(#tx{i}{j})" stroke-width="{[52, 44, 36][j]}" fill="none" stroke-linecap="round"/>'
                    for j in range(3))
    return (f'<figure class="pill"><svg viewBox="0 0 200 520" role="img" aria-label="Textura sobre {base}">'
            f'<defs>{defs}<clipPath id="pc{i}"><rect width="200" height="520" rx="100"/></clipPath></defs>'
            f'<g clip-path="url(#pc{i})"><rect width="200" height="520" fill="{C[base]}"/><g{flip}>{paths}</g></g></svg>'
            f'<span class="pill-dot" style="background:{C[base]}"></span><figcaption class="pill-n">{base}</figcaption></figure>')
def legend(names):
    seen = []
    for n in names:
        if n not in seen: seen.append(n)
    return '<div class="legend"><p class="label">Cores usadas</p><div class="legend-g">' + "".join(crow(n, C[n]) for n in seen) + "</div></div>"

TEXTURES = ('<div class="pills">' + "".join(pill(i, b, r) for i, (b, r) in enumerate(textures)) + "</div>"
            + legend([b for b, _ in textures] + [c for _, rs in textures for ab in rs for c in ab]))

# ---------- listras onduladas ----------
stripes = [
    ("Azul Céu", ("Verde Inah", "Verde Folha"), ("Rio", "Verde Inah")),
    ("Verde Inah", ("Azul Inah", "Azul Céu"), ("Rio", "Azul Céu")),
    ("Azul Noite", ("Azul Céu", "Rio"), ("Verde Inah", "Rio")),
    ("Areia", ("Terra", "Verde Mata"), ("Verde Mata", "Verde Inah")),
]
def stripe(i, base, a, b):
    defs = "".join(f'<linearGradient id="st{i}{k}" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{C[g[0]]}"/>'
                   f'<stop offset="1" stop-color="{C[g[1]]}"/></linearGradient>' for k, g in enumerate((a, b)))
    bands = ""
    for n, y in enumerate(range(30, 560, 96)):
        d = -34 if n % 2 else 34
        bands += f'<path d="M-30 {y} C 50 {y - d} 130 {y + d} 230 {y}" stroke="url(#st{i}{n % 2})" stroke-width="50" fill="none"/>'
    return (f'<figure class="pill"><svg viewBox="0 0 200 520" role="img" aria-label="Listras onduladas sobre {base}">'
            f'<defs>{defs}<clipPath id="sc{i}"><rect width="200" height="520" rx="100"/></clipPath></defs>'
            f'<g clip-path="url(#sc{i})"><rect width="200" height="520" fill="{C[base]}"/>{bands}</g></svg>'
            f'<span class="pill-dot" style="background:{C[base]}"></span><figcaption class="pill-n">{base}</figcaption></figure>')
STRIPES = ('<div class="pills">' + "".join(stripe(i, *t) for i, t in enumerate(stripes)) + "</div>"
           + legend([t[0] for t in stripes] + [c for t in stripes for g in t[1:] for c in g]))

# ---------- curvas de nível ----------
contours = [("Azul Inah", "Verde Inah", 3), ("Verde Inah", "Azul Inah", 7), ("Areia", "Verde Mata", 5), ("Azul Noite", "Azul Céu", 11)]
CONTOURS = ('<div class="tx-tiles">' + "".join(
    f'<figure><canvas class="contour tx-tile" data-bg="{C[bg]}" data-fg="{C[fg]}" data-seed="{sd}" role="img" '
    f'aria-label="Curvas de nível em {fg} sobre {bg}"></canvas><figcaption class="pill-n">{fg} sobre {bg}</figcaption></figure>'
    for bg, fg, sd in contours) + "</div>" + legend([c for bg, fg, _ in contours for c in (bg, fg)]))

# ---------- padrão de flores ----------
flores = [("Azul Inah", "azul500", "Azul 500", "tom sobre tom"), ("Verde Inah", "verde300", "Verde 300", "tom sobre tom"),
          ("Azul Inah", "verde", "Verde Inah", "contraste"), ("Areia", "mata", "Verde Mata", "contraste")]
SC = {"Azul 500": mix(AZUL, BRANCO, .28), "Verde 300": mix(VERDE, BRANCO, .45)}
def fcol(n): return C.get(n) or SC[n]
FLORES = ('<div class="tx-tiles">' + "".join(
    f'<figure><div class="tx-tile" role="img" aria-label="Padrão de flores {fl} sobre {bg}" '
    f'style="background:url(img/padrao-flor-{f}.png) 0 0/100px 100px repeat,{C[bg]}"></div>'
    f'<figcaption class="pill-n">{fl} sobre {bg} <span class="role">· {kind}</span></figcaption></figure>'
    for bg, f, fl, kind in flores) + "</div>"
    + '<div class="legend"><p class="label">Cores usadas</p><div class="legend-g">'
    + "".join(crow(n, fcol(n)) for n in ["Azul Inah", "Azul 500", "Verde Inah", "Verde 300", "Areia", "Verde Mata"]) + "</div></div>")

# ---------- ramos ----------
ramos = [
    ("filhotes", "Filhotes", "Ramo nacional da primeira infância. O grupo atende a partir de 6,5 anos: use esta marca apenas se houver seção Filhotes.",
     "Brincar e aprender", "Viver Juntos", "Hello Headline",
     [("Laranja", "#E95722", "principal"), ("Amarelo", "#EF8F1F", ""), ("Turquesa", "#00AF98", ""), ("Marrom", "#8F5F36", "")]),
    ("lobinho", "Lobinho", "6,5 a 10 anos · Alcateia, dividida em matilhas", "Ser livre como os lobos", "Melhor Possível", "Sanremo",
     [("Amarelo", "#F3B21E", "principal"), ("Azul escuro", "#014285", ""), ("Grafite", "#8D8D8C", ""), ("Cinza", "#C9C9C9", "")]),
    ("escoteiro", "Escoteiro", "11 a 14 anos · Tropa Escoteira, em patrulhas", "Descobrir novos territórios com um grupo de amigos",
     "Sempre Alerta", "SK Boncuk", [("Verde escuro", "#004F1F", "principal"), ("Verde", "#8EBB1E", "")]),
    ("senior", "Sênior", "15 a 17 anos · Tropa Sênior, em patrulhas · seniores e guias", "Viver aventuras, superar desafios", "Sempre Alerta",
     "Misadventures", [("Grená", "#A41D3A", "principal"), ("Azul escuro", "#004D99", ""), ("Ciano", "#0099D7", "")]),
    ("pioneiro", "Pioneiro", "18 a 21 anos · Clã", "Explorar o mundo, ampliar horizontes", "Servir", "Afragus ExtraBold",
     [("Vermelho", "#DC2A10", "principal"), ("Roxo", "#524491", ""), ("Azul petróleo", "#01969F", "")]),
]
def ramo(slug, name, meta, concept, lema, font, cols):
    rows = "".join(crow(n, h, r) for n, h, r in cols)
    return (f'<article class="ramo"><div class="plate p-branco"><img src="img/ramo-{slug}.png" alt="Marca do Ramo {name}"></div>'
            f'<div class="ramo-body"><h4>{name}</h4><p class="ramo-meta">{meta}</p><q>{concept}</q>'
            f'<dl class="kv"><dt>Lema</dt><dd>{lema}</dd><dt>Lettering</dt><dd>{font}</dd></dl>'
            f'<div class="crows">{rows}</div></div></article>')
RAMOS = '<div class="ramos mt">' + "".join(ramo(*r) for r in ramos) + "</div>"

# ---------- Escoteiros do Brasil e tema 2026 ----------
eb = [("Estrela", "#002F73"), ("Água", "#009CC4"), ("Sol", "#FFED02"), ("Broto", "#C0BC01"), ("Floresta", "#007D32")]
EB = '<div class="ctiles c5">' + "".join(tile(n, h) for n, h in eb) + "</div>"
tema = [("Verde escuro", "#08BA54"), ("Verde claro", "#B0DD43"), ("Azul claro", "#02A1D9"), ("Azul escuro", "#0649D5"), ("Amarelo", "#FFDA3E")]
TEMA = '<div class="ctiles c5">' + "".join(tile(n, h) for n, h in tema) + "</div>"

# ---------- cores principais ----------
def main_spec(h):
    r, g, b = hx(h); c, m, y, k = cmyk(h)
    return f'<dt>HEX</dt><dd>{h}</dd><dt>RGB</dt><dd>{r} · {g} · {b}</dd><dt>CMYK</dt><dd>{c} · {m} · {y} · {k}</dd>'

ICON_CODES = '<div class="legend-g">' + "".join(crow(n, C[n]) for n in ["Azul Inah", "Verde Inah", "Verde Folha", "Rio", "Azul Céu"]) + "</div>"
DARK_CODES = '<div class="legend-g">' + "".join(crow(n, C[n]) for n in ["Branco", "Verde Inah", "Azul Inah"]) + "</div>"

html = open(TPL, encoding="utf-8").read()
rep = {"{{GRAYS}}": GRAYS, "{{PALETTES}}": PALETTES, "{{SCALES}}": SCALES, "{{PAIRS}}": PAIRS,
       "{{GRADIENTS}}": GRADIENTS, "{{MESHES}}": MESHES, "{{TEXTURES}}": TEXTURES, "{{RAMOS}}": RAMOS,
       "{{EB}}": EB, "{{TEMA}}": TEMA, "{{SPEC_AZUL}}": main_spec(AZUL), "{{SPEC_VERDE}}": main_spec(VERDE),
       "{{MESH_FOGUEIRA}}": MESH["fogueira"],
       "{{GRAD_LIS}}": GRAD_CSS["Lis"], "{{GRAD_MATA}}": GRAD_CSS["Mata"],
       "{{MESH_LIS}}": MESH["lis"], "{{MESH_NOITE}}": MESH["noite"],
       "{{STRIPES}}": STRIPES, "{{DARK_CODES}}": DARK_CODES, "{{ICON_CODES}}": ICON_CODES, "{{MESH_MATA}}": MESH["mataprofunda"], "{{CONTOURS}}": CONTOURS, "{{FLORES}}": FLORES}
for k, v in rep.items():
    html = html.replace(k, v)
assert "{{" not in html, html[html.index("{{"):html.index("{{") + 40]
open(OUT, "w", encoding="utf-8").write(html)
print("ok", len(html) // 1024, "KB")
