"""
Kočka co sní vesmír - Hlavní herní soubor
==========================================
Kočka začíná v laborce jako malý tvor a postupně roste od mikroskopické
úrovně až po vesmír. Hra má 4 levely: Laborka → Zahrada → Město → Vesmír.

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
ORANZOVA = (255, 160, 40)

# Rychlost kočky (px/snímek)
RYCHLOST_KOCKY = 3

# Počty objektů každého druhu na mapě
MAX_OBJEKTU_KAZDEHO_DRUHU = 3

# Definice levelů – od laborky po vesmír
LEVELY = [
    {
        "cislo": 1,
        "nazev": "Laborka",
        "popis": "Jsi miniaturní kočka v laboratorní misce!\nSněz co nejvíce a vyrosteš...",
        "pozadi_soubor": "lab_bg.png",
        "objekty": [
            {"nazev": "Virus",    "soubor": "virus.png",      "zakladni_velikost": 10, "min_velikost_kocky": 10},
            {"nazev": "Bakterie", "soubor": "bacterium.png",  "zakladni_velikost": 14, "min_velikost_kocky": 16},
            {"nazev": "Krvinka",  "soubor": "blood_cell.png", "zakladni_velikost": 18, "min_velikost_kocky": 22},
            {"nazev": "Améba",    "soubor": "amoeba.png",     "zakladni_velikost": 24, "min_velikost_kocky": 32},
            {"nazev": "Prvok",    "soubor": "protozoa.png",   "zakladni_velikost": 32, "min_velikost_kocky": 44},
            {"nazev": "Roztoč",   "soubor": "mite.png",       "zakladni_velikost": 42, "min_velikost_kocky": 58},
        ],
        "rust": {"Virus": 2, "Bakterie": 3, "Krvinka": 5, "Améba": 8, "Prvok": 12, "Roztoč": 18},
        "zacatecni_velikost": 12,
        "velikost_pro_postup": 160,
        "posledni": False,
    },
    {
        "cislo": 2,
        "nazev": "Zahrada",
        "popis": "Kočka vyrostla a ocitá se na zahradě!\nSněz hmyz a malá zvířata...",
        "pozadi_soubor": "garden_bg.png",
        "objekty": [
            {"nazev": "Mravenec", "soubor": "ant.png",       "zakladni_velikost": 14, "min_velikost_kocky": 20},
            {"nazev": "Moucha",   "soubor": "fly.png",       "zakladni_velikost": 18, "min_velikost_kocky": 26},
            {"nazev": "Brouk",    "soubor": "beetle.png",    "zakladni_velikost": 26, "min_velikost_kocky": 38},
            {"nazev": "Červ",     "soubor": "worm.png",      "zakladni_velikost": 34, "min_velikost_kocky": 50},
            {"nazev": "Myš",      "soubor": "mouse.png",     "zakladni_velikost": 48, "min_velikost_kocky": 72},
            {"nazev": "Ježek",    "soubor": "hedgehog.png",  "zakladni_velikost": 65, "min_velikost_kocky": 105},
        ],
        "rust": {"Mravenec": 3, "Moucha": 5, "Brouk": 9, "Červ": 14, "Myš": 22, "Ježek": 38},
        "zacatecni_velikost": 30,
        "velikost_pro_postup": 360,
        "posledni": False,
    },
    {
        "cislo": 3,
        "nazev": "Město",
        "popis": "Kočka je obrovská a prochází ulicemi města!\nSněz auta, domy i mraky...",
        "pozadi_soubor": "city_bg.png",
        "objekty": [
            {"nazev": "Pes",    "soubor": "dog.png",   "zakladni_velikost": 18, "min_velikost_kocky": 26},
            {"nazev": "Člověk", "soubor": "human.png", "zakladni_velikost": 26, "min_velikost_kocky": 38},
            {"nazev": "Auto",   "soubor": "car.png",   "zakladni_velikost": 36, "min_velikost_kocky": 54},
            {"nazev": "Strom",  "soubor": "tree.png",  "zakladni_velikost": 50, "min_velikost_kocky": 78},
            {"nazev": "Dům",    "soubor": "house.png", "zakladni_velikost": 68, "min_velikost_kocky": 115},
            {"nazev": "Mrak",   "soubor": "cloud.png", "zakladni_velikost": 90, "min_velikost_kocky": 170},
        ],
        "rust": {"Pes": 7, "Člověk": 11, "Auto": 19, "Strom": 30, "Dům": 52, "Mrak": 88},
        "zacatecni_velikost": 60,
        "velikost_pro_postup": 580,
        "posledni": False,
    },
    {
        "cislo": 4,
        "nazev": "Vesmír",
        "popis": "Kočka vstoupila do vesmíru!\nSněz galaxii a získej vesmírné vítězství!",
        "pozadi_soubor": "background.png",
        "objekty": [
            {"nazev": "Hvězda",   "soubor": "star.png",     "zakladni_velikost": 24,  "min_velikost_kocky": 40},
            {"nazev": "Asteroid", "soubor": "asteroid.png", "zakladni_velikost": 38,  "min_velikost_kocky": 58},
            {"nazev": "Měsíc",    "soubor": "moon.png",     "zakladni_velikost": 52,  "min_velikost_kocky": 88},
            {"nazev": "Planeta",  "soubor": "planet.png",   "zakladni_velikost": 68,  "min_velikost_kocky": 130},
            {"nazev": "Slunce",   "soubor": "sun.png",      "zakladni_velikost": 90,  "min_velikost_kocky": 200},
            {"nazev": "Galaxie",  "soubor": "galaxy.png",   "zakladni_velikost": 120, "min_velikost_kocky": 300},
        ],
        "rust": {"Hvězda": 4, "Asteroid": 7, "Měsíc": 12, "Planeta": 20, "Slunce": 35, "Galaxie": 60},
        "zacatecni_velikost": 100,
        "velikost_pro_postup": None,  # Poslední level – výhra snězením Galaxie
        "posledni": True,
    },
]


class HerniObjekt:
    """Třída reprezentující jeden herní objekt na mapě (pro všechny levely)."""

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
        self.velikost = zacatecni_velikost
        self.x = SIRKA // 2
        self.y = VYSKA // 2
        self.rychlost = RYCHLOST_KOCKY
        self.snedeno = 0            # Počet snědených objektů (celkem)
        self.smer = "prava"         # Aktuální směr pohybu pro otočení
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

        polomer = self.velikost // 2
        self.x = max(polomer, min(SIRKA - polomer, self.x + pohyb_x))
        self.y = max(polomer, min(VYSKA - polomer, self.y + pohyb_y))
        self.rect.x = self.x - polomer
        self.rect.y = self.y - polomer

        if pohyb_x != 0 or pohyb_y != 0:
            self.animacni_cas += 0.2

    def snezt(self, objekt, rust_tabulka):
        """Zpracuje snězení objektu – zvětší kočku."""
        rust = rust_tabulka.get(objekt.nazev, 5)
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

    def __init__(self):
        """Inicializace hry – vytvoří okno, načte textury, připraví herní objekty."""
        self.okno = pygame.display.set_mode((SIRKA, VYSKA))
        pygame.display.set_caption(NAZEV_HRY)
        self.hodiny = pygame.time.Clock()

        # Načtení textur
        self.textury = self._nacti_textury()

        # Fonty
        self.font_velky = pygame.font.SysFont("segoeui", 36, bold=True)
        self.font_stredni = pygame.font.SysFont("segoeui", 24)
        self.font_maly = pygame.font.SysFont("segoeui", 18)

        # Herní stav – "intro", "hra", "level_complete", "vyhra"
        self.aktualni_level_idx = 0
        self.stav = "intro"
        self.zprava_snezeni = None
        self.cas_zpravy = 0

        # Level_complete animace (časovač)
        self.level_complete_cas = 0

        # Inicializace kočky a prvního levelu
        level = LEVELY[self.aktualni_level_idx]
        self.kocka = Kocka(self.textury["cat"], level["zacatecni_velikost"])
        self.objekty = []
        self._nacti_level(self.aktualni_level_idx)

    def _nacti_textury(self):
        """Načte všechny textury ze složky assets/."""
        textury = {}
        soubory = {
            "cat":        "cat.png",
            "background": "background.png",
            "star":       "star.png",
            "asteroid":   "asteroid.png",
            "moon":       "moon.png",
            "planet":     "planet.png",
            "sun":        "sun.png",
            "galaxy":     "galaxy.png",
            # Level 1 – Laborka
            "lab_bg":     "lab_bg.png",
            "virus":      "virus.png",
            "bacterium":  "bacterium.png",
            "blood_cell": "blood_cell.png",
            "amoeba":     "amoeba.png",
            "protozoa":   "protozoa.png",
            "mite":       "mite.png",
            # Level 2 – Zahrada
            "garden_bg":  "garden_bg.png",
            "ant":        "ant.png",
            "fly":        "fly.png",
            "beetle":     "beetle.png",
            "worm":       "worm.png",
            "mouse":      "mouse.png",
            "hedgehog":   "hedgehog.png",
            # Level 3 – Město
            "city_bg":    "city_bg.png",
            "dog":        "dog.png",
            "human":      "human.png",
            "car":        "car.png",
            "tree":       "tree.png",
            "house":      "house.png",
            "cloud":      "cloud.png",
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

    def _nacti_level(self, idx):
        """Načte data levelu – pozadí a objekty."""
        level = LEVELY[idx]
        pozadi_klic = level["pozadi_soubor"].replace(".png", "")
        self.pozadi = pygame.transform.scale(self.textury[pozadi_klic], (SIRKA, VYSKA))
        self.objekty = []
        self._naplni_objekty()

    def _naplni_objekty(self):
        """Naplní mapu počátečními objekty aktuálního levelu."""
        level = LEVELY[self.aktualni_level_idx]
        for typ in level["objekty"]:
            for _ in range(MAX_OBJEKTU_KAZDEHO_DRUHU):
                self._pridej_objekt(typ)

    def _pridej_objekt(self, typ=None):
        """Přidá nový objekt na náhodné místo na mapě (dle aktuálního levelu)."""
        level = LEVELY[self.aktualni_level_idx]
        if typ is None:
            vahy = [5, 4, 3, 2, 1, 0.5][:len(level["objekty"])]
            typ = random.choices(level["objekty"], weights=vahy)[0]

        klic_textury = typ["soubor"].replace(".png", "")
        textura = self.textury[klic_textury]
        obj = HerniObjekt(typ, textura)

        # Ujistit se, že nový objekt není příliš blízko kočce
        min_vzdalenost = self.kocka.velikost * 3
        for _ in range(20):
            dx = obj.x - self.kocka.x
            dy = obj.y - self.kocka.y
            if (dx * dx + dy * dy) ** 0.5 > min_vzdalenost:
                break
            obj.x = random.randint(50, SIRKA - 50)
            obj.y = random.randint(50, VYSKA - 50)

        self.objekty.append(obj)

    def _zpracuj_vstup(self):
        """Zpracuje události (klávesnice, zavření okna)."""
        for udalost in pygame.event.get():
            if udalost.type == pygame.QUIT:
                return False
            if udalost.type == pygame.KEYDOWN:
                if udalost.key == pygame.K_ESCAPE:
                    return False
                # Intro – jakákoli klávesa spustí hru
                if self.stav == "intro":
                    self.stav = "hra"
                # Level přechod – jakákoli klávesa po prodlevě
                elif self.stav == "level_complete" and self.level_complete_cas > 90:
                    self._postup_na_dalsi_level()
                # Výhra – R restartuje celou hru
                elif self.stav == "vyhra" and udalost.key == pygame.K_r:
                    self.__init__()
                    return True

        if self.stav == "hra":
            klaves_stav = pygame.key.get_pressed()
            self.kocka.pohyb(klaves_stav)

        return True

    def _postup_na_dalsi_level(self):
        """Přejde na další level."""
        self.aktualni_level_idx += 1
        level = LEVELY[self.aktualni_level_idx]
        # Nastaví velikost kočky na startovní pro nový level, ale zachová celkový počet snězených
        snedeno_celkem = self.kocka.snedeno
        self.kocka = Kocka(self.textury["cat"], level["zacatecni_velikost"])
        self.kocka.snedeno = snedeno_celkem
        self._nacti_level(self.aktualni_level_idx)
        self.stav = "intro"
        self.zprava_snezeni = None
        self.cas_zpravy = 0

    def _zkontroluj_kolize(self):
        """Zkontroluje kolize kočky s objekty a výhru/postup do dalšího levelu."""
        level = LEVELY[self.aktualni_level_idx]
        rust_tabulka = level["rust"]
        snedeno = []

        for obj in self.objekty:
            dx = self.kocka.x - obj.x
            dy = self.kocka.y - obj.y
            vzdalenost = (dx * dx + dy * dy) ** 0.5
            prah_kolize = (self.kocka.velikost + obj.velikost) * 0.35

            if vzdalenost < prah_kolize and self.kocka.muze_snizt(obj):
                snedeno.append(obj)
                self.kocka.snezt(obj, rust_tabulka)
                self.zprava_snezeni = "Snědeno: " + obj.nazev + "!"
                self.cas_zpravy = 120

                # Výhra snězením Galaxie (pouze v posledním levelu)
                if level["posledni"] and obj.nazev == "Galaxie":
                    self.stav = "vyhra"

        for obj in snedeno:
            self.objekty.remove(obj)
            # Respawn, pokud to není konec levelu (Galaxie v posledním)
            if not (level["posledni"] and obj.nazev == "Galaxie"):
                vahy = [5, 4, 3, 2, 1, 0.5][:len(level["objekty"])]
                novy_typ = random.choices(level["objekty"], weights=vahy)[0]
                self._pridej_objekt(novy_typ)

        # Kontrola podmínky pro postup do dalšího levelu (ne v posledním)
        if (self.stav == "hra" and not level["posledni"]
                and level["velikost_pro_postup"] is not None
                and self.kocka.velikost >= level["velikost_pro_postup"]):
            self.stav = "level_complete"
            self.level_complete_cas = 0

    def _doplneni_objektu(self):
        """Průběžně doplňuje objekty na mapě."""
        level = LEVELY[self.aktualni_level_idx]
        pocty = {typ["nazev"]: 0 for typ in level["objekty"]}
        for obj in self.objekty:
            pocty[obj.nazev] = pocty.get(obj.nazev, 0) + 1

        for typ in level["objekty"]:
            while pocty[typ["nazev"]] < MAX_OBJEKTU_KAZDEHO_DRUHU:
                if level["posledni"] and typ["nazev"] == "Galaxie" and self.stav == "vyhra":
                    break
                self._pridej_objekt(typ)
                pocty[typ["nazev"]] += 1

    def _vykresli_ui(self):
        """Vykreslí herní uživatelské rozhraní."""
        level = LEVELY[self.aktualni_level_idx]

        # Panel nahoře
        panel = pygame.Surface((SIRKA, 50), pygame.SRCALPHA)
        panel.fill((0, 0, 30, 160))
        self.okno.blit(panel, (0, 0))

        # Level badge
        text_level = self.font_stredni.render(
            "Level " + str(level["cislo"]) + ": " + level["nazev"], True, ORANZOVA
        )
        self.okno.blit(text_level, (15, 12))

        # Počet snědených objektů
        text_snezeno = self.font_stredni.render(
            "Snězeno: " + str(self.kocka.snedeno), True, BILA
        )
        self.okno.blit(text_snezeno, (310, 12))

        # Aktuální velikost kočky
        text_velikost = self.font_stredni.render(
            "Velikost: " + str(self.kocka.velikost), True, SVETLE_MODRA
        )
        self.okno.blit(text_velikost, (490, 12))

        # Progress bar do dalšího levelu (ne v posledním)
        if not level["posledni"] and level["velikost_pro_postup"] is not None:
            zacatek = level["zacatecni_velikost"]
            cil = level["velikost_pro_postup"]
            prog = min(1.0, (self.kocka.velikost - zacatek) / max(1, cil - zacatek))
            bar_x, bar_y, bar_w, bar_h = SIRKA - 170, 14, 150, 16
            pygame.draw.rect(self.okno, (60, 60, 60), (bar_x, bar_y, bar_w, bar_h))
            pygame.draw.rect(self.okno, ZELENA, (bar_x, bar_y, int(bar_w * prog), bar_h))
            pygame.draw.rect(self.okno, BILA, (bar_x, bar_y, bar_w, bar_h), 1)
            text_prog = self.font_maly.render("do dalšího levelu", True, SEDA)
            self.okno.blit(text_prog, (bar_x, bar_y + bar_h + 2))

        # Zpráva o snězení (dočasná)
        if self.cas_zpravy > 0:
            surf_zprava = self.font_velky.render(self.zprava_snezeni, True, ZELENA)
            x_zprava = SIRKA // 2 - surf_zprava.get_width() // 2
            self.okno.blit(surf_zprava, (x_zprava, VYSKA // 2 - 60))
            self.cas_zpravy -= 1

        # Ovládání (malé, v rohu dole)
        text_ovladani = self.font_maly.render("WASD / Šipky: pohyb  |  ESC: konec", True, SEDA)
        self.okno.blit(text_ovladani, (SIRKA - text_ovladani.get_width() - 10, VYSKA - 22))

    def _vykresli_intro_obrazovku(self):
        """Zobrazí úvodní obrazovku aktuálního levelu."""
        level = LEVELY[self.aktualni_level_idx]

        overlay = pygame.Surface((SIRKA, VYSKA), pygame.SRCALPHA)
        overlay.fill((0, 0, 20, 200))
        self.okno.blit(overlay, (0, 0))

        # Číslo levelu
        text_level = self.font_velky.render(
            "LEVEL " + str(level["cislo"]), True, ORANZOVA
        )
        x = SIRKA // 2 - text_level.get_width() // 2
        self.okno.blit(text_level, (x, VYSKA // 2 - 120))

        # Název levelu
        text_nazev = self.font_velky.render(level["nazev"].upper(), True, ZLUTA)
        x = SIRKA // 2 - text_nazev.get_width() // 2
        self.okno.blit(text_nazev, (x, VYSKA // 2 - 70))

        # Popis (více řádků)
        for i, radek in enumerate(level["popis"].split("\n")):
            text_p = self.font_stredni.render(radek, True, BILA)
            x = SIRKA // 2 - text_p.get_width() // 2
            self.okno.blit(text_p, (x, VYSKA // 2 - 10 + i * 32))

        # Výzva
        text_start = self.font_stredni.render("Stiskněte libovolnou klávesu...", True, ZELENA)
        x = SIRKA // 2 - text_start.get_width() // 2
        self.okno.blit(text_start, (x, VYSKA // 2 + 80))

    def _vykresli_level_complete_obrazovku(self):
        """Zobrazí obrazovku po dokončení levelu."""
        level = LEVELY[self.aktualni_level_idx]
        self.level_complete_cas += 1

        overlay = pygame.Surface((SIRKA, VYSKA), pygame.SRCALPHA)
        overlay.fill((0, 20, 0, 190))
        self.okno.blit(overlay, (0, 0))

        # Nadpis
        text_done = self.font_velky.render(
            "LEVEL " + str(level["cislo"]) + " DOKONČEN!", True, ZLUTA
        )
        x = SIRKA // 2 - text_done.get_width() // 2
        self.okno.blit(text_done, (x, VYSKA // 2 - 110))

        # Název dalšího levelu
        dalsi = LEVELY[self.aktualni_level_idx + 1]
        text_dalsi = self.font_velky.render(
            "Další: Level " + str(dalsi["cislo"]) + " – " + dalsi["nazev"], True, SVETLE_MODRA
        )
        x = SIRKA // 2 - text_dalsi.get_width() // 2
        self.okno.blit(text_dalsi, (x, VYSKA // 2 - 55))

        # Statistiky
        text_stat = self.font_stredni.render(
            "Snězeno celkem: " + str(self.kocka.snedeno), True, BILA
        )
        x = SIRKA // 2 - text_stat.get_width() // 2
        self.okno.blit(text_stat, (x, VYSKA // 2 + 10))

        # Tlačítko pokračovat (po prodlevě)
        if self.level_complete_cas > 90:
            text_pokr = self.font_stredni.render("Stiskněte libovolnou klávesu...", True, ZELENA)
            x = SIRKA // 2 - text_pokr.get_width() // 2
            self.okno.blit(text_pokr, (x, VYSKA // 2 + 60))

    def _vykresli_vyhranu_obrazovku(self):
        """Zobrazí obrazovku výhry (po snězení Galaxie)."""
        overlay = pygame.Surface((SIRKA, VYSKA), pygame.SRCALPHA)
        overlay.fill((0, 0, 20, 180))
        self.okno.blit(overlay, (0, 0))

        text_vitez = self.font_velky.render("VYHRÁLI JSTE!", True, ZLUTA)
        x = SIRKA // 2 - text_vitez.get_width() // 2
        self.okno.blit(text_vitez, (x, VYSKA // 2 - 110))

        text_popis = self.font_stredni.render(
            "Kočka snědla celý vesmír!", True, SVETLE_MODRA
        )
        x = SIRKA // 2 - text_popis.get_width() // 2
        self.okno.blit(text_popis, (x, VYSKA // 2 - 55))

        text_stat = self.font_stredni.render(
            "Snězeno celkem: " + str(self.kocka.snedeno) + "   |   Finální velikost: " + str(self.kocka.velikost),
            True, BILA
        )
        x = SIRKA // 2 - text_stat.get_width() // 2
        self.okno.blit(text_stat, (x, VYSKA // 2))

        text_restart = self.font_stredni.render("Stiskněte R pro novou hru", True, ZELENA)
        x = SIRKA // 2 - text_restart.get_width() // 2
        self.okno.blit(text_restart, (x, VYSKA // 2 + 60))

    def _vykresli_ukazatel_jedlosti(self):
        """Vedle každého objektu zobrazí malý indikátor dostupnosti."""
        for obj in self.objekty:
            barva = (100, 255, 100) if self.kocka.muze_snizt(obj) else (255, 80, 80)
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
                if snimek % 180 == 0:
                    self._doplneni_objektu()
                for obj in self.objekty:
                    obj.aktualizuj()

            # Kreslení
            self.okno.blit(self.pozadi, (0, 0))

            for obj in self.objekty:
                obj.vykresli(self.okno)

            self._vykresli_ukazatel_jedlosti()
            self.kocka.vykresli(self.okno)
            self._vykresli_ui()

            if self.stav == "intro":
                self._vykresli_intro_obrazovku()
            elif self.stav == "level_complete":
                self._vykresli_level_complete_obrazovku()
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

    hra = Hra()
    hra.spust()


if __name__ == "__main__":
    main()
