# Kočka co sní vesmír 🐱🌌

Hra v Pythonu a Pygame inspirovaná Tasty Planet. Ovládáte kočku, která prochází **třemi levely** – od mikroskopického světa laboratoře až po celý vesmír. S každým snědeným objektem kočka roste a může pojídat stále větší věci!

## Levely

### 🔬 Level 1: Laboratoř
Kočka začíná jako miniaturní tvor v laboratoři. Sněz vše od bakterií po krysu a unikni!

| Objekt | Pořadí |
|--------|--------|
| 🦠 Bakterie | od začátku |
| 🔵 Buňka | po několika bakteriích |
| 🐜 Mravenec | po buňkách |
| 🪰 Moucha | střední objekty |
| 🐭 Myš | velké objekty |
| 🐀 **Krysa** | **boss – snězením postoupíš do města** |

### 🏙️ Level 2: Město
Kočka dobývá město. Sněz vše od psů po mrakodrap!

| Objekt | Pořadí |
|--------|--------|
| 🐕 Pes | od začátku |
| 🧍 Člověk | brzy |
| 🚗 Auto | střední objekty |
| 🚌 Autobus | větší objekty |
| 🏠 Dům | velké objekty |
| 🏢 **Mrakodrap** | **boss – snězením postoupíš do vesmíru** |

### 🌌 Level 3: Vesmír
Kočka dobývá vesmír. Sněz hvězdy, planety a nakonec celou galaxii!

| Objekt | Pořadí |
|--------|--------|
| ⭐ Hvězda | od začátku |
| ☄️ Asteroid | brzy |
| 🌙 Měsíc | střední objekty |
| 🪐 Planeta | velké objekty |
| ☀️ Slunce | velmi velké objekty |
| 🌌 **Galaxie** | **finální boss – výhra!** |

## Otevření ve Visual Studio Code

1. **Stáhněte projekt** – klikněte na zelené tlačítko **Code → Download ZIP** na GitHubu a rozbalte archiv, nebo použijte Git:
   ```bash
   git clone https://github.com/FoxikCode/Kocka_co_sni_vesmir.git
   ```
2. **Otevřete složku ve VS Code** – spusťte VS Code, zvolte **Soubor → Otevřít složku…** (`Ctrl+K Ctrl+O`) a vyberte staženou složku `Kocka_co_sni_vesmir`.
3. **Nainstalujte doporučená rozšíření** – VS Code nabídne instalaci rozšíření Python a Pylance. Klikněte **Nainstalovat vše**.
4. **Vyberte Python interpreter** – stiskněte `Ctrl+Shift+P`, napište `Python: Select Interpreter` a vyberte dostupný Python 3.
5. **Nainstalujte závislosti** – otevřete terminál ve VS Code (`Ctrl+ˇ`) a spusťte:
   ```bash
   pip install -r requirements.txt
   ```
6. **Vygenerujte textury** – v panelu **Spustit a ladit** (`Ctrl+Shift+D`) vyberte konfiguraci **Generovat textury** a stiskněte ▶ (nebo použijte terminál: `python generate_assets.py`).
7. **Spusťte hru** – vyberte konfiguraci **Spustit hru** a stiskněte ▶ (nebo `python main.py` v terminálu).

> 💡 **Tip:** Hru i generátor textur můžete také spustit přímo klávesou `F5` po otevření příslušného souboru (`main.py` nebo `generate_assets.py`).

## Instalace závislostí

```bash
pip install -r requirements.txt
```

## Generování textur

Před prvním spuštěním hry je potřeba vygenerovat herní textury:

```bash
python generate_assets.py
```

Skript vytvoří složku `assets/` a vygeneruje všechny potřebné PNG soubory pomocí knihovny Pillow.

## Spuštění hry

```bash
python main.py
```

## Ovládání

| Klávesa | Akce |
|---------|------|
| `W` nebo `↑` | Pohyb nahoru |
| `S` nebo `↓` | Pohyb dolů |
| `A` nebo `←` | Pohyb doleva |
| `D` nebo `→` | Pohyb doprava |
| `libovolná klávesa` | Pokračovat na další level |
| `R` | Nová hra (po výhře) |
| `ESC` | Ukončení hry |

## Pravidla hry

- Kočka může sníst pouze objekty, u kterých je dostatečně velká.
- **Zelená tečka** pod objektem = kočka ho může sníst.
- **Červená tečka** pod objektem = kočka ještě není dost velká.
- Po snězení objektu se kočka zvětší.
- Nové objekty se průběžně objevují na náhodných místech.
- Sněz **boss objekt** levelu (Krysa / Mrakodrap / Galaxie) a postoupíš do dalšího levelu.
- Po každém levelu se kočka přesune do nového prostředí a začne v odpovídající velikosti.

## Technické požadavky

- Python 3.8+
- Pygame 2.0+
- Pillow 9.0+
- Rozlišení: 1024×768
- FPS: 60