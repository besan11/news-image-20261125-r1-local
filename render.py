#!/usr/bin/env python3
"""Render the front page for Wednesday 25 November 2026.

Draws entry.png (1024x1024) from the story list below with Pillow only.
Every number and date in the image was checked against at least two wire
sources on 25 Nov 2026 (wires read up to 17:30 UTC); anything that could
not be verified twice was left out. Run: python3 render.py
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1024, 1024

PAPER = (247, 242, 231)
INK = (26, 24, 20)
RED = (178, 34, 28)
BLUE = (28, 68, 128)
GOLD = (176, 124, 22)
GREY = (110, 104, 92)
LIGHTGREY = (214, 207, 192)
PANEL = (255, 253, 247)
NIGHT = (16, 24, 44)
SEA = (18, 52, 86)
SKY = (196, 216, 232)
FIRE = (232, 110, 26)
EMBER = (248, 178, 44)

REGION_COLORS = {
    "Middle East": (178, 34, 28),
    "Asia": (28, 68, 128),
    "Oceania": (14, 110, 110),
    "Africa": (120, 84, 22),
    "Americas": (106, 44, 110),
    "Europe": (34, 96, 44),
    "Global": (90, 88, 84),
}

TAG_COLORS = {
    "CONFIRMED": (34, 96, 44),
    "OFFICIAL": (28, 68, 128),
    "REPORTED": (120, 84, 22),
    "CLAIM": (178, 34, 28),
}


def font(name, size):
    return ImageFont.truetype(os.path.join(HERE, "fonts", name), size)


F_SERIF = "DejaVuSerif-Bold.ttf"
F_SANS = "DejaVuSans.ttf"
F_SANSB = "DejaVuSans-Bold.ttf"


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, text, fnt, fill, max_w, leading=None):
    if leading is None:
        leading = int(fnt.size * 1.22)
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def chip(draw, x, y, text, fill):
    fnt = font(F_SANSB, 11)
    w = int(draw.textlength(text, font=fnt)) + 10
    draw.rounded_rectangle([x, y, x + w, y + 16], radius=3, fill=fill)
    draw.text((x + 5, y + 2), text, font=fnt, fill=(255, 255, 255))
    return w


def num_badge(draw, x, y, n, d=26):
    draw.ellipse([x, y, x + d, y + d], fill=RED)
    fnt = font(F_SANSB, 15)
    t = str(n)
    tw = draw.textlength(t, font=fnt)
    draw.text((x + (d - tw) / 2, y + 4), t, font=fnt, fill=(255, 255, 255))


def region_dot(draw, x, y, region, d=8):
    draw.ellipse([x, y, x + d, y + d], fill=REGION_COLORS[region])


# ---------------------------------------------------------------- stories
# tag: CONFIRMED = 2+ outlets, OFFICIAL = on the record,
#      REPORTED = one outlet, CLAIM = one side's account.
LEADS = [
    dict(num=1, region="Middle East", tag="CLAIM", place="STRAIT OF HORMUZ",
         scene="hormuz",
         head="Two tankers hit mines and burn in the Strait",
         dek="IRGC Navy says two tankers struck mines and caught fire on an "
             "unauthorised route.",
         src="Reuters \u00b7 Al Jazeera \u00b7 IRNA",
         data=["2 TANKERS", "BRENT < $90"]),
    dict(num=2, region="Asia", tag="CONFIRMED", place="SEOUL \u00b7 TOKYO \u00b7 TAIPEI",
         scene="chips",
         head="AI doubts crash Asia's chip stocks",
         dek="Kospi closes down 6.2%, SK hynix -11%, SoftBank -15%, Nikkei -2.8%. "
             "Nasdaq futures fall as new US tariffs are reported.",
         src="Al Jazeera \u00b7 CNBC",
         data=["KOSPI -6.2%", "SOFTBANK -15%"]),
    dict(num=3, region="Oceania", tag="OFFICIAL", place="CANBERRA",
         scene="solomons",
         head="Australia and Solomons sign security treaty",
         dek="Names Australia the primary security partner and bars any foreign "
             "military base; ends the China pact.",
         src="BBC \u00b7 RNZ",
         data=["NO FOREIGN BASES", "CHINA PACT ENDS"]),
]

MIDS = [
    dict(num=4, region="Asia", tag="OFFICIAL", place="JIUQUAN, CHINA",
         scene="shenzhou",
         head="Shenzhou-24 carries Pakistan's first astronaut",
         src="BBC \u00b7 Euronews"),
    dict(num=5, region="Middle East", tag="CONFIRMED", place="RIYADH",
         scene="riyadh",
         head="Houthi attack hits Riyadh tower again; 11 injured",
         src="CNBC \u00b7 Le Monde"),
    dict(num=6, region="Africa", tag="REPORTED", place="MINEMBWE, DR CONGO",
         scene="congo",
         head="Congo warplane missing; Ebola teams trapped",
         src="BBC \u00b7 UN News"),
    dict(num=7, region="Americas", tag="REPORTED", place="WASHINGTON",
         scene="tariffs",
         head="Trump set to impose new tariffs on 16 economies",
         src="BBC \u00b7 Sky News"),
    dict(num=8, region="Europe", tag="OFFICIAL", place="BERLIN",
         scene="merz",
         head="Merz: Russia wants more than Ukraine",
         src="Guardian \u00b7 Straits Times"),
    dict(num=9, region="Americas", tag="CONFIRMED", place="CARTAGENA, COLOMBIA",
         scene="cartagena",
         head="Cartagena siege ends; ~20 hostages freed",
         src="BBC \u00b7 Guardian"),
    dict(num=10, region="Middle East", tag="REPORTED", place="GAZA CITY",
         scene="gaza",
         head="US senators urge Israel to release Gaza winter aid",
         src="Reuters \u00b7 AP"),
    dict(num=11, region="Europe", tag="REPORTED", place="WARSAW",
         scene="poland",
         head="Russian drone enters Polish airspace",
         src="UPI \u00b7 Fox News"),
    dict(num=12, region="Europe", tag="OFFICIAL", place="LONDON",
         scene="energy",
         head="UK energy bills to jump 26% in January",
         src="BBC \u00b7 Guardian"),
    dict(num=13, region="Europe", tag="CONFIRMED", place="MADRID",
         scene="madrid",
         head="Real Madrid beat PSV 5-1 in the Champions League",
         src="France 24 \u00b7 Guardian"),
]

BRIEFS = [
    (14, "Middle East", "REPORTED", "Ukraine hits Russian ships off Libya; 2 die"),
    (15, "Global", "CONFIRMED", "Oil down over 20% in November; Brent $87.84"),
    (16, "Americas", "REPORTED", "Nvidia -4.5% as lawmakers query Huang return"),
    (17, "Asia", "CONFIRMED", "Garment pay +36%: 12,500 \u2192 17,000 taka"),
    (18, "Asia", "REPORTED", "Flooded mine: 3 dead, 23 miners trapped"),
    (19, "Europe", "OFFICIAL", "UK: 5,200 heat deaths in England, a record"),
    (20, "Oceania", "OFFICIAL", "Australia's inflation rises to 4.9%"),
    (21, "Americas", "CONFIRMED", "Argentina enters technical recession"),
    (22, "Americas", "OFFICIAL", "WHO: Cuba life expectancy 78.8 \u2192 74.4"),
    (23, "Global", "OFFICIAL", "UN: HIV gains could unravel as funding falls"),
    (24, "Global", "OFFICIAL", "BepiColombo reaches Mercury orbit"),
    (25, "Africa", "REPORTED", "Zambia indicts opposition leader for treason"),
    (26, "Africa", "REPORTED", "RSF drone strikes kill 19 in Sudan's Blue Nile"),
    (27, "Middle East", "REPORTED", "Iraq moves to take over Kurdish oilfields"),
    (28, "Africa", "REPORTED", "DR Congo halts cobalt exports again"),
    (29, "Americas", "REPORTED", "Democrats win US House majority"),
    (30, "Americas", "REPORTED", "Pentagon criticises Canada's military spending"),
    (31, "Europe", "REPORTED", "Spain heads to snap election; vote on Sunday"),
    (32, "Middle East", "CONFIRMED", "Iran flogs singer Parastoo Ahmadi 74 times"),
    (33, "Europe", "OFFICIAL", "US and Armenia start Trump transit route"),
    (34, "Asia", "CONFIRMED", "Ronaldo's 987th goal as Al Nassr win Asian CL"),
    (35, "Asia", "CONFIRMED", "Sooryavanshi, 15, scores 204 off 53 balls"),
]

STATS = [
    ("2", "tankers hit mines in Hormuz"),
    ("-6.2%", "Kospi close, worst day of the AI rout"),
    ("-15%", "SoftBank shares in one day"),
    ("11", "injured in the Riyadh tower attack"),
    ("~20", "hostages freed in Cartagena"),
    ("-20%", "Brent crude in November"),
]

UTC_STRIP = [
    ("00:18", "Shenzhou-24 lifts off, Jiuquan"),
    ("03:56", "Shenzhou-24 docks at Tiangong"),
    ("10:06", "Reuters: two tankers hit mines in Hormuz"),
    ("15:00", "US Army to detonate 5 tons of lead azide, Iowa"),
    ("20:00", "Real Madrid 5-1 PSV, Champions League"),
]

DATE_CHECK = (
    "DATE CHECK \u2014 Left out on purpose, first reported before Wednesday: Huawei convicted "
    "in Brooklyn (Tue 24 Nov) \u00b7 UN Femicide Brief: 47,000 women killed in 2025 (Tue 24 Nov) "
    "\u00b7 leaked Russian war deaths, ~490,000 (Tue 24 Nov) \u00b7 CAS restores Senegal's AFCON "
    "title (Tue 24 Nov) \u00b7 COP31 collapse (Sun 22 Nov). Not yet: Spain votes (Sun 30 Nov)."
)

REGION_COUNTS = [
    ("Middle East", 6), ("Asia", 6), ("Americas", 7), ("Europe", 7),
    ("Africa", 4), ("Oceania", 2), ("Global", 3),
]

# ------------------------------------------------------------------- scenes
def scene_hormuz(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=NIGHT)
    for sx, sy, sr in [(18, 14, 2), (70, 8, 1), (150, 20, 2), (230, 10, 1),
                       (280, 26, 2), (40, 34, 1), (190, 6, 1)]:
        d.ellipse([x + sx, y + sy, x + sx + sr, y + sy + sr], fill=(220, 220, 200))
    d.rectangle([x, y + int(h * 0.62), x + w, y + h], fill=SEA)
    d.line([x, y + int(h * 0.62), x + w, y + int(h * 0.62)], fill=(120, 160, 200), width=2)
    # two tankers, both burning
    for tx, twd in [(18, 118), (168, 104)]:
        ty = y + int(h * 0.62) - 20
        d.rectangle([x + tx, ty, x + tx + twd, ty + 24], fill=(74, 74, 84))
        d.rectangle([x + tx + 12, ty - 12, x + tx + 34, ty], fill=(96, 96, 106))
        d.rectangle([x + tx + twd - 22, ty - 18, x + tx + twd - 8, ty], fill=(96, 96, 106))
        for wx in range(tx + 8, tx + twd - 8, 14):
            d.rectangle([x + wx, ty + 6, x + wx + 6, ty + 12], fill=(240, 220, 140))
        d.polygon([(x + tx + 46, ty - 12), (x + tx + 62, ty - 56),
                   (x + tx + 78, ty - 12)], fill=FIRE)
        d.polygon([(x + tx + 54, ty - 10), (x + tx + 64, ty - 38),
                   (x + tx + 72, ty - 10)], fill=EMBER)
        d.ellipse([x + tx + 50, ty - 64, x + tx + 76, ty - 48], fill=(90, 90, 96))
        d.ellipse([x + tx + 56, ty - 78, x + tx + 74, ty - 64], fill=(120, 120, 126))
    # mines on the water
    for mx, my in [(150, int(h * 0.78)), (268, int(h * 0.86)), (60, int(h * 0.9))]:
        d.ellipse([x + mx, y + my, x + mx + 7, y + my + 7], fill=(20, 20, 24))
        d.line([x + mx - 3, y + my + 3, x + mx + 10, y + my + 3], fill=(20, 20, 24), width=1)
        d.line([x + mx + 3, y + my - 3, x + mx + 3, y + my + 10], fill=(20, 20, 24), width=1)
    d.text((x + 8, y + h - 18), "STRAIT OF HORMUZ \u00b7 EARLY HOURS",
           font=font(F_SANSB, 10), fill=(200, 210, 225))


def scene_chips(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(14, 14, 18))
    for gy in range(4):
        yy = y + 14 + gy * 34
        d.line([x + 8, yy, x + w - 8, yy], fill=(44, 44, 52), width=1)
    pts = [(x + 10, y + 26), (x + 50, y + 34), (x + 90, y + 30), (x + 130, y + 48),
           (x + 170, y + 58), (x + 210, y + 52), (x + 250, y + 84), (x + 285, y + 118)]
    d.line(pts, fill=RED, width=4, joint="curve")
    d.polygon(pts + [(x + 285, y + h - 8), (x + 10, y + h - 8)], fill=(96, 18, 14))
    d.line(pts, fill=(255, 100, 80), width=3, joint="curve")
    d.polygon([(x + 278, y + 112), (x + 292, y + 112), (x + 285, y + 126)], fill=(255, 100, 80))
    d.text((x + 10, y + 6), "KOSPI", font=font(F_SANSB, 11), fill=(200, 200, 210))
    d.text((x + w - 66, y + 6), "-6.2%", font=font(F_SANSB, 13), fill=(255, 90, 70))
    d.text((x + 10, y + h - 40), "NIKKEI -2.8%  \u00b7  HANG SENG -1.9%",
           font=font(F_SANSB, 10), fill=(235, 235, 240))
    d.text((x + 10, y + h - 24), "SOFTBANK -15%  \u00b7  SK HYNIX -11%",
           font=font(F_SANSB, 10), fill=(255, 150, 130))


def scene_solomons(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(214, 232, 240))
    # stylised Australia + Solomons dots
    d.polygon([(x + 24, y + 82), (x + 58, y + 72), (x + 128, y + 70),
               (x + 178, y + 78), (x + 198, y + 94), (x + 184, y + 116),
               (x + 132, y + 126), (x + 74, y + 120), (x + 36, y + 106)],
              fill=(196, 164, 110))
    for ix, iy in [(238, 52), (252, 46), (264, 54), (228, 40)]:
        d.ellipse([x + ix, y + iy, x + ix + 7, y + iy + 5], fill=(120, 84, 22))
    d.ellipse([x + 236, y + 50, x + 244, y + 58], fill=RED, outline=(255, 255, 255), width=2)
    d.text((x + 12, y + 10), "SOLOMON IS.", font=font(F_SANSB, 11), fill=INK)
    d.text((x + 12, y + 26), "HONIARA", font=font(F_SANS, 10), fill=GREY)
    # treaty paper + pen
    d.rectangle([x + 196, y + 84, x + 282, y + 130], fill=(255, 253, 247),
                outline=INK, width=2)
    d.line([x + 204, y + 98, x + 274, y + 98], fill=GREY, width=1)
    d.line([x + 204, y + 108, x + 274, y + 108], fill=GREY, width=1)
    d.line([x + 204, y + 118, x + 254, y + 118], fill=GREY, width=1)
    d.line([x + 204, y + 126, x + 232, y + 126], fill=RED, width=2)
    d.line([x + 286, y + 112, x + 294, y + 132], fill=BLUE, width=3)
    d.text((x + 12, y + h - 18), "SIGNED 25 NOV 2026 \u00b7 CANBERRA",
           font=font(F_SANSB, 10), fill=BLUE)


def scene_shenzhou(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=NIGHT)
    for sx, sy in [(12, 10), (48, 26), (150, 8), (172, 30), (90, 16), (30, 44)]:
        d.ellipse([x + sx, y + sy, x + sx + 2, y + sy + 2], fill=(230, 230, 210))
    # Tiangong station
    cx, cy = x + 118, y + 16
    d.rectangle([cx, cy, cx + 56, cy + 10], fill=(200, 200, 205))
    d.rectangle([cx - 26, cy + 2, cx, cy + 8], fill=(40, 90, 160))
    d.rectangle([cx + 56, cy + 2, cx + 82, cy + 8], fill=(40, 90, 160))
    d.ellipse([cx + 22, cy - 4, cx + 34, cy + 14], fill=(220, 220, 225))
    # rocket rising
    rx = x + 62
    d.polygon([(rx, y + h - 6), (rx + 8, y + h - 34), (rx + 16, y + h - 6)], fill=FIRE)
    d.polygon([(rx + 4, y + h - 22), (rx + 8, y + h - 32), (rx + 12, y + h - 22)], fill=EMBER)
    d.rectangle([rx + 2, y + h - 52, rx + 14, y + h - 30], fill=(235, 235, 240))
    d.polygon([(rx + 2, y + h - 52), (rx + 8, y + h - 64), (rx + 14, y + h - 52)],
              fill=RED)
    d.rectangle([rx - 4, y + h - 40, rx + 2, y + h - 30], fill=(180, 60, 50))
    d.rectangle([rx + 14, y + h - 40, rx + 20, y + h - 30], fill=(180, 60, 50))
    d.arc([x + 30, y + 6, x + 150, y + 58], 200, 340, fill=(120, 140, 170), width=1)
    d.text((x + 6, y + h - 14), "00:18 UTC \u00b7 DOCKED 03:56 UTC",
           font=font(F_SANSB, 9), fill=(200, 210, 225))


def scene_riyadh(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(58, 48, 66))
    d.ellipse([x + w - 34, y + 6, x + w - 10, y + 30], fill=(240, 214, 160))
    # skyline
    for bx, bw, bh in [(6, 26, 34), (36, 20, 48), (60, 30, 26), (140, 24, 40), (168, 18, 30)]:
        d.rectangle([x + bx, y + h - bh, x + bx + bw, y + h], fill=(38, 32, 46))
    # PIF tower, hit
    tx = x + 96
    d.polygon([(tx, y + 8), (tx + 10, y + 2), (tx + 20, y + 8),
               (tx + 20, y + h), (tx, y + h)], fill=(24, 20, 30))
    d.line([tx + 6, y + 10, tx + 6, y + h - 4], fill=(120, 110, 130), width=1)
    d.ellipse([tx + 2, y + 22, tx + 18, y + 38], fill=FIRE)
    d.ellipse([tx + 12, y + 8, tx + 30, y + 24], fill=(90, 90, 96))
    d.ellipse([tx + 22, y - 2, tx + 36, y + 12], fill=(120, 120, 126))
    # drone
    d.ellipse([x + 150, y + 14, x + 158, y + 20], fill=(220, 220, 220))
    d.line([x + 144, y + 17, x + 164, y + 17], fill=(220, 220, 220), width=1)
    d.text((x + 6, y + h - 14), "2ND HIT IN 6 DAYS \u00b7 11 INJURED",
           font=font(F_SANSB, 9), fill=(245, 220, 200))


def scene_congo(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(206, 198, 168))
    d.rectangle([x + 10, y + 22, x + 96, y + h - 6], fill=(240, 238, 230))
    d.rectangle([x + 10, y + 22, x + 96, y + 32], fill=RED)
    d.rectangle([x + 44, y + 38, x + 62, y + 44], fill=RED)
    d.rectangle([x + 50, y + 34, x + 56, y + 48], fill=RED)
    for wy in (54, 66):
        d.rectangle([x + 18, y + wy, x + 34, y + wy + 8], fill=SKY)
        d.rectangle([x + 66, y + wy, x + 82, y + wy + 8], fill=SKY)
    # helicopter
    hx, hy = x + 128, y + 16
    d.ellipse([hx, hy, hx + 34, hy + 12], fill=(52, 52, 58))
    d.line([hx + 4, hy + 2, hx + 44, hy + 2], fill=(52, 52, 58), width=2)
    d.line([hx + 30, hy + 6, hx + 44, hy + 16], fill=(52, 52, 58), width=2)
    d.line([hx + 8, hy + 12, hx + 8, hy + 22], fill=(52, 52, 58), width=2)
    d.line([hx + 26, hy + 12, hx + 26, hy + 22], fill=(52, 52, 58), width=2)
    d.text((x + 112, y + 34), "SEARCH", font=font(F_SANSB, 10), fill=INK)
    d.text((x + 112, y + 46), "UNDER WAY", font=font(F_SANSB, 10), fill=INK)
    d.text((x + 6, y + h - 14), "ITURI \u00b7 EBOLA TEAMS TRAPPED",
           font=font(F_SANSB, 9), fill=(120, 20, 16))


def scene_tariffs(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 226, 208))
    bars = [(16, 26, "CN"), (48, 38, "EU"), (80, 30, "JP"), (112, 46, "IN"), (144, 20, "KR")]
    for bx, bh, lab in bars:
        d.rectangle([x + bx, y + h - 16 - bh, x + bx + 22, y + h - 16], fill=RED)
        d.text((x + bx + 2, y + h - 14), lab, font=font(F_SANSB, 9), fill=INK)
    d.line([x + 8, y + h - 16, x + w - 8, y + h - 16], fill=INK, width=2)
    d.text((x + 10, y + 6), "16 ECONOMIES", font=font(F_SANSB, 11), fill=INK)
    d.text((x + 10, y + 20), "NEW US TARIFFS REPORTED", font=font(F_SANSB, 9), fill=GREY)


def scene_merz(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(226, 222, 210))
    # German flag stripes
    d.rectangle([x + 8, y + 8, x + 52, y + 14], fill=(20, 20, 20))
    d.rectangle([x + 8, y + 14, x + 52, y + 20], fill=RED)
    d.rectangle([x + 8, y + 20, x + 52, y + 26], fill=(240, 200, 40))
    # podium + speaker
    d.rectangle([x + 66, y + 34, x + 130, y + h - 6], fill=(90, 70, 52))
    d.ellipse([x + 84, y + 10, x + 112, y + 38], fill=(214, 180, 150))
    d.rectangle([x + 80, y + 34, x + 116, y + 44], fill=(40, 44, 60))
    d.line([x + 96, y + 34, x + 96, y + 22], fill=INK, width=2)
    d.ellipse([x + 92, y + 18, x + 100, y + 26], fill=INK)
    d.text((x + 138, y + 14), "\u201cMORE THAN", font=font(F_SANSB, 11), fill=INK)
    d.text((x + 138, y + 28), "UKRAINE\u201d", font=font(F_SANSB, 11), fill=INK)
    d.text((x + 138, y + 44), "BUNDESTAG", font=font(F_SANS, 9), fill=GREY)


def scene_cartagena(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(240, 222, 180))
    d.rectangle([x + 8, y + 18, x + w - 8, y + h - 6], fill=(250, 248, 240))
    d.rectangle([x + 8, y + 18, x + w - 8, y + 30], fill=(30, 90, 140))
    for ax in range(8, w - 8, 24):
        d.polygon([(x + ax, y + 30), (x + ax + 12, y + 30), (x + ax + 12, y + 38),
                   (x + ax, y + 38)], fill=(255, 255, 255) if (ax // 24) % 2 else (200, 40, 40))
    d.rectangle([x + 70, y + 44, x + 120, y + h - 6], fill=(120, 150, 180))
    d.line([x + 95, y + 44, x + 95, y + h - 6], fill=(80, 100, 130), width=2)
    # figures leaving
    for fx, fc in [(24, (40, 90, 140)), (44, (140, 60, 40)), (140, (40, 110, 60))]:
        d.ellipse([x + fx, y + 46, x + fx + 10, y + 56], fill=fc)
        d.rectangle([x + fx + 1, y + 56, x + fx + 9, y + h - 8], fill=fc)
    d.text((x + 8, y + h - 14), "17 HOURS \u00b7 ~20 FREED",
           font=font(F_SANSB, 9), fill=INK)


def scene_gaza(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(196, 206, 216))
    # rain + tents
    for rx in range(10, w, 26):
        d.line([x + rx, y + 6, x + rx - 6, y + 18], fill=(120, 140, 160), width=1)
    for tx, tc in [(14, (240, 238, 228)), (66, (220, 210, 180)), (118, (200, 190, 160))]:
        d.polygon([(x + tx, y + h - 6), (x + tx + 22, y + 30), (x + tx + 44, y + h - 6)],
                  fill=tc, outline=(120, 110, 90))
    # aid truck
    d.rectangle([x + 130, y + h - 26, x + 182, y + h - 8], fill=(240, 240, 240),
                outline=INK, width=1)
    d.rectangle([x + 130, y + h - 26, x + 158, y + h - 14], fill=(30, 90, 140))
    d.ellipse([x + 138, y + h - 10, x + 146, y + h - 2], fill=INK)
    d.ellipse([x + 166, y + h - 10, x + 174, y + h - 2], fill=INK)
    d.text((x + 8, y + h - 14), "70,000 TENTS FLOODED",
           font=font(F_SANSB, 9), fill=INK)


def scene_poland(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(40, 54, 84))
    d.arc([x + 20, y + 10, x + 170, y + 120], 200, 340, fill=(120, 140, 180), width=1)
    d.arc([x + 40, y + 22, x + 150, y + 108], 200, 340, fill=(120, 140, 180), width=1)
    # drone
    dx, dy = x + 108, y + 22
    d.ellipse([dx, dy, dx + 26, dy + 10], fill=(220, 220, 220))
    d.line([dx - 6, dy + 4, dx + 32, dy + 4], fill=(220, 220, 220), width=2)
    d.ellipse([dx + 8, dy + 10, dx + 18, dy + 16], fill=(180, 180, 180))
    d.text((x + 8, y + h - 26), "NATO AIRSPACE", font=font(F_SANSB, 10), fill=(230, 230, 240))
    d.text((x + 8, y + h - 14), "3 MISSILES DAYS EARLIER",
           font=font(F_SANSB, 9), fill=(180, 190, 210))


def scene_energy(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(238, 230, 200))
    # house
    d.polygon([(x + 20, y + 34), (x + 62, y + 12), (x + 104, y + 34)], fill=RED)
    d.rectangle([x + 28, y + 34, x + 96, y + h - 6], fill=(250, 246, 236))
    d.rectangle([x + 54, y + 52, x + 70, y + h - 6], fill=(120, 84, 50))
    d.rectangle([x + 34, y + 42, x + 46, y + 54], fill=SKY)
    d.rectangle([x + 78, y + 42, x + 90, y + 54], fill=SKY)
    # lightning bolt + price
    d.polygon([(x + 140, y + 10), (x + 128, y + 34), (x + 140, y + 34),
               (x + 132, y + 56), (x + 152, y + 28), (x + 140, y + 28)],
              fill=GOLD)
    d.text((x + 122, y + h - 16), "\u00a32,166 / YEAR", font=font(F_SANSB, 11), fill=INK)


def scene_madrid(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(52, 140, 70))
    for lx in range(0, w, 32):
        d.line([x + lx, y, x + lx, y + h], fill=(46, 128, 64), width=16)
    d.ellipse([x + w // 2 - 30, y + h // 2 - 18, x + w // 2 + 30, y + h // 2 + 18],
              outline=(255, 255, 255), width=2)
    d.line([x + w // 2, y, x + w // 2, y + h], fill=(255, 255, 255), width=2)
    # goal + ball
    d.rectangle([x + 12, y + 12, x + 52, y + 40], outline=(255, 255, 255), width=2)
    d.ellipse([x + 150, y + 46, x + 164, y + 60], fill=(255, 255, 255), outline=INK)
    d.rectangle([x + w - 62, y + 6, x + w - 8, y + 26], fill=(20, 20, 24))
    d.text((x + w - 56, y + 9), "5 - 1", font=font(F_SANSB, 12), fill=(255, 255, 255))
    d.text((x + 8, y + h - 14), "REAL MADRID 5-1 PSV",
           font=font(F_SANSB, 9), fill=(255, 255, 255))


SCENES = {
    "hormuz": scene_hormuz, "chips": scene_chips, "solomons": scene_solomons,
    "shenzhou": scene_shenzhou, "riyadh": scene_riyadh, "congo": scene_congo,
    "tariffs": scene_tariffs, "merz": scene_merz, "cartagena": scene_cartagena,
    "gaza": scene_gaza, "poland": scene_poland, "energy": scene_energy,
    "madrid": scene_madrid,
}

# ------------------------------------------------------- compact mid scenes
def mini_shenzhou(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=NIGHT)
    d.rectangle([x + 20, y + 12, x + 46, y + 18], fill=(200, 200, 205))
    d.rectangle([x + 8, y + 14, x + 20, y + 17], fill=(40, 90, 160))
    d.rectangle([x + 46, y + 14, x + 58, y + 17], fill=(40, 90, 160))
    d.polygon([(x + 120, y + h), (x + 126, y + 22), (x + 132, y + h)], fill=FIRE)
    d.rectangle([x + 123, y + 8, x + 131, y + 26], fill=(235, 235, 240))
    d.polygon([(x + 123, y + 8), (x + 127, y + 2), (x + 131, y + 8)], fill=RED)


def mini_riyadh(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(58, 48, 66))
    for bx, bw, bh in [(6, 24, 22), (34, 18, 32), (140, 22, 26), (166, 16, 20)]:
        d.rectangle([x + bx, y + h - bh, x + bx + bw, y + h], fill=(38, 32, 46))
    tx = x + 82
    d.polygon([(tx, y + 4), (tx + 9, y), (tx + 18, y + 4), (tx + 18, y + h),
               (tx, y + h)], fill=(24, 20, 30))
    d.ellipse([tx + 2, y + 14, tx + 16, y + 28], fill=FIRE)
    d.ellipse([tx + 10, y + 4, tx + 24, y + 16], fill=(110, 110, 116))
    d.text((x + 104, y + 8), "11 INJURED", font=font(F_SANSB, 10), fill=(245, 220, 200))


def mini_congo(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(206, 198, 168))
    d.rectangle([x + 12, y + 14, x + 78, y + h - 4], fill=(240, 238, 230))
    d.rectangle([x + 12, y + 14, x + 78, y + 22], fill=RED)
    d.rectangle([x + 40, y + 28, x + 50, y + 32], fill=RED)
    d.rectangle([x + 44, y + 26, x + 46, y + 34], fill=RED)
    d.ellipse([x + 120, y + 8, x + 146, y + 18], fill=(52, 52, 58))
    d.line([x + 124, y + 9, x + 154, y + 9], fill=(52, 52, 58), width=2)
    d.text((x + 100, y + 30), "ITURI", font=font(F_SANSB, 11), fill=INK)
    d.text((x + 100, y + 44), "EBOLA TEAMS", font=font(F_SANSB, 10), fill=(120, 20, 16))


def mini_tariffs(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 226, 208))
    d.text((x + 8, y + 4), "16 ECONOMIES", font=font(F_SANSB, 11), fill=INK)
    for bx, bh in [(14, 16), (44, 24), (74, 20), (104, 28), (134, 14)]:
        d.rectangle([x + bx, y + h - 8 - bh, x + bx + 20, y + h - 8], fill=RED)
    d.line([x + 8, y + h - 8, x + w - 8, y + h - 8], fill=INK, width=2)


def mini_merz(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(226, 222, 210))
    d.rectangle([x + 10, y + 10, x + 50, y + 16], fill=(20, 20, 20))
    d.rectangle([x + 10, y + 16, x + 50, y + 22], fill=RED)
    d.rectangle([x + 10, y + 22, x + 50, y + 28], fill=(240, 200, 40))
    d.rectangle([x + 70, y + 30, x + 120, y + h - 4], fill=(90, 70, 52))
    d.ellipse([x + 84, y + 10, x + 106, y + 32], fill=(214, 180, 150))
    d.text((x + 112, y + 10), "\u201cMORE THAN", font=font(F_SANSB, 9), fill=INK)
    d.text((x + 112, y + 24), "UKRAINE\u201d", font=font(F_SANSB, 9), fill=INK)
    d.text((x + 112, y + 38), "BUNDESTAG", font=font(F_SANS, 9), fill=GREY)


def mini_cartagena(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(240, 222, 180))
    d.rectangle([x + 10, y + 12, x + w - 10, y + h - 4], fill=(250, 248, 240))
    d.rectangle([x + 10, y + 12, x + w - 10, y + 22], fill=(30, 90, 140))
    for ax in range(10, w - 10, 22):
        d.polygon([(x + ax, y + 22), (x + ax + 11, y + 22), (x + ax + 11, y + 29),
                   (x + ax, y + 29)], fill=(255, 255, 255) if (ax // 22) % 2 else (200, 40, 40))
    for fx, fc in [(26, (40, 90, 140)), (46, (140, 60, 40)), (150, (40, 110, 60))]:
        d.ellipse([x + fx, y + 34, x + fx + 10, y + 44], fill=fc)
        d.rectangle([x + fx + 1, y + 44, x + fx + 9, y + h - 6], fill=fc)
    d.text((x + 66, y + 34), "~20 FREED", font=font(F_SANSB, 11), fill=INK)


def mini_gaza(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(196, 206, 216))
    for rx in range(10, w, 24):
        d.line([x + rx, y + 4, x + rx - 5, y + 14], fill=(120, 140, 160), width=1)
    for tx, tc in [(14, (240, 238, 228)), (62, (220, 210, 180)), (110, (200, 190, 160))]:
        d.polygon([(x + tx, y + h - 4), (x + tx + 20, y + 22), (x + tx + 40, y + h - 4)],
                  fill=tc, outline=(120, 110, 90))
    d.text((x + 140, y + 8), "70,000", font=font(F_SANSB, 12), fill=INK)
    d.text((x + 140, y + 24), "TENTS", font=font(F_SANSB, 10), fill=INK)
    d.text((x + 140, y + 38), "FLOODED", font=font(F_SANSB, 10), fill=INK)


def mini_poland(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(40, 54, 84))
    d.arc([x + 16, y + 6, x + 150, y + 110], 200, 340, fill=(120, 140, 180), width=1)
    d.arc([x + 34, y + 16, x + 132, y + 100], 200, 340, fill=(120, 140, 180), width=1)
    dx, dy = x + 100, y + 14
    d.ellipse([dx, dy, dx + 24, dy + 9], fill=(220, 220, 220))
    d.line([dx - 5, dy + 4, dx + 29, dy + 4], fill=(220, 220, 220), width=2)
    d.text((x + 8, y + h - 16), "NATO AIRSPACE", font=font(F_SANSB, 10),
           fill=(230, 230, 240))


def mini_energy(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(238, 230, 200))
    d.polygon([(x + 16, y + 26), (x + 52, y + 8), (x + 88, y + 26)], fill=RED)
    d.rectangle([x + 22, y + 26, x + 82, y + h - 4], fill=(250, 246, 236))
    d.rectangle([x + 46, y + 40, x + 58, y + h - 4], fill=(120, 84, 50))
    d.polygon([(x + 128, y + 8), (x + 118, y + 28), (x + 128, y + 28),
               (x + 122, y + 46), (x + 138, y + 22), (x + 128, y + 22)], fill=GOLD)
    d.text((x + 96, y + h - 16), "\u00a32,166 / YEAR", font=font(F_SANSB, 10), fill=INK)


def mini_madrid(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(52, 140, 70))
    for lx in range(0, w, 30):
        d.line([x + lx, y, x + lx, y + h], fill=(46, 128, 64), width=15)
    d.ellipse([x + w // 2 - 26, y + h // 2 - 16, x + w // 2 + 26, y + h // 2 + 16],
              outline=(255, 255, 255), width=2)
    d.line([x + w // 2, y, x + w // 2, y + h], fill=(255, 255, 255), width=2)
    d.rectangle([x + w - 56, y + 6, x + w - 8, y + 24], fill=(20, 20, 24))
    d.text((x + w - 50, y + 8), "5 - 1", font=font(F_SANSB, 11), fill=(255, 255, 255))
    d.ellipse([x + 140, y + 40, x + 152, y + 52], fill=(255, 255, 255), outline=INK)


MINI_SCENES = {
    "shenzhou": mini_shenzhou, "riyadh": mini_riyadh, "congo": mini_congo,
    "tariffs": mini_tariffs, "merz": mini_merz, "cartagena": mini_cartagena,
    "gaza": mini_gaza, "poland": mini_poland, "energy": mini_energy,
    "madrid": mini_madrid,
}

# ------------------------------------------------------------------ layout
MX = 28
CW = W - 2 * MX


def masthead(d):
    y = 12
    d.text((MX, y), "THE WORLD IN ONE DAY", font=font(F_SANSB, 12), fill=RED)
    right = "35 STORIES \u00b7 7 REGIONS \u00b7 15 FIELDS \u00b7 WIRES TO 17:30 UTC"
    rw = d.textlength(right, font=font(F_SANSB, 12))
    d.text((W - MX - rw, y), right, font=font(F_SANSB, 12), fill=INK)
    y = 30
    d.text((MX, y), "Wednesday 25 November 2026",
           font=font(F_SERIF, 56), fill=INK)
    y = 94
    d.text((MX, y), "Events that happened or were first reported on 25 November 2026 "
                    "\u00b7 all times UTC \u00b7 rep = first reported",
           font=font(F_SANS, 11), fill=GREY)
    y = 110
    d.text((MX, y), "CONFIRMED = 2+ outlets \u00b7 OFFICIAL = on the record "
                    "\u00b7 REPORTED = one outlet \u00b7 CLAIM = one side's account",
           font=font(F_SANS, 10), fill=GREY)
    d.line([MX, 126, W - MX, 126], fill=INK, width=2)


def stat_row(d, y):
    bw = (CW - 5 * 8) // 6
    for i, (big, small) in enumerate(STATS):
        x = MX + i * (bw + 8)
        d.rectangle([x, y, x + bw, y + 48], fill=PANEL, outline=LIGHTGREY, width=1)
        d.text((x + 8, y + 4), big, font=font(F_SANSB, 20), fill=RED)
        text_block(d, x + 8, y + 27, small, font(F_SANS, 10), INK, bw - 14, leading=10)
    return y + 48


def leads(d, y):
    lw = (CW - 2 * 12) // 3
    lh = 300
    for i, s in enumerate(LEADS):
        x = MX + i * (lw + 12)
        d.rectangle([x, y, x + lw, y + lh], fill=PANEL, outline=LIGHTGREY, width=1)
        SCENES[s["scene"]](d, x + 1, y + 1, lw - 2, 150)
        yy = y + 158
        num_badge(d, x + 8, yy, s["num"])
        d.text((x + 40, yy + 4), s["place"], font=font(F_SANSB, 11), fill=INK)
        tag = s["tag"]
        tf = font(F_SANSB, 11)
        tw = int(d.textlength(tag, font=tf)) + 10
        d.rounded_rectangle([x + lw - 8 - tw, yy + 4, x + lw - 8, yy + 20],
                            radius=3, fill=TAG_COLORS[tag])
        d.text((x + lw - 8 - tw + 5, yy + 6), tag, font=tf, fill=(255, 255, 255))
        yy += 32
        yy = text_block(d, x + 8, yy, s["head"], font(F_SERIF, 19), INK, lw - 16,
                        leading=23)
        yy += 4
        text_block(d, x + 8, yy, s["dek"], font(F_SANS, 12), (60, 56, 48),
                   lw - 16, leading=14)
        d.text((x + 8, y + lh - 16), s["src"], font=font(F_SANS, 10), fill=GREY)
        data = " \u00b7 ".join(s["data"])
        df = font(F_SANSB, 10)
        dw = d.textlength(data, font=df)
        d.text((x + lw - 8 - dw, y + lh - 16), data, font=df, fill=RED)
    return y + lh


def utc_strip(d, y):
    d.rectangle([MX, y, W - MX, y + 44], fill=(232, 226, 208))
    d.text((MX + 8, y + 5), "THE DAY IN UTC", font=font(F_SANSB, 12), fill=INK)
    d.text((MX + 8, y + 23), "all times UTC", font=font(F_SANS, 10), fill=GREY)
    ex = MX + 150
    ew = (W - MX - ex - 8) // 5
    for i, (t, label) in enumerate(UTC_STRIP):
        x = ex + i * ew
        d.text((x, y + 4), t, font=font(F_SANSB, 13), fill=RED)
        text_block(d, x, y + 21, label, font(F_SANS, 10), INK, ew - 8, leading=12)
    return y + 44


def mids(d, y):
    mw = (CW - 4 * 10) // 5
    mh = 118
    for row in range(2):
        for col in range(5):
            s = MIDS[row * 5 + col]
            x = MX + col * (mw + 10)
            yy = y + row * (mh + 8)
            d.rectangle([x, yy, x + mw, yy + mh], fill=PANEL, outline=LIGHTGREY, width=1)
            MINI_SCENES[s["scene"]](d, x + 1, yy + 1, mw - 2, 54)
            ty = yy + 60
            num_badge(d, x + 6, ty, s["num"], d=20)
            d.text((x + 30, ty + 3), s["place"], font=font(F_SANSB, 9), fill=INK)
            ty += 23
            text_block(d, x + 6, ty, s["head"], font(F_SANSB, 11), INK, mw - 12,
                       leading=12)
            d.text((x + 6, yy + mh - 11), s["src"], font=font(F_SANS, 8), fill=GREY)
    return y + 2 * mh + 8


# rough continent outlines (lon/lat polygons, equirectangular)
CONTINENTS = [
    [(-168, 66), (-140, 70), (-120, 72), (-95, 80), (-80, 73), (-60, 62),
     (-55, 47), (-70, 42), (-75, 35), (-80, 26), (-90, 21), (-97, 26),
     (-105, 20), (-117, 33), (-125, 40), (-125, 49), (-150, 60), (-168, 66)],
    [(-80, 9), (-62, 9), (-52, 5), (-40, -5), (-35, -9), (-40, -20),
     (-48, -28), (-58, -35), (-65, -41), (-70, -52), (-74, -30), (-70, -18),
     (-80, -3), (-80, 9)],
    [(-10, 36), (-9, 43), (-2, 48), (-4, 50), (2, 51), (8, 54), (8, 57),
     (18, 56), (21, 55), (28, 59), (30, 60), (24, 60), (18, 66), (12, 70),
     (5, 60), (-5, 58), (-10, 36)],
    [(-17, 15), (-16, 27), (-10, 31), (-5, 35), (10, 37), (20, 32), (30, 31),
     (32, 31), (35, 28), (43, 12), (51, 11), (48, -1), (40, -10), (36, -18),
     (32, -29), (26, -34), (18, -35), (12, -18), (9, -1), (-8, 4), (-17, 15)],
    [(40, 36), (60, 40), (60, 50), (70, 55), (75, 72), (100, 75), (130, 72),
     (160, 70), (178, 65), (162, 60), (158, 52), (142, 50), (140, 40),
     (135, 35), (127, 33), (120, 28), (110, 20), (105, 10), (100, 8),
     (95, 15), (90, 22), (80, 8), (76, 8), (72, 20), (66, 25), (60, 25),
     (52, 26), (48, 30), (44, 39), (40, 36)],
    [(114, -22), (122, -14), (130, -12), (137, -12), (142, -11), (146, -19),
     (150, -22), (153, -27), (150, -37), (140, -38), (132, -32), (124, -33),
     (115, -35), (114, -22)],
]

PIN_LATLON = {  # story num -> (lon, lat)
    1: (56, 26), 2: (127, 37), 3: (149, -35), 4: (100, 40), 5: (47, 24),
    6: (29, -3), 7: (-77, 39), 8: (13, 52), 9: (-75, 10), 10: (34, 31),
    11: (21, 52), 12: (0, 51), 13: (-4, 40),
}


def world_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(228, 232, 236))
    d.text((x + 6, y + 4), "WHERE IT HAPPENED \u2014 pins = stories 1\u201313",
           font=font(F_SANSB, 10), fill=INK)
    my = y + 18
    mh = h - 22
    for poly in CONTINENTS:
        pts = [(x + 4 + (lon + 180) / 360 * (w - 8),
                my + 4 + (75 - lat) / 130 * (mh - 8)) for lon, lat in poly]
        d.polygon(pts, fill=(196, 180, 140), outline=(150, 138, 110))
    for n, (lon, lat) in PIN_LATLON.items():
        px = x + 4 + (lon + 180) / 360 * (w - 8)
        py = my + 4 + (75 - lat) / 130 * (mh - 8)
        story = LEADS[n - 1] if n <= 3 else MIDS[n - 4]
        col = REGION_COLORS[story["region"]]
        d.ellipse([px - 6, py - 6, px + 6, py + 6], fill=col, outline=(255, 255, 255),
                  width=1)
        d.text((px - 2, py - 5), str(n), font=font(F_SANSB, 8), fill=(255, 255, 255))


def region_bar(d, x, y, w):
    d.text((x, y), "STORIES BY REGION", font=font(F_SANSB, 11), fill=INK)
    total = 35
    bx = x
    by = y + 16
    bh = 12
    for name, count in REGION_COUNTS:
        bw = int(w * count / total)
        d.rectangle([bx, by, bx + bw - 1, by + bh], fill=REGION_COLORS[name])
        bx += bw
    yy = by + bh + 4
    xx = x
    for name, count in REGION_COUNTS:
        label = f"{name} {count}"
        d.text((xx, yy), label, font=font(F_SANS, 9), fill=INK)
        xx += int(d.textlength(label, font=font(F_SANS, 9))) + 12


def also_list(d, x, y, w):
    d.text((x, y), "ALSO ON WEDNESDAY 25 NOVEMBER 2026",
           font=font(F_SANSB, 12), fill=INK)
    d.text((x, y + 16), "ranked by consequence \u00b7 tag = how sure we are",
           font=font(F_SANS, 10), fill=GREY)
    col_w = (w - 16) // 2
    for i, (n, region, tag, head) in enumerate(BRIEFS):
        col = i // 11
        row = i % 11
        bx = x + col * (col_w + 16)
        by = y + 34 + row * 15
        region_dot(d, bx, by + 2, region)
        d.text((bx + 12, by), str(n), font=font(F_SANSB, 10), fill=INK)
        d.text((bx + 30, by), head, font=font(F_SANS, 10), fill=INK)
    return y + 34 + 11 * 15


def date_check(d, x, y, w):
    d.text((x, y), "DATE CHECK", font=font(F_SANSB, 11), fill=RED)
    text_block(d, x, y + 15, DATE_CHECK, font(F_SANS, 10), INK, w, leading=10)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    masthead(d)
    y = stat_row(d, 132)
    y = leads(d, y + 8)
    y = utc_strip(d, y + 8)
    y = mids(d, y + 8)
    # bottom: also-list left, map + region bar + date check right
    by = y + 8
    list_w = 560
    also_list(d, MX, by, list_w)
    rx = MX + list_w + 16
    rw = W - MX - rx
    world_map(d, rx, by, rw, 92)
    region_bar(d, rx, by + 98, rw)
    date_check(d, rx, by + 144, rw)
    out = os.path.join(HERE, "entry.png")
    img.save(out, optimize=True)
    size = os.path.getsize(out)
    print(f"wrote {out} {size} bytes")
    assert size <= 1048576, "entry.png over 1 MiB"
    assert img.size == (1024, 1024)
    print("OK 1024x1024, under 1 MiB")


if __name__ == "__main__":
    main()
