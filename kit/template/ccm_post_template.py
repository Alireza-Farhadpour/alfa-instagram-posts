"""Critical Chain Method carousel (9 slides) in the approved ALFA style (illustrated cover + card slides)."""
import asyncio, pathlib, re
from playwright.async_api import async_playwright

ROOT = pathlib.Path(__file__).parent
A = (ROOT / "assets").as_uri()
F = (ROOT / "node_modules/@fontsource").as_uri()
ICONS = ROOT / "node_modules/lucide-static/icons"
OUT = ROOT / "out_ccm"; OUT.mkdir(exist_ok=True)

GOLD, BLUE, LAV, CYAN, NAVY = "#AE9471", "#4C71B7", "#B4C7E7", "#00B0F0", "#1b1d3a"
ORANGE, RED, GREEN, YELLOW = "#FF9A3C", "#FF3D5A", "#2ECC71", "#FFC93C"


def inner(name):
    s = (ICONS / f"{name}.svg").read_text()
    s = re.sub(r'<!--.*?-->', '', s, flags=re.S)
    return re.search(r'<svg[^>]*>(.*)</svg>', s, re.S).group(1)


def icon(name, size=56, color=CYAN, stroke=1.8):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" '
            f'stroke="{color}" stroke-width="{stroke}" stroke-linecap="round" stroke-linejoin="round">{inner(name)}</svg>')


def sicon(name, x, y, scale, color, stroke=1.8, filt=True):
    """Lucide icon placed inside an SVG at (x, y) top-left."""
    f = ' filter="url(#glowS)"' if filt else ''
    return (f'<g transform="translate({x} {y}) scale({scale})" fill="none" stroke="{color}" stroke-width="{stroke}" '
            f'stroke-linecap="round" stroke-linejoin="round"{f}>{inner(name)}</g>')


DEFS = f"""<defs>
 <linearGradient id="gGold" x1="0" x2="1"><stop offset="0" stop-color="#8f7655"/><stop offset="1" stop-color="#D9BC8C"/></linearGradient>
 <linearGradient id="gBlue" x1="0" x2="1"><stop offset="0" stop-color="#4C71B7"/><stop offset="1" stop-color="#5AA8FF"/></linearGradient>
 <linearGradient id="gOrange" x1="0" x2="1"><stop offset="0" stop-color="#FFC15E"/><stop offset="1" stop-color="#FF7A1A"/></linearGradient>
 <linearGradient id="gCyan" x1="0" x2="1"><stop offset="0" stop-color="#0090D0"/><stop offset="1" stop-color="#5FF3FF"/></linearGradient>
 <linearGradient id="gRed" x1="0" x2="1"><stop offset="0" stop-color="#FF7A1A"/><stop offset="1" stop-color="#FF3D5A"/></linearGradient>
 <linearGradient id="gFever" x1="0" y1="1" x2="1" y2="0"><stop offset="0" stop-color="{GREEN}"/><stop offset=".5" stop-color="{YELLOW}"/><stop offset="1" stop-color="{RED}"/></linearGradient>
 <pattern id="hatch" width="10" height="10" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
  <rect width="10" height="10" fill="rgba(255,154,60,.18)"/><line x1="0" y1="0" x2="0" y2="10" stroke="{ORANGE}" stroke-width="4"/></pattern>
 <pattern id="hatchG" width="10" height="10" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
  <rect width="10" height="10" fill="rgba(180,199,231,.10)"/><line x1="0" y1="0" x2="0" y2="10" stroke="#8a93b8" stroke-width="3"/></pattern>
 <radialGradient id="gHaloC"><stop offset="0" stop-color="rgba(0,176,240,.40)"/><stop offset="1" stop-color="rgba(0,176,240,0)"/></radialGradient>
 <radialGradient id="gHaloR"><stop offset="0" stop-color="rgba(255,61,90,.45)"/><stop offset="1" stop-color="rgba(255,61,90,0)"/></radialGradient>
 <radialGradient id="gFloor"><stop offset="0" stop-color="rgba(0,176,240,.30)"/><stop offset="1" stop-color="rgba(0,176,240,0)"/></radialGradient>
 <filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="7" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
 <filter id="glowS" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="3.5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
 <filter id="shadow" x="-20%" y="-20%" width="140%" height="160%"><feDropShadow dx="0" dy="14" stdDeviation="14" flood-color="#000" flood-opacity=".5"/></filter>
 <marker id="arr" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="{CYAN}"/></marker>
 <marker id="arrO" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="{ORANGE}"/></marker>
</defs>"""

SVG_STYLE = 'style="font-family:MP,sans-serif;font-weight:700"'


def block(x, y, w, h, fill, label="", color="#fff", fs=20, rx=10):
    t = f'<text x="{x + w / 2}" y="{y + h / 2 + fs * .36}" text-anchor="middle" fill="{color}" font-size="{fs}">{label}</text>' if label else ""
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}"/>{t}'


# ───────────────────────────── COVER ─────────────────────────────
def cover():
    thieves = [(110, "hourglass", "Parkinson’s Law"), (250, "alarm-clock", "Student Syndrome"), (390, "shuffle", "Multitasking")]
    th = ""
    for y, ic, lab in thieves:
        th += f'<circle cx="100" cy="{y}" r="74" fill="url(#gHaloR)"/>'
        th += f'<circle cx="100" cy="{y}" r="46" fill="rgba(14,18,44,.92)" stroke="{RED}" stroke-width="3" filter="url(#glowS)"/>'
        th += sicon(ic, 76, y - 24, 2, "#FF8A9A", 2)
        th += f'<text x="160" y="{y + 8}" fill="#FFB0BB" font-size="21">{lab}</text>'
        th += f'<path d="M 330 {y} L 368 {y}" stroke="{RED}" stroke-width="3" stroke-dasharray="6 6" marker-end="url(#arrO)" opacity=".85"/>'
    # board
    bx, by, bw, bh = 380, 40, 670, 380
    chain = ""
    xs = [410, 520, 630, 740]
    for i, x in enumerate(xs):
        chain += block(x, 150, 82, 58, "url(#gGold)", "ABCD"[i], NAVY, 26)
        if i < 3:
            chain += sicon("link", x + 85, 166, 1.1, CYAN, 2.4)
    # project buffer
    chain += f'<rect x="850" y="138" width="150" height="82" rx="14" fill="url(#gOrange)" filter="url(#glowS)"/>'
    chain += sicon("shield-check", 905, 146, 1.7, NAVY, 2.2, False)
    chain += f'<text x="925" y="207" text-anchor="middle" fill="{NAVY}" font-size="16">PROJECT BUFFER</text>'
    chain += sicon("flag", 1010, 152, 1.5, "#fff", 2)
    # feeding chain
    chain += block(520, 300, 82, 50, "url(#gBlue)", "E", "#fff", 22)
    chain += sicon("link", 605, 312, 1.0, CYAN, 2.2)
    chain += block(630, 300, 82, 50, "url(#gBlue)", "F", "#fff", 22)
    chain += f'<rect x="722" y="300" width="96" height="50" rx="10" fill="url(#gCyan)"/>'
    chain += f'<text x="770" y="321" text-anchor="middle" fill="{NAVY}" font-size="14">FEEDING</text><text x="770" y="339" text-anchor="middle" fill="{NAVY}" font-size="14">BUFFER</text>'
    chain += f'<path d="M 818 325 C 860 325, 860 260, 800 214" fill="none" stroke="{CYAN}" stroke-width="3.5" marker-end="url(#arr)"/>'
    # resource buffer bell above D
    chain += f'<circle cx="781" cy="112" r="22" fill="rgba(255,201,60,.18)" stroke="{YELLOW}" stroke-width="2"/>'
    chain += sicon("bell-ring", 769, 100, 1.0, YELLOW, 2.2)
    chain += f'<text x="810" y="104" fill="{YELLOW}" font-size="15">RESOURCE BUFFER</text>'

    fever = ""
    fx, fy, fw = 470, 470, 520
    fever += f'<text x="{fx}" y="{fy - 14}" fill="{LAV}" font-size="18" letter-spacing="1.5">BUFFER STATUS</text>'
    fever += f'<rect x="{fx}" y="{fy}" width="{fw / 3}" height="22" rx="11" fill="{GREEN}"/>'
    fever += f'<rect x="{fx + fw / 3}" y="{fy}" width="{fw / 3}" height="22" fill="{YELLOW}"/>'
    fever += f'<rect x="{fx + 2 * fw / 3}" y="{fy}" width="{fw / 3}" height="22" rx="11" fill="{RED}"/>'
    fever += f'<rect x="{fx + 2 * fw / 3 - 10}" y="{fy}" width="20" height="22" fill="{RED}"/>'
    fever += f'<path d="M {fx + fw * .42} {fy - 6} l -10 -16 h 20 z" fill="#fff" filter="url(#glowS)"/>'

    floor = "".join(f'<line x1="540" y1="470" x2="{x}" y2="560" stroke="rgba(0,176,240,.10)" stroke-width="1.5"/>' for x in range(-300, 1400, 110))
    sparks = "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}" opacity=".85" filter="url(#glowS)"/>' for x, y, r, c in [
        (40, 30, 3, CYAN), (360, 510, 2.5, ORANGE), (1050, 470, 3, CYAN), (300, 20, 2.5, GOLD), (1040, 20, 2.5, ORANGE), (420, 450, 2, GOLD)])

    illu = f"""<svg viewBox="0 0 1080 560" xmlns="http://www.w3.org/2000/svg" {SVG_STYLE}>{DEFS}
{floor}<ellipse cx="640" cy="505" rx="460" ry="55" fill="url(#gFloor)"/>
<g filter="url(#shadow)"><rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="24" fill="rgba(13,16,38,.92)" stroke="rgba(0,176,240,.65)" stroke-width="2.5"/></g>
<rect x="{bx}" y="{by}" width="{bw}" height="46" rx="24" fill="rgba(0,176,240,.10)"/>
<circle cx="{bx + 30}" cy="63" r="7" fill="#FF5F57"/><circle cx="{bx + 52}" cy="63" r="7" fill="#FFBD2E"/><circle cx="{bx + 74}" cy="63" r="7" fill="#28C840"/>
<text x="{bx + bw - 24}" y="70" text-anchor="end" fill="{CYAN}" font-size="20" letter-spacing="2">CRITICAL CHAIN</text>
<text x="410" y="138" fill="{GOLD}" font-size="16" letter-spacing="1">CRITICAL CHAIN</text>
<text x="520" y="290" fill="#8fb3ff" font-size="16" letter-spacing="1">FEEDING CHAIN</text>
{chain}{th}{fever}{sparks}</svg>"""

    return f"""<!doctype html><html lang='fa'><head><meta charset='utf-8'><style>{FONTS}
* {{ margin:0; padding:0; box-sizing:border-box; }}
html,body {{ width:1080px; height:1080px; overflow:hidden; }}
body {{ position:relative; direction:rtl; font-family:'VZ',sans-serif; font-weight:900; color:#fff;
  background: radial-gradient(600px 380px at 85% 78%, rgba(255,122,26,.20), rgba(255,122,26,0)),
    radial-gradient(520px 420px at 10% 60%, rgba(255,61,90,.16), rgba(255,61,90,0)),
    url('{A}/content_bg.png') center/1080px 1080px no-repeat; }}
.en {{ font-family:'MP',sans-serif; font-weight:700; direction:ltr; unicode-bidi:isolate; white-space:nowrap; }}
.chev {{ position:absolute; top:22px; left:0; right:0; height:60px; }}
.box {{ position:absolute; left:64px; right:64px; top:92px; height:196px; border:4px solid #fff; border-radius:4px;
  background:linear-gradient(180deg, rgba(27,29,58,.82), rgba(20,22,46,.82)); box-shadow:0 0 40px rgba(0,176,240,.18), inset 0 0 40px rgba(0,0,0,.25);
  display:flex; align-items:center; justify-content:center; padding-bottom:34px; }}
.t {{ font-size:66px; line-height:1; text-shadow:0 4px 12px rgba(0,0,0,.55); white-space:nowrap; }}
.t .n {{ font-size:132px; vertical-align:-12px; margin-left:14px;
  background:linear-gradient(180deg,#FFD27A,#FF9A3C 55%,#E0782A); -webkit-background-clip:text; background-clip:text; color:transparent;
  filter:drop-shadow(0 0 18px rgba(255,154,60,.6)); }}
.t .k {{ color:{CYAN}; text-shadow:0 0 22px rgba(0,176,240,.65), 0 4px 12px rgba(0,0,0,.5); }}
.enbox {{ position:absolute; left:180px; width:720px; top:252px; height:72px; border:4px solid #fff; border-radius:4px;
  background:#252640; display:flex; align-items:center; justify-content:center; font-size:40px; color:{GOLD}; box-shadow:0 8px 20px rgba(0,0,0,.4); }}
.arc {{ position:absolute; left:0; top:330px; width:1080px; height:60px; }}
.illu {{ position:absolute; left:0; top:372px; width:1080px; height:560px; direction:ltr; }}
.illu svg {{ width:1080px; height:560px; }}
.brand {{ position:absolute; left:0; right:0; top:950px; display:flex; justify-content:center; align-items:center; gap:22px; direction:ltr; }}
.brand .e {{ height:96px; }} .brand .w {{ height:66px; }}
.stamp {{ position:absolute; left:812px; top:922px; width:212px; height:128px; border:5px solid #FF2A2A; transform:rotate(-12deg);
  color:#FF2A2A; text-align:center; font-weight:900; background:rgba(20,22,46,.35); }}
.stamp .s1 {{ font-size:20px; margin-top:6px; }} .stamp .s2 {{ font-size:34px; line-height:1.05; }} .stamp .s3 {{ font-size:32px; line-height:1.15; }}
</style></head><body>
<svg class="chev" viewBox="0 0 1080 60" xmlns="http://www.w3.org/2000/svg">
 <defs><filter id="g1"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
 <linearGradient id="lL" x1="0" x2="1"><stop offset="0" stop-color="#FF9A3C" stop-opacity="0"/><stop offset="1" stop-color="#FFB347"/></linearGradient>
 <linearGradient id="lR" x1="1" x2="0"><stop offset="0" stop-color="#FF9A3C" stop-opacity="0"/><stop offset="1" stop-color="#FFB347"/></linearGradient></defs>
 <g filter="url(#g1)" stroke-linecap="round" stroke-linejoin="round" fill="none" stroke-width="9">
  <path d="M478 14 L496 30 L478 46" stroke="#FF9A3C"/><path d="M512 14 L530 30 L512 46" stroke="{GOLD}"/><path d="M546 14 L564 30 L546 46" stroke="{CYAN}"/></g>
 <path d="M260 34 Q 360 22 450 30" stroke="url(#lL)" stroke-width="4" fill="none" filter="url(#g1)"/>
 <path d="M820 34 Q 720 22 630 30" stroke="url(#lR)" stroke-width="4" fill="none" filter="url(#g1)"/>
</svg>
<div class="box"><div class="t"><span class="n">۳</span>دزد زمان و <span class="k">زنجیره بحرانی</span></div></div>
<div class="enbox"><span class="en">Critical Chain Method (CCM)</span></div>
<svg class="arc" viewBox="0 0 1080 60" xmlns="http://www.w3.org/2000/svg">
 <defs><linearGradient id="ga" x1="0" x2="1"><stop offset="0" stop-color="#FF9A3C" stop-opacity="0"/><stop offset=".5" stop-color="#FFB347"/><stop offset="1" stop-color="#FF9A3C" stop-opacity="0"/></linearGradient>
 <filter id="g2"><feGaussianBlur stdDeviation="4" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>
 <path d="M200 46 Q 540 4 880 46" stroke="url(#ga)" stroke-width="6" fill="none" filter="url(#g2)"/></svg>
<div class="illu">{illu}</div>
<div class="brand"><img class="e" src="{A}/logo_emblem.png"><img class="w" src="{A}/logo_word.png"></div>
<div class="stamp"><div class="s1">مرجع:</div><div class="s2"><span class="en">PMBOK</span></div><div class="s3">ویرایش ۸</div></div>
</body></html>"""


# ───────────────────────────── CONTENT SLIDES ─────────────────────────────
FONTS = f"""
@font-face {{ font-family:'VZ'; font-weight:800; src: local('B Titr'), url('{F}/vazirmatn/files/vazirmatn-arabic-800-normal.woff2'); }}
@font-face {{ font-family:'VZ'; font-weight:900; src: local('B Titr'), url('{F}/vazirmatn/files/vazirmatn-arabic-900-normal.woff2'); }}
@font-face {{ font-family:'MP'; font-weight:700; src: local('Myriad Pro Bold'), url('{F}/source-sans-3/files/source-sans-3-latin-700-normal.woff2'); }}
"""

BASE = FONTS + f"""
* {{ margin:0; padding:0; box-sizing:border-box; }}
html,body {{ width:1080px; height:1080px; overflow:hidden; }}
body {{ position:relative; font-family:'VZ',sans-serif; font-weight:800; color:#fff; direction:rtl;
  background: radial-gradient(560px 300px at 50% 12%, rgba(174,148,113,.20), rgba(174,148,113,0)),
    radial-gradient(520px 380px at 92% 92%, rgba(255,122,26,.12), rgba(255,122,26,0)),
    radial-gradient(520px 380px at 6% 70%, rgba(0,176,240,.10), rgba(0,176,240,0)),
    url('{A}/content_bg.png') center/1080px 1080px no-repeat; }}
.en {{ font-family:'MP',sans-serif; font-weight:700; direction:ltr; unicode-bidi:isolate; white-space:nowrap; }}
.chip {{ position:absolute; top:52px; left:0; right:0; text-align:center; }}
.chip span {{ display:inline-block; padding:8px 26px; border:2px solid rgba(0,176,240,.55); border-radius:40px;
  color:{CYAN}; font-size:26px; background:rgba(0,176,240,.08); }}
.chip.o span {{ border-color:rgba(255,61,90,.6); color:#FF8A9A; background:rgba(255,61,90,.10); }}
.title {{ position:absolute; top:108px; left:50px; right:50px; text-align:center; color:{GOLD}; font-weight:900;
  font-size:58px; line-height:1.25; text-shadow:0 3px 14px rgba(0,0,0,.5); }}
.title .w {{ color:#fff; }} .title .c {{ color:{CYAN}; }}
.title .sub {{ display:block; font-size:44px; color:{CYAN}; margin-top:2px; }}
.accent {{ position:absolute; top:{{ACC}}px; left:440px; width:200px; height:6px; border-radius:3px;
  background:linear-gradient(90deg, rgba(255,154,60,0), {ORANGE}, rgba(255,154,60,0)); }}
.hero {{ position:absolute; left:60px; right:60px; border-radius:30px; padding:18px 24px; direction:ltr;
  background:linear-gradient(180deg, rgba(16,19,44,.94), rgba(27,29,58,.88)); border:2px solid rgba(0,176,240,.55);
  box-shadow:0 14px 34px rgba(0,0,0,.45), 0 0 30px rgba(0,176,240,.10); }}
.hero svg {{ width:100%; height:100%; }}
.def {{ position:absolute; left:60px; right:60px; border-radius:30px; display:flex; align-items:center;
  background:linear-gradient(180deg, rgba(255,255,255,.10), rgba(255,255,255,.04)); border:2px solid rgba(174,148,113,.38); padding:18px 28px; }}
.def .ic {{ width:84px; height:84px; border-radius:50%; flex:none; display:flex; align-items:center; justify-content:center; margin-left:24px; }}
.def .tx {{ font-size:37px; line-height:1.5; color:#fff; }}
.def .tx b {{ color:{GOLD}; }} .def .tx i {{ font-style:normal; color:{CYAN}; }}
.ans {{ position:absolute; left:60px; right:60px; border-radius:26px; display:flex; align-items:center; padding:14px 26px;
  background:linear-gradient(90deg, rgba(0,176,240,.18), rgba(0,176,240,.06)); border:2px solid rgba(0,176,240,.6); }}
.ans .tag {{ flex:none; background:{CYAN}; color:{NAVY}; border-radius:18px; padding:4px 16px; font-size:30px; margin-left:20px; }}
.ans .tx {{ font-size:36px; line-height:1.45; }}
.card {{ position:absolute; left:60px; right:60px; height:180px; border-radius:30px; overflow:hidden;
  background:linear-gradient(180deg, rgba(255,255,255,.10), rgba(255,255,255,.04));
  border:2px solid rgba(174,148,113,.38); box-shadow:0 12px 30px rgba(0,0,0,.35); display:flex; align-items:center; }}
.card .badge {{ width:96px; align-self:stretch; display:flex; align-items:center; justify-content:center;
  background:linear-gradient(180deg, #FFC15E, {ORANGE} 55%, #E0782A); color:{NAVY}; font-size:64px; font-weight:900; }}
.card .ic {{ width:108px; height:108px; margin:0 24px 0 22px; border-radius:50%; flex:none; display:flex; align-items:center; justify-content:center;
  border:2px solid rgba(255,61,90,.6); background:rgba(255,61,90,.10); box-shadow:0 0 24px rgba(255,61,90,.2) inset; }}
.card .sep {{ width:2px; height:104px; background:rgba(180,199,231,.25); margin-left:24px; flex:none; }}
.card .tx {{ flex:1; padding-left:26px; }}
.card .t {{ font-size:46px; line-height:1.25; color:#fff; }}
.card .t .en {{ font-size:26px; color:{CYAN}; margin-right:10px; vertical-align:middle; }}
.card .d {{ font-size:36px; line-height:1.45; color:{LAV}; margin-top:4px; }}
.swipe {{ position:absolute; left:110px; right:110px; top:956px; height:84px; border-radius:42px; display:flex; align-items:center;
  background:#14162e; border:2px solid rgba(174,148,113,.55); box-shadow:0 10px 26px rgba(0,0,0,.45); padding:0 34px 0 10px; }}
.swipe .tx {{ flex:1; font-size:34px; color:#fff; }}
.swipe .tx b {{ color:{ORANGE}; }}
.swipe .go {{ width:64px; height:64px; border-radius:50%; background:linear-gradient(180deg,#FFC15E,{ORANGE}); display:flex; align-items:center; justify-content:center; flex:none; }}
"""


def doc(body, css="", acc=222):
    return f"<!doctype html><html lang='fa'><head><meta charset='utf-8'><style>{BASE.replace('{ACC}', str(acc))}{css}</style></head><body>{body}</body></html>"


def swipe(text):
    return f'<div class="swipe"><div class="tx">{text}</div><div class="go">{icon("arrow-right", 38, NAVY, 2.6)}</div></div>'


def en(s):
    return f'<span class="en">{s}</span>'


def hero(svg, top, h):
    return f'<div class="hero" style="top:{top}px; height:{h}px">{svg}</div>'


def defcard(text, ic, top, h, bg=GOLD):
    return (f'<div class="def" style="top:{top}px; min-height:{h}px"><div class="ic" style="background:{bg}">{icon(ic, 46, NAVY, 2.2)}</div>'
            f'<div class="tx">{text}</div></div>')


def answer(text, top):
    return f'<div class="ans" style="top:{top}px"><div class="tag">پاسخ {en("CCM")}</div><div class="tx">{text}</div></div>'


def svg(w, h, body):
    return f'<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" {SVG_STYLE}>{DEFS}{body}</svg>'


SLIDES = [cover()]

# 2 ─ What is CCM: CPM padding vs CCM buffer
u = 1.45
def row_cpm():
    s, x = "", 140
    for lab, d, p in [("A", 100, 60), ("B", 80, 50), ("C", 90, 60)]:
        s += block(x, 60, d * u, 52, "url(#gGold)", lab, NAVY, 24, 8); x += d * u
        s += f'<rect x="{x}" y="60" width="{p * u}" height="52" rx="8" fill="url(#hatchG)" stroke="#8a93b8" stroke-width="1.5"/>'; x += p * u + 4
    return s, x
cpm, cpm_end = row_cpm()
ccm, x = "", 140
for lab, d in [("A", 100), ("B", 80), ("C", 90)]:
    ccm += block(x, 170, d * u, 52, "url(#gGold)", lab, NAVY, 24, 8); x += d * u + 4
ccm += f'<rect x="{x}" y="170" width="{85 * u}" height="52" rx="8" fill="url(#gOrange)" filter="url(#glowS)"/>'
ccm += f'<text x="{x + 85 * u / 2}" y="203" text-anchor="middle" fill="{NAVY}" font-size="19">BUFFER</text>'
ccm_end = x + 85 * u
S2 = svg(940, 300, f"""
<text x="20" y="94" fill="#fff" font-size="26">CPM</text>{cpm}
<text x="140" y="44" fill="#8a93b8" font-size="18">hidden safety inside every task</text>
<text x="20" y="204" fill="#fff" font-size="26">CCM</text>{ccm}
<line x1="{ccm_end}" y1="240" x2="{cpm_end - 4}" y2="240" stroke="{CYAN}" stroke-width="3" marker-start="url(#arr)" marker-end="url(#arr)"/>
<text x="{(ccm_end + cpm_end) / 2}" y="272" text-anchor="middle" fill="{CYAN}" font-size="22">time saved</text>
<line x1="{ccm_end}" y1="160" x2="{ccm_end}" y2="248" stroke="{CYAN}" stroke-width="2" stroke-dasharray="5 5"/>
<line x1="{cpm_end - 4}" y1="50" x2="{cpm_end - 4}" y2="248" stroke="#8a93b8" stroke-width="2" stroke-dasharray="5 5"/>
""")
SLIDES.append(doc(f"""
<div class="chip"><span class="en">PMBOK 8 · Develop Schedule</span></div>
<div class="title">زنجیره بحرانی <span class="w">چیست؟</span><span class="sub en">Critical Chain Method</span></div>
<div class="accent"></div>
{hero(S2, 296, 330)}
{defcard('ذخیره‌های <b>پنهانِ</b> هر فعالیت حذف و یک‌جا به‌صورت <i>بافر</i> در انتهای مسیر قرار می‌گیرد؛ با در نظر گرفتن <b>محدودیت منابع</b>.', 'link', 652, 250)}
{swipe('ورق بزنید و <b>۳ دزد زمان</b> را بشناسید')}
""", acc=262))

# 3 ─ Three time thieves (cards)
def card(top, n, title, en_t, desc, ic):
    return f"""<div class="card" style="top:{top}px"><div class="badge">{n}</div>
<div class="ic">{icon(ic, 56, "#FF8A9A")}</div><div class="sep"></div>
<div class="tx"><div class="t">{title}{en(en_t)}</div><div class="d">{desc}</div></div></div>"""

SLIDES.append(doc(f"""
<div class="chip o"><span>چرا پروژه‌ها دیر تمام می‌شوند؟</span></div>
<div class="title"><span class="w">۳</span> دزد زمانِ پروژه</div>
<div class="accent"></div>
{card(282, '۱', 'قانون پارکینسون', "Parkinson’s Law", 'کار، تمام زمانِ داده‌شده را پر می‌کند.', 'hourglass')}
{card(486, '۲', 'سندرم دانشجویی', 'Student Syndrome', 'شروع کار تا لحظه آخر عقب می‌افتد.', 'alarm-clock')}
{card(690, '۳', 'اتلاف چندوظیفگی', 'Multitasking', 'پرش بین کارها، همه را دیرتر تمام می‌کند.', 'shuffle')}
{swipe('ورق بزنید و <b>هر دزد</b> را از نزدیک ببینید')}
"""))

# 4 ─ Parkinson's law
P = svg(940, 290, f"""
<text x="20" y="78" fill="#fff" font-size="24">Planned</text>
<rect x="190" y="50" width="680" height="46" rx="10" fill="none" stroke="{BLUE}" stroke-width="3"/>
<text x="860" y="81" text-anchor="end" fill="#8fb3ff" font-size="22">10 days</text>
<text x="20" y="158" fill="#fff" font-size="24">Real work</text>
<rect x="190" y="130" width="408" height="46" rx="10" fill="url(#gGold)"/>
<text x="394" y="161" text-anchor="middle" fill="{NAVY}" font-size="22">6 days</text>
<rect x="602" y="130" width="268" height="46" rx="10" fill="url(#hatch)" stroke="{ORANGE}" stroke-width="2"/>
<text x="736" y="161" text-anchor="middle" fill="#FFD08A" font-size="20">work expands</text>
<path d="M 610 205 L 860 205" stroke="{ORANGE}" stroke-width="3" marker-end="url(#arrO)"/>
<line x1="598" y1="118" x2="598" y2="240" stroke="{GREEN}" stroke-width="2.5" stroke-dasharray="6 6"/>
<line x1="870" y1="40" x2="870" y2="240" stroke="{RED}" stroke-width="2.5" stroke-dasharray="6 6"/>
<text x="598" y="268" text-anchor="middle" fill="{GREEN}" font-size="20">could finish</text>
<text x="870" y="268" text-anchor="middle" fill="#FF8A9A" font-size="20">reported finish</text>
""")
SLIDES.append(doc(f"""
<div class="chip o"><span>دزد زمان ۱ از ۳</span></div>
<div class="title">قانون پارکینسون<span class="sub en">Parkinson’s Law</span></div>
<div class="accent"></div>
{hero(P, 296, 320)}
{defcard('کار آن‌قدر کش می‌آید که <b>تمام زمانِ داده‌شده</b> را پر کند؛ زودکردها هم اعلام نمی‌شوند.', 'hourglass', 640, 170, ORANGE)}
{answer('حذف ذخیره پنهان و اعلام فوری اتمام کار', 838)}
{swipe('دزد بعدی را ببینید')}
""", acc=262))

# 5 ─ Student syndrome
xs = [150 + i * 70 for i in range(11)]
effort = [8, 8, 9, 9, 10, 12, 20, 40, 80, 150, 175]
pts = " ".join(f"{x},{240 - e}" for x, e in zip(xs, effort))
area = f"150,240 {pts} {xs[-1]},240"
SS = svg(940, 300, f"""
<line x1="150" y1="240" x2="880" y2="240" stroke="{LAV}" stroke-width="2"/>
<line x1="150" y1="240" x2="150" y2="40" stroke="{LAV}" stroke-width="2"/>
<text x="40" y="150" fill="{LAV}" font-size="20">effort</text>
<rect x="152" y="40" width="358" height="198" fill="url(#hatch)" opacity=".75"/>
<text x="331" y="120" text-anchor="middle" fill="#FFD08A" font-size="24">safety time</text>
<text x="331" y="150" text-anchor="middle" fill="#FFD08A" font-size="24">wasted</text>
<polygon points="{area}" fill="rgba(174,148,113,.30)"/>
<polyline points="{pts}" fill="none" stroke="url(#gGold)" stroke-width="5" filter="url(#glowS)"/>
<line x1="850" y1="30" x2="850" y2="240" stroke="{RED}" stroke-width="3" stroke-dasharray="7 6"/>
<text x="850" y="272" text-anchor="middle" fill="#FF8A9A" font-size="20">deadline</text>
<g transform="translate(700 70)" filter="url(#glowS)"><path d="M0 -26 L26 20 L-26 20 Z" fill="url(#gOrange)"/><text x="0" y="14" text-anchor="middle" fill="{NAVY}" font-size="30">!</text></g>
<text x="640" y="40" text-anchor="middle" fill="#FFB0BB" font-size="20">problem appears → no time left</text>
""")
SLIDES.append(doc(f"""
<div class="chip o"><span>دزد زمان ۲ از ۳</span></div>
<div class="title">سندرم دانشجویی<span class="sub en">Student Syndrome</span></div>
<div class="accent"></div>
{hero(SS, 296, 320)}
{defcard('کار را تا <b>لحظه آخر</b> شروع نمی‌کنیم؛ ذخیره احتیاطی همان اول کار هدر می‌رود.', 'alarm-clock', 640, 170, ORANGE)}
{answer('شروع به‌محض آماده شدن؛ نه دقیقه ۹۰', 838)}
{swipe('آخرین دزد را ببینید')}
""", acc=262))

# 6 ─ Multitasking
d = 24
def seg(x, y, n, lab, fill, col):
    return block(x, y, n * d - 3, 48, fill, lab, col, 20, 7)
F1 = seg(150, 60, 10, "A", "url(#gGold)", NAVY) + seg(150 + 240, 60, 10, "B", "url(#gBlue)", "#fff") + seg(150 + 480, 60, 10, "C", "url(#gCyan)", NAVY)
M1, x = "", 150
for lab, fill, col in [("A", "url(#gGold)", NAVY), ("B", "url(#gBlue)", "#fff"), ("C", "url(#gCyan)", NAVY)] * 2:
    M1 += seg(x, 170, 5, lab, fill, col); x += 120
zaps = "".join(sicon("zap", 150 + 120 * k - 12, 140, 1.0, ORANGE, 2.2) for k in range(1, 6))
MT = svg(940, 300, f"""
<text x="20" y="92" fill="#fff" font-size="24">Focused</text>{F1}
<text x="20" y="202" fill="#fff" font-size="24">Multitask</text>{M1}{zaps}
<line x1="387" y1="40" x2="387" y2="122" stroke="{GREEN}" stroke-width="2.5" stroke-dasharray="6 6"/>
<text x="387" y="34" text-anchor="middle" fill="{GREEN}" font-size="20">A done: day 10</text>
<line x1="627" y1="160" x2="627" y2="246" stroke="{RED}" stroke-width="2.5" stroke-dasharray="6 6"/>
<text x="627" y="272" text-anchor="middle" fill="#FF8A9A" font-size="20">A done: day 20</text>
<text x="880" y="272" text-anchor="end" fill="{LAV}" font-size="18">+ switching cost</text>
""")
SLIDES.append(doc(f"""
<div class="chip o"><span>دزد زمان ۳ از ۳</span></div>
<div class="title">اتلاف چندوظیفگی<span class="sub en">Multitasking</span></div>
<div class="accent"></div>
{hero(MT, 296, 320)}
{defcard('با <b>تمرکز</b>، کار A روز ۱۰ تحویل می‌شود؛ با چندوظیفگی روز ۲۰، آن هم بدون احتساب زمان جابه‌جایی.', 'shuffle', 640, 170, ORANGE)}
{answer('رفتار دونده امدادی؛ یک کار در یک زمان', 838)}
{swipe('راه‌حل اصلی: <b>بافرها</b>')}
""", acc=262))

# 7 ─ Buffers
BF = ""
xs = [40, 170, 300, 430]
for i, x in enumerate(xs):
    BF += block(x, 70, 104, 60, "url(#gGold)", "ABCD"[i], NAVY, 26)
    if i < 3: BF += sicon("link", x + 107, 88, 1.0, CYAN, 2.4)
BF += f'<rect x="560" y="58" width="200" height="84" rx="14" fill="url(#gOrange)" filter="url(#glowS)"/>'
BF += sicon("shield-check", 572, 82, 1.5, NAVY, 2.2, False)
BF += f'<text x="680" y="96" text-anchor="middle" fill="{NAVY}" font-size="19">PROJECT</text><text x="680" y="120" text-anchor="middle" fill="{NAVY}" font-size="19">BUFFER</text>'
BF += sicon("flag", 784, 76, 1.9, "#fff", 2)
BF += f'<text x="806" y="150" text-anchor="middle" fill="#fff" font-size="17">due date</text>'
BF += block(40, 210, 104, 52, "url(#gBlue)", "E", "#fff", 22) + sicon("link", 147, 224, 1.0, CYAN, 2.2) + block(170, 210, 104, 52, "url(#gBlue)", "F", "#fff", 22)
BF += f'<rect x="284" y="210" width="120" height="52" rx="10" fill="url(#gCyan)"/><text x="344" y="232" text-anchor="middle" fill="{NAVY}" font-size="15">FEEDING</text><text x="344" y="252" text-anchor="middle" fill="{NAVY}" font-size="15">BUFFER</text>'
BF += f'<path d="M 404 236 C 450 236, 470 190, 470 140" fill="none" stroke="{CYAN}" stroke-width="3.5" marker-end="url(#arr)"/>'
BF += f'<circle cx="352" cy="32" r="20" fill="rgba(255,201,60,.18)" stroke="{YELLOW}" stroke-width="2"/>' + sicon("bell-ring", 341, 21, .92, YELLOW, 2.2)
BF += f'<text x="380" y="38" fill="{YELLOW}" font-size="16">RESOURCE BUFFER</text>'
BF += f'<text x="40" y="168" fill="{GOLD}" font-size="16" letter-spacing="1">CRITICAL CHAIN</text><text x="40" y="292" fill="#8fb3ff" font-size="16" letter-spacing="1">FEEDING CHAIN</text>'
BUF = svg(860, 300, BF)


def brow(top, color, title, en_t, desc):
    return (f'<div class="brow" style="top:{top}px"><div class="dot" style="background:{color}; box-shadow:0 0 16px {color}"></div>'
            f'<div class="bt">{title} {en(en_t)}</div><div class="bd">{desc}</div></div>')

SLIDES.append(doc(f"""
<div class="chip"><span>راه‌حل زنجیره بحرانی</span></div>
<div class="title">بافرها؛ <span class="w">سپر محافظ پروژه</span></div>
<div class="accent"></div>
{hero(BUF, 252, 330)}
{brow(612, ORANGE, 'بافر پروژه', 'Project Buffer', 'انتهای زنجیره بحرانی؛ محافظ تاریخ تحویل')}
{brow(724, CYAN, 'بافر تغذیه', 'Feeding Buffer', 'محل اتصال مسیر غیربحرانی به زنجیره')}
{brow(836, YELLOW, 'بافر منابع', 'Resource Buffer', 'هشدار به منبع کلیدی قبل از نوبتش')}
""", f"""
.brow {{ position:absolute; left:60px; right:60px; height:96px; border-radius:24px; padding:8px 28px 8px 24px;
  background:linear-gradient(180deg, rgba(255,255,255,.09), rgba(255,255,255,.035)); border:2px solid rgba(180,199,231,.22); }}
.brow .dot {{ position:absolute; right:26px; top:34px; width:26px; height:26px; border-radius:50%; }}
.brow .bt {{ position:absolute; right:70px; top:6px; font-size:36px; color:#fff; }}
.brow .bt .en {{ font-size:24px; color:{LAV}; margin-right:6px; }}
.brow .bd {{ position:absolute; right:70px; top:50px; font-size:30px; color:{LAV}; }}
"""))

# 8 ─ Fever chart / BPI
FX, FY, FW, FH = 150, 30, 640, 230
zones = (f'<polygon points="{FX},{FY + FH} {FX + FW},{FY + FH} {FX + FW},{FY + FH * .0} {FX},{FY + FH * .66}" fill="rgba(46,204,113,.0)"/>')
fever = f"""
<polygon points="{FX},{FY + FH} {FX + FW},{FY + FH} {FX + FW},{FY + FH * .33} {FX},{FY + FH * .85}" fill="rgba(46,204,113,.28)"/>
<polygon points="{FX},{FY + FH * .85} {FX + FW},{FY + FH * .33} {FX + FW},{FY} {FX},{FY + FH * .62}" fill="rgba(255,201,60,.28)"/>
<polygon points="{FX},{FY + FH * .62} {FX + FW},{FY} {FX},{FY}" fill="rgba(255,61,90,.30)"/>
<rect x="{FX}" y="{FY}" width="{FW}" height="{FH}" fill="none" stroke="{LAV}" stroke-width="2"/>
<polyline points="{FX},{FY + FH} {FX + 90},{FY + FH - 25} {FX + 190},{FY + FH - 45} {FX + 290},{FY + FH - 110} {FX + 380},{FY + FH - 150}" fill="none" stroke="#fff" stroke-width="4" filter="url(#glowS)"/>
{"".join(f'<circle cx="{FX + a}" cy="{FY + FH - b}" r="7" fill="#fff"/>' for a, b in [(90, 25), (190, 45), (290, 110)])}
<circle cx="{FX + 380}" cy="{FY + FH - 150}" r="11" fill="{YELLOW}" stroke="#fff" stroke-width="3" filter="url(#glowS)"/>
<text x="{FX + 400}" y="{FY + FH - 158}" fill="{YELLOW}" font-size="20">act now!</text>
<text x="{FX + FW - 12}" y="{FY + 30}" text-anchor="end" fill="#FF8A9A" font-size="22">RED</text>
<text x="{FX + FW - 12}" y="{FY + 112}" text-anchor="end" fill="{YELLOW}" font-size="22">YELLOW</text>
<text x="{FX + FW - 12}" y="{FY + FH - 14}" text-anchor="end" fill="{GREEN}" font-size="22">GREEN</text>
<text x="{FX + FW / 2}" y="{FY + FH + 34}" text-anchor="middle" fill="{LAV}" font-size="20">critical chain completed % →</text>
<text x="{FX - 16}" y="{FY + FH / 2 - 10}" text-anchor="end" fill="{LAV}" font-size="20">buffer</text>
<text x="{FX - 16}" y="{FY + FH / 2 + 16}" text-anchor="end" fill="{LAV}" font-size="20">used %</text>
"""
FEV = svg(940, 300, fever)
SLIDES.append(doc(f"""
<div class="chip"><span>کنترل پروژه در زنجیره بحرانی</span></div>
<div class="title">تب‌سنج بافر<span class="sub en">Fever Chart · BPI</span></div>
<div class="accent"></div>
{hero(FEV, 296, 330)}
{defcard('به‌جای ددلاین هر کار، <b>مصرف بافر</b> را با <i>پیشرفت زنجیره</i> مقایسه کنید؛ در <b>PMBOK 8</b> این سیگنال <i>BPI</i> نام دارد.', 'thermometer', 652, 250, CYAN)}
{swipe('شما کدام را تجربه کرده‌اید؟')}
""", acc=262))

# 9 ─ Engagement
def opt(top, n, t, ic):
    return f'<div class="opt" style="top:{top}px"><div class="n">{n}</div><div class="t">{t}</div><div class="oi">{icon(ic, 40, "#FF8A9A", 2)}</div></div>'

SLIDES.append(doc(f"""
<div class="bubble">{icon('message-circle', 80, NAVY, 2.2)}</div>
<div class="title" style="top:196px">کدام <span class="c">دزد زمان</span> در پروژه‌های<br><span class="w">شما</span> فعال‌تر است؟</div>
{opt(392, '۱', 'قانون پارکینسون', 'hourglass')}
{opt(502, '۲', 'سندرم دانشجویی', 'alarm-clock')}
{opt(612, '۳', 'اتلاف چندوظیفگی', 'shuffle')}
<div class="cta">{icon('message-circle', 46, NAVY, 2.4)}<span>شماره‌اش را کامنت کنید</span></div>
<div class="acts"><div>{icon('bookmark', 40, GOLD, 2)}<span>ذخیره کنید</span></div>
<div>{icon('send', 40, GOLD, 2)}<span>برای تیمتان بفرستید</span></div></div>
<div class="foot"><span class="en">@alfa.pmi&nbsp;&nbsp;|&nbsp;&nbsp;www.alfapmi.com</span></div>
""", f"""
.bubble {{ position:absolute; left:472px; top:52px; width:136px; height:136px; border-radius:50%; background:linear-gradient(180deg,#FFC15E,{ORANGE});
  display:flex; align-items:center; justify-content:center; box-shadow:0 0 50px rgba(255,154,60,.5); }}
.opt {{ position:absolute; left:150px; right:150px; height:90px; border-radius:45px; display:flex; align-items:center;
  background:linear-gradient(180deg, rgba(255,255,255,.10), rgba(255,255,255,.04)); border:2px solid rgba(174,148,113,.38); padding:0 12px; }}
.opt .n {{ width:66px; height:66px; border-radius:50%; background:{GOLD}; color:{NAVY}; font-size:42px; font-weight:900;
  display:flex; align-items:center; justify-content:center; flex:none; }}
.opt .t {{ font-size:38px; margin-right:26px; flex:1; }}
.opt .oi {{ margin-left:18px; display:flex; }}
.cta {{ position:absolute; left:150px; right:150px; top:740px; height:98px; border-radius:49px; background:linear-gradient(180deg,#FFC15E,{ORANGE});
  display:flex; align-items:center; justify-content:center; gap:20px; color:{NAVY}; font-size:42px; font-weight:900; box-shadow:0 12px 30px rgba(0,0,0,.4); }}
.acts {{ position:absolute; left:120px; right:120px; top:872px; display:flex; justify-content:center; gap:70px; font-size:34px; }}
.acts div {{ display:flex; align-items:center; gap:14px; }}
.foot {{ position:absolute; left:0; right:0; top:972px; text-align:center; font-size:32px; color:{LAV}; }}
"""))


async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox", "--allow-file-access-from-files"])
        pg = await b.new_page(viewport={"width": 1080, "height": 1080})
        for i, html in enumerate(SLIDES, 1):
            f = ROOT / f"ccm_slide{i}.html"; f.write_text(html, encoding="utf-8")
            await pg.goto(f.as_uri()); await pg.evaluate("document.fonts.ready"); await pg.wait_for_timeout(350)
            await pg.screenshot(path=str(OUT / f"CCM_{i:02d}.png"))
        await b.close()

asyncio.run(main())
print("ok", len(SLIDES))
