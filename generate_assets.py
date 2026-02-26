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


def vytvor_pozadi_lab(sirka=1024, vyska=768):
    """Vytvoří pozadí laboratoře – světlé s mřížkou a siluetami vybavení."""
    img = Image.new("RGBA", (sirka, vyska), (225, 232, 240, 255))
    draw = ImageDraw.Draw(img)

    # Mřížka na podlaze (spodní polovina)
    for x in range(0, sirka, 48):
        draw.line([x, vyska // 2, x, vyska], fill=(200, 210, 220, 180), width=1)
    for y in range(vyska // 2, vyska, 48):
        draw.line([0, y, sirka, y], fill=(200, 210, 220, 180), width=1)

    # Laboratorní stůl
    draw.rectangle([0, vyska // 2 - 20, sirka, vyska // 2 + 12], fill=(180, 170, 150, 255))
    draw.rectangle([0, vyska // 2 + 12, sirka, vyska // 2 + 16], fill=(140, 130, 110, 255))

    # Silueta Erlenmeyerovy baňky vlevo
    bx, by = 120, vyska // 2 - 180
    draw.polygon([(bx, by), (bx - 50, by + 160), (bx + 50, by + 160)], fill=(180, 220, 230, 80))
    draw.rectangle([bx - 12, by - 40, bx + 12, by], fill=(180, 220, 230, 80))

    # Silueta zkumavek vpravo
    for i in range(5):
        rx = sirka - 200 + i * 26
        draw.rectangle([rx, vyska // 2 - 140, rx + 14, vyska // 2 - 10], fill=(180, 230, 200, 80))
        draw.ellipse([rx, vyska // 2 - 16, rx + 14, vyska // 2 - 2], fill=(180, 230, 200, 80))

    # Svítící lampa nahoře
    draw.ellipse([sirka // 2 - 80, 10, sirka // 2 + 80, 60], fill=(255, 250, 220, 120))

    img.save("assets/background_lab.png")
    print("✓ background_lab.png vygenerován")


def vytvor_pozadi_kuchyne(sirka=1024, vyska=768):
    """Vytvoří pozadí kuchyně – dlaždice, pracovní deska, skříňky."""
    img = Image.new("RGBA", (sirka, vyska), (245, 238, 218, 255))
    draw = ImageDraw.Draw(img)

    # Horní skříňky
    draw.rectangle([0, 0, sirka, 120], fill=(190, 165, 120, 255))
    for cx in range(0, sirka, 200):
        draw.rectangle([cx + 10, 10, cx + 190, 110], fill=(210, 185, 140, 255))
        draw.rectangle([cx + 10, 10, cx + 190, 110], outline=(160, 135, 90, 255), width=2)
        draw.ellipse([cx + 88, 55, cx + 102, 65], fill=(160, 135, 90, 255))

    # Obkladačky na zdi
    for tx in range(0, sirka, 64):
        for ty in range(120, vyska // 2, 64):
            barva = (240, 232, 215, 255) if ((tx // 64 + ty // 64) % 2 == 0) else (230, 222, 205, 255)
            draw.rectangle([tx, ty, tx + 63, ty + 63], fill=barva)
            draw.rectangle([tx, ty, tx + 63, ty + 63], outline=(210, 200, 183, 255), width=1)

    # Pracovní deska
    draw.rectangle([0, vyska // 2 - 20, sirka, vyska // 2 + 15], fill=(180, 155, 110, 255))
    draw.rectangle([0, vyska // 2 + 15, sirka, vyska // 2 + 20], fill=(140, 120, 85, 255))

    # Podlahové dlaždice
    for px in range(0, sirka, 80):
        for py in range(vyska // 2 + 20, vyska, 80):
            barva = (210, 200, 185, 255) if ((px // 80 + py // 80) % 2 == 0) else (225, 215, 198, 255)
            draw.rectangle([px, py, px + 79, py + 79], fill=barva)

    img.save("assets/background_kitchen.png")
    print("✓ background_kitchen.png vygenerován")


def vytvor_pozadi_zahrady(sirka=1024, vyska=768):
    """Vytvoří pozadí zahrady – obloha, tráva, stromy."""
    img = Image.new("RGBA", (sirka, vyska), (130, 195, 255, 255))
    draw = ImageDraw.Draw(img)

    # Přechod oblohy
    for y in range(vyska // 2):
        t = y / (vyska // 2)
        r = int(130 + 60 * t)
        g = int(195 + 20 * t)
        b = 255
        draw.line([0, y, sirka, y], fill=(r, g, b, 255))

    # Oblaka
    random.seed(77)
    for cx, cy in [(150, 90), (420, 70), (700, 100), (920, 55), (280, 140)]:
        for ox, oy, rr in [(-35, 0, 28), (0, -18, 22), (30, -5, 25), (55, 5, 20)]:
            draw.ellipse([cx + ox - rr, cy + oy - rr, cx + ox + rr, cy + oy + rr],
                         fill=(255, 255, 255, 210))

    # Tráva (přechod)
    for y in range(vyska // 2, vyska):
        t = (y - vyska // 2) / (vyska // 2)
        g = int(165 - 30 * t)
        draw.line([0, y, sirka, y], fill=(40, g + 10, 35, 255))

    # Stromy
    for tx in [130, 350, 680, 900]:
        # Kmen
        draw.rectangle([tx - 10, vyska // 2 - 90, tx + 10, vyska // 2 + 10], fill=(100, 70, 40, 255))
        # Koruna
        draw.ellipse([tx - 55, vyska // 2 - 160, tx + 55, vyska // 2 - 60], fill=(35, 120, 35, 255))
        draw.ellipse([tx - 40, vyska // 2 - 180, tx + 40, vyska // 2 - 90], fill=(50, 145, 50, 255))

    # Plot v dálce
    for fx in range(0, sirka, 30):
        draw.rectangle([fx, vyska // 2 - 5, fx + 6, vyska // 2 + 30], fill=(160, 130, 90, 180))
    draw.line([0, vyska // 2 + 8, sirka, vyska // 2 + 8], fill=(140, 110, 70, 180), width=4)

    img.save("assets/background_garden.png")
    print("✓ background_garden.png vygenerován")


def vytvor_pozadi_mesta(sirka=1024, vyska=768):
    """Vytvoří pozadí města – budovy, silnice, obloha."""
    random.seed(33)
    img = Image.new("RGBA", (sirka, vyska), (160, 175, 205, 255))
    draw = ImageDraw.Draw(img)

    # Obloha s mrakem
    for y in range(vyska // 2):
        t = y / (vyska // 2)
        draw.line([0, y, sirka, y], fill=(int(160 + 30 * t), int(175 + 15 * t), int(205 + 10 * t), 255))

    # Budovy v pozadí
    buildings = [
        (0, 300, 120, 768),
        (100, 180, 260, 768),
        (230, 320, 370, 768),
        (340, 140, 500, 768),
        (470, 260, 590, 768),
        (570, 100, 720, 768),
        (700, 220, 830, 768),
        (810, 150, 950, 768),
        (930, 280, 1024, 768),
    ]
    for bx1, by1, bx2, by2 in buildings:
        shade = random.randint(0, 30)
        barva = (90 + shade, 95 + shade, 105 + shade, 255)
        draw.rectangle([bx1, by1, bx2, by2], fill=barva)
        # Okna
        for wy in range(by1 + 15, by2 - 20, 28):
            for wx in range(bx1 + 8, bx2 - 8, 18):
                if random.random() > 0.3:
                    draw.rectangle([wx, wy, wx + 10, wy + 16], fill=(255, 240, 160, 200))
                else:
                    draw.rectangle([wx, wy, wx + 10, wy + 16], fill=(60, 70, 90, 200))

    # Silnice
    draw.rectangle([0, vyska - 100, sirka, vyska], fill=(70, 72, 80, 255))
    # Středová čára
    for sx in range(0, sirka, 80):
        draw.rectangle([sx, vyska - 52, sx + 50, vyska - 46], fill=(255, 220, 0, 255))
    # Chodník
    draw.rectangle([0, vyska - 110, sirka, vyska - 100], fill=(160, 155, 148, 255))

    img.save("assets/background_city.png")
    print("✓ background_city.png vygenerován")


# ── Level 1 – Laboratoř ──────────────────────────────────────────────────────

def vytvor_bakterii(velikost=32):
    """Vytvoří bakterii – zelený ovál s bičíky."""
    img = Image.new("RGBA", (velikost, velikost), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    cx, cy = velikost // 2, velikost // 2

    # Tělo
    draw.ellipse([cx - 11, cy - 6, cx + 11, cy + 6],
                 fill=(50, 190, 80, 230), outline=(20, 130, 50, 255), width=2)
    # Bičíky
    for i in range(4):
        angle = math.pi / 2 * i
        x1 = int(cx + 11 * math.cos(angle))
        y1 = int(cy + 6 * math.sin(angle))
        x2 = int(cx + 15 * math.cos(angle))
        y2 = int(cy + 10 * math.sin(angle))
        draw.line([x1, y1, x2, y2], fill=(20, 140, 50, 200), width=1)
    # Lesklý bod
    draw.ellipse([cx - 4, cy - 3, cx, cy], fill=(150, 240, 150, 180))

    img.save("assets/bacteria.png")
    print("✓ bacteria.png vygenerován")


def vytvor_molekulu(velikost=32):
    """Vytvoří molekulu – atomy spojené vazbami."""
    img = Image.new("RGBA", (velikost, velikost), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    cx, cy = velikost // 2, velikost // 2

    # Vazby
    draw.line([cx, cy, cx - 9, cy - 9], fill=(180, 180, 200, 200), width=2)
    draw.line([cx, cy, cx + 9, cy - 8], fill=(180, 180, 200, 200), width=2)
    draw.line([cx, cy, cx, cy + 10], fill=(180, 180, 200, 200), width=2)

    # Atomy
    draw.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=(210, 80, 80, 255))
    draw.ellipse([cx - 15, cy - 15, cx - 4, cy - 4], fill=(80, 120, 230, 255))
    draw.ellipse([cx + 3, cy - 14, cx + 14, cy - 3], fill=(80, 120, 230, 255))
    draw.ellipse([cx - 5, cy + 4, cx + 5, cy + 15], fill=(100, 210, 100, 255))

    img.save("assets/molecule.png")
    print("✓ molecule.png vygenerován")


def vytvor_bunku(velikost=32):
    """Vytvoří buňku – průhledná membrána s jádrem."""
    img = Image.new("RGBA", (velikost, velikost), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    cx, cy = velikost // 2, velikost // 2
    r = velikost // 2 - 3

    # Buněčná membrána
    draw.ellipse([cx - r, cy - r, cx + r, cy + r],
                 fill=(180, 225, 255, 100), outline=(100, 165, 225, 200), width=2)
    # Jádro
    rn = r // 3
    draw.ellipse([cx - rn, cy - rn, cx + rn, cy + rn],
                 fill=(120, 80, 210, 200), outline=(80, 50, 160, 255), width=1)
    # Organely
    draw.ellipse([cx + 4, cy + 4, cx + 9, cy + 9], fill=(100, 210, 160, 180))
    draw.ellipse([cx - 9, cy + 4, cx - 4, cy + 9], fill=(210, 160, 100, 180))

    img.save("assets/cell.png")
    print("✓ cell.png vygenerován")


def vytvor_kapicku(velikost=32):
    """Vytvoří kapičku vody – slzový tvar."""
    img = Image.new("RGBA", (velikost, velikost), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    cx = velikost // 2
    r = (velikost - 8) // 2

    # Tělo kapky (kruh dole + trojúhelník nahoře)
    bot = velikost - 4
    top_circle = bot - 2 * r
    draw.ellipse([cx - r, top_circle, cx + r, bot], fill=(80, 165, 255, 210))
    draw.polygon([(cx, 3), (cx - r, top_circle + r), (cx + r, top_circle + r)],
                 fill=(80, 165, 255, 210))
    # Odlesk
    draw.ellipse([cx - r // 2, top_circle + 2, cx - r // 4, top_circle + r // 2],
                 fill=(200, 230, 255, 160))

    img.save("assets/droplet.png")
    print("✓ droplet.png vygenerován")


def vytvor_petri(velikost=64):
    """Vytvoří Petriho misku s bakteriálními koloniemi."""
    img = Image.new("RGBA", (velikost, velikost), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    cx, cy = velikost // 2, velikost // 2
    r = velikost // 2 - 4

    # Vnější kroužek (sklo)
    draw.ellipse([cx - r, cy - r, cx + r, cy + r],
                 fill=(200, 235, 255, 80), outline=(100, 165, 215, 200), width=3)
    # Vnitřní kroužek (víčko)
    ri = r - 7
    draw.ellipse([cx - ri, cy - ri, cx + ri, cy + ri], outline=(120, 185, 235, 150), width=2)
    # Agarové médium
    draw.ellipse([cx - ri + 2, cy - ri + 2, cx + ri - 2, cy + ri - 2],
                 fill=(220, 235, 200, 60))
    # Bakteriální kolonie
    for bx, by, br in [(cx - 8, cy - 5, 5), (cx + 10, cy + 6, 4),
                       (cx - 5, cy + 11, 3), (cx + 4, cy - 12, 4)]:
        draw.ellipse([bx - br, by - br, bx + br, by + br], fill=(60, 190, 80, 200))
    # Odlesk skla
    draw.arc([cx - r + 4, cy - r + 4, cx - 4, cy - 4], 210, 300, fill=(255, 255, 255, 100), width=2)

    img.save("assets/petri.png")
    print("✓ petri.png vygenerován")


# ── Level 2 – Kuchyně ────────────────────────────────────────────────────────

def vytvor_drobecek(velikost=32):
    """Vytvoří drobeček chleba."""
    img = Image.new("RGBA", (velikost, velikost), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    cx, cy = velikost // 2, velikost // 2

    random.seed(55)
    body = []
    for i in range(9):
        angle = 2 * math.pi * i / 9
        r = random.randint(6, 11)
        body.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))
    draw.polygon(body, fill=(185, 135, 68, 255), outline=(145, 100, 48, 255))
    # Textura
    draw.ellipse([cx - 3, cy - 2, cx + 2, cy + 3], fill=(210, 165, 95, 200))

    img.save("assets/crumb.png")
    print("✓ crumb.png vygenerován")


def vytvor_cukr(velikost=32):
    """Vytvoří krystal cukru – hexagon s třpytem."""
    img = Image.new("RGBA", (velikost, velikost), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    cx, cy = velikost // 2, velikost // 2

    body = []
    for i in range(6):
        angle = math.pi * i / 3 - math.pi / 6
        body.append((cx + 10 * math.cos(angle), cy + 10 * math.sin(angle)))
    draw.polygon(body, fill=(245, 245, 255, 230), outline=(200, 200, 245, 255))

    # Třpyt
    for dx, dy in [(0, -13), (-11, -7), (11, -7)]:
        draw.line([cx + dx, cy + dy, cx + dx, cy + dy + 4], fill=(255, 255, 210, 255), width=2)
        draw.line([cx + dx - 2, cy + dy + 2, cx + dx + 2, cy + dy + 2],
                  fill=(255, 255, 210, 200), width=1)

    img.save("assets/sugar.png")
    print("✓ sugar.png vygenerován")


def vytvor_mravence(velikost=32):
    """Vytvoří mravence."""
    img = Image.new("RGBA", (velikost, velikost), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    cerna = (30, 20, 20, 255)

    # Zadeček
    draw.ellipse([16, 17, 27, 26], fill=cerna)
    # Hruď
    draw.ellipse([11, 14, 19, 22], fill=cerna)
    # Hlava
    draw.ellipse([4, 12, 13, 20], fill=cerna)
    # Tykadla
    draw.line([8, 12, 4, 6], fill=cerna, width=1)
    draw.line([11, 12, 14, 6], fill=cerna, width=1)
    draw.ellipse([3, 5, 6, 8], fill=cerna)
    draw.ellipse([13, 5, 16, 8], fill=cerna)
    # Nožičky
    for ly in [15, 18, 21]:
        draw.line([11, ly, 5, ly - 4], fill=cerna, width=1)
        draw.line([19, ly, 25, ly - 4], fill=cerna, width=1)

    img.save("assets/ant.png")
    print("✓ ant.png vygenerován")


def vytvor_svaba(velikost=48):
    """Vytvoří švába."""
    img = Image.new("RGBA", (velikost, velikost), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    cx, cy = velikost // 2, velikost // 2
    barva = (100, 62, 22, 255)
    tmave = (60, 32, 10, 255)

    # Tělo
    draw.ellipse([cx - 15, cy - 8, cx + 15, cy + 8], fill=barva, outline=tmave, width=1)
    # Hlava
    draw.ellipse([cx + 11, cy - 6, cx + 20, cy + 6], fill=tmave)
    # Tykadla
    draw.line([cx + 20, cy - 3, cx + 30, cy - 12], fill=tmave, width=1)
    draw.line([cx + 20, cy + 3, cx + 30, cy + 10], fill=tmave, width=1)
    # Nožičky
    for i, ly in enumerate([-5, 0, 5]):
        draw.line([cx - 8 + i * 4, cy + 8, cx - 13 + i * 4, cy + 16], fill=tmave, width=1)
        draw.line([cx - 8 + i * 4, cy - 8, cx - 13 + i * 4, cy - 16], fill=tmave, width=1)
    # Lesk na krovkách
    draw.arc([cx - 12, cy - 6, cx + 4, cy + 2], 200, 320, fill=(160, 110, 60, 180), width=2)

    img.save("assets/cockroach.png")
    print("✓ cockroach.png vygenerován")


def vytvor_mysku(velikost=64):
    """Vytvoří myšku."""
    img = Image.new("RGBA", (velikost, velikost), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    cx, cy = velikost // 2, velikost // 2
    seda = (165, 155, 155, 255)
    tmave = (120, 110, 110, 255)
    ruzova = (255, 185, 185, 255)

    # Tělo
    draw.ellipse([cx - 18, cy - 12, cx + 18, cy + 13], fill=seda)
    # Hlava
    draw.ellipse([cx + 10, cy - 13, cx + 30, cy + 5], fill=seda)
    # Uši
    draw.ellipse([cx + 12, cy - 22, cx + 21, cy - 12], fill=seda, outline=ruzova, width=2)
    draw.ellipse([cx + 21, cy - 20, cx + 30, cy - 10], fill=seda, outline=ruzova, width=2)
    # Oko
    draw.ellipse([cx + 22, cy - 9, cx + 27, cy - 4], fill=(30, 20, 20, 255))
    draw.ellipse([cx + 23, cy - 9, cx + 25, cy - 7], fill=(180, 180, 180, 160))
    # Čumák
    draw.ellipse([cx + 28, cy - 5, cx + 32, cy - 1], fill=ruzova)
    # Ocas
    draw.arc([cx - 32, cy, cx - 10, cy + 22], 180, 360, fill=tmave, width=2)

    img.save("assets/mouse.png")
    print("✓ mouse.png vygenerován")


# ── Level 3 – Zahrada ────────────────────────────────────────────────────────

def vytvor_kvet(velikost=48):
    """Vytvoří květ s okvětními lístky."""
    img = Image.new("RGBA", (velikost, velikost), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    cx, cy = velikost // 2, velikost // 2

    # Stonek
    draw.line([cx, cy + 8, cx, cy + 22], fill=(50, 160, 50, 255), width=3)
    # Lístky
    draw.ellipse([cx - 10, cy + 12, cx, cy + 22], fill=(70, 190, 60, 255))
    draw.ellipse([cx, cy + 12, cx + 10, cy + 22], fill=(70, 190, 60, 255))
    # Okvětní lístky
    for i in range(6):
        angle = math.pi * i / 3
        px = cx + int(12 * math.cos(angle))
        py = cy + int(12 * math.sin(angle))
        draw.ellipse([px - 7, py - 7, px + 7, py + 7], fill=(255, 100, 160, 230))
    # Střed
    draw.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=(255, 225, 50, 255))
    draw.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=(220, 160, 20, 255))

    img.save("assets/flower.png")
    print("✓ flower.png vygenerován")


def vytvor_slepici(velikost=56):
    """Vytvoří slepici."""
    img = Image.new("RGBA", (velikost, velikost), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    cx, cy = velikost // 2, velikost // 2
    bila = (242, 237, 222, 255)
    oranzova = (240, 155, 30, 255)
    cervena = (225, 50, 50, 255)

    # Tělo
    draw.ellipse([cx - 18, cy - 11, cx + 18, cy + 15], fill=bila)
    # Křídlo
    draw.ellipse([cx - 14, cy - 5, cx + 6, cy + 12], fill=(215, 210, 195, 255))
    # Hlava
    draw.ellipse([cx + 10, cy - 22, cx + 28, cy - 4], fill=bila)
    # Zobák
    draw.polygon([(cx + 28, cy - 13), (cx + 36, cy - 11), (cx + 28, cy - 9)], fill=oranzova)
    # Hřebínek
    draw.polygon([(cx + 14, cy - 22), (cx + 17, cy - 30), (cx + 20, cy - 22),
                  (cx + 23, cy - 28), (cx + 26, cy - 22)], fill=cervena)
    # Oko
    draw.ellipse([cx + 21, cy - 18, cx + 26, cy - 13], fill=(30, 20, 20, 255))
    draw.ellipse([cx + 22, cy - 17, cx + 24, cy - 15], fill=(200, 200, 200, 160))
    # Nožičky
    for nx in [cx - 6, cx + 6]:
        draw.line([nx, cy + 15, nx, cy + 25], fill=oranzova, width=3)
        draw.line([nx, cy + 25, nx - 5, cy + 28], fill=oranzova, width=2)
        draw.line([nx, cy + 25, nx + 5, cy + 28], fill=oranzova, width=2)

    img.save("assets/chicken.png")
    print("✓ chicken.png vygenerován")


def vytvor_kralika(velikost=64):
    """Vytvoří králíka s dlouhými ušima."""
    img = Image.new("RGBA", (velikost, velikost), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    cx, cy = velikost // 2, velikost // 2
    bila = (240, 236, 236, 255)
    ruzova = (255, 200, 200, 255)
    tmave = (200, 190, 190, 255)

    # Tělo
    draw.ellipse([cx - 16, cy - 8, cx + 16, cy + 20], fill=bila)
    # Ocas
    draw.ellipse([cx - 20, cy + 8, cx - 10, cy + 18], fill=bila)
    # Hlava
    draw.ellipse([cx - 12, cy - 26, cx + 12, cy - 4], fill=bila)
    # Dlouhé uši
    draw.ellipse([cx - 12, cy - 52, cx - 4, cy - 22], fill=bila, outline=tmave, width=1)
    draw.ellipse([cx - 10, cy - 50, cx - 6, cy - 26], fill=ruzova)
    draw.ellipse([cx + 4, cy - 52, cx + 12, cy - 22], fill=bila, outline=tmave, width=1)
    draw.ellipse([cx + 6, cy - 50, cx + 10, cy - 26], fill=ruzova)
    # Oko
    draw.ellipse([cx - 6, cy - 20, cx - 2, cy - 16], fill=(30, 20, 20, 255))
    draw.ellipse([cx - 5, cy - 20, cx - 3, cy - 18], fill=(200, 200, 200, 160))
    # Čumák
    draw.ellipse([cx - 3, cy - 13, cx + 3, cy - 7], fill=ruzova)
    # Vousky
    draw.line([cx - 10, cy - 10, cx - 3, cy - 10], fill=tmave, width=1)
    draw.line([cx + 3, cy - 10, cx + 10, cy - 10], fill=tmave, width=1)

    img.save("assets/rabbit.png")
    print("✓ rabbit.png vygenerován")


def vytvor_psa(velikost=72):
    """Vytvoří psa."""
    img = Image.new("RGBA", (velikost, velikost), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    cx, cy = velikost // 2, velikost // 2
    hneda = (185, 135, 72, 255)
    tmave = (135, 90, 40, 255)

    # Ocas
    draw.arc([cx - 32, cy - 14, cx - 18, cy + 4], 270, 90, fill=tmave, width=5)
    # Tělo
    draw.ellipse([cx - 24, cy - 13, cx + 24, cy + 15], fill=hneda)
    # Nožičky
    for lx in [cx - 15, cx - 5, cx + 5, cx + 15]:
        draw.rectangle([lx, cy + 13, lx + 9, cy + 28], fill=hneda)
        draw.ellipse([lx, cy + 26, lx + 9, cy + 32], fill=tmave)
    # Hlava
    draw.ellipse([cx + 14, cy - 26, cx + 38, cy - 2], fill=hneda)
    # Uši (visaté)
    draw.ellipse([cx + 14, cy - 34, cx + 24, cy - 16], fill=tmave)
    draw.ellipse([cx + 28, cy - 34, cx + 38, cy - 16], fill=tmave)
    # Rypák
    draw.ellipse([cx + 28, cy - 18, cx + 42, cy - 6], fill=(205, 175, 125, 255))
    draw.ellipse([cx + 33, cy - 16, cx + 38, cy - 11], fill=(55, 38, 28, 255))
    # Oko
    draw.ellipse([cx + 22, cy - 22, cx + 27, cy - 17], fill=(30, 20, 20, 255))
    draw.ellipse([cx + 23, cy - 22, cx + 25, cy - 20], fill=(200, 200, 200, 160))

    img.save("assets/dog.png")
    print("✓ dog.png vygenerován")


def vytvor_cloveka(velikost=80):
    """Vytvoří figurku člověka."""
    img = Image.new("RGBA", (velikost, velikost), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    cx = velikost // 2
    telova = (220, 172, 132, 255)
    modra = (50, 100, 210, 255)
    tmave_modra = (30, 65, 150, 255)
    cerna = (30, 20, 20, 255)

    # Hlava
    draw.ellipse([cx - 11, 3, cx + 11, 25], fill=telova)
    # Vlasy
    draw.arc([cx - 11, 3, cx + 11, 18], 180, 360, fill=(80, 50, 30, 255), width=4)
    # Obličej
    draw.ellipse([cx - 4, 10, cx - 1, 13], fill=cerna)
    draw.ellipse([cx + 1, 10, cx + 4, 13], fill=cerna)
    draw.arc([cx - 4, 15, cx + 4, 22], 0, 180, fill=cerna, width=1)
    # Tělo
    draw.rectangle([cx - 11, 27, cx + 11, 54], fill=modra)
    # Paže
    draw.line([cx - 11, 30, cx - 24, 48], fill=modra, width=7)
    draw.line([cx + 11, 30, cx + 24, 48], fill=modra, width=7)
    draw.ellipse([cx - 28, 44, cx - 18, 54], fill=telova)
    draw.ellipse([cx + 18, 44, cx + 28, 54], fill=telova)
    # Nohy
    draw.line([cx - 6, 54, cx - 11, 76], fill=tmave_modra, width=7)
    draw.line([cx + 6, 54, cx + 11, 76], fill=tmave_modra, width=7)

    img.save("assets/person.png")
    print("✓ person.png vygenerován")


# ── Level 4 – Město ──────────────────────────────────────────────────────────

def vytvor_auto(velikost=72):
    """Vytvoří auto (pohled ze strany)."""
    img = Image.new("RGBA", (velikost, velikost), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    cervena = (225, 52, 52, 255)
    tmave_cervena = (155, 28, 28, 255)
    seda = (155, 155, 165, 255)
    cerna = (28, 28, 28, 255)
    bila = (240, 240, 240, 255)

    # Karoserie
    draw.rectangle([4, 34, 68, 56], fill=cervena)
    draw.rectangle([4, 34, 68, 38], fill=tmave_cervena)
    # Střecha / kabina
    draw.polygon([(16, 34), (20, 15), (52, 15), (56, 34)], fill=cervena)
    # Okna
    draw.polygon([(21, 32), (24, 17), (40, 17), (40, 32)], fill=(185, 225, 255, 200))
    draw.polygon([(42, 32), (42, 17), (50, 17), (54, 32)], fill=(185, 225, 255, 200))
    # Přední světla
    draw.rectangle([63, 36, 68, 44], fill=(255, 255, 185, 255))
    # Zadní světla
    draw.rectangle([4, 36, 9, 44], fill=(255, 80, 80, 200))
    # Kola
    for wx in [19, 52]:
        draw.ellipse([wx - 11, 50, wx + 11, 72], fill=cerna)
        draw.ellipse([wx - 7, 54, wx + 7, 68], fill=seda)
        draw.ellipse([wx - 3, 58, wx + 3, 64], fill=(80, 80, 88, 255))
    # Dveřní linka
    draw.line([28, 34, 28, 54], fill=tmave_cervena, width=1)

    img.save("assets/car.png")
    print("✓ car.png vygenerován")


def vytvor_autobus(velikost=88):
    """Vytvoří autobus."""
    img = Image.new("RGBA", (velikost, velikost), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    zluta = (252, 205, 22, 255)
    tmave_zluta = (185, 145, 12, 255)
    seda = (155, 155, 165, 255)
    cerna = (28, 28, 28, 255)

    # Hlavní karoserie
    draw.rectangle([4, 20, 84, 68], fill=zluta)
    draw.rectangle([4, 20, 84, 26], fill=tmave_zluta)
    draw.rectangle([4, 62, 84, 68], fill=tmave_zluta)
    # Přední a zadní čelo
    draw.rectangle([4, 20, 16, 68], fill=tmave_zluta)
    draw.rectangle([72, 20, 84, 68], fill=tmave_zluta)
    # Přední světlo
    draw.rectangle([4, 28, 12, 38], fill=(255, 255, 185, 255))
    # Okna
    for wx in range(18, 72, 16):
        draw.rectangle([wx, 28, wx + 12, 48], fill=(185, 225, 255, 200))
    # Dveře
    draw.rectangle([16, 46, 32, 68], fill=tmave_zluta)
    draw.line([24, 46, 24, 68], fill=(150, 110, 8, 255), width=1)
    # Kola
    for wx in [22, 64]:
        draw.ellipse([wx - 12, 62, wx + 12, 86], fill=cerna)
        draw.ellipse([wx - 8, 66, wx + 8, 82], fill=seda)
        draw.ellipse([wx - 3, 71, wx + 3, 77], fill=(80, 80, 88, 255))

    img.save("assets/bus.png")
    print("✓ bus.png vygenerován")


def vytvor_dum(velikost=80):
    """Vytvoří rodinný dům."""
    img = Image.new("RGBA", (velikost, velikost), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Stěny
    draw.rectangle([8, 40, 72, 76], fill=(222, 185, 142, 255), outline=(175, 132, 90, 255), width=2)
    # Střecha
    draw.polygon([(4, 42), (40, 5), (76, 42)], fill=(185, 60, 50, 255), outline=(145, 40, 30, 255))
    # Komín
    draw.rectangle([55, 14, 65, 38], fill=(175, 125, 92, 255))
    draw.rectangle([53, 12, 67, 18], fill=(145, 100, 70, 255))
    # Okna
    draw.rectangle([12, 48, 28, 62], fill=(185, 225, 255, 200), outline=(155, 155, 160, 200))
    draw.line([20, 48, 20, 62], fill=(155, 155, 160, 200), width=1)
    draw.line([12, 55, 28, 55], fill=(155, 155, 160, 200), width=1)
    draw.rectangle([52, 48, 68, 62], fill=(185, 225, 255, 200), outline=(155, 155, 160, 200))
    draw.line([60, 48, 60, 62], fill=(155, 155, 160, 200), width=1)
    draw.line([52, 55, 68, 55], fill=(155, 155, 160, 200), width=1)
    # Dveře
    draw.rectangle([30, 56, 50, 76], fill=(125, 82, 42, 255))
    draw.ellipse([44, 65, 48, 69], fill=(200, 165, 80, 255))

    img.save("assets/house.png")
    print("✓ house.png vygenerován")


def vytvor_panelak(velikost=96):
    """Vytvoří panelový dům."""
    img = Image.new("RGBA", (velikost, velikost), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Budova
    draw.rectangle([10, 8, 86, 92], fill=(182, 182, 188, 255), outline=(142, 142, 148, 255), width=2)
    # Střecha
    draw.rectangle([10, 8, 86, 16], fill=(152, 152, 158, 255))
    # Okna (4 řady × 4 sloupce)
    for row in range(4):
        for col in range(4):
            wx = 16 + col * 18
            wy = 18 + row * 18
            draw.rectangle([wx, wy, wx + 11, wy + 13], fill=(185, 225, 255, 200))
            draw.line([wx + 5, wy, wx + 5, wy + 13], fill=(155, 195, 225, 150), width=1)
    # Vchod
    draw.rectangle([38, 68, 58, 92], fill=(102, 82, 62, 255))
    draw.arc([38, 60, 58, 80], 180, 360, fill=(102, 82, 62, 255), width=4)
    # Římsa
    draw.rectangle([8, 62, 88, 68], fill=(155, 155, 162, 255))

    img.save("assets/building.png")
    print("✓ building.png vygenerován")


def vytvor_horu(velikost=112):
    """Vytvoří horu se sněžným vrcholkem."""
    img = Image.new("RGBA", (velikost, velikost), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Hlavní vrchol
    draw.polygon([(56, 8), (4, 104), (108, 104)], fill=(122, 112, 102, 255), outline=(92, 82, 72, 255))
    # Druhý menší vrchol vlevo
    draw.polygon([(26, 60), (4, 104), (55, 104)], fill=(108, 98, 90, 255))
    # Třetí menší vrchol vpravo
    draw.polygon([(82, 52), (55, 104), (108, 104)], fill=(112, 102, 94, 255))
    # Sněhová čepice
    draw.polygon([(56, 8), (34, 50), (78, 50)], fill=(245, 245, 250, 255))
    draw.polygon([(56, 8), (42, 36), (70, 36)], fill=(255, 255, 255, 255))
    # Stíny / textury
    draw.line([56, 8, 30, 80], fill=(90, 82, 74, 150), width=2)
    draw.line([56, 8, 82, 75], fill=(140, 130, 120, 150), width=1)

    img.save("assets/mountain.png")
    print("✓ mountain.png vygenerován")


if __name__ == "__main__":
    print("Generování textur pro hru 'Kočka co sní vesmír'...")
    print("=" * 50)

    # Původní textury (Level 5 – Vesmír)
    vytvor_pozadi()
    vytvor_kocku()
    vytvor_hvezdu()
    vytvor_asteroid()
    vytvor_mesic()
    vytvor_planetu()
    vytvor_slunce()
    vytvor_galaxii()

    print()
    print("── Nová pozadí ──────────────────────────────────")
    vytvor_pozadi_lab()
    vytvor_pozadi_kuchyne()
    vytvor_pozadi_zahrady()
    vytvor_pozadi_mesta()

    print()
    print("── Level 1 – Laboratoř ──────────────────────────")
    vytvor_bakterii()
    vytvor_molekulu()
    vytvor_bunku()
    vytvor_kapicku()
    vytvor_petri()

    print()
    print("── Level 2 – Kuchyně ────────────────────────────")
    vytvor_drobecek()
    vytvor_cukr()
    vytvor_mravence()
    vytvor_svaba()
    vytvor_mysku()

    print()
    print("── Level 3 – Zahrada ────────────────────────────")
    vytvor_kvet()
    vytvor_slepici()
    vytvor_kralika()
    vytvor_psa()
    vytvor_cloveka()

    print()
    print("── Level 4 – Město ──────────────────────────────")
    vytvor_auto()
    vytvor_autobus()
    vytvor_dum()
    vytvor_panelak()
    vytvor_horu()

    print()
    print("=" * 50)
    print("Všechny textury byly úspěšně vygenerovány do složky assets/")
    print("Nyní můžete spustit hru: python main.py")
