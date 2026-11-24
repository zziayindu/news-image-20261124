#!/usr/bin/env python3
"""Sum up 24 November 2026 world news in one image.

Deterministic, no network. Writes /output/entry.png (1024x1024, <1 MiB).
Run twice -> identical bytes. All 37 stories first reported on
Tuesday 24 November 2026 in some time zone; 22-23 Nov stories are
listed only in the DATE CHECK exclusion footer.
"""
import os
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
OUT = Path(os.environ.get("OUTPUT_PATH", "/output/entry.png"))

BG = (247, 243, 232)      # cream paper
PAPER = (255, 253, 246)
INK = (24, 28, 34)
MUTED = (88, 94, 102)
FAINT = (120, 126, 134)
RED = (178, 34, 34)
NAVY = (15, 42, 68)
NAVY2 = (27, 68, 102)
TEAL = (14, 116, 110)
GOLD = (201, 162, 39)
CARD = (255, 255, 255)
LINE = (214, 206, 188)
BAND = (238, 232, 214)


def font(size, bold=False, serif=False):
    base = "/usr/share/fonts/truetype/dejavu/"
    name = ("DejaVuSerif" if serif else "DejaVuSans") + ("-Bold" if bold else "") + ".ttf"
    try:
        return ImageFont.truetype(base + name, size)
    except Exception:
        return ImageFont.load_default()


def wrap(draw, text, fnt, max_w):
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(d, x, y, text, fnt, max_w, fill, leading, max_lines=None):
    yy = y
    lines = wrap(d, text, fnt, max_w)
    if max_lines is not None:
        lines = lines[:max_lines]
    for ln in lines:
        d.text((x, yy), ln, font=fnt, fill=fill)
        yy += leading
    return yy


def tag_chip(d, x, y, label, bg):
    w = d.textlength(label, font=font(11, True)) + 14
    d.rounded_rectangle([x, y, x + w, y + 18], radius=9, fill=bg)
    d.text((x + 7, y + 3), label, font=font(11, True), fill=(255, 255, 255))
    return x + w


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # ---------- Masthead ----------
    d.text((36, 14), "THE WORLD ON ONE PAGE", font=font(15, True), fill=RED)
    d.text((36, 34), "Tuesday 24 November 2026", font=font(44, True, serif=True), fill=INK)
    d.text((36, 88), "37 STORIES  \u2022  7 CONTINENTS  \u2022  9 FIELDS  \u2022  ALL FROM THIS TUESDAY",
           font=font(14, True), fill=MUTED)
    d.rectangle([36, 112, 988, 114], fill=LINE)

    # ---------- THE DAY IN UTC ----------
    d.text((36, 122), "THE DAY IN UTC", font=font(13, True), fill=RED)
    timeline = [
        ("OVERNIGHT", "Nvidia board reverses course"),
        ("04:58 IST", "N. Korea aircraft near Ulleung"),
        ("MORNING", "Pakistan quake, magnitude 4.1"),
        ("08:41 IST", "Trump halts Iowa detonation"),
        ("MIDDAY", "Zanzibar hotels burn, 180 out"),
        ("AFTERNOON", "2031 World Cup hosts named"),
        ("EVENING", "States sue Musk over Grok"),
    ]
    tx = 36
    for i, (t, ev) in enumerate(timeline):
        d.ellipse([tx + 2, 146, tx + 10, 154], fill=RED if i == 0 else NAVY2)
        d.text((tx, 158), t, font=font(10, True), fill=NAVY2)
        text_block(d, tx, 172, ev, font(11), 128, MUTED, 13)
        tx += 138
    d.rectangle([36, 214, 988, 216], fill=LINE)

    # ---------- THE DAY IN NUMBERS ----------
    d.text((36, 224), "THE DAY IN NUMBERS", font=font(13, True), fill=RED)
    numbers = [
        ("810,592", "Honda cars recalled\nover Takata airbags"),
        ("180", "tourists evacuated\nfrom Zanzibar hotels"),
        ("4.1", "magnitude of the\nPakistan earthquake"),
        ("$2.4bn", "US defence offer\nto the Philippines"),
        ("$30bn", "sought to rebuild\nthe FAA after chaos"),
        ("500,000", "Russian war dead in\nnew hacked data"),
    ]
    nx = 36
    for num, lab in numbers:
        d.text((nx, 244), num, font=font(24, True, serif=True), fill=INK)
        yy = 274
        for ln in lab.split("\n"):
            d.text((nx, yy), ln, font=font(11), fill=MUTED)
            yy += 14
        nx += 160
    d.rectangle([36, 308, 988, 310], fill=LINE)

    # ---------- 3 heroes ----------
    heroes = [
        ("1", "TECH  \u2022  USA", RED, "Nvidia brings back\nJensen Huang",
         "Trump pushed, Vance lobbied the board \u2014 and the ousted chief is CEO again.",
         "CONFIRMED", "chip"),
        ("2", "ASIA  \u2022  KOREA", NAVY2, "Two intrusions in\nKorea's skies",
         "A suspected N. Korean aircraft nears Ulleung; Russian jets enter the air zone too.",
         "CONFIRMED", "plane"),
        ("3", "SPACE  \u2022  EUROPE", TEAL, "NATO warns of a\nRussian space weapon",
         "Allies say Moscow may launch a nuclear anti-satellite weapon next month.",
         "REPORTED", "sat"),
    ]
    hx, hw, hh = 36, 304, 176
    for i, (num, tag, col, title, body, src, kind) in enumerate(heroes):
        x = hx + i * (hw + 20)
        y = 322
        d.rounded_rectangle([x, y, x + hw, y + hh], radius=12, fill=CARD, outline=LINE, width=2)
        d.rectangle([x, y, x + hw, y + 6], fill=col)
        d.ellipse([x + 16, y + 20, x + 48, y + 52], fill=col)
        d.text((x + 32, y + 36), num, font=font(20, True), fill=(255, 255, 255), anchor="mm")
        d.text((x + 60, y + 24), tag, font=font(12, True), fill=col)
        yy = y + 58
        for ln in title.split("\n"):
            d.text((x + 16, yy), ln, font=font(21, True, serif=True), fill=INK)
            yy += 26
        yy += 2
        yy = text_block(d, x + 16, yy, body, font(13), hw - 32, MUTED, 16, max_lines=2)
        tag_chip(d, x + 16, y + hh - 28, src, col)

    # ---------- 10 mid cards: 5 cols x 2 rows ----------
    mids = [
        ("4", "USA", RED, "Trump halts Iowa blast", "Army told to stop detonating old explosives.", "OFFICIALS"),
        ("5", "USA", RED, "Executions to speed up", "Trump orders federal executions expedited.", "OFFICIALS"),
        ("6", "USA", NAVY2, "Gomez quits Congress", "Resigns after ethics panel finds misconduct.", "CONFIRMED"),
        ("7", "AFRICA", TEAL, "Six hotels burn, Zanzibar", "Fire engulfs six hotels; 180 tourists out.", "CONFIRMED"),
        ("8", "USA", NAVY2, "Amtrak derails in Louisiana", "Train hits a truck; 95 aboard, five hurt.", "CONFIRMED"),
        ("9", "USA", (120, 60, 20), "Honda recalls 810,592 cars", "Takata airbags may rupture, hurling metal.", "CONFIRMED"),
        ("10", "SPORT", (90, 40, 110), "2031 Women's World Cup", "USA, Mexico, Costa Rica, Jamaica host; UK 2035.", "CONFIRMED"),
        ("11", "ASIA", TEAL, "Pakistan quake 4.1", "Morning tremor shakes the country.", "CONFIRMED"),
        ("12", "MIDEAST", (120, 60, 20), "Iran: tankers hit mines", "Tehran says three tankers struck naval mines.", "REPORTED"),
        ("13", "TECH", (90, 40, 110), "States sue Musk over Grok", "States say the chatbot made sexualised images.", "REPORTED"),
    ]
    cw, chh, gap = 184, 108, 20
    for i, (num, tag, col, title, body, src) in enumerate(mids):
        x = 36 + (i % 5) * (cw + gap)
        y = 506 + (i // 5) * (chh + 12)
        d.rounded_rectangle([x, y, x + cw, y + chh], radius=10, fill=CARD, outline=LINE, width=1)
        d.text((x + 10, y + 8), num + "  " + tag, font=font(11, True), fill=col)
        yy = text_block(d, x + 10, y + 26, title, font(13, True), cw - 20, INK, 16, max_lines=2)
        text_block(d, x + 10, yy + 2, body, font(11), cw - 20, MUTED, 13, max_lines=2)
        d.text((x + 10, y + chh - 16), src, font=font(9, True), fill=FAINT)

    # ---------- Bottom: map (left) + ALSO ON (right) ----------
    d.rectangle([36, 748, 988, 750], fill=LINE)
    d.text((36, 758), "WHERE IT HAPPENED", font=font(13, True), fill=RED)
    # Simple stylised world map: continents as soft shapes
    mx, my = 36, 786
    d.rounded_rectangle([mx, my, mx + 330, my + 150], radius=10, fill=PAPER, outline=LINE, width=1)
    # North America
    d.ellipse([mx + 18, my + 18, mx + 92, my + 62], fill=(196, 214, 196))
    # South America
    d.ellipse([mx + 62, my + 78, mx + 108, my + 128], fill=(196, 214, 196))
    # Europe
    d.ellipse([mx + 158, my + 22, mx + 196, my + 52], fill=(196, 214, 196))
    # Africa
    d.ellipse([mx + 158, my + 62, mx + 202, my + 112], fill=(196, 214, 196))
    # Asia
    d.ellipse([mx + 206, my + 16, mx + 312, my + 66], fill=(196, 214, 196))
    # Oceania
    d.ellipse([mx + 282, my + 96, mx + 316, my + 120], fill=(196, 214, 196))
    dots = [(52, 40, "1"), (240, 40, "2"), (176, 36, "3"), (70, 60, "5"),
            (180, 86, "7"), (64, 100, "8"), (84, 44, "9"), (258, 44, "11"),
            (218, 62, "12"), (246, 108, "14")]
    for dx, dy, n in dots:
        d.ellipse([mx + dx - 7, my + dy - 7, mx + dx + 7, my + dy + 7], fill=RED, outline=(255, 255, 255), width=1)
        d.text((mx + dx, my + dy), n, font=font(8, True), fill=(255, 255, 255), anchor="mm")
    d.text((mx, my + 156), "Europe 8  \u2022  Asia 9  \u2022  Americas 7  \u2022  Africa 5  \u2022  Mideast 3",
           font=font(10, True), fill=MUTED)

    # ALSO ON 14-37
    ax = 392
    d.text((ax, 758), "ALSO ON TUESDAY  \u2014  14 TO 37", font=font(13, True), fill=RED)
    also = [
        ("14", "Russia hits drone sites, Starlink in Sumy"),
        ("15", "Hacked data: Russian war dead near 500,000"),
        ("16", "Moscow: Estonia near 'open war'"),
        ("17", "N. Korea threatens to shut Swiss office"),
        ("18", "China: death sentence for spying official"),
        ("19", "WHO chief in Cuba as health system fails"),
        ("20", "UN chief wants AI risk rules in a year"),
        ("21", "Trump offers Philippines $2.4bn defence"),
        ("22", "Indonesia charges ex-police chief, treason"),
        ("23", "Hasina seeks return to Bangladesh"),
        ("24", "Nepal PM in India for talks"),
        ("25", "Drones hit homes, UN building in Sudan"),
        ("26", "Thousands protest Turkey media closures"),
        ("27", "Macron eyes curbs on spending"),
        ("28", "UK: GTA VI hacker gets 7 years"),
        ("29", "UK concert evacuated, unknown substance"),
        ("30", "Aviation groups seek $30bn for FAA"),
        ("31", "IDB eyes $6bn loans for Venezuela"),
        ("32", "India-EU trade pact likely signed Dec 16"),
        ("33", "Storms threaten Thanksgiving travel"),
        ("34", "Canada PM brings Trump lookalike on stage"),
        ("35", "Ms Rachel protests child migrant hearings"),
        ("36", "India-Nepal Saryu-Kamala Express opens"),
        ("37", "Pant hits 128 in Wellington Test"),
    ]
    col_w = 300
    for i, (num, line) in enumerate(also):
        cx = ax + (i // 12) * col_w
        cy = 784 + (i % 12) * 14
        d.text((cx, cy), num, font=font(11, True), fill=RED)
        d.text((cx + 26, cy), line, font=font(11), fill=INK)

    # ---------- DATE CHECK footer ----------
    d.rectangle([36, 956, 988, 958], fill=LINE)
    d.text((36, 964), "DATE CHECK \u2014 NOT THIS TUESDAY, SO LEFT OUT:", font=font(11, True), fill=RED)
    d.text((36, 980),
           "COP31 collapse (22\u201323 Nov)  \u2022  Democrats' 258 House seats (23 Nov)  \u2022  Warship sunk off Libya (22 Nov)",
           font=font(11), fill=MUTED)
    d.text((36, 996),
           "Kyiv-region strike, Dymer (22\u201323 Nov)  \u2022  Indonesia factory fire, 24 dead (22 Nov)  \u2022  'El Chapo Isidro' caught (22 Nov)",
           font=font(11), fill=MUTED)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    img.save(OUT, format="PNG", compress_level=9, optimize=True)


if __name__ == "__main__":
    main()
