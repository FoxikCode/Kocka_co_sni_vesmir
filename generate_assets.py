"""
Generátor textur pro hru "Kočka co sní vesmír"
Tento skript vytvoří všechny potřebné PNG textury pomocí knihovny Pillow.
Spusťte tento skript před spuštěním hry: python generate_assets.py
"""

import os
import math
import random
from PIL import Image, ImageDraw, ImageFilter

# Vytvoření složky assets, pokud neexistuje
os.makedirs("assets", exist_ok=True)


def vytvor_pozadi(sirka=1024, vyska=768):
    """Vytvoří vesmírné pozadí s hvězdičkami."""
    img = Image.new("RGBA", (sirka, vyska), (5, 5, 20, 255))
    draw = ImageDraw.Draw(img)

    # Nakreslení náhodných hvězdiček na pozadí
    random.seed(42)
    for _ in range(300):
        x = random.randint(0, sirka - 1)
        y = random.randint(0, vyska - 1)
        jas = random.randint(150, 255)
        velikost = random.choice([1, 1, 1, 2])
        draw.ellipse([x, y, x + velikost, y + velikost], fill=(jas, jas, jas, 255))

    # Přidání barevných mlhovin
    for _ in range(5):
        x = random.randint(0, sirka)
        y = random.randint(0, vyska)
        r = random.randint(60, 150)
        barva = random.choice([
            (30, 0, 60, 40),
            (0, 20, 60, 40),
            (60, 0, 30, 30),
        ])
        mlhovina = Image.new("RGBA", (sirka, vyska), (0, 0, 0, 0))
        d = ImageDraw.Draw(mlhovina)
        d.ellipse([x - r, y - r, x + r, y + r], fill=barva)
        mlhovina = mlhovina.filter(ImageFilter.GaussianBlur(radius=40))
        img = Image.alpha_composite(img, mlhovina)

    img.save("assets/background.png")
    print("✓ background.png vygenerován")


def vytvor_kocku(velikost=64):
    """Vytvoří pixel art kočku."""
    img = Image.new("RGBA", (velikost, velikost), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Měřítko pixelů
    px = velikost // 16

    def pixel(x, y, barva):
        draw.rectangle([x * px, y * px, (x + 1) * px - 1, (y + 1) * px - 1], fill=barva)

    # Tělo kočky - oranžová
    telo = (220, 120, 40, 255)
    svetle = (240, 160, 80, 255)
    tmave = (180, 90, 20, 255)
    bila = (255, 255, 255, 255)
    ruzova = (255, 180, 180, 255)
    modra = (100, 180, 255, 255)
    cerna = (30, 20, 20, 255)

    # Uši
    pixel(3, 1, telo)
    pixel(4, 0, telo)
    pixel(5, 0, telo)
    pixel(4, 1, telo)
    pixel(10, 0, telo)
    pixel(11, 0, telo)
    pixel(11, 1, telo)
    pixel(10, 1, telo)
    # Vnitřek uší
    pixel(4, 0, ruzova)
    pixel(11, 0, ruzova)

    # Hlava
    for x in range(3, 13):
        for y in range(2, 9):
            pixel(x, y, telo)

    # Obličej - oči
    pixel(5, 4, modra)
    pixel(6, 4, modra)
    pixel(5, 5, modra)
    pixel(6, 5, modra)
    pixel(5, 4, cerna)
    pixel(6, 5, cerna)
    pixel(9, 4, modra)
    pixel(10, 4, modra)
    pixel(9, 5, modra)
    pixel(10, 5, modra)
    pixel(10, 4, cerna)
    pixel(9, 5, cerna)

    # Nos
    pixel(7, 6, ruzova)
    pixel(8, 6, ruzova)

    # Ústa
    pixel(6, 7, cerna)
    pixel(9, 7, cerna)
    pixel(7, 8, cerna)
    pixel(8, 8, cerna)

    # Vousy
    for x in range(0, 4):
        pixel(x, 6, (200, 200, 200, 200))
    for x in range(12, 16):
        pixel(x, 6, (200, 200, 200, 200))

    # Tělo
    for x in range(4, 12):
        for y in range(9, 14):
            pixel(x, y, telo)

    # Břicho (světlejší)
    for x in range(6, 10):
        for y in range(10, 13):
            pixel(x, y, svetle)

    # Přední tlapky
    pixel(4, 13, telo)
    pixel(4, 14, telo)
    pixel(5, 14, telo)
    pixel(5, 15, bila)
    pixel(4, 15, bila)
    pixel(11, 13, telo)
    pixel(11, 14, telo)
    pixel(10, 14, telo)
    pixel(10, 15, bila)
    pixel(11, 15, bila)

    # Zadní tlapky
    pixel(5, 13, telo)
    pixel(6, 13, tmave)
    pixel(9, 13, tmave)
    pixel(10, 13, telo)

    # Ocas
    pixel(12, 11, telo)
    pixel(13, 10, telo)
    pixel(14, 9, telo)
    pixel(15, 8, telo)
    pixel(15, 7, tmave)
    pixel(14, 8, tmave)

    # Hvězdičky/vesmírný vzor na těle
    pixel(7, 10, (255, 255, 100, 200))
    pixel(8, 11, (100, 200, 255, 200))

    img.save("assets/cat.png")
    print("✓ cat.png vygenerován")


def vytvor_hvezdu(velikost=32):
    """Vytvoří žlutou hvězdu."""
    img = Image.new("RGBA", (velikost, velikost), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    cx, cy = velikost // 2, velikost // 2
    r_vnejsi = velikost // 2 - 2
    r_vnitrni = r_vnejsi // 2

    # Pěticípá hvězda
    body = []
    for i in range(10):
        uhel = math.pi * i / 5 - math.pi / 2
        if i % 2 == 0:
            r = r_vnejsi
        else:
            r = r_vnitrni
        x = cx + r * math.cos(uhel)
        y = cy + r * math.sin(uhel)
        body.append((x, y))

    # Záře kolem hvězdy
    glow = Image.new("RGBA", (velikost, velikost), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.polygon(body, fill=(255, 255, 100, 80))
    glow = glow.filter(ImageFilter.GaussianBlur(radius=3))
    img = Image.alpha_composite(img, glow)

    draw = ImageDraw.Draw(img)
    draw.polygon(body, fill=(255, 220, 0, 255), outline=(255, 255, 150, 255))

    # Střed hvězdy
    draw.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=(255, 255, 200, 255))

    img.save("assets/star.png")
    print("✓ star.png vygenerován")


def vytvor_asteroid(velikost=48):
    """Vytvoří šedohnědý asteroid s nepravidelným tvarem."""
    img = Image.new("RGBA", (velikost, velikost), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    cx, cy = velikost // 2, velikost // 2
    r_zaklad = velikost // 2 - 3

    # Nepravidelný tvar asteroidu
    random.seed(7)
    body = []
    pocet_bodu = 12
    for i in range(pocet_bodu):
        uhel = 2 * math.pi * i / pocet_bodu
        odchylka = random.uniform(0.6, 1.0)
        r = r_zaklad * odchylka
        x = cx + r * math.cos(uhel)
        y = cy + r * math.sin(uhel)
        body.append((x, y))

    # Stín asteroidu
    shadow = Image.new("RGBA", (velikost, velikost), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    posun_body = [(x + 2, y + 2) for x, y in body]
    sd.polygon(posun_body, fill=(0, 0, 0, 80))
    shadow = shadow.filter(ImageFilter.GaussianBlur(radius=2))
    img = Image.alpha_composite(img, shadow)

    draw = ImageDraw.Draw(img)
    # Základní tvar
    draw.polygon(body, fill=(100, 85, 70, 255), outline=(60, 50, 40, 255))

    # Textura - světlejší plochy
    for _ in range(8):
        x = random.randint(cx - r_zaklad + 5, cx + r_zaklad - 5)
        y = random.randint(cy - r_zaklad + 5, cy + r_zaklad - 5)
        r = random.randint(2, 5)
        draw.ellipse([x - r, y - r, x + r, y + r], fill=(130, 115, 95, 180))

    # Krátery
    for _ in range(3):
        x = random.randint(cx - r_zaklad // 2, cx + r_zaklad // 2)
        y = random.randint(cy - r_zaklad // 2, cy + r_zaklad // 2)
        r = random.randint(2, 4)
        draw.ellipse([x - r, y - r, x + r, y + r], fill=(70, 60, 50, 255))

    img.save("assets/asteroid.png")
    print("✓ asteroid.png vygenerován")


def vytvor_mesic(velikost=56):
    """Vytvoří šedý měsíc s krátery."""
    img = Image.new("RGBA", (velikost, velikost), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    cx, cy = velikost // 2, velikost // 2
    r = velikost // 2 - 2

    # Záře
    glow = Image.new("RGBA", (velikost, velikost), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse([cx - r - 3, cy - r - 3, cx + r + 3, cy + r + 3], fill=(200, 200, 180, 40))
    glow = glow.filter(ImageFilter.GaussianBlur(radius=4))
    img = Image.alpha_composite(img, glow)

    draw = ImageDraw.Draw(img)
    # Základní kruh
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(180, 180, 170, 255), outline=(150, 150, 140, 255))

    # Osvětlená strana
    draw.ellipse([cx - r + 2, cy - r + 2, cx + r - 4, cy + r - 4], fill=(200, 200, 190, 255))

    # Stín na pravé straně
    stinova = Image.new("RGBA", (velikost, velikost), (0, 0, 0, 0))
    sd = ImageDraw.Draw(stinova)
    sd.ellipse([cx, cy - r, cx + r + 5, cy + r], fill=(100, 100, 95, 120))
    stinova = stinova.filter(ImageFilter.GaussianBlur(radius=5))
    img = Image.alpha_composite(img, stinova)

    draw = ImageDraw.Draw(img)
    # Krátery
    random.seed(13)
    kratery = [
        (cx - 8, cy - 5, 5),
        (cx + 5, cy + 8, 4),
        (cx - 3, cy + 10, 3),
        (cx + 10, cy - 8, 3),
        (cx - 12, cy + 5, 2),
    ]
    for kx, ky, kr in kratery:
        draw.ellipse([kx - kr, ky - kr, kx + kr, ky + kr], fill=(150, 148, 140, 255), outline=(120, 118, 110, 255))
        draw.ellipse([kx - kr + 1, ky - kr + 1, kx + kr - 1, ky + kr - 1], fill=(170, 168, 160, 255))

    img.save("assets/moon.png")
    print("✓ moon.png vygenerován")


def vytvor_planetu(velikost=72):
    """Vytvoří barevnou planetu s prstenci."""
    img = Image.new("RGBA", (velikost, velikost), (0, 0, 0, 0))

    cx, cy = velikost // 2, velikost // 2
    r = velikost // 2 - 8

    # Záře planety
    glow = Image.new("RGBA", (velikost, velikost), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse([cx - r - 5, cy - r - 5, cx + r + 5, cy + r + 5], fill=(80, 120, 220, 50))
    glow = glow.filter(ImageFilter.GaussianBlur(radius=6))
    img = Image.alpha_composite(img, glow)

    draw = ImageDraw.Draw(img)

    # Prstence planety (za planetou)
    draw.ellipse([3, cy - 4, velikost - 3, cy + 4], fill=(150, 120, 80, 150), outline=(180, 150, 100, 200))

    # Základní kruh planety
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(70, 100, 200, 255))

    # Barevné pruhy atmosféry
    draw.arc([cx - r + 2, cy - r + 2, cx + r - 2, cy + r - 2], 180, 0, fill=(100, 150, 240, 200), width=4)
    draw.arc([cx - r + 6, cy - r + 6, cx + r - 6, cy + r - 6], 180, 0, fill=(140, 190, 255, 180), width=3)
    draw.arc([cx - r + 2, cy, cx + r - 2, cy + r - 2], 0, 180, fill=(50, 80, 180, 200), width=4)

    # Atmosférické mraky
    draw.ellipse([cx - 8, cy - 5, cx + 5, cy + 2], fill=(150, 180, 255, 120))
    draw.ellipse([cx + 3, cy + 3, cx + r - 3, cy + 8], fill=(100, 140, 230, 120))

    # Odlesk
    draw.ellipse([cx - r + 3, cy - r + 3, cx - 5, cy - 5], fill=(200, 220, 255, 80))

    # Prstence planety (před planetou - spodní část)
    draw.arc([3, cy - 4, velikost - 3, cy + 4], 0, 180, fill=(150, 120, 80, 180), width=3)

    img.save("assets/planet.png")
    print("✓ planet.png vygenerován")


def vytvor_slunce(velikost=96):
    """Vytvoří žluto-oranžové slunce se září."""
    img = Image.new("RGBA", (velikost, velikost), (0, 0, 0, 0))

    cx, cy = velikost // 2, velikost // 2
    r = velikost // 2 - 10

    # Velká záře slunce
    for i in range(5, 0, -1):
        glow = Image.new("RGBA", (velikost, velikost), (0, 0, 0, 0))
        gd = ImageDraw.Draw(glow)
        rg = r + i * 6
        alpha = 30 - i * 4
        gd.ellipse([cx - rg, cy - rg, cx + rg, cy + rg], fill=(255, 200, 50, alpha))
        glow = glow.filter(ImageFilter.GaussianBlur(radius=i * 3))
        img = Image.alpha_composite(img, glow)

    draw = ImageDraw.Draw(img)

    # Paprsky slunce
    for i in range(12):
        uhel = 2 * math.pi * i / 12
        x1 = cx + (r + 3) * math.cos(uhel)
        y1 = cy + (r + 3) * math.sin(uhel)
        x2 = cx + (r + 12) * math.cos(uhel)
        y2 = cy + (r + 12) * math.sin(uhel)
        draw.line([x1, y1, x2, y2], fill=(255, 220, 50, 200), width=3)

    # Kratší paprsky
    for i in range(12):
        uhel = 2 * math.pi * i / 12 + math.pi / 12
        x1 = cx + (r + 2) * math.cos(uhel)
        y1 = cy + (r + 2) * math.sin(uhel)
        x2 = cx + (r + 7) * math.cos(uhel)
        y2 = cy + (r + 7) * math.sin(uhel)
        draw.line([x1, y1, x2, y2], fill=(255, 180, 30, 160), width=2)

    # Základní kruh slunce
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 160, 20, 255))

    # Přechod barvy
    for i in range(r, 0, -3):
        t = i / r
        cervena = int(255)
        zelena = int(120 + 80 * t)
        modra = int(10 * (1 - t))
        alpha = int(200 * (1 - (i / r) ** 2))
        draw.ellipse([cx - i, cy - i, cx + i, cy + i], fill=(cervena, zelena, modra, alpha))

    # Střed - nejsvětlejší
    draw.ellipse([cx - r // 3, cy - r // 3, cx + r // 3, cy + r // 3], fill=(255, 240, 180, 200))

    # Sluneční skvrny
    draw.ellipse([cx - 8, cy + 5, cx - 2, cy + 9], fill=(200, 100, 10, 180))
    draw.ellipse([cx + 5, cy - 8, cx + 10, cy - 4], fill=(200, 100, 10, 150))

    img.save("assets/sun.png")
    print("✓ sun.png vygenerován")


def vytvor_galaxii(velikost=128):
    """Vytvoří spirální galaxii ve fialovo-modré barvě."""
    img = Image.new("RGBA", (velikost, velikost), (0, 0, 0, 0))

    cx, cy = velikost // 2, velikost // 2

    # Záře galaxie
    glow = Image.new("RGBA", (velikost, velikost), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse([cx - 50, cy - 50, cx + 50, cy + 50], fill=(100, 50, 180, 60))
    glow = glow.filter(ImageFilter.GaussianBlur(radius=20))
    img = Image.alpha_composite(img, glow)

    # Spirální ramena galaxie
    draw = ImageDraw.Draw(img)
    random.seed(99)

    # Nakreslení hvězd ve spirálních ramenech
    for arm in range(3):
        uhel_offset = arm * 2 * math.pi / 3
        for i in range(200):
            t = i / 200
            uhel = t * 4 * math.pi + uhel_offset
            r = t * (velikost // 2 - 5)
            rozsyp = random.gauss(0, r * 0.15 + 2)

            x = cx + int((r + rozsyp) * math.cos(uhel))
            y = cy + int((r + rozsyp) * math.sin(uhel) * 0.5)  # zploštění

            if 0 <= x < velikost and 0 <= y < velikost:
                jas = int(200 * (1 - t * 0.5))
                modra = min(255, jas + 50)
                fialova = min(255, jas + 30)
                alpha = int(220 * (1 - t * 0.3))
                velikost_hvezdy = max(1, int(3 * (1 - t * 0.7)))
                draw.ellipse(
                    [x - velikost_hvezdy, y - velikost_hvezdy, x + velikost_hvezdy, y + velikost_hvezdy],
                    fill=(fialova, jas // 2, modra, alpha)
                )

    # Centrální jádro galaxie
    jadro = Image.new("RGBA", (velikost, velikost), (0, 0, 0, 0))
    jd = ImageDraw.Draw(jadro)
    jd.ellipse([cx - 15, cy - 8, cx + 15, cy + 8], fill=(255, 240, 200, 200))
    jadro = jadro.filter(ImageFilter.GaussianBlur(radius=5))
    img = Image.alpha_composite(img, jadro)

    draw = ImageDraw.Draw(img)
    draw.ellipse([cx - 5, cy - 3, cx + 5, cy + 3], fill=(255, 255, 230, 255))

    img.save("assets/galaxy.png")
    print("✓ galaxy.png vygenerován")



# ── Nová pozadí ────────────────────────────────────────────────────────────────

def vytvor_pozadi_laborator(sirka=1024, vyska=768):
    """Vytvoří pozadí laboratoře s dlaždicemi a vybavením."""
    rng = random.Random(77)
    img = Image.new("RGBA", (sirka, vyska), (190, 200, 190, 255))
    draw = ImageDraw.Draw(img)

    # Dlaždice podlahy
    tile = 80
    for gy in range(0, vyska, tile):
        for gx in range(0, sirka, tile):
            c = (200, 210, 200) if (gx // tile + gy // tile) % 2 == 0 else (185, 196, 185)
            draw.rectangle([gx, gy, gx + tile - 1, gy + tile - 1], fill=c)

    # Mřížka dlaždic
    for gx in range(0, sirka, tile):
        draw.line([(gx, 0), (gx, vyska)], fill=(165, 175, 165), width=1)
    for gy in range(0, vyska, tile):
        draw.line([(0, gy), (sirka, gy)], fill=(165, 175, 165), width=1)

    # Laboratorní stůl (horní část)
    draw.rectangle([0, 0, sirka, 110], fill=(130, 150, 135))
    draw.rectangle([0, 105, sirka, 115], fill=(100, 120, 105))

    # Erlenmeyerova baňka (vlevo)
    cx, cy = 160, 65
    draw.polygon([(cx - 12, cy + 35), (cx + 12, cy + 35),
                  (cx + 22, cy - 18), (cx - 22, cy - 18)],
                 fill=(120, 190, 170, 210), outline=(80, 140, 120))
    draw.rectangle([cx - 6, cy - 28, cx + 6, cy - 18], fill=(100, 120, 110))
    # Kapalina uvnitř baňky
    draw.polygon([(cx - 10, cy + 35), (cx + 10, cy + 35),
                  (cx + 14, cy + 10), (cx - 14, cy + 10)],
                 fill=(60, 200, 140, 180))

    # Zkumavky (vpravo nahoře)
    for i, col in enumerate([(180, 100, 100, 190), (100, 180, 100, 190), (100, 100, 210, 190)]):
        tx = 920 + i * 22
        draw.rounded_rectangle([tx - 5, 18, tx + 5, 80], radius=4, fill=col, outline=(80, 80, 80))
        draw.rectangle([tx - 3, 18, tx + 3, 30], fill=(80, 80, 80))

    # Mikroskop (uprostřed vpravo)
    mx, my = 700, 80
    draw.ellipse([mx - 28, my + 15, mx + 28, my + 28], fill=(60, 65, 75))
    draw.rectangle([mx - 6, my - 35, mx + 6, my + 22], fill=(60, 65, 75))
    draw.rectangle([mx + 6, my - 8, mx + 35, my - 2], fill=(60, 65, 75))
    draw.rectangle([mx + 28, my - 35, mx + 36, my - 6], fill=(60, 65, 75))
    draw.ellipse([mx + 22, my - 40, mx + 42, my - 34], fill=(55, 55, 65))
    draw.ellipse([mx + 25, my - 8, mx + 39, my - 1], fill=(180, 210, 190, 160))

    # Petriho misky (uprostřed stolu)
    for i in range(3):
        px, py = 430 + i * 70, 72
        draw.ellipse([px - 30, py - 12, px + 30, py + 12],
                     fill=(225, 240, 225, 200), outline=(160, 185, 160))
        draw.ellipse([px - 25, py - 8, px + 25, py + 8],
                     fill=(0, 0, 0, 0), outline=(160, 185, 160))

    img.save("assets/bg_lab.png")
    print("✓ bg_lab.png vygenerován")


def vytvor_pozadi_mesto(sirka=1024, vyska=768):
    """Vytvoří pozadí města s mrakodrapy a ulicemi."""
    rng = random.Random(55)
    img = Image.new("RGBA", (sirka, vyska), (120, 165, 220, 255))
    draw = ImageDraw.Draw(img)

    # Gradient oblohy
    for y in range(vyska // 2):
        t = y / (vyska // 2)
        r = int(120 + 40 * t)
        g = int(165 + 20 * t)
        b = int(220 - 10 * t)
        draw.line([(0, y), (sirka, y)], fill=(r, g, b))

    # Budovy v pozadí
    buildings = [
        (0,   350, 100, 700, (95, 100, 115)),
        (80,  230, 180, 700, (85,  90, 105)),
        (150, 380, 250, 700, (100, 105, 120)),
        (220, 160, 310, 700, (80,  85, 100)),
        (280, 320, 370, 700, (90,  95, 110)),
        (340, 270, 430, 700, (85,  90, 105)),
        (400, 420, 480, 700, (100, 105, 120)),
        (450, 110, 530, 700, (75,  80,  95)),
        (510, 340, 590, 700, (90,  95, 110)),
        (560, 200, 650, 700, (85,  90, 105)),
        (620, 360, 710, 700, (95, 100, 115)),
        (680, 190, 760, 700, (80,  85, 100)),
        (730, 310, 820, 700, (88,  93, 108)),
        (790, 420, 870, 700, (95, 100, 115)),
        (840, 140, 930, 700, (78,  83,  98)),
        (900, 290, 1024, 700, (85,  90, 105)),
    ]
    for x1, y1, x2, y2, col in buildings:
        draw.rectangle([x1, y1, x2, y2], fill=col)
        # Okna
        for wy in range(y1 + 15, y2 - 15, 22):
            for wx in range(x1 + 7, x2 - 7, 16):
                if rng.random() > 0.25:
                    wc = (255, 240, 170, 200) if rng.random() > 0.3 else (180, 200, 255, 160)
                    draw.rectangle([wx, wy, wx + 8, wy + 12], fill=wc)

    # Asfaltová silnice
    draw.rectangle([0, 695, sirka, 768], fill=(85, 80, 78))
    draw.rectangle([0, 692, sirka, 698], fill=(180, 170, 155))
    # Středové čáry
    for x in range(0, sirka, 100):
        draw.rectangle([x + 20, 727, x + 60, 737], fill=(210, 195, 90))

    img.save("assets/bg_city.png")
    print("✓ bg_city.png vygenerován")


# ── Laboratorní objekty ────────────────────────────────────────────────────────

def vytvor_bakterii(velikost=32):
    """Vytvoří bakterii – zelený ovál s bičíkem."""
    img = Image.new("RGBA", (velikost, velikost), (0, 0, 0, 0))
    cx, cy = velikost // 2, velikost // 2

    # Záře
    glow = Image.new("RGBA", (velikost, velikost), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse([cx - 10, cy - 7, cx + 10, cy + 7], fill=(80, 200, 60, 70))
    glow = glow.filter(ImageFilter.GaussianBlur(2))
    img = Image.alpha_composite(img, glow)

    draw = ImageDraw.Draw(img)
    # Tělo
    draw.ellipse([cx - 9, cy - 6, cx + 9, cy + 6], fill=(80, 200, 60, 230), outline=(50, 150, 35))
    # Jádro
    draw.ellipse([cx - 3, cy - 2, cx + 3, cy + 2], fill=(40, 140, 30, 220))
    # Bičík
    for i in range(10):
        t = i / 9.0
        bx = int(cx + 9 + t * 11)
        by = int(cy + math.sin(t * math.pi * 2.5) * 4)
        draw.ellipse([bx - 1, by - 1, bx + 1, by + 1], fill=(60, 170, 45, 200))

    img.save("assets/bacteria.png")
    print("✓ bacteria.png vygenerován")


def vytvor_bunku(velikost=32):
    """Vytvoří buňku – průsvitný kruh s jádrem."""
    img = Image.new("RGBA", (velikost, velikost), (0, 0, 0, 0))
    cx, cy = velikost // 2, velikost // 2
    r = velikost // 2 - 2

    # Cytoplazma (průsvitná)
    glow = Image.new("RGBA", (velikost, velikost), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(220, 180, 130, 80))
    glow = glow.filter(ImageFilter.GaussianBlur(2))
    img = Image.alpha_composite(img, glow)

    draw = ImageDraw.Draw(img)
    draw.ellipse([cx - r, cy - r, cx + r, cy + r],
                 fill=(230, 200, 155, 140), outline=(185, 145, 100, 210))
    # Jádro
    draw.ellipse([cx - 6, cy - 6, cx + 6, cy + 6],
                 fill=(190, 100, 80, 220), outline=(150, 70, 55))
    draw.ellipse([cx - 2, cy - 2, cx + 2, cy + 2], fill=(230, 155, 130, 255))

    img.save("assets/cell.png")
    print("✓ cell.png vygenerován")


def vytvor_mravence(velikost=48):
    """Vytvoří mravence – černé segmentované tělo se 6 nohami."""
    img = Image.new("RGBA", (velikost, velikost), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    cx, cy = velikost // 2 - 2, velikost // 2
    col = (35, 30, 25, 255)
    out = (15, 10, 5)

    # Tělo (3 segmenty: zadeček, hrudník, hlava)
    draw.ellipse([cx - 12, cy - 5, cx - 1,  cy + 5], fill=col, outline=out)
    draw.ellipse([cx - 3,  cy - 4, cx + 7,  cy + 4], fill=col, outline=out)
    draw.ellipse([cx + 5,  cy - 5, cx + 15, cy + 5], fill=col, outline=out)

    # Oči
    draw.ellipse([cx + 11, cy - 4, cx + 14, cy - 1], fill=(180, 50, 50))

    # Tykadla
    draw.line([(cx + 14, cy - 4), (cx + 20, cy - 11)], fill=(25, 20, 15), width=1)
    draw.line([(cx + 14, cy - 4), (cx + 21, cy - 7)],  fill=(25, 20, 15), width=1)

    # Nohy (3 páry) – každá noha je trojice bodů (x, y)
    legs = [
        ((cx + 2,  cy + 3),  (cx + 7,  cy + 13), (cx + 10, cy + 15)),
        ((cx + 2,  cy - 3),  (cx + 7,  cy - 13), (cx + 10, cy - 15)),
        ((cx - 4,  cy + 3),  (cx - 8,  cy + 12), (cx - 11, cy + 14)),
        ((cx - 4,  cy - 3),  (cx - 8,  cy - 12), (cx - 11, cy - 14)),
        ((cx - 9,  cy + 3),  (cx - 14, cy + 9),  (cx - 17, cy + 11)),
        ((cx - 9,  cy - 3),  (cx - 14, cy - 9),  (cx - 17, cy - 11)),
    ]
    for p1, p2, p3 in legs:
        draw.line([p1, p2], fill=(25, 20, 15), width=1)
        draw.line([p2, p3], fill=(25, 20, 15), width=1)

    img.save("assets/ant.png")
    print("✓ ant.png vygenerován")


def vytvor_mouchu(velikost=48):
    """Vytvoří mouchu – tmavé tělo s průsvitnými křídly."""
    img = Image.new("RGBA", (velikost, velikost), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    cx, cy = velikost // 2, velikost // 2

    # Křídla (průsvitná)
    draw.ellipse([cx - 18, cy - 20, cx + 1,  cy - 5],
                 fill=(210, 230, 255, 130), outline=(160, 180, 220, 160))
    draw.ellipse([cx - 1,  cy - 20, cx + 18, cy - 5],
                 fill=(210, 230, 255, 130), outline=(160, 180, 220, 160))

    # Hrudník
    draw.ellipse([cx - 8, cy - 4, cx + 8, cy + 6], fill=(45, 45, 38, 255))

    # Zadeček (s pruhy)
    draw.ellipse([cx - 10, cy + 3, cx + 2, cy + 15], fill=(40, 40, 32, 255))
    for stripe_y in range(cy + 5, cy + 14, 3):
        draw.line([(cx - 9, stripe_y), (cx + 1, stripe_y)], fill=(80, 80, 65, 200), width=1)

    # Hlava
    draw.ellipse([cx + 5, cy - 8, cx + 16, cy + 2], fill=(45, 45, 38, 255))
    # Složené oči
    draw.ellipse([cx + 6,  cy - 7, cx + 11, cy - 2], fill=(180, 50, 50, 220))
    draw.ellipse([cx + 11, cy - 7, cx + 16, cy - 2], fill=(180, 50, 50, 220))

    img.save("assets/fly.png")
    print("✓ fly.png vygenerován")


def vytvor_mysi(velikost=48):
    """Vytvoří myš – šedé tělo s ušima a ocasem."""
    img = Image.new("RGBA", (velikost, velikost), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    cx, cy = velikost // 2 - 2, velikost // 2 + 4

    # Ocas
    draw.line([(cx - 14, cy + 1), (cx - 22, cy - 7), (cx - 27, cy - 3)],
              fill=(180, 150, 140), width=2)

    # Tělo
    draw.ellipse([cx - 13, cy - 9, cx + 13, cy + 9],
                 fill=(185, 180, 178, 255), outline=(145, 138, 135))

    # Uši
    for ex, ey in [(cx + 2, cy - 17), (cx - 14, cy - 17)]:
        draw.ellipse([ex, ey, ex + 12, ey + 10], fill=(205, 178, 178), outline=(165, 130, 128))
        draw.ellipse([ex + 2, ey + 2, ex + 10, ey + 8], fill=(240, 185, 183))

    # Hlava
    draw.ellipse([cx + 3, cy - 11, cx + 19, cy + 4],
                 fill=(188, 183, 181, 255), outline=(145, 138, 135))

    # Oko
    draw.ellipse([cx + 12, cy - 8, cx + 17, cy - 3], fill=(25, 22, 20))
    draw.ellipse([cx + 13, cy - 8, cx + 14, cy - 7], fill=(200, 200, 200))

    # Čumák
    draw.ellipse([cx + 17, cy - 4, cx + 21, cy], fill=(220, 150, 148))

    img.save("assets/mouse.png")
    print("✓ mouse.png vygenerován")


def vytvor_krysu(velikost=64):
    """Vytvoří krysu – větší a drsnější než myš."""
    img = Image.new("RGBA", (velikost, velikost), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    cx, cy = velikost // 2 - 2, velikost // 2 + 5

    # Ocas (delší, klikatý)
    draw.line([(cx - 18, cy + 2), (cx - 28, cy - 5),
               (cx - 34, cy + 1), (cx - 40, cy - 3)],
              fill=(155, 125, 105), width=3)

    # Tělo
    draw.ellipse([cx - 16, cy - 11, cx + 16, cy + 11],
                 fill=(155, 145, 128, 255), outline=(118, 108, 92))

    # Uši
    draw.ellipse([cx + 3,  cy - 21, cx + 16, cy - 11],
                 fill=(170, 148, 138), outline=(132, 110, 100))
    draw.ellipse([cx + 5,  cy - 19, cx + 14, cy - 13], fill=(210, 170, 160))

    # Hlava (delší čenich)
    draw.ellipse([cx + 8,  cy - 13, cx + 30, cy + 6],
                 fill=(160, 150, 132, 255), outline=(118, 108, 92))

    # Oko
    draw.ellipse([cx + 19, cy - 10, cx + 25, cy - 4], fill=(18, 15, 12))
    draw.ellipse([cx + 20, cy - 10, cx + 21, cy - 9], fill=(190, 190, 190))

    # Čumák
    draw.ellipse([cx + 28, cy - 5, cx + 33, cy], fill=(200, 125, 118))

    # Vousy
    for i in range(-2, 3):
        draw.line([(cx + 30, cy - 3 + i * 2), (cx + 43, cy - 4 + i * 2)],
                  fill=(200, 188, 175), width=1)

    img.save("assets/rat.png")
    print("✓ rat.png vygenerován")


# ── Městské objekty ────────────────────────────────────────────────────────────

def vytvor_psa(velikost=64):
    """Vytvoří psa – hnědý, se čtyřmi nohami a ocasem."""
    img = Image.new("RGBA", (velikost, velikost), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    cx, cy = velikost // 2, velikost // 2 + 6
    col = (185, 128, 72, 255)
    dark = (148, 98, 50)
    out = (118, 78, 38)

    # Ocas
    draw.line([(cx - 15, cy - 6), (cx - 24, cy - 17), (cx - 19, cy - 23)],
              fill=dark, width=5)

    # Nohy (4 ks)
    for lx in [cx - 11, cx - 3, cx + 5, cx + 13]:
        draw.rectangle([lx, cy + 8, lx + 6, cy + 22], fill=col, outline=out)

    # Tělo
    draw.ellipse([cx - 16, cy - 9, cx + 20, cy + 12], fill=col, outline=out)

    # Hlava
    draw.ellipse([cx + 10, cy - 20, cx + 32, cy + 2], fill=col, outline=out)

    # Ucho (visící)
    draw.ellipse([cx + 23, cy - 16, cx + 34, cy + 3], fill=dark, outline=out)

    # Oko
    draw.ellipse([cx + 17, cy - 14, cx + 23, cy - 8], fill=(25, 18, 10))
    draw.ellipse([cx + 18, cy - 14, cx + 19, cy - 13], fill=(200, 200, 200))

    # Nos
    draw.ellipse([cx + 29, cy - 8, cx + 34, cy - 3], fill=(48, 38, 32))

    img.save("assets/dog.png")
    print("✓ dog.png vygenerován")


def vytvor_cloveka(velikost=64):
    """Vytvoří postavu člověka."""
    img = Image.new("RGBA", (velikost, velikost), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    cx = velikost // 2
    skin  = (255, 200, 148, 255)
    shirt = (65, 105, 195, 255)
    pants = (48, 58, 118, 255)
    shoe  = (55, 45, 38)
    hair  = (78, 48, 20)

    # Nohy
    draw.rectangle([cx - 8, 42, cx - 1, 58], fill=pants)
    draw.rectangle([cx + 1, 42, cx + 8, 58], fill=pants)

    # Boty
    draw.ellipse([cx - 11, 55, cx + 2,  62], fill=shoe)
    draw.ellipse([cx,      55, cx + 13, 62], fill=shoe)

    # Trup
    draw.rectangle([cx - 9, 22, cx + 9, 43], fill=shirt)

    # Ruce
    draw.line([(cx - 9, 25), (cx - 19, 38)], fill=skin, width=5)
    draw.line([(cx + 9, 25), (cx + 19, 38)], fill=skin, width=5)

    # Hlava
    draw.ellipse([cx - 8, 4, cx + 8, 22], fill=skin, outline=(210, 160, 110))

    # Vlasy
    draw.ellipse([cx - 8, 4, cx + 8, 14], fill=hair)

    # Oči
    draw.ellipse([cx - 4, 11, cx - 1, 15], fill=(30, 25, 20))
    draw.ellipse([cx + 1, 11, cx + 4, 15], fill=(30, 25, 20))

    img.save("assets/person.png")
    print("✓ person.png vygenerován")


def vytvor_auto(velikost=64):
    """Vytvoří auto – pohled z boku."""
    img = Image.new("RGBA", (velikost, velikost), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Karoserie
    draw.rectangle([4, 30, 60, 50], fill=(200, 50, 50, 255), outline=(155, 30, 30))

    # Střecha
    draw.polygon([(14, 30), (50, 30), (46, 15), (18, 15)],
                 fill=(180, 40, 40), outline=(135, 25, 25))

    # Okna
    draw.rectangle([20, 17, 36, 29], fill=(155, 205, 235, 210), outline=(105, 155, 185))
    draw.rectangle([38, 17, 46, 29], fill=(155, 205, 235, 210), outline=(105, 155, 185))

    # Kola
    for wx in [12, 48]:
        draw.ellipse([wx - 10, 44, wx + 10, 62], fill=(38, 38, 38), outline=(18, 18, 18))
        draw.ellipse([wx - 5,  49, wx + 5,  57], fill=(95, 95, 95))

    # Světla
    draw.rectangle([57, 32, 63, 38], fill=(255, 240, 140, 225))
    draw.rectangle([1,  32, 6,  38], fill=(255, 90, 90, 200))

    img.save("assets/car.png")
    print("✓ car.png vygenerován")


def vytvor_autobus(velikost=80):
    """Vytvoří autobus – žlutý školní autobus."""
    img = Image.new("RGBA", (velikost, velikost), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Karoserie
    draw.rectangle([3, 22, 77, 60], fill=(228, 192, 38, 255), outline=(185, 152, 20))

    # Přední část
    draw.rectangle([66, 22, 77, 52], fill=(210, 175, 25))

    # Okna
    for wx in range(7, 62, 17):
        draw.rectangle([wx, 26, wx + 13, 40], fill=(155, 205, 235, 210), outline=(105, 155, 185))

    # Přední okno
    draw.rectangle([64, 26, 76, 40], fill=(155, 205, 235, 210), outline=(105, 155, 185))

    # Dveře
    draw.rectangle([5, 42, 18, 60], fill=(192, 158, 22))
    draw.line([(11, 42), (11, 60)], fill=(155, 122, 15), width=1)

    # Kola
    for wx in [15, 60]:
        draw.ellipse([wx - 11, 54, wx + 11, 74], fill=(38, 38, 38), outline=(18, 18, 18))
        draw.ellipse([wx - 5,  60, wx + 5,  68], fill=(95, 95, 95))

    # Světla
    draw.rectangle([74, 28, 79, 35], fill=(255, 240, 140, 225))
    draw.rectangle([74, 44, 79, 51], fill=(255, 90, 90, 200))

    img.save("assets/bus.png")
    print("✓ bus.png vygenerován")


def vytvor_dum(velikost=96):
    """Vytvoří rodinný dům s okny a dveřmi."""
    img = Image.new("RGBA", (velikost, velikost), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Stěny
    draw.rectangle([10, 46, 86, 90], fill=(215, 195, 168, 255), outline=(170, 148, 118))

    # Střecha
    draw.polygon([(5, 46), (91, 46), (48, 10)], fill=(180, 75, 55, 255), outline=(145, 55, 38))

    # Okna
    for wx, wy in [(18, 54), (64, 54)]:
        draw.rectangle([wx, wy, wx + 16, wy + 18], fill=(155, 210, 235, 220), outline=(105, 160, 185))
        draw.line([(wx + 8, wy), (wx + 8, wy + 18)], fill=(105, 160, 185), width=1)
        draw.line([(wx, wy + 9), (wx + 16, wy + 9)], fill=(105, 160, 185), width=1)

    # Dveře
    draw.rectangle([38, 65, 58, 90], fill=(140, 95, 55), outline=(105, 70, 38))
    draw.ellipse([53, 76, 57, 80], fill=(200, 165, 55))

    # Komín
    draw.rectangle([65, 5, 75, 30], fill=(180, 120, 88), outline=(140, 90, 62))
    draw.rectangle([63, 4, 77, 10], fill=(155, 100, 72))

    img.save("assets/house.png")
    print("✓ house.png vygenerován")


def vytvor_mrakodrap(velikost=112):
    """Vytvoří mrakodrap se skleněnou fasádou a okny."""
    img = Image.new("RGBA", (velikost, velikost), (0, 0, 0, 0))

    # Záře odlesku
    glow = Image.new("RGBA", (velikost, velikost), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.rectangle([22, 2, 90, velikost - 4], fill=(80, 130, 200, 40))
    glow = glow.filter(ImageFilter.GaussianBlur(8))
    img = Image.alpha_composite(img, glow)

    draw = ImageDraw.Draw(img)

    # Hlavní věž
    draw.rectangle([24, 4, 88, velikost - 4], fill=(85, 115, 162, 255), outline=(62, 90, 138))

    # Skleněné vodorovné pruhy
    for y in range(8, velikost - 8, 18):
        draw.rectangle([25, y, 87, y + 10], fill=(105, 145, 195, 200))

    # Okna
    for wy in range(10, velikost - 10, 18):
        for wx in range(28, 85, 14):
            wc = (175, 215, 255, 220) if (wx + wy) % 3 != 0 else (255, 245, 180, 200)
            draw.rectangle([wx, wy, wx + 9, wy + 7], fill=wc)

    # Střecha / anténa
    draw.rectangle([50, 0, 62, 6], fill=(72, 72, 82))
    draw.rectangle([54, -4, 58, 2], fill=(62, 62, 72))

    # Základ
    draw.rectangle([18, velikost - 8, 94, velikost - 2], fill=(65, 65, 75))

    img.save("assets/skyscraper.png")
    print("✓ skyscraper.png vygenerován")


if __name__ == "__main__":
    print("Generování textur pro hru 'Kočka co sní vesmír'...")
    print("=" * 50)

    # Vesmírné objekty (Level 3)
    vytvor_pozadi()
    vytvor_kocku()
    vytvor_hvezdu()
    vytvor_asteroid()
    vytvor_mesic()
    vytvor_planetu()
    vytvor_slunce()
    vytvor_galaxii()

    # Nová pozadí (Level 1 & 2)
    vytvor_pozadi_laborator()
    vytvor_pozadi_mesto()

    # Laboratorní objekty (Level 1)
    vytvor_bakterii()
    vytvor_bunku()
    vytvor_mravence()
    vytvor_mouchu()
    vytvor_mysi()
    vytvor_krysu()

    # Městské objekty (Level 2)
    vytvor_psa()
    vytvor_cloveka()
    vytvor_auto()
    vytvor_autobus()
    vytvor_dum()
    vytvor_mrakodrap()

    print("=" * 50)
    print("Všechny textury byly úspěšně vygenerovány do složky assets/")
    print("Nyní můžete spustit hru: python main.py")
