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


def vytvor_lab_pozadi(sirka=1024, vyska=768):
    """Vytvoří laboratorní pozadí s dlaždicemi a Petriho miskou."""
    img = Image.new("RGBA", (sirka, vyska), (215, 235, 215, 255))
    draw = ImageDraw.Draw(img)

    # Dlaždice
    tile = 80
    for tx in range(0, sirka, tile):
        for ty in range(0, vyska, tile):
            draw.rectangle([tx, ty, tx + tile - 1, ty + tile - 1],
                           outline=(170, 200, 170, 255), width=1)

    # Světlý odlesk dlaždic
    for tx in range(0, sirka, tile):
        for ty in range(0, vyska, tile):
            draw.rectangle([tx + 2, ty + 2, tx + 10, ty + 10],
                           fill=(240, 250, 240, 120))

    # Petriho miska – velký průhledný kruh uprostřed
    cx, cy = sirka // 2, vyska // 2
    r = min(sirka, vyska) // 2 - 30
    petri = Image.new("RGBA", (sirka, vyska), (0, 0, 0, 0))
    pd = ImageDraw.Draw(petri)
    pd.ellipse([cx - r, cy - r, cx + r, cy + r],
               fill=(180, 240, 180, 25), outline=(80, 160, 80, 120), width=4)
    # Vnitřní odlesk misky
    pd.arc([cx - r + 10, cy - r + 10, cx + r - 10, cy + r - 10],
           200, 340, fill=(255, 255, 255, 60), width=6)
    petri = petri.filter(ImageFilter.GaussianBlur(radius=2))
    img = Image.alpha_composite(img, petri)

    img.save("assets/lab_bg.png")
    print("✓ lab_bg.png vygenerován")


def vytvor_virus(velikost=20):
    """Vytvoří červený hexagonální virus s trny."""
    img = Image.new("RGBA", (velikost, velikost), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    cx, cy = velikost // 2, velikost // 2
    r = velikost // 2 - 4

    # Záře
    glow = Image.new("RGBA", (velikost, velikost), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse([cx - r - 2, cy - r - 2, cx + r + 2, cy + r + 2], fill=(255, 80, 80, 60))
    glow = glow.filter(ImageFilter.GaussianBlur(radius=2))
    img = Image.alpha_composite(img, glow)

    draw = ImageDraw.Draw(img)
    # Šestihranný tvar
    body = []
    for i in range(6):
        uhel = math.pi * i / 3 - math.pi / 6
        body.append((cx + r * math.cos(uhel), cy + r * math.sin(uhel)))
    draw.polygon(body, fill=(200, 50, 50, 255), outline=(240, 100, 100, 255))

    # Trny
    for i in range(6):
        uhel = math.pi * i / 3 - math.pi / 6
        x1 = cx + r * math.cos(uhel)
        y1 = cy + r * math.sin(uhel)
        x2 = cx + (r + 3) * math.cos(uhel)
        y2 = cy + (r + 3) * math.sin(uhel)
        draw.line([x1, y1, x2, y2], fill=(255, 130, 130, 255), width=1)
        draw.ellipse([x2 - 1, y2 - 1, x2 + 1, y2 + 1], fill=(255, 180, 180, 255))

    # Střed
    draw.ellipse([cx - 2, cy - 2, cx + 2, cy + 2], fill=(255, 160, 160, 255))

    img.save("assets/virus.png")
    print("✓ virus.png vygenerován")


def vytvor_bakterii(velikost=24):
    """Vytvoří zelenou tyčinkovitou bakterii."""
    img = Image.new("RGBA", (velikost, velikost), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    cx, cy = velikost // 2, velikost // 2
    w, h = int(velikost * 0.45), int(velikost * 0.2)

    # Záře
    glow = Image.new("RGBA", (velikost, velikost), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse([cx - w - 2, cy - h - 2, cx + w + 2, cy + h + 2], fill=(80, 200, 80, 60))
    glow = glow.filter(ImageFilter.GaussianBlur(radius=2))
    img = Image.alpha_composite(img, glow)

    draw = ImageDraw.Draw(img)
    # Tělo bakterie (zaoblený obdélník)
    draw.ellipse([cx - w, cy - h, cx + w, cy + h], fill=(60, 180, 60, 255), outline=(100, 220, 100, 255))
    # Světlejší vnitřek
    draw.ellipse([cx - w + 3, cy - h + 2, cx + w - 3, cy + h - 2], fill=(100, 210, 100, 180))
    # Bičík
    bx, by = cx + w, cy
    for i in range(5):
        t = i / 4
        ox = int(bx + t * 8)
        oy = int(by + math.sin(t * math.pi * 2) * 3)
        draw.ellipse([ox - 1, oy - 1, ox + 1, oy + 1], fill=(80, 200, 80, 150))

    img.save("assets/bacterium.png")
    print("✓ bacterium.png vygenerován")


def vytvor_krvinku(velikost=28):
    """Vytvoří červenou krvičku (bikonkávní disk)."""
    img = Image.new("RGBA", (velikost, velikost), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    cx, cy = velikost // 2, velikost // 2
    r = velikost // 2 - 3

    # Záře
    glow = Image.new("RGBA", (velikost, velikost), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse([cx - r - 2, cy - r - 2, cx + r + 2, cy + r + 2], fill=(220, 50, 50, 50))
    glow = glow.filter(ImageFilter.GaussianBlur(radius=3))
    img = Image.alpha_composite(img, glow)

    draw = ImageDraw.Draw(img)
    # Základní červený disk
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(210, 40, 40, 255), outline=(240, 80, 80, 255))
    # Bikonkávní proláklina (tmavší střed)
    inner_r = r // 2
    draw.ellipse([cx - inner_r, cy - inner_r, cx + inner_r, cy + inner_r],
                 fill=(160, 20, 20, 200))
    # Odlesk
    draw.ellipse([cx - r + 2, cy - r + 2, cx - 3, cy - 3], fill=(255, 100, 100, 80))

    img.save("assets/blood_cell.png")
    print("✓ blood_cell.png vygenerován")


def vytvor_amoebu(velikost=36):
    """Vytvoří nepravidelnou průsvitnou amébu."""
    img = Image.new("RGBA", (velikost, velikost), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    cx, cy = velikost // 2, velikost // 2
    r = velikost // 2 - 4

    random.seed(21)
    body = []
    pocet = 14
    for i in range(pocet):
        uhel = 2 * math.pi * i / pocet
        odchylka = random.uniform(0.65, 1.0)
        rb = r * odchylka
        body.append((cx + rb * math.cos(uhel), cy + rb * math.sin(uhel)))

    # Záře
    glow = Image.new("RGBA", (velikost, velikost), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.polygon(body, fill=(100, 200, 100, 50))
    glow = glow.filter(ImageFilter.GaussianBlur(radius=3))
    img = Image.alpha_composite(img, glow)

    draw = ImageDraw.Draw(img)
    draw.polygon(body, fill=(80, 180, 80, 170), outline=(120, 220, 120, 255))
    # Jádro
    draw.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=(50, 140, 50, 220))
    # Vakuoly
    draw.ellipse([cx + 4, cy - 6, cx + 9, cy - 1], fill=(150, 230, 150, 150))
    draw.ellipse([cx - 9, cy + 3, cx - 4, cy + 8], fill=(150, 230, 150, 120))

    img.save("assets/amoeba.png")
    print("✓ amoeba.png vygenerován")


def vytvor_prvoka(velikost=44):
    """Vytvoří prvoka (paramécium) – protažený ovál s řasinkami."""
    img = Image.new("RGBA", (velikost, velikost), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    cx, cy = velikost // 2, velikost // 2
    aw = int(velikost * 0.4)
    ah = int(velikost * 0.2)

    # Záře
    glow = Image.new("RGBA", (velikost, velikost), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse([cx - aw - 2, cy - ah - 2, cx + aw + 2, cy + ah + 2], fill=(140, 100, 200, 60))
    glow = glow.filter(ImageFilter.GaussianBlur(radius=3))
    img = Image.alpha_composite(img, glow)

    draw = ImageDraw.Draw(img)
    draw.ellipse([cx - aw, cy - ah, cx + aw, cy + ah],
                 fill=(160, 120, 210, 200), outline=(200, 160, 255, 255))
    # Světlejší vnitřek
    draw.ellipse([cx - aw + 4, cy - ah + 3, cx + aw - 4, cy + ah - 3],
                 fill=(190, 160, 240, 130))
    # Jádro
    draw.ellipse([cx - 5, cy - 4, cx + 5, cy + 4], fill=(120, 80, 180, 230))
    # Řasinky
    random.seed(55)
    for i in range(16):
        uhel = 2 * math.pi * i / 16
        x1 = cx + aw * math.cos(uhel) * 0.9
        y1 = cy + ah * math.sin(uhel) * 0.9
        x2 = x1 + math.cos(uhel) * 4
        y2 = y1 + math.sin(uhel) * 4
        draw.line([x1, y1, x2, y2], fill=(200, 160, 255, 160), width=1)

    img.save("assets/protozoa.png")
    print("✓ protozoa.png vygenerován")


def vytvor_roztoce(velikost=56):
    """Vytvoří roztoče – pavoukovitý tvar."""
    img = Image.new("RGBA", (velikost, velikost), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    cx, cy = velikost // 2, velikost // 2

    # Tělo (2 části)
    draw.ellipse([cx - 8, cy - 10, cx + 8, cy + 2], fill=(130, 100, 60, 255))   # hlavohruď
    draw.ellipse([cx - 10, cy, cx + 10, cy + 14], fill=(100, 75, 40, 255))       # zadeček

    # 8 noh
    nohy = [
        (-8, -6, -18, -14), (-8, -2, -20, -4), (-8, 4, -18, 10), (-8, 8, -16, 18),
        (8, -6, 18, -14),   (8, -2, 20, -4),   (8, 4, 18, 10),  (8, 8, 16, 18),
    ]
    for x1, y1, x2, y2 in nohy:
        draw.line([cx + x1, cy + y1, cx + x2, cy + y2], fill=(110, 85, 50, 255), width=2)

    # Oči
    draw.ellipse([cx - 4, cy - 9, cx - 1, cy - 6], fill=(220, 50, 50, 255))
    draw.ellipse([cx + 1, cy - 9, cx + 4, cy - 6], fill=(220, 50, 50, 255))

    img.save("assets/mite.png")
    print("✓ mite.png vygenerován")


def vytvor_zahradni_pozadi(sirka=1024, vyska=768):
    """Vytvoří zahradní pozadí s trávou a oblohou."""
    img = Image.new("RGBA", (sirka, vyska), (135, 190, 240, 255))  # obloha
    draw = ImageDraw.Draw(img)

    # Přechod oblohy
    for y in range(vyska // 2):
        t = y / (vyska // 2)
        r = int(135 + t * 30)
        g = int(190 + t * 20)
        b = int(240 - t * 40)
        draw.line([(0, y), (sirka, y)], fill=(r, g, b, 255))

    # Půda
    draw.rectangle([0, vyska * 3 // 4, sirka, vyska], fill=(100, 65, 30, 255))
    # Přechod půdy
    for y in range(vyska * 3 // 4, vyska * 3 // 4 + 20):
        t = (y - vyska * 3 // 4) / 20
        r = int(60 + t * 40)
        g = int(90 + t * (-25))
        draw.line([(0, y), (sirka, y)], fill=(r, g, 30, 255))

    # Tráva
    trava_y = vyska * 3 // 4
    random.seed(5)
    for x in range(0, sirka, 6):
        h = random.randint(20, 50)
        lean = random.randint(-5, 5)
        draw.line([(x, trava_y), (x + lean, trava_y - h)],
                  fill=(50, 160, 50, 255), width=2)

    # Oblaka
    random.seed(8)
    for _ in range(6):
        ox = random.randint(50, sirka - 50)
        oy = random.randint(30, vyska // 3)
        for dx, dy, rr in [(-30, 0, 25), (0, -15, 30), (30, 0, 25), (15, 10, 20), (-15, 10, 20)]:
            draw.ellipse([ox + dx - rr, oy + dy - rr, ox + dx + rr, oy + dy + rr],
                         fill=(255, 255, 255, 200))

    img.save("assets/garden_bg.png")
    print("✓ garden_bg.png vygenerován")


def vytvor_mravence(velikost=24):
    """Vytvoří mravence."""
    img = Image.new("RGBA", (velikost, velikost), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    cx, cy = velikost // 2, velikost // 2
    # Tři části těla
    draw.ellipse([cx - 3, cy - 9, cx + 3, cy - 4], fill=(30, 20, 20, 255))   # hlava
    draw.ellipse([cx - 4, cy - 4, cx + 4, cy + 2], fill=(30, 20, 20, 255))   # hruď
    draw.ellipse([cx - 5, cy + 1, cx + 5, cy + 9], fill=(30, 20, 20, 255))   # zadeček
    # Tykadla
    draw.line([cx - 2, cy - 8, cx - 6, cy - 12], fill=(50, 40, 40, 255), width=1)
    draw.line([cx + 2, cy - 8, cx + 6, cy - 12], fill=(50, 40, 40, 255), width=1)
    # Nožky
    for lx, ly in [(-4, -2), (-4, 0), (-4, 3), (4, -2), (4, 0), (4, 3)]:
        dx = -6 if lx < 0 else 6
        draw.line([cx + lx, cy + ly, cx + lx + dx, cy + ly + 3], fill=(40, 30, 30, 255), width=1)

    img.save("assets/ant.png")
    print("✓ ant.png vygenerován")


def vytvor_mouchu(velikost=28):
    """Vytvoří mouchu s průhledými křídly."""
    img = Image.new("RGBA", (velikost, velikost), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    cx, cy = velikost // 2, velikost // 2
    # Křídla
    draw.ellipse([cx - 12, cy - 8, cx - 1, cy + 2], fill=(200, 220, 255, 120))
    draw.ellipse([cx + 1, cy - 8, cx + 12, cy + 2], fill=(200, 220, 255, 120))
    # Tělo
    draw.ellipse([cx - 4, cy - 8, cx + 4, cy - 2], fill=(50, 50, 40, 255))  # hlava
    draw.ellipse([cx - 5, cy - 3, cx + 5, cy + 7], fill=(60, 60, 50, 255))  # tělo
    # Oči
    draw.ellipse([cx - 4, cy - 8, cx - 1, cy - 5], fill=(180, 0, 0, 255))
    draw.ellipse([cx + 1, cy - 8, cx + 4, cy - 5], fill=(180, 0, 0, 255))
    # Nožky
    for lx in [-5, 5]:
        for ly in [-1, 2, 5]:
            dx = -8 if lx < 0 else 8
            draw.line([cx + lx, cy + ly, cx + lx + dx, cy + ly + 4], fill=(50, 50, 40, 255), width=1)

    img.save("assets/fly.png")
    print("✓ fly.png vygenerován")


def vytvor_brouka(velikost=36):
    """Vytvoří brouka s lesklým krunýřem."""
    img = Image.new("RGBA", (velikost, velikost), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    cx, cy = velikost // 2, velikost // 2
    # Krunýř (elytra) – dvě půlky
    draw.ellipse([cx - 9, cy - 10, cx, cy + 10], fill=(30, 80, 30, 255))
    draw.ellipse([cx, cy - 10, cx + 9, cy + 10], fill=(30, 80, 30, 255))
    draw.line([cx, cy - 10, cx, cy + 10], fill=(20, 60, 20, 255), width=1)
    # Odlesk krunýře
    draw.ellipse([cx - 7, cy - 8, cx - 2, cy - 3], fill=(80, 160, 80, 120))
    # Hlava
    draw.ellipse([cx - 5, cy - 14, cx + 5, cy - 8], fill=(20, 50, 20, 255))
    # Tykadla
    draw.line([cx - 3, cy - 13, cx - 9, cy - 18], fill=(30, 50, 30, 255), width=1)
    draw.line([cx + 3, cy - 13, cx + 9, cy - 18], fill=(30, 50, 30, 255), width=1)
    # Nožky
    for lx in [-9, 9]:
        for ly in [-4, 0, 5]:
            dx = -7 if lx < 0 else 7
            draw.line([cx + lx, cy + ly, cx + lx + dx, cy + ly + 4], fill=(25, 60, 25, 255), width=1)

    img.save("assets/beetle.png")
    print("✓ beetle.png vygenerován")


def vytvor_cerva(velikost=44):
    """Vytvoří červa – vlnité růžové tělo."""
    img = Image.new("RGBA", (velikost, velikost), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    cx, cy = velikost // 2, velikost // 2
    # Segmenty červa po diagonále
    segmenty = []
    for i in range(8):
        t = i / 7
        x = int(cx - 16 + t * 32)
        y = int(cy + math.sin(t * math.pi * 2) * 8)
        segmenty.append((x, y))

    for i, (sx, sy) in enumerate(segmenty):
        r = 5 if i > 0 else 6
        barva = (220, 120, 140, 255) if i % 2 == 0 else (200, 100, 120, 255)
        draw.ellipse([sx - r, sy - r, sx + r, sy + r], fill=barva)

    # Hlava (první segment)
    hx, hy = segmenty[0]
    draw.ellipse([hx - 2, hy - 2, hx + 2, hy + 2], fill=(240, 160, 160, 255))

    img.save("assets/worm.png")
    print("✓ worm.png vygenerován")


def vytvor_mys(velikost=56):
    """Vytvoří šedou myš."""
    img = Image.new("RGBA", (velikost, velikost), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    cx, cy = velikost // 2, velikost // 2
    # Tělo
    draw.ellipse([cx - 14, cy - 8, cx + 14, cy + 10], fill=(160, 160, 160, 255))
    # Hlava
    draw.ellipse([cx + 6, cy - 12, cx + 20, cy + 2], fill=(160, 160, 160, 255))
    # Uši
    draw.ellipse([cx + 8, cy - 19, cx + 15, cy - 11], fill=(180, 140, 140, 255))
    draw.ellipse([cx + 15, cy - 17, cx + 22, cy - 9], fill=(180, 140, 140, 255))
    # Oko
    draw.ellipse([cx + 14, cy - 9, cx + 17, cy - 6], fill=(20, 20, 20, 255))
    # Nos
    draw.ellipse([cx + 18, cy - 4, cx + 21, cy - 1], fill=(220, 100, 100, 255))
    # Ocas
    for i in range(10):
        t = i / 9
        tx = int(cx - 14 - t * 18)
        ty = int(cy + 5 + math.sin(t * math.pi) * 6)
        draw.ellipse([tx - 2, ty - 2, tx + 2, ty + 2], fill=(140, 120, 120, 200))
    # Nožky
    for nx, ny in [(cx - 8, cy + 9), (cx, cy + 10), (cx + 8, cy + 9), (cx - 4, cy + 9)]:
        draw.ellipse([nx - 4, ny, nx + 4, ny + 5], fill=(150, 150, 150, 255))

    img.save("assets/mouse.png")
    print("✓ mouse.png vygenerován")


def vytvor_jezka(velikost=72):
    """Vytvoří ježka s trny."""
    img = Image.new("RGBA", (velikost, velikost), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    cx, cy = velikost // 2, velikost // 2
    # Trny (pozadí)
    random.seed(17)
    for i in range(20):
        uhel = math.pi * 1.2 + i * math.pi * 0.8 / 19
        rx = 14 * math.cos(uhel)
        ry = 10 * math.sin(uhel)
        ex = cx + rx * 1.2 + random.uniform(-2, 2)
        ey = cy + ry * 1.2 + random.uniform(-2, 2)
        draw.line([cx + rx * 0.8, cy + ry * 0.8, ex, ey], fill=(80, 55, 25, 255), width=2)

    # Tělo (hnědý ovál)
    draw.ellipse([cx - 16, cy - 10, cx + 16, cy + 12], fill=(140, 100, 55, 255))
    # Hlava
    draw.ellipse([cx + 10, cy - 12, cx + 26, cy + 4], fill=(170, 130, 75, 255))
    # Čumák
    draw.ellipse([cx + 22, cy - 4, cx + 28, cy + 2], fill=(80, 50, 30, 255))
    # Oko
    draw.ellipse([cx + 16, cy - 8, cx + 19, cy - 5], fill=(20, 20, 20, 255))
    # Nožky
    for nx in [cx - 10, cx - 2, cx + 7]:
        draw.ellipse([nx - 4, cy + 10, nx + 4, cy + 16], fill=(130, 90, 50, 255))

    img.save("assets/hedgehog.png")
    print("✓ hedgehog.png vygenerován")


def vytvor_mestske_pozadi(sirka=1024, vyska=768):
    """Vytvoří městské pozadí s budovami a silnicí."""
    img = Image.new("RGBA", (sirka, vyska), (160, 190, 220, 255))  # oblačná obloha
    draw = ImageDraw.Draw(img)

    # Přechod oblohy
    for y in range(vyska // 2):
        t = y / (vyska // 2)
        r = int(160 + t * 20)
        g = int(190 + t * 10)
        b = int(220 - t * 30)
        draw.line([(0, y), (sirka, y)], fill=(r, g, b, 255))

    # Budovy v pozadí
    random.seed(33)
    zeme_y = vyska * 2 // 3
    for _ in range(18):
        bw = random.randint(50, 100)
        bh = random.randint(80, 250)
        bx = random.randint(0, sirka - bw)
        by = zeme_y - bh
        barva_b = (random.randint(100, 160), random.randint(100, 160), random.randint(110, 170), 255)
        draw.rectangle([bx, by, bx + bw, zeme_y], fill=barva_b)
        # Okna
        for wy in range(by + 10, zeme_y - 5, 20):
            for wx in range(bx + 8, bx + bw - 8, 16):
                if random.random() > 0.3:
                    draw.rectangle([wx, wy, wx + 8, wy + 12],
                                   fill=(255, 240, 150, 180) if random.random() > 0.4 else (100, 130, 180, 200))

    # Chodník/silnice
    draw.rectangle([0, zeme_y, sirka, vyska], fill=(80, 80, 80, 255))
    # Žluté čáry na silnici
    for x in range(0, sirka, 80):
        draw.rectangle([x + 20, zeme_y + (vyska - zeme_y) // 2 - 4,
                        x + 60, zeme_y + (vyska - zeme_y) // 2 + 4],
                       fill=(240, 220, 60, 255))
    # Okraj chodníku
    draw.rectangle([0, zeme_y, sirka, zeme_y + 15], fill=(100, 100, 90, 255))

    img.save("assets/city_bg.png")
    print("✓ city_bg.png vygenerován")


def vytvor_psa(velikost=44):
    """Vytvoří hnědého psa."""
    img = Image.new("RGBA", (velikost, velikost), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    cx, cy = velikost // 2, velikost // 2
    pes = (160, 110, 60, 255)
    tmavsi = (120, 80, 40, 255)
    # Tělo
    draw.ellipse([cx - 14, cy - 6, cx + 10, cy + 10], fill=pes)
    # Hlava
    draw.ellipse([cx + 6, cy - 14, cx + 22, cy + 2], fill=pes)
    # Ucho
    draw.ellipse([cx + 6, cy - 14, cx + 12, cy - 5], fill=tmavsi)
    draw.ellipse([cx + 15, cy - 16, cx + 20, cy - 7], fill=tmavsi)
    # Čumák
    draw.ellipse([cx + 18, cy - 6, cx + 23, cy - 1], fill=(200, 160, 100, 255))
    draw.ellipse([cx + 20, cy - 4, cx + 23, cy - 1], fill=(60, 40, 30, 255))
    # Oko
    draw.ellipse([cx + 14, cy - 11, cx + 17, cy - 8], fill=(30, 20, 10, 255))
    # Nohy
    for nx in [cx - 10, cx - 3, cx + 4]:
        draw.rectangle([nx - 3, cy + 9, nx + 3, cy + 18], fill=pes)
    # Ocas
    draw.line([cx - 14, cy - 2, cx - 22, cy - 12], fill=pes, width=4)

    img.save("assets/dog.png")
    print("✓ dog.png vygenerován")


def vytvor_cloveka(velikost=52):
    """Vytvoří jednoduchou postavu člověka."""
    img = Image.new("RGBA", (velikost, velikost), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    cx, cy = velikost // 2, velikost // 2
    # Hlava
    draw.ellipse([cx - 6, cy - 22, cx + 6, cy - 10], fill=(240, 190, 140, 255))
    # Tělo (triko)
    draw.rectangle([cx - 7, cy - 10, cx + 7, cy + 8], fill=(60, 100, 200, 255))
    # Ruce
    draw.line([cx - 7, cy - 8, cx - 16, cy + 2], fill=(60, 100, 200, 255), width=4)
    draw.line([cx + 7, cy - 8, cx + 16, cy + 2], fill=(60, 100, 200, 255), width=4)
    # Ruce (kůže)
    draw.ellipse([cx - 19, cy, cx - 13, cy + 6], fill=(240, 190, 140, 255))
    draw.ellipse([cx + 13, cy, cx + 19, cy + 6], fill=(240, 190, 140, 255))
    # Kalhoty
    draw.rectangle([cx - 7, cy + 8, cx - 1, cy + 22], fill=(50, 50, 120, 255))
    draw.rectangle([cx + 1, cy + 8, cx + 7, cy + 22], fill=(50, 50, 120, 255))
    # Vlasy
    draw.arc([cx - 6, cy - 22, cx + 6, cy - 12], 180, 0, fill=(80, 50, 20, 255), width=3)

    img.save("assets/human.png")
    print("✓ human.png vygenerován")


def vytvor_auto(velikost=64):
    """Vytvoří barevné auto."""
    img = Image.new("RGBA", (velikost, velikost), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    cx, cy = velikost // 2, velikost // 2
    auto_barva = (200, 60, 60, 255)
    # Karoserie (dolní část)
    draw.rectangle([cx - 28, cy + 2, cx + 28, cy + 18], fill=auto_barva)
    # Karoserie (horní část)
    draw.polygon([
        (cx - 18, cy + 2), (cx - 22, cy - 12),
        (cx + 22, cy - 12), (cx + 18, cy + 2)
    ], fill=auto_barva)
    # Okna
    draw.polygon([
        (cx - 15, cy + 1), (cx - 18, cy - 10),
        (cx - 2, cy - 10), (cx - 2, cy + 1)
    ], fill=(160, 210, 255, 220))
    draw.polygon([
        (cx + 2, cy + 1), (cx + 2, cy - 10),
        (cx + 18, cy - 10), (cx + 15, cy + 1)
    ], fill=(160, 210, 255, 220))
    # Kola
    for kx in [cx - 16, cx + 16]:
        draw.ellipse([kx - 9, cy + 12, kx + 9, cy + 30], fill=(30, 30, 30, 255))
        draw.ellipse([kx - 5, cy + 16, kx + 5, cy + 26], fill=(120, 120, 120, 255))
    # Světla
    draw.rectangle([cx + 24, cy + 5, cx + 28, cy + 12], fill=(255, 240, 100, 255))
    draw.rectangle([cx - 28, cy + 5, cx - 24, cy + 12], fill=(200, 80, 80, 255))

    img.save("assets/car.png")
    print("✓ car.png vygenerován")


def vytvor_strom(velikost=72):
    """Vytvoří strom s kulatou korunou."""
    img = Image.new("RGBA", (velikost, velikost), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    cx, cy = velikost // 2, velikost // 2
    # Kmen
    draw.rectangle([cx - 5, cy + 4, cx + 5, cy + 30], fill=(120, 80, 40, 255))
    # Kořeny
    draw.line([cx - 5, cy + 28, cx - 14, cy + 34], fill=(100, 65, 30, 255), width=3)
    draw.line([cx + 5, cy + 28, cx + 14, cy + 34], fill=(100, 65, 30, 255), width=3)
    # Koruna – více vrstev zelené
    draw.ellipse([cx - 24, cy - 26, cx + 24, cy + 10], fill=(40, 140, 40, 255))
    draw.ellipse([cx - 20, cy - 30, cx + 20, cy + 5], fill=(60, 170, 60, 255))
    draw.ellipse([cx - 16, cy - 32, cx + 16, cy, ], fill=(80, 190, 60, 255))
    # Odlesk
    draw.ellipse([cx - 10, cy - 28, cx + 2, cy - 16], fill=(120, 220, 80, 120))

    img.save("assets/tree.png")
    print("✓ tree.png vygenerován")


def vytvor_dum(velikost=84):
    """Vytvoří domeček se střechou."""
    img = Image.new("RGBA", (velikost, velikost), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    cx, cy = velikost // 2, velikost // 2
    # Stěny
    draw.rectangle([cx - 26, cy - 6, cx + 26, cy + 32], fill=(220, 200, 160, 255))
    # Střecha
    draw.polygon([
        (cx - 30, cy - 6), (cx, cy - 36), (cx + 30, cy - 6)
    ], fill=(180, 70, 50, 255))
    # Střecha – tmavší spodní okraj
    draw.line([cx - 30, cy - 6, cx + 30, cy - 6], fill=(140, 50, 30, 255), width=3)
    # Dveře
    draw.rectangle([cx - 7, cy + 10, cx + 7, cy + 32], fill=(120, 80, 40, 255))
    draw.ellipse([cx + 4, cy + 20, cx + 7, cy + 23], fill=(240, 200, 60, 255))
    # Okna
    for wx in [cx - 20, cx + 10]:
        draw.rectangle([wx, cy, wx + 14, cy + 12], fill=(160, 210, 255, 220))
        draw.line([wx + 7, cy, wx + 7, cy + 12], fill=(180, 180, 180, 255), width=1)
        draw.line([wx, cy + 6, wx + 14, cy + 6], fill=(180, 180, 180, 255), width=1)
    # Komín
    draw.rectangle([cx + 12, cy - 36, cx + 20, cy - 18], fill=(180, 90, 70, 255))
    draw.rectangle([cx + 10, cy - 40, cx + 22, cy - 36], fill=(160, 70, 50, 255))

    img.save("assets/house.png")
    print("✓ house.png vygenerován")


def vytvor_oblak(velikost=100):
    """Vytvoří bílý oblak."""
    img = Image.new("RGBA", (velikost, velikost), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    cx, cy = velikost // 2, velikost // 2
    # Záře
    glow = Image.new("RGBA", (velikost, velikost), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse([cx - 40, cy - 25, cx + 40, cy + 20], fill=(220, 230, 255, 60))
    glow = glow.filter(ImageFilter.GaussianBlur(radius=8))
    img = Image.alpha_composite(img, glow)

    draw = ImageDraw.Draw(img)
    # Oblak – více překrývajících se elips
    for ox, oy, rr in [
        (0, 5, 28), (-22, 8, 20), (22, 8, 20),
        (-10, -5, 22), (10, -5, 22), (0, -10, 18),
    ]:
        draw.ellipse([cx + ox - rr, cy + oy - rr, cx + ox + rr, cy + oy + rr],
                     fill=(250, 252, 255, 240))

    img.save("assets/cloud.png")
    print("✓ cloud.png vygenerován")


if __name__ == "__main__":
    print("Generování textur pro hru 'Kočka co sní vesmír'...")
    print("=" * 50)

    vytvor_pozadi()
    vytvor_kocku()
    vytvor_hvezdu()
    vytvor_asteroid()
    vytvor_mesic()
    vytvor_planetu()
    vytvor_slunce()
    vytvor_galaxii()

    # Level 1 – Laborka
    vytvor_lab_pozadi()
    vytvor_virus()
    vytvor_bakterii()
    vytvor_krvinku()
    vytvor_amoebu()
    vytvor_prvoka()
    vytvor_roztoce()

    # Level 2 – Zahrada
    vytvor_zahradni_pozadi()
    vytvor_mravence()
    vytvor_mouchu()
    vytvor_brouka()
    vytvor_cerva()
    vytvor_mys()
    vytvor_jezka()

    # Level 3 – Město
    vytvor_mestske_pozadi()
    vytvor_psa()
    vytvor_cloveka()
    vytvor_auto()
    vytvor_strom()
    vytvor_dum()
    vytvor_oblak()

    print("=" * 50)
    print("Všechny textury byly úspěšně vygenerovány do složky assets/")
    print("Nyní můžete spustit hru: python main.py")
