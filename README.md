# Kočka co sní vesmír 🐱🌌

Jednoduchá 2D hra v Pythonu a Pygame, kde ovládáte kosmickou kočku. Kočka se pohybuje po vesmírné mapě, jí vesmírné objekty a s každým snědeným objektem se zvětšuje. Cíl hry je sníst celý vesmír!

## Popis hry

Kočka začíná malá a může nejprve jíst pouze hvězdy. S každým snědeným objektem roste a může pojídat stále větší objekty – asteroidy, měsíce, planety, slunce a nakonec celé galaxie. Hra končí výhrou po snězení galaxie.

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
| `R` | Nová hra (po výhře) |
| `ESC` | Ukončení hry |

## Pravidla hry

- Kočka může sníst pouze objekty, u kterých je dostatečně velká.
- **Zelená tečka** pod objektem = kočka ho může sníst.
- **Červená tečka** pod objektem = kočka ještě není dost velká.
- Po snězení objektu se kočka zvětší.
- Nové objekty se průběžně objevují na náhodných místech.
- Hra končí výhrou, když kočka sní galaxii.

## Pořadí objektů od nejmenšího po největší

1. ⭐ **Hvězda** – lze jíst od začátku
2. ☄️ **Asteroid** – po několika hvězdách
3. 🌙 **Měsíc** – střední objekty
4. 🪐 **Planeta** – velké objekty
5. ☀️ **Slunce** – velmi velké objekty
6. 🌌 **Galaxie** – finální objekt, snězením vyhrajete!

## Technické požadavky

- Python 3.8+
- Pygame 2.0+
- Pillow 9.0+
- Rozlišení: 1024×768
- FPS: 60