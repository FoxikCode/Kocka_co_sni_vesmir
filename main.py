"""
Kočka co sní vesmír - Hlavní herní soubor
==========================================
Kočka se pohybuje po vesmírné mapě, jí vesmírné objekty a s každým
snědeným objektem se zvětšuje. Cíl hry je sníst celý vesmír!

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

# Definice vesmírných objektů: název, soubor textury, základní velikost, min. velikost kočky pro snězení
OBJEKTY = [
    {"nazev": "Hvězda",   "soubor": "star.png",     "zakladni_velikost": 24,  "min_velikost_kocky": 40},
    {"nazev": "Asteroid", "soubor": "asteroid.png",  "zakladni_velikost": 38,  "min_velikost_kocky": 50},
    {"nazev": "Měsíc",    "soubor": "moon.png",      "zakladni_velikost": 52,  "min_velikost_kocky": 70},
    {"nazev": "Planeta",  "soubor": "planet.png",    "zakladni_velikost": 68,  "min_velikost_kocky": 100},
    {"nazev": "Slunce",   "soubor": "sun.png",       "zakladni_velikost": 90,  "min_velikost_kocky": 150},
    {"nazev": "Galaxie",  "soubor": "galaxy.png",    "zakladni_velikost": 120, "min_velikost_kocky": 220},
]

# Počty objektů na mapě
MAX_OBJEKTU_KAZDEHO_DRUHU = 3

# Růst kočky při snězení objektu (přičteno k velikosti)
RUST_PO_SNEZENI = {
    "Hvězda":   4,
    "Asteroid": 7,
    "Měsíc":    12,
    "Planeta":  20,
    "Slunce":   35,
    "Galaxie":  60,
}


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

    def __init__(self, textura):
        """Inicializace kočky uprostřed obrazovky."""
        self.textura_orig = textura
        self.velikost = 64          # Počáteční velikost kočky v pixelech
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

    def snezt(self, objekt):
        """Zpracuje snězení objektu – zvětší kočku."""
        rust = RUST_PO_SNEZENI.get(objekt.nazev, 5)
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

        # Herní stav
        self.kocka = Kocka(self.textury["cat"])
        self.objekty = []          # Seznam aktivních objektů na mapě
        self.stav = "hra"          # "hra", "vyhra", "pauza"
        self.zprava_snezeni = None  # Zpráva při snězení objektu (název + čas zobrazení)
        self.cas_zpravy = 0

        # Fonty pro zobrazení textu
        self.font_velky = pygame.font.SysFont("segoeui", 36, bold=True)
        self.font_stredni = pygame.font.SysFont("segoeui", 24)
        self.font_maly = pygame.font.SysFont("segoeui", 18)

        # Naplnění mapy objekty při startu
        self._naplni_objekty()

        # Pozadí (přetiluje celé okno)
        self.pozadi = pygame.transform.scale(self.textury["background"], (SIRKA, VYSKA))

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
        """Naplní mapu počátečními objekty."""
        for typ in OBJEKTY:
            for _ in range(MAX_OBJEKTU_KAZDEHO_DRUHU):
                self._pridej_objekt(typ)

    def _pridej_objekt(self, typ=None):
        """Přidá nový vesmírný objekt na náhodné místo na mapě."""
        if typ is None:
            # Vyber náhodný typ objektu (s váhami – menší objekty se objevují častěji)
            vahy = [5, 4, 3, 2, 1, 0.5]
            typ = random.choices(OBJEKTY, weights=vahy)[0]

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
                # Restart hry po výhře
                if self.stav == "vyhra" and udalost.key == pygame.K_r:
                    self.__init__()
                    return True

        # Pohyb kočky
        if self.stav == "hra":
            klaves_stav = pygame.key.get_pressed()
            self.kocka.pohyb(klaves_stav)

        return True

    def _zkontroluj_kolize(self):
        """Zkontroluje kolize kočky s vesmírnými objekty."""
        snedeno = []
        for obj in self.objekty:
            # Detekce kruhové kolize (přesnější než rect)
            dx = self.kocka.x - obj.x
            dy = self.kocka.y - obj.y
            vzdalenost = (dx * dx + dy * dy) ** 0.5
            prah_kolize = (self.kocka.velikost + obj.velikost) * 0.35

            if vzdalenost < prah_kolize:
                if self.kocka.muze_snizt(obj):
                    # Kočka snědla objekt!
                    snedeno.append(obj)
                    self.kocka.snezt(obj)
                    self.zprava_snezeni = "Snědena: " + obj.nazev + "!"
                    self.cas_zpravy = 120  # 2 sekundy při 60 FPS

                    # Výhra – snezení galaxie
                    if obj.nazev == "Galaxie":
                        self.stav = "vyhra"

        # Odstranění snědených objektů
        for obj in snedeno:
            self.objekty.remove(obj)
            # Respawn nového objektu (kromě galaxie)
            if obj.nazev != "Galaxie":
                # Přidáme nový objekt s malou prodlevou (náhodný typ)
                vahy = [5, 4, 3, 2, 1, 0.5]
                novy_typ = random.choices(OBJEKTY, weights=vahy)[0]
                self._pridej_objekt(novy_typ)

    def _doplneni_objektu(self):
        """Průběžně doplňuje objekty na mapě, aby jich bylo vždy dost."""
        pocty = {typ["nazev"]: 0 for typ in OBJEKTY}
        for obj in self.objekty:
            pocty[obj.nazev] = pocty.get(obj.nazev, 0) + 1

        for typ in OBJEKTY:
            while pocty[typ["nazev"]] < MAX_OBJEKTU_KAZDEHO_DRUHU:
                # Galaxii přidáme jen pokud ještě nebyla snězena
                if typ["nazev"] == "Galaxie" and self.stav == "vyhra":
                    break
                self._pridej_objekt(typ)
                pocty[typ["nazev"]] += 1

    def _vykresli_ui(self):
        """Vykreslí herní uživatelské rozhraní (skóre, velikost kočky, atd.)."""
        # Panel nahoře – poloprůhledné pozadí
        panel = pygame.Surface((SIRKA, 50), pygame.SRCALPHA)
        panel.fill((0, 0, 30, 160))
        self.okno.blit(panel, (0, 0))

        # Počet snědených objektů
        text_snezeno = self.font_stredni.render(
            "Snězeno: " + str(self.kocka.snedeno), True, BILA
        )
        self.okno.blit(text_snezeno, (15, 12))

        # Aktuální velikost kočky
        text_velikost = self.font_stredni.render(
            "Velikost: " + str(self.kocka.velikost), True, SVETLE_MODRA
        )
        self.okno.blit(text_velikost, (220, 12))

        # Nápověda – co může kočka sníst
        dalsi = self._co_muze_snizt()
        if dalsi:
            text_cil = self.font_maly.render(
                "Může sníst: " + dalsi, True, ZLUTA
            )
        else:
            text_cil = self.font_maly.render(
                "Vše snězeno! Hledej galaxii!", True, ZLUTA
            )
        self.okno.blit(text_cil, (450, 16))

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
        for typ in OBJEKTY:
            if self.kocka.velikost >= typ["min_velikost_kocky"]:
                mozne.append(typ["nazev"])
        # Vrátíme jen ty, které jsou ještě na mapě a kočka je může sníst
        na_mape = {obj.nazev for obj in self.objekty}
        return ", ".join(n for n in mozne if n in na_mape) or None

    def _vykresli_vyhranu_obrazovku(self):
        """Zobrazí obrazovku výhry."""
        # Poloprůhledný tmavý překryv
        overlay = pygame.Surface((SIRKA, VYSKA), pygame.SRCALPHA)
        overlay.fill((0, 0, 20, 180))
        self.okno.blit(overlay, (0, 0))

        # Nadpis
        text_vitez = self.font_velky.render("VYHRÁLI JSTE!", True, ZLUTA)
        x = SIRKA // 2 - text_vitez.get_width() // 2
        self.okno.blit(text_vitez, (x, VYSKA // 2 - 100))

        # Podnadpis
        text_popis = self.font_stredni.render(
            "Kočka snědla celý vesmír!", True, SVETLE_MODRA
        )
        x = SIRKA // 2 - text_popis.get_width() // 2
        self.okno.blit(text_popis, (x, VYSKA // 2 - 50))

        # Statistiky
        text_stat = self.font_stredni.render(
            "Snězeno objektů: " + str(self.kocka.snedeno) + "   |   Finální velikost: " + str(self.kocka.velikost),
            True, BILA
        )
        x = SIRKA // 2 - text_stat.get_width() // 2
        self.okno.blit(text_stat, (x, VYSKA // 2))

        # Restart
        text_restart = self.font_stredni.render("Stiskněte R pro novou hru", True, ZELENA)
        x = SIRKA // 2 - text_restart.get_width() // 2
        self.okno.blit(text_restart, (x, VYSKA // 2 + 60))

    def _vykresli_ukazatel_jedlosti(self):
        """Vedle každého objektu zobrazí malý indikátor, zda ho kočka může sníst."""
        for obj in self.objekty:
            muze = self.kocka.muze_snizt(obj)
            if muze:
                # Zelený kroužek – dostupný objekt
                barva = (100, 255, 100)
            else:
                # Červený kroužek – nedostupný (kočka je moc malá)
                barva = (255, 80, 80)

            # Malý indikátor pod objektem
            ind_x = obj.x
            ind_y = obj.y + obj.velikost // 2 + 6
            pygame.draw.circle(self.okno, barva, (ind_x, ind_y), 4)

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

            # Obrazovka výhry
            if self.stav == "vyhra":
                self._vykresli_vyhranu_obrazovku()

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
