"""
Kočka co sní vesmír - Hlavní herní soubor
==========================================
Kočka prochází pěti prostředími podobně jako ve hře Tasty Planet:
  Level 1 – Laboratoř  (bakterie, molekuly, buňky …)
  Level 2 – Kuchyně    (drobečky, mravenci, myška …)
  Level 3 – Zahrada    (květ, slepice, králík, pes, člověk …)
  Level 4 – Město      (auta, domy, paneláky, hora …)
  Level 5 – Vesmír     (hvězdy, planety, galaxie …)
Sněz boss-objekt každého levelu a postup dál!

Ovládání: Šipky nebo WASD
"""

import pygame
import random
import os
import sys
import math

# Inicializace Pygame
pygame.init()

# Konstanty okna
SIRKA = 1024
VYSKA = 768
FPS = 60
NAZEV_HRY = "Kočka co sní vesmír"

# Barvy
BILA = (255, 255, 255)
CERNA = (0, 0, 0)
ZLUTA = (255, 220, 50)
SVETLE_MODRA = (150, 200, 255)
ZELENA = (100, 220, 100)
CERVENA = (255, 100, 100)
FIALOVA = (180, 100, 255)
SEDA = (150, 150, 150)
TMAVE_MODRA = (20, 30, 80)

# Rychlost kočky (px/snímek)
RYCHLOST_KOCKY = 3

# Počty objektů na mapě
MAX_OBJEKTU_KAZDEHO_DRUHU = 3

# ─── Definice levelů ─────────────────────────────────────────────────────────
# Každý level má své prostředí, objekty a boss-objekt.
# Snězením boss-objektu kočka postoupí do dalšího levelu.
LEVELY = [
    {
        "nazev": "Laboratoř",
        "popis": "Jsi malá kočka v laboratoři. Sněz vše co najdeš!",
        "pozadi": "background_lab",
        "kocka_start": 20,
        "objekty": [
            {"nazev": "Bakterie",      "soubor": "bacteria.png",  "zakladni_velikost": 8,  "min_velikost_kocky": 15},
            {"nazev": "Molekula",      "soubor": "molecule.png",  "zakladni_velikost": 12, "min_velikost_kocky": 20},
            {"nazev": "Buňka",         "soubor": "cell.png",      "zakladni_velikost": 18, "min_velikost_kocky": 27},
            {"nazev": "Kapička",       "soubor": "droplet.png",   "zakladni_velikost": 26, "min_velikost_kocky": 38},
            {"nazev": "Petriho miska", "soubor": "petri.png",     "zakladni_velikost": 38, "min_velikost_kocky": 55},
        ],
        "sef": "Petriho miska",
        "rust": {"Bakterie": 3, "Molekula": 5, "Buňka": 8, "Kapička": 14, "Petriho miska": 22},
    },
    {
        "nazev": "Kuchyně",
        "popis": "Kočka unikla z laboratoře do kuchyně!",
        "pozadi": "background_kitchen",
        "kocka_start": 40,
        "objekty": [
            {"nazev": "Drobeček",  "soubor": "crumb.png",      "zakladni_velikost": 14, "min_velikost_kocky": 35},
            {"nazev": "Cukr",      "soubor": "sugar.png",       "zakladni_velikost": 20, "min_velikost_kocky": 42},
            {"nazev": "Mravenec",  "soubor": "ant.png",         "zakladni_velikost": 28, "min_velikost_kocky": 55},
            {"nazev": "Šváb",      "soubor": "cockroach.png",   "zakladni_velikost": 38, "min_velikost_kocky": 73},
            {"nazev": "Myška",     "soubor": "mouse.png",       "zakladni_velikost": 52, "min_velikost_kocky": 98},
        ],
        "sef": "Myška",
        "rust": {"Drobeček": 4, "Cukr": 7, "Mravenec": 12, "Šváb": 20, "Myška": 35},
    },
    {
        "nazev": "Zahrada",
        "popis": "Kočka vyšla ven na zahradu!",
        "pozadi": "background_garden",
        "kocka_start": 55,
        "objekty": [
            {"nazev": "Květ",    "soubor": "flower.png",   "zakladni_velikost": 18, "min_velikost_kocky": 50},
            {"nazev": "Slepice", "soubor": "chicken.png",  "zakladni_velikost": 28, "min_velikost_kocky": 65},
            {"nazev": "Králík",  "soubor": "rabbit.png",   "zakladni_velikost": 40, "min_velikost_kocky": 90},
            {"nazev": "Pes",     "soubor": "dog.png",      "zakladni_velikost": 55, "min_velikost_kocky": 120},
            {"nazev": "Člověk",  "soubor": "person.png",   "zakladni_velikost": 72, "min_velikost_kocky": 162},
        ],
        "sef": "Člověk",
        "rust": {"Květ": 5, "Slepice": 12, "Králík": 22, "Pes": 38, "Člověk": 60},
    },
    {
        "nazev": "Město",
        "popis": "Obrovská kočka terorizuje město!",
        "pozadi": "background_city",
        "kocka_start": 70,
        "objekty": [
            {"nazev": "Auto",    "soubor": "car.png",       "zakladni_velikost": 40, "min_velikost_kocky": 65},
            {"nazev": "Dům",     "soubor": "house.png",     "zakladni_velikost": 55, "min_velikost_kocky": 90},
            {"nazev": "Autobus", "soubor": "bus.png",       "zakladni_velikost": 70, "min_velikost_kocky": 125},
            {"nazev": "Panelák", "soubor": "building.png",  "zakladni_velikost": 88, "min_velikost_kocky": 175},
            {"nazev": "Hora",    "soubor": "mountain.png",  "zakladni_velikost": 110, "min_velikost_kocky": 240},
        ],
        "sef": "Hora",
        "rust": {"Auto": 15, "Dům": 28, "Autobus": 48, "Panelák": 75, "Hora": 120},
    },
    {
        "nazev": "Vesmír",
        "popis": "Kočka snědla Zemi a teď jí vesmír!",
        "pozadi": "background",
        "kocka_start": 64,
        "objekty": [
            {"nazev": "Hvězda",   "soubor": "star.png",     "zakladni_velikost": 24,  "min_velikost_kocky": 40},
            {"nazev": "Asteroid", "soubor": "asteroid.png",  "zakladni_velikost": 38,  "min_velikost_kocky": 50},
            {"nazev": "Měsíc",    "soubor": "moon.png",      "zakladni_velikost": 52,  "min_velikost_kocky": 70},
            {"nazev": "Planeta",  "soubor": "planet.png",    "zakladni_velikost": 68,  "min_velikost_kocky": 100},
            {"nazev": "Slunce",   "soubor": "sun.png",       "zakladni_velikost": 90,  "min_velikost_kocky": 150},
            {"nazev": "Galaxie",  "soubor": "galaxy.png",    "zakladni_velikost": 120, "min_velikost_kocky": 220},
        ],
        "sef": "Galaxie",
        "rust": {"Hvězda": 4, "Asteroid": 7, "Měsíc": 12, "Planeta": 20, "Slunce": 35, "Galaxie": 60},
    },
]


class VesmirskyObjekt:
    """Třída reprezentující jeden vesmírný objekt na mapě."""

    def __init__(self, typ_dat, textura):
        """Inicializace objektu s daným typem a texturou."""
        self.nazev = typ_dat["nazev"]
        self.zakladni_velikost = typ_dat["zakladni_velikost"]
        self.min_velikost_kocky = typ_dat["min_velikost_kocky"]
        self.textura_orig = textura

        # Náhodná velikost (±20% od základní)
        variace = random.uniform(0.85, 1.15)
        self.velikost = int(self.zakladni_velikost * variace)

        # Náhodná pozice (mimo okraje)
        okraj = self.velikost + 10
        self.x = random.randint(okraj, SIRKA - okraj)
        self.y = random.randint(okraj, VYSKA - okraj)

        # Mírné pulsování objektu
        self.puls_cas = random.uniform(0, 6.28)
        self.puls_rychlost = random.uniform(0.02, 0.05)

        # Připravení textury ve správné velikosti
        self._aktualizuj_texturu()

    def _aktualizuj_texturu(self):
        """Přepočítá texturu na aktuální velikost."""
        self.textura = pygame.transform.scale(
            self.textura_orig, (self.velikost, self.velikost)
        )
        self.rect = pygame.Rect(
            self.x - self.velikost // 2,
            self.y - self.velikost // 2,
            self.velikost,
            self.velikost
        )

    def aktualizuj(self):
        """Aktualizuje animaci pulsování."""
        self.puls_cas += self.puls_rychlost

    def vykresli(self, povrch):
        """Vykreslí objekt na herní plochu."""
        # Mírné pulsování velikosti
        puls = math.sin(self.puls_cas) * 0.05
        vel_puls = int(self.velikost * (1 + puls))
        if vel_puls != self.textura.get_width():
            tex = pygame.transform.scale(self.textura_orig, (vel_puls, vel_puls))
            rect = tex.get_rect(center=(self.x, self.y))
            povrch.blit(tex, rect)
        else:
            rect = self.textura.get_rect(center=(self.x, self.y))
            povrch.blit(self.textura, rect)


class Kocka:
    """Třída reprezentující hráčovu kočku."""

    def __init__(self, textura, zacatecni_velikost=64):
        """Inicializace kočky uprostřed obrazovky."""
        self.textura_orig = textura
        self.velikost = zacatecni_velikost  # Počáteční velikost kočky v pixelech
        self.x = SIRKA // 2
        self.y = VYSKA // 2
        self.rychlost = RYCHLOST_KOCKY
        self.snedeno = 0            # Počet snědených objektů
        self.smer = "prava"         # Aktuální směr pohybu pro otočení

        # Nastavení animace
        self.animacni_cas = 0

        self._aktualizuj_texturu()

    def _aktualizuj_texturu(self):
        """Přepočítá texturu na aktuální velikost."""
        self.textura = pygame.transform.scale(
            self.textura_orig, (self.velikost, self.velikost)
        )
        self.rect = pygame.Rect(
            self.x - self.velikost // 2,
            self.y - self.velikost // 2,
            self.velikost,
            self.velikost
        )

    def pohyb(self, klaves_stav):
        """Zpracuje vstup z klávesnice a pohybuje kočkou."""
        pohyb_x = 0
        pohyb_y = 0

        # Šipky nebo WASD
        if klaves_stav[pygame.K_LEFT] or klaves_stav[pygame.K_a]:
            pohyb_x -= self.rychlost
            self.smer = "leva"
        if klaves_stav[pygame.K_RIGHT] or klaves_stav[pygame.K_d]:
            pohyb_x += self.rychlost
            self.smer = "prava"
        if klaves_stav[pygame.K_UP] or klaves_stav[pygame.K_w]:
            pohyb_y -= self.rychlost
        if klaves_stav[pygame.K_DOWN] or klaves_stav[pygame.K_s]:
            pohyb_y += self.rychlost

        # Pohyb kočky s omezením na hranice okna
        polomer = self.velikost // 2
        self.x = max(polomer, min(SIRKA - polomer, self.x + pohyb_x))
        self.y = max(polomer, min(VYSKA - polomer, self.y + pohyb_y))

        # Aktualizace rect
        self.rect.x = self.x - polomer
        self.rect.y = self.y - polomer

        # Animace chůze
        if pohyb_x != 0 or pohyb_y != 0:
            self.animacni_cas += 0.2

    def snezt(self, rust=5):
        """Zpracuje snězení objektu – zvětší kočku o zadaný počet pixelů."""
        self.velikost += rust
        self.snedeno += 1
        self._aktualizuj_texturu()

    def muze_snizt(self, objekt):
        """Vrátí True, pokud je kočka dostatečně velká, aby snědla objekt."""
        return self.velikost >= objekt.min_velikost_kocky

    def vykresli(self, povrch):
        """Vykreslí kočku na herní plochu (otočí dle směru)."""
        if self.smer == "leva":
            tex = pygame.transform.flip(self.textura, True, False)
        else:
            tex = self.textura
        rect = tex.get_rect(center=(self.x, self.y))
        povrch.blit(tex, rect)


class Hra:
    """Hlavní herní třída, která řídí celý průběh hry."""

    def __init__(self, level=0):
        """Inicializace hry – vytvoří okno, načte textury, připraví herní objekty."""
        self.okno = pygame.display.set_mode((SIRKA, VYSKA))
        pygame.display.set_caption(NAZEV_HRY)
        self.hodiny = pygame.time.Clock()

        # Aktuální level
        self.aktualni_level = level
        self.data_levelu = LEVELY[level]

        # Načtení textur
        self.textury = self._nacti_textury()

        # Herní stav: "hra", "prechod_levelu", "vyhra"
        self.kocka = Kocka(self.textury["cat"], self.data_levelu["kocka_start"])
        self.objekty = []
        self.stav = "hra"
        self.zprava_snezeni = None
        self.cas_zpravy = 0

        # Fonty pro zobrazení textu
        self.font_velky = pygame.font.SysFont("segoeui", 36, bold=True)
        self.font_stredni = pygame.font.SysFont("segoeui", 24)
        self.font_maly = pygame.font.SysFont("segoeui", 18)

        # Naplnění mapy objekty při startu
        self._naplni_objekty()

        # Pozadí specifické pro aktuální level
        self.pozadi = pygame.transform.scale(
            self.textury[self.data_levelu["pozadi"]], (SIRKA, VYSKA)
        )

    def _nacti_textury(self):
        """Načte všechny textury ze složky assets/ (pro všechny levely najednou)."""
        textury = {}
        soubory = {
            # Společné
            "cat":                "cat.png",
            # Pozadí
            "background":         "background.png",
            "background_lab":     "background_lab.png",
            "background_kitchen": "background_kitchen.png",
            "background_garden":  "background_garden.png",
            "background_city":    "background_city.png",
            # Level 1 – Laboratoř
            "bacteria":   "bacteria.png",
            "molecule":   "molecule.png",
            "cell":       "cell.png",
            "droplet":    "droplet.png",
            "petri":      "petri.png",
            # Level 2 – Kuchyně
            "crumb":      "crumb.png",
            "sugar":      "sugar.png",
            "ant":        "ant.png",
            "cockroach":  "cockroach.png",
            "mouse":      "mouse.png",
            # Level 3 – Zahrada
            "flower":     "flower.png",
            "chicken":    "chicken.png",
            "rabbit":     "rabbit.png",
            "dog":        "dog.png",
            "person":     "person.png",
            # Level 4 – Město
            "car":        "car.png",
            "house":      "house.png",
            "bus":        "bus.png",
            "building":   "building.png",
            "mountain":   "mountain.png",
            # Level 5 – Vesmír
            "star":       "star.png",
            "asteroid":   "asteroid.png",
            "moon":       "moon.png",
            "planet":     "planet.png",
            "sun":        "sun.png",
            "galaxy":     "galaxy.png",
        }

        for klic, soubor in soubory.items():
            cesta = os.path.join("assets", soubor)
            if not os.path.exists(cesta):
                print(f"CHYBA: Textura '{cesta}' nenalezena!")
                print("Spusťte nejprve: python generate_assets.py")
                pygame.quit()
                sys.exit(1)
            textury[klic] = pygame.image.load(cesta).convert_alpha()

        return textury

    def _naplni_objekty(self):
        """Naplní mapu počátečními objekty aktuálního levelu."""
        for typ in self.data_levelu["objekty"]:
            for _ in range(MAX_OBJEKTU_KAZDEHO_DRUHU):
                self._pridej_objekt(typ)

    def _pridej_objekt(self, typ=None):
        """Přidá nový objekt na náhodné místo na mapě."""
        if typ is None:
            objekty_levelu = self.data_levelu["objekty"]
            vahy = [5, 4, 3, 2, 1, 0.5][:len(objekty_levelu)]
            typ = random.choices(objekty_levelu, weights=vahy)[0]

        klic_textury = typ["soubor"].replace(".png", "")
        textura = self.textury[klic_textury]
        obj = VesmirskyObjekt(typ, textura)

        # Ujistit se, že nový objekt není příliš blízko kočce
        min_vzdalenost = self.kocka.velikost * 3
        pokusy = 0
        while pokusy < 20:
            dx = obj.x - self.kocka.x
            dy = obj.y - self.kocka.y
            if (dx * dx + dy * dy) ** 0.5 > min_vzdalenost:
                break
            obj.x = random.randint(50, SIRKA - 50)
            obj.y = random.randint(50, VYSKA - 50)
            pokusy += 1

        self.objekty.append(obj)

    def _zpracuj_vstup(self):
        """Zpracuje události (klávesnice, zavření okna)."""
        for udalost in pygame.event.get():
            if udalost.type == pygame.QUIT:
                return False
            if udalost.type == pygame.KEYDOWN:
                if udalost.key == pygame.K_ESCAPE:
                    return False
                # Přechod na další level
                if self.stav == "prechod_levelu" and udalost.key in (
                    pygame.K_r, pygame.K_RETURN, pygame.K_SPACE
                ):
                    self.__init__(self.aktualni_level + 1)
                    return True
                # Restart hry od začátku po výhře
                if self.stav == "vyhra" and udalost.key == pygame.K_r:
                    self.__init__(0)
                    return True

        # Pohyb kočky
        if self.stav == "hra":
            klaves_stav = pygame.key.get_pressed()
            self.kocka.pohyb(klaves_stav)

        return True

    def _zkontroluj_kolize(self):
        """Zkontroluje kolize kočky s objekty."""
        snedeno = []
        for obj in self.objekty:
            dx = self.kocka.x - obj.x
            dy = self.kocka.y - obj.y
            vzdalenost = (dx * dx + dy * dy) ** 0.5
            prah_kolize = (self.kocka.velikost + obj.velikost) * 0.35

            if vzdalenost < prah_kolize:
                if self.kocka.muze_snizt(obj):
                    snedeno.append(obj)
                    rust = self.data_levelu["rust"].get(obj.nazev, 5)
                    self.kocka.snezt(rust)
                    self.zprava_snezeni = "Snědena: " + obj.nazev + "!"
                    self.cas_zpravy = 120  # 2 sekundy při 60 FPS

                    # Boss snědena → konec levelu
                    if obj.nazev == self.data_levelu["sef"]:
                        if self.aktualni_level + 1 < len(LEVELY):
                            self.stav = "prechod_levelu"
                        else:
                            self.stav = "vyhra"

        # Odstranění snědených objektů a respawn
        for obj in snedeno:
            self.objekty.remove(obj)
            if obj.nazev != self.data_levelu["sef"]:
                vahy = [5, 4, 3, 2, 1, 0.5][:len(self.data_levelu["objekty"])]
                novy_typ = random.choices(self.data_levelu["objekty"], weights=vahy)[0]
                self._pridej_objekt(novy_typ)

    def _doplneni_objektu(self):
        """Průběžně doplňuje objekty na mapě, aby jich bylo vždy dost."""
        pocty = {typ["nazev"]: 0 for typ in self.data_levelu["objekty"]}
        for obj in self.objekty:
            pocty[obj.nazev] = pocty.get(obj.nazev, 0) + 1

        for typ in self.data_levelu["objekty"]:
            while pocty[typ["nazev"]] < MAX_OBJEKTU_KAZDEHO_DRUHU:
                if typ["nazev"] == self.data_levelu["sef"] and self.stav in ("prechod_levelu", "vyhra"):
                    break
                self._pridej_objekt(typ)
                pocty[typ["nazev"]] += 1

    def _vykresli_ui(self):
        """Vykreslí herní uživatelské rozhraní."""
        # Panel nahoře – poloprůhledné pozadí
        panel = pygame.Surface((SIRKA, 50), pygame.SRCALPHA)
        panel.fill((0, 0, 30, 160))
        self.okno.blit(panel, (0, 0))

        # Číslo a název levelu
        text_level = self.font_stredni.render(
            "Level " + str(self.aktualni_level + 1) + ": " + self.data_levelu["nazev"],
            True, ZLUTA
        )
        self.okno.blit(text_level, (15, 12))

        # Počet snědených objektů
        text_snezeno = self.font_maly.render(
            "Snězeno: " + str(self.kocka.snedeno), True, BILA
        )
        self.okno.blit(text_snezeno, (310, 16))

        # Aktuální velikost kočky
        text_velikost = self.font_maly.render(
            "Velikost: " + str(self.kocka.velikost), True, SVETLE_MODRA
        )
        self.okno.blit(text_velikost, (460, 16))

        # Nápověda – co může kočka sníst
        dalsi = self._co_muze_snizt()
        if dalsi:
            text_cil = self.font_maly.render("Může sníst: " + dalsi, True, ZELENA)
        else:
            text_cil = self.font_maly.render(
                "Hledej: " + self.data_levelu["sef"] + "!", True, ZLUTA
            )
        self.okno.blit(text_cil, (610, 16))

        # Zpráva o snězení (dočasná)
        if self.cas_zpravy > 0:
            surf_zprava = self.font_velky.render(self.zprava_snezeni, True, ZELENA)
            x_zprava = SIRKA // 2 - surf_zprava.get_width() // 2
            self.okno.blit(surf_zprava, (x_zprava, VYSKA // 2 - 60))
            self.cas_zpravy -= 1

        # Ovládání (malé, v rohu)
        text_ovladani = self.font_maly.render("WASD / Šipky: pohyb  |  ESC: konec", True, SEDA)
        self.okno.blit(text_ovladani, (SIRKA - text_ovladani.get_width() - 10, VYSKA - 22))

    def _co_muze_snizt(self):
        """Vrátí seznam názvů objektů, které kočka může nyní sníst."""
        mozne = []
        for typ in self.data_levelu["objekty"]:
            if self.kocka.velikost >= typ["min_velikost_kocky"]:
                mozne.append(typ["nazev"])
        na_mape = {obj.nazev for obj in self.objekty}
        return ", ".join(n for n in mozne if n in na_mape) or None

    def _vykresli_prechod_levelu(self):
        """Zobrazí obrazovku přechodu mezi levely."""
        overlay = pygame.Surface((SIRKA, VYSKA), pygame.SRCALPHA)
        overlay.fill((0, 20, 0, 210))
        self.okno.blit(overlay, (0, 0))

        dalsi = LEVELY[self.aktualni_level + 1]

        text_hotovo = self.font_velky.render(
            "LEVEL " + str(self.aktualni_level + 1) + " DOKONČEN!", True, ZLUTA
        )
        x = SIRKA // 2 - text_hotovo.get_width() // 2
        self.okno.blit(text_hotovo, (x, VYSKA // 2 - 130))

        text_snezenym = self.font_stredni.render(
            "Snědena: " + self.data_levelu["sef"] + "!", True, ZELENA
        )
        x = SIRKA // 2 - text_snezenym.get_width() // 2
        self.okno.blit(text_snezenym, (x, VYSKA // 2 - 70))

        text_dalsi = self.font_stredni.render(
            "Další prostředí: " + dalsi["nazev"], True, SVETLE_MODRA
        )
        x = SIRKA // 2 - text_dalsi.get_width() // 2
        self.okno.blit(text_dalsi, (x, VYSKA // 2 - 15))

        text_popis = self.font_stredni.render(dalsi["popis"], True, BILA)
        x = SIRKA // 2 - text_popis.get_width() // 2
        self.okno.blit(text_popis, (x, VYSKA // 2 + 40))

        text_pokracuj = self.font_stredni.render(
            "Stiskněte ENTER nebo MEZERNÍK pro pokračování", True, ZELENA
        )
        x = SIRKA // 2 - text_pokracuj.get_width() // 2
        self.okno.blit(text_pokracuj, (x, VYSKA // 2 + 100))

    def _vykresli_vyhranu_obrazovku(self):
        """Zobrazí obrazovku konečné výhry (všechny levely dokončeny)."""
        overlay = pygame.Surface((SIRKA, VYSKA), pygame.SRCALPHA)
        overlay.fill((0, 0, 20, 180))
        self.okno.blit(overlay, (0, 0))

        text_vitez = self.font_velky.render("KOČKA SNĚDLA CELÝ VESMÍR!", True, ZLUTA)
        x = SIRKA // 2 - text_vitez.get_width() // 2
        self.okno.blit(text_vitez, (x, VYSKA // 2 - 110))

        text_popis = self.font_stredni.render(
            "Gratulujeme! Prošli jste všemi " + str(len(LEVELY)) + " úrovněmi!", True, SVETLE_MODRA
        )
        x = SIRKA // 2 - text_popis.get_width() // 2
        self.okno.blit(text_popis, (x, VYSKA // 2 - 55))

        text_stat = self.font_stredni.render(
            "Snězeno objektů: " + str(self.kocka.snedeno)
            + "   |   Finální velikost: " + str(self.kocka.velikost),
            True, BILA
        )
        x = SIRKA // 2 - text_stat.get_width() // 2
        self.okno.blit(text_stat, (x, VYSKA // 2))

        text_restart = self.font_stredni.render(
            "Stiskněte R pro novou hru od Level 1", True, ZELENA
        )
        x = SIRKA // 2 - text_restart.get_width() // 2
        self.okno.blit(text_restart, (x, VYSKA // 2 + 60))

    def _vykresli_ukazatel_jedlosti(self):
        """Vedle každého objektu zobrazí malý indikátor, zda ho kočka může sníst."""
        for obj in self.objekty:
            muze = self.kocka.muze_snizt(obj)
            barva = (100, 255, 100) if muze else (255, 80, 80)
            ind_x = obj.x
            ind_y = obj.y + obj.velikost // 2 + 6
            pygame.draw.circle(self.okno, barva, (ind_x, ind_y), 4)

    def spust(self):
        """Hlavní herní smyčka."""
        bezi = True
        snimek = 0

        while bezi:
            bezi = self._zpracuj_vstup()

            if self.stav == "hra":
                self._zkontroluj_kolize()

                # Pravidelné doplňování objektů (každých 180 snímků = 3 sekundy)
                if snimek % 180 == 0:
                    self._doplneni_objektu()

                # Aktualizace animací objektů
                for obj in self.objekty:
                    obj.aktualizuj()

            # Kreslení
            self.okno.blit(self.pozadi, (0, 0))

            for obj in self.objekty:
                obj.vykresli(self.okno)

            self._vykresli_ukazatel_jedlosti()
            self.kocka.vykresli(self.okno)
            self._vykresli_ui()

            if self.stav == "prechod_levelu":
                self._vykresli_prechod_levelu()
            elif self.stav == "vyhra":
                self._vykresli_vyhranu_obrazovku()

            pygame.display.flip()
            self.hodiny.tick(FPS)
            snimek += 1

        pygame.quit()
        sys.exit()


def main():
    """Vstupní bod hry."""
    # Kontrola, zda existuje složka assets
    if not os.path.exists("assets"):
        print("CHYBA: Složka 'assets' neexistuje.")
        print("Spusťte nejprve: python generate_assets.py")
        sys.exit(1)

    hra = Hra(level=0)
    hra.spust()


if __name__ == "__main__":
    main()
