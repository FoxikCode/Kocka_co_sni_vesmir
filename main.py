"""
Kočka co sní vesmír - Hlavní herní soubor
==========================================
Hra s více levely inspirovaná Tasty Planet.
Kočka prochází třemi úrovněmi: Laboratoř → Město → Vesmír.

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
ORANZOVA = (255, 160, 30)

# Rychlost kočky (px/snímek)
RYCHLOST_KOCKY = 3

# Definice levelů: Laboratoř → Město → Vesmír
# Každý level má vlastní pozadí, sadu objektů a finální boss objekt.
LEVELY = [
    {
        "cislo": 1,
        "nazev": "Laboratoř",
        "popis": "Sněz krysu a unikni z laboratoře!",
        "pozadi_klic": "bg_lab",
        "pocatecni_velikost_kocky": 16,
        "objekty": [
            {"nazev": "Bakterie",  "soubor": "bacteria.png", "zakladni_velikost": 14, "min_velikost_kocky": 12, "rust": 2},
            {"nazev": "Buňka",    "soubor": "cell.png",     "zakladni_velikost": 20, "min_velikost_kocky": 18, "rust": 3},
            {"nazev": "Mravenec", "soubor": "ant.png",      "zakladni_velikost": 28, "min_velikost_kocky": 24, "rust": 5},
            {"nazev": "Moucha",   "soubor": "fly.png",      "zakladni_velikost": 36, "min_velikost_kocky": 32, "rust": 8},
            {"nazev": "Myš",      "soubor": "mouse.png",    "zakladni_velikost": 46, "min_velikost_kocky": 42, "rust": 12},
            {"nazev": "Krysa",    "soubor": "rat.png",      "zakladni_velikost": 58, "min_velikost_kocky": 54, "rust": 18},
        ],
        "finalni_objekt": "Krysa",
        "zprava_prechodu": "Kočka unikla z laboratoře!",
        "zprava_prechodu2": "Nyní dobyde město!",
    },
    {
        "cislo": 2,
        "nazev": "Město",
        "popis": "Sněz mrakodrap a dobyj celé město!",
        "pozadi_klic": "bg_city",
        "pocatecni_velikost_kocky": 48,
        "objekty": [
            {"nazev": "Pes",       "soubor": "dog.png",        "zakladni_velikost": 52,  "min_velikost_kocky": 44,  "rust": 10},
            {"nazev": "Člověk",    "soubor": "person.png",     "zakladni_velikost": 58,  "min_velikost_kocky": 50,  "rust": 12},
            {"nazev": "Auto",      "soubor": "car.png",        "zakladni_velikost": 68,  "min_velikost_kocky": 62,  "rust": 18},
            {"nazev": "Autobus",   "soubor": "bus.png",        "zakladni_velikost": 80,  "min_velikost_kocky": 74,  "rust": 26},
            {"nazev": "Dům",       "soubor": "house.png",      "zakladni_velikost": 94,  "min_velikost_kocky": 88,  "rust": 36},
            {"nazev": "Mrakodrap", "soubor": "skyscraper.png", "zakladni_velikost": 110, "min_velikost_kocky": 104, "rust": 50},
        ],
        "finalni_objekt": "Mrakodrap",
        "zprava_prechodu": "Kočka dobyla město!",
        "zprava_prechodu2": "Nyní dobyje vesmír!",
    },
    {
        "cislo": 3,
        "nazev": "Vesmír",
        "popis": "Sněz galaxii a dobyj celý vesmír!",
        "pozadi_klic": "background",
        "pocatecni_velikost_kocky": 100,
        "objekty": [
            {"nazev": "Hvězda",   "soubor": "star.png",     "zakladni_velikost": 24,  "min_velikost_kocky": 90,  "rust": 4},
            {"nazev": "Asteroid", "soubor": "asteroid.png", "zakladni_velikost": 38,  "min_velikost_kocky": 110, "rust": 7},
            {"nazev": "Měsíc",    "soubor": "moon.png",     "zakladni_velikost": 52,  "min_velikost_kocky": 130, "rust": 12},
            {"nazev": "Planeta",  "soubor": "planet.png",   "zakladni_velikost": 68,  "min_velikost_kocky": 155, "rust": 20},
            {"nazev": "Slunce",   "soubor": "sun.png",      "zakladni_velikost": 90,  "min_velikost_kocky": 190, "rust": 35},
            {"nazev": "Galaxie",  "soubor": "galaxy.png",   "zakladni_velikost": 120, "min_velikost_kocky": 240, "rust": 60},
        ],
        "finalni_objekt": "Galaxie",
        "zprava_prechodu": "Kočka snědla celý vesmír!",
        "zprava_prechodu2": "",
    },
]

# Počty objektů každého druhu na mapě najednou
MAX_OBJEKTU_KAZDEHO_DRUHU = 3


class VesmirskyObjekt:
    """Třída reprezentující jeden herní objekt na mapě."""

    def __init__(self, typ_dat, textura):
        """Inicializace objektu s daným typem a texturou."""
        self.nazev = typ_dat["nazev"]
        self.zakladni_velikost = typ_dat["zakladni_velikost"]
        self.min_velikost_kocky = typ_dat["min_velikost_kocky"]
        self.rust = typ_dat["rust"]
        self.textura_orig = textura

        # Náhodná velikost (±15% od základní)
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

    def __init__(self, textura, pocatecni_velikost=64):
        """Inicializace kočky uprostřed obrazovky."""
        self.textura_orig = textura
        self.velikost = pocatecni_velikost
        self.x = SIRKA // 2
        self.y = VYSKA // 2
        self.rychlost = RYCHLOST_KOCKY
        self.snedeno = 0
        self.smer = "prava"
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

    def snezt(self, objekt):
        """Zpracuje snězení objektu – zvětší kočku o rust objektu."""
        self.velikost += objekt.rust
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

        # Aktuální level (0-based index do LEVELY)
        self.aktualni_level_idx = 0
        self.level_data = LEVELY[self.aktualni_level_idx]

        # Herní stav: "hra", "prechod_levelu", "vyhra"
        self.kocka = Kocka(self.textury["cat"], self.level_data["pocatecni_velikost_kocky"])
        self.objekty = []
        self.stav = "hra"
        self.zprava_snezeni = None
        self.cas_zpravy = 0
        self.prechod_text = ""
        self.prechod_text2 = ""

        # Fonty pro zobrazení textu
        self.font_velky = pygame.font.SysFont("segoeui", 36, bold=True)
        self.font_stredni = pygame.font.SysFont("segoeui", 24)
        self.font_maly = pygame.font.SysFont("segoeui", 18)

        # Naplnění mapy objekty při startu
        self._naplni_objekty()

        # Pozadí dle aktuálního levelu
        self._aktualizuj_pozadi()

    def _nacti_textury(self):
        """Načte všechny textury ze složky assets/."""
        textury = {}
        soubory = {
            "cat":         "cat.png",
            "background":  "background.png",
            "bg_lab":      "bg_lab.png",
            "bg_city":     "bg_city.png",
            # Vesmírné objekty
            "star":        "star.png",
            "asteroid":    "asteroid.png",
            "moon":        "moon.png",
            "planet":      "planet.png",
            "sun":         "sun.png",
            "galaxy":      "galaxy.png",
            # Laboratorní objekty
            "bacteria":    "bacteria.png",
            "cell":        "cell.png",
            "ant":         "ant.png",
            "fly":         "fly.png",
            "mouse":       "mouse.png",
            "rat":         "rat.png",
            # Městské objekty
            "dog":         "dog.png",
            "person":      "person.png",
            "car":         "car.png",
            "bus":         "bus.png",
            "house":       "house.png",
            "skyscraper":  "skyscraper.png",
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

    def _aktualizuj_pozadi(self):
        """Nastaví pozadí dle aktuálního levelu."""
        klic = self.level_data["pozadi_klic"]
        self.pozadi = pygame.transform.scale(self.textury[klic], (SIRKA, VYSKA))

    def _naplni_objekty(self):
        """Naplní mapu počátečními objekty dle aktuálního levelu."""
        self.objekty = []
        for typ in self.level_data["objekty"]:
            for _ in range(MAX_OBJEKTU_KAZDEHO_DRUHU):
                self._pridej_objekt(typ)

    def _pridej_objekt(self, typ=None):
        """Přidá nový herní objekt na náhodné místo na mapě."""
        if typ is None:
            pocet = len(self.level_data["objekty"])
            vahy = [max(0.5, pocet - i) for i in range(pocet)]
            typ = random.choices(self.level_data["objekty"], weights=vahy)[0]

        klic_textury = typ["soubor"].replace(".png", "")
        textura = self.textury[klic_textury]
        obj = VesmirskyObjekt(typ, textura)

        # Nový objekt nesmí být příliš blízko kočce
        min_vzdalenost = self.kocka.velikost * 3
        for pokusy in range(20):
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
                # Restart hry po výhře
                if self.stav == "vyhra" and udalost.key == pygame.K_r:
                    self.__init__()
                    return True
                # Přechod na další level po stisknutí libovolné klávesy
                if self.stav == "prechod_levelu":
                    self._posun_na_dalsi_level()
                    return True

        # Pohyb kočky pouze během hry
        if self.stav == "hra":
            klaves_stav = pygame.key.get_pressed()
            self.kocka.pohyb(klaves_stav)

        return True

    def _zkontroluj_kolize(self):
        """Zkontroluje kolize kočky s herními objekty."""
        snedeno = []
        for obj in self.objekty:
            dx = self.kocka.x - obj.x
            dy = self.kocka.y - obj.y
            vzdalenost = (dx * dx + dy * dy) ** 0.5
            prah_kolize = (self.kocka.velikost + obj.velikost) * 0.35

            if vzdalenost < prah_kolize:
                if self.kocka.muze_snizt(obj):
                    snedeno.append(obj)
                    self.kocka.snezt(obj)
                    self.zprava_snezeni = "Snědena: " + obj.nazev + "!"
                    self.cas_zpravy = 120  # 2 sekundy při 60 FPS

                    # Detekce dokončení levelu – snězení finálního objektu
                    if obj.nazev == self.level_data["finalni_objekt"]:
                        if self.aktualni_level_idx >= len(LEVELY) - 1:
                            self.stav = "vyhra"
                        else:
                            self.stav = "prechod_levelu"
                            self.prechod_text = self.level_data["zprava_prechodu"]
                            self.prechod_text2 = self.level_data.get("zprava_prechodu2", "")

        for obj in snedeno:
            self.objekty.remove(obj)
            # Respawn – ne pro finální objekt po dokončení levelu
            if self.stav == "hra":
                pocet = len(self.level_data["objekty"])
                vahy = [max(0.5, pocet - i) for i in range(pocet)]
                novy_typ = random.choices(self.level_data["objekty"], weights=vahy)[0]
                self._pridej_objekt(novy_typ)

    def _doplneni_objektu(self):
        """Průběžně doplňuje objekty na mapě, aby jich bylo vždy dost."""
        pocty = {typ["nazev"]: 0 for typ in self.level_data["objekty"]}
        for obj in self.objekty:
            pocty[obj.nazev] = pocty.get(obj.nazev, 0) + 1

        finalni = self.level_data["finalni_objekt"]
        for typ in self.level_data["objekty"]:
            while pocty[typ["nazev"]] < MAX_OBJEKTU_KAZDEHO_DRUHU:
                if typ["nazev"] == finalni and self.stav != "hra":
                    break
                self._pridej_objekt(typ)
                pocty[typ["nazev"]] += 1

    def _vykresli_ui(self):
        """Vykreslí herní uživatelské rozhraní (skóre, level, velikost kočky, atd.)."""
        # Panel nahoře – poloprůhledné pozadí
        panel = pygame.Surface((SIRKA, 50), pygame.SRCALPHA)
        panel.fill((0, 0, 30, 160))
        self.okno.blit(panel, (0, 0))

        # Level info
        text_level = self.font_stredni.render(
            "Level " + str(self.level_data["cislo"]) + ": " + self.level_data["nazev"],
            True, ORANZOVA
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

        # Nápověda – co může kočka sníst
        dalsi = self._co_muze_snizt()
        if dalsi:
            text_cil = self.font_maly.render(
                "Může sníst: " + dalsi, True, ZLUTA
            )
        else:
            text_cil = self.font_maly.render(
                "Sněz " + self.level_data["finalni_objekt"] + "!", True, ZLUTA
            )
        self.okno.blit(text_cil, (690, 16))

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
        for typ in self.level_data["objekty"]:
            if self.kocka.velikost >= typ["min_velikost_kocky"]:
                mozne.append(typ["nazev"])
        na_mape = {obj.nazev for obj in self.objekty}
        return ", ".join(n for n in mozne if n in na_mape) or None

    def _vykresli_vyhranu_obrazovku(self):
        """Zobrazí obrazovku výhry."""
        overlay = pygame.Surface((SIRKA, VYSKA), pygame.SRCALPHA)
        overlay.fill((0, 0, 20, 180))
        self.okno.blit(overlay, (0, 0))

        text_vitez = self.font_velky.render("VYHRÁLI JSTE!", True, ZLUTA)
        x = SIRKA // 2 - text_vitez.get_width() // 2
        self.okno.blit(text_vitez, (x, VYSKA // 2 - 100))

        text_popis = self.font_stredni.render(
            "Kočka snědla celý vesmír!", True, SVETLE_MODRA
        )
        x = SIRKA // 2 - text_popis.get_width() // 2
        self.okno.blit(text_popis, (x, VYSKA // 2 - 50))

        text_stat = self.font_stredni.render(
            "Snězeno objektů: " + str(self.kocka.snedeno) + "   |   Finální velikost: " + str(self.kocka.velikost),
            True, BILA
        )
        x = SIRKA // 2 - text_stat.get_width() // 2
        self.okno.blit(text_stat, (x, VYSKA // 2))

        text_restart = self.font_stredni.render("Stiskněte R pro novou hru", True, ZELENA)
        x = SIRKA // 2 - text_restart.get_width() // 2
        self.okno.blit(text_restart, (x, VYSKA // 2 + 60))

    def _vykresli_prechod_levelu_obrazovku(self):
        """Zobrazí obrazovku přechodu na další level."""
        overlay = pygame.Surface((SIRKA, VYSKA), pygame.SRCALPHA)
        overlay.fill((0, 20, 0, 200))
        self.okno.blit(overlay, (0, 0))

        # Hlavní zpráva
        text_hlavni = self.font_velky.render(self.prechod_text, True, ZLUTA)
        x = SIRKA // 2 - text_hlavni.get_width() // 2
        self.okno.blit(text_hlavni, (x, VYSKA // 2 - 90))

        # Podtext
        if self.prechod_text2:
            text_pod = self.font_stredni.render(self.prechod_text2, True, SVETLE_MODRA)
            x = SIRKA // 2 - text_pod.get_width() // 2
            self.okno.blit(text_pod, (x, VYSKA // 2 - 40))

        # Informace o dalším levelu
        dalsi_idx = self.aktualni_level_idx + 1
        if dalsi_idx < len(LEVELY):
            dalsi = LEVELY[dalsi_idx]
            text_dalsi = self.font_stredni.render(
                "Další level: " + str(dalsi["cislo"]) + " – " + dalsi["nazev"]
                + "  |  " + dalsi["popis"],
                True, ORANZOVA
            )
            x = SIRKA // 2 - text_dalsi.get_width() // 2
            self.okno.blit(text_dalsi, (x, VYSKA // 2 + 10))

        text_pokrac = self.font_stredni.render(
            "Stiskněte libovolnou klávesu pro pokračování", True, ZELENA
        )
        x = SIRKA // 2 - text_pokrac.get_width() // 2
        self.okno.blit(text_pokrac, (x, VYSKA // 2 + 70))

    def _vykresli_ukazatel_jedlosti(self):
        """Vedle každého objektu zobrazí malý indikátor, zda ho kočka může sníst."""
        for obj in self.objekty:
            barva = (100, 255, 100) if self.kocka.muze_snizt(obj) else (255, 80, 80)
            ind_x = obj.x
            ind_y = obj.y + obj.velikost // 2 + 6
            pygame.draw.circle(self.okno, barva, (ind_x, ind_y), 4)

    def _posun_na_dalsi_level(self):
        """Přesune hru na další level."""
        self.aktualni_level_idx += 1
        self.level_data = LEVELY[self.aktualni_level_idx]

        # Reset kočky na počáteční velikost nového levelu
        self.kocka = Kocka(self.textury["cat"], self.level_data["pocatecni_velikost_kocky"])

        self._naplni_objekty()
        self._aktualizuj_pozadi()

        self.stav = "hra"
        self.cas_zpravy = 0
        self.zprava_snezeni = None

    def spust(self):
        """Hlavní herní smyčka."""
        bezi = True
        snimek = 0

        while bezi:
            # Zpracování vstupů
            bezi = self._zpracuj_vstup()

            if self.stav == "hra":
                # Aktualizace herní logiky
                self._zkontroluj_kolize()

                # Pravidelné doplňování objektů (každých 180 snímků = 3 sekundy)
                if snimek % 180 == 0:
                    self._doplneni_objektu()

                # Aktualizace animací objektů
                for obj in self.objekty:
                    obj.aktualizuj()

            # Kreslení
            self.okno.blit(self.pozadi, (0, 0))

            # Vykreslení objektů
            for obj in self.objekty:
                obj.vykresli(self.okno)

            # Indikátory jedlosti
            self._vykresli_ukazatel_jedlosti()

            # Vykreslení kočky
            self.kocka.vykresli(self.okno)

            # UI
            self._vykresli_ui()

            # Obrazovky přechodu/výhry
            if self.stav == "vyhra":
                self._vykresli_vyhranu_obrazovku()
            elif self.stav == "prechod_levelu":
                self._vykresli_prechod_levelu_obrazovku()

            # Zobrazení výsledku na obrazovce
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
