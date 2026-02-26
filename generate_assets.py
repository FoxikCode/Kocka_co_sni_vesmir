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

    print("=" * 50)
    print("Všechny textury byly úspěšně vygenerovány do složky assets/")
    print("Nyní můžete spustit hru: python main.py")
