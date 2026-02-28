import pygame
import random
import math
import os
from PIL import Image, ImageDraw

# Inicializace Pygame
pygame.init()

# Konstanty
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700
FPS = 60
BASE_CAT_SIZE = 40
MAX_CAT_SIZE = 250

# Barvy
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARK_GRAY = (40, 40, 40)
LIGHT_GRAY = (200, 200, 200)
LAB_FLOOR = (220, 220, 220)

ALIEN_GREEN_DARK = (30, 120, 60)
ALIEN_GREEN_MAIN = (80, 180, 100)
ALIEN_GREEN_LIGHT = (120, 220, 140)

class TextureGenerator:
    """Generuje textury automaticky pokud neexistují"""
    @staticmethod
    def create_cat_texture(size=100):
        """Vytvoří texturu kočky"""
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Tělo
        draw.ellipse([size*0.1, size*0.2, size*0.9, size*0.8], 
                     fill=(80, 180, 100), outline=(30, 120, 60), width=2)
        
        # Hlava
        head_size = size * 0.4
        head_y = size * 0.25
        draw.ellipse([size*0.3, head_y, size*0.7, head_y + head_size], 
                     fill=(80, 180, 100), outline=(30, 120, 60), width=2)
        
        # Oči
        eye_y = head_y + size * 0.1
        draw.ellipse([size*0.35, eye_y, size*0.45, eye_y + size*0.1], 
                     fill=WHITE, outline=BLACK, width=1)
        draw.ellipse([size*0.55, eye_y, size*0.65, eye_y + size*0.1], 
                     fill=WHITE, outline=BLACK, width=1)
        
        # Pupily
        draw.ellipse([size*0.38, eye_y + size*0.02, size*0.43, eye_y + size*0.07], 
                     fill=BLACK)
        draw.ellipse([size*0.58, eye_y + size*0.02, size*0.63, eye_y + size*0.07], 
                     fill=BLACK)
        
        # Uši
        ear_left = [(size*0.35, head_y), (size*0.25, head_y - size*0.15), (size*0.4, head_y - size*0.05)]
        ear_right = [(size*0.65, head_y), (size*0.75, head_y - size*0.15), (size*0.6, head_y - size*0.05)]
        draw.polygon(ear_left, fill=(80, 180, 100), outline=(30, 120, 60))
        draw.polygon(ear_right, fill=(80, 180, 100), outline=(30, 120, 60))
        
        # Nos
        draw.ellipse([size*0.45, head_y + size*0.2, size*0.55, head_y + size*0.3], 
                     fill=(200, 100, 180), outline=(180, 80, 160))
        
        return pygame.image.fromstring(img.tobytes(), img.size, 'RGBA')
    
    @staticmethod
    def create_bug_texture(size=20):
        """Vytvoří texturu brouka"""
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        draw.ellipse([size*0.2, size*0.3, size*0.8, size*0.8], 
                     fill=(180, 100, 30), outline=(120, 60, 20))
        return pygame.image.fromstring(img.tobytes(), img.size, 'RGBA')
    
    @staticmethod
    def create_mouse_texture(size=20):
        """Vytvoří texturu myši"""
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        draw.ellipse([size*0.1, size*0.2, size*0.9, size*0.9], 
                     fill=(200, 150, 120), outline=(150, 100, 80))
        draw.ellipse([size*0.75, size*0.3, size*0.95, size*0.45], 
                     fill=(200, 150, 120), outline=(150, 100, 80))
        return pygame.image.fromstring(img.tobytes(), img.size, 'RGBA')
    
    @staticmethod
    def create_container_texture(size=20):
        """Vytvoří texturu kontejneru"""
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        draw.rectangle([size*0.1, size*0.1, size*0.9, size*0.9], 
                       fill=(100, 120, 180), outline=(60, 80, 150), width=2)
        draw.line([(size*0.1, size*0.5), (size*0.9, size*0.5)], fill=(60, 80, 150), width=1)
        return pygame.image.fromstring(img.tobytes(), img.size, 'RGBA')
    
    @staticmethod
    def create_plant_texture(size=20):
        """Vytvoří texturu rostliny"""
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        draw.ellipse([size*0.3, size*0.1, size*0.7, size*0.5], 
                     fill=(100, 180, 80), outline=(70, 150, 50))
        draw.ellipse([size*0.1, size*0.4, size*0.4, size*0.8], 
                     fill=(100, 180, 80), outline=(70, 150, 50))
        draw.ellipse([size*0.6, size*0.4, size*0.9, size*0.8], 
                     fill=(100, 180, 80), outline=(70, 150, 50))
        return pygame.image.fromstring(img.tobytes(), img.size, 'RGBA')

    @staticmethod
    def create_lab_floor_texture(size=64):
        """Vytvoří pixel-art texturu podlahy vesmírné laboratoře"""
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        pixels = img.load()

        # Základní barvy kovových panelů
        panel_base = (85, 90, 105)       # tmavě šedý kov
        panel_light = (110, 115, 130)    # světlejší kov
        panel_dark = (60, 65, 78)        # tmavší okraj
        rivet_color = (140, 145, 155)    # nýty
        rivet_shadow = (50, 55, 65)      # stín nýtu
        groove_color = (45, 50, 60)      # drážky mezi panely
        glow_color = (40, 180, 160)      # zeleno-modrý sci-fi glow
        glow_dim = (25, 100, 90)         # tlumený glow
        vent_dark = (35, 38, 48)         # větrací mřížka
        vent_light = (70, 75, 88)        # světlá část mřížky

        # Vyplň základní barvou panelu
        for y in range(size):
            for x in range(size):
                # Jemná variace pro texturu kovu
                noise = ((x * 7 + y * 13) % 5) - 2
                r = max(0, min(255, panel_base[0] + noise))
                g = max(0, min(255, panel_base[1] + noise))
                b = max(0, min(255, panel_base[2] + noise))
                pixels[x, y] = (r, g, b, 255)

        # Drážky mezi panely (kříž uprostřed)
        half = size // 2
        for i in range(size):
            # Horizontální drážka
            pixels[i, half - 1] = groove_color + (255,)
            pixels[i, half] = groove_color + (255,)
            if i > 0:
                pixels[i, half - 2] = panel_dark + (255,)
            if i < size - 1:
                pixels[i, half + 1] = panel_light + (255,)
            # Vertikální drážka
            pixels[half - 1, i] = groove_color + (255,)
            pixels[half, i] = groove_color + (255,)
            if i > 0:
                pixels[half - 2, i] = panel_dark + (255,)
            if i < size - 1:
                pixels[half + 1, i] = panel_light + (255,)

        # Okraj celého tile (pro seamless tiling)
        for i in range(size):
            pixels[i, 0] = groove_color + (255,)
            pixels[i, size - 1] = groove_color + (255,)
            pixels[0, i] = groove_color + (255,)
            pixels[size - 1, i] = groove_color + (255,)

        # Nýty v rozích každého sub-panelu
        rivet_positions = [
            (4, 4), (half - 5, 4), (4, half - 5), (half - 5, half - 5),
            (half + 4, 4), (size - 6, 4), (half + 4, half - 5), (size - 6, half - 5),
            (4, half + 4), (half - 5, half + 4), (4, size - 6), (half - 5, size - 6),
            (half + 4, half + 4), (size - 6, half + 4), (half + 4, size - 6), (size - 6, size - 6),
        ]
        for rx, ry in rivet_positions:
            pixels[rx, ry] = rivet_color + (255,)
            pixels[rx + 1, ry] = rivet_color + (255,)
            pixels[rx, ry + 1] = rivet_color + (255,)
            pixels[rx + 1, ry + 1] = rivet_shadow + (255,)

        # Sci-fi glow proužek v dolním pravém sub-panelu
        glow_y = half + half // 2
        for gx in range(half + 6, size - 6):
            pixels[gx, glow_y] = glow_color + (255,)
            pixels[gx, glow_y - 1] = glow_dim + (255,)
            pixels[gx, glow_y + 1] = glow_dim + (255,)

        # Větrací mřížka v levém horním sub-panelu
        for vy in range(8, half - 6, 4):
            for vx in range(8, half - 6):
                if vy % 4 == 0:
                    pixels[vx, vy] = vent_dark + (255,)
                    pixels[vx, vy + 1] = vent_light + (255,)

        return pygame.image.fromstring(img.tobytes(), img.size, 'RGBA')

    @staticmethod
    def create_lab_wall_texture(size=64):
        """Vytvoří pixel-art texturu stěny vesmírné laboratoře"""
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        pixels = img.load()

        # Barvy stěny
        wall_base = (55, 60, 78)         # tmavý kov stěny
        wall_light = (75, 80, 98)        # světlejší
        wall_dark = (40, 44, 58)         # tmavší
        pipe_main = (90, 95, 110)        # trubka
        pipe_highlight = (120, 125, 140) # odlesk trubky
        pipe_shadow = (55, 58, 70)       # stín trubky
        warning_yellow = (200, 180, 40)  # výstražný pruh
        warning_dark = (50, 48, 30)      # tmavý pruh
        bolt_color = (130, 135, 145)     # šrouby
        screen_bg = (15, 25, 35)         # obrazovka
        screen_glow = (30, 200, 170)     # glow obrazovky
        screen_text = (50, 255, 200)     # text na obrazovce

        # Základní výplň stěny
        for y in range(size):
            for x in range(size):
                noise = ((x * 3 + y * 11) % 4) - 1
                r = max(0, min(255, wall_base[0] + noise))
                g = max(0, min(255, wall_base[1] + noise))
                b = max(0, min(255, wall_base[2] + noise))
                pixels[x, y] = (r, g, b, 255)

        # Horizontální panelové čáry
        for x in range(size):
            pixels[x, size // 3] = wall_dark + (255,)
            pixels[x, size // 3 + 1] = wall_light + (255,)
            pixels[x, 2 * size // 3] = wall_dark + (255,)
            pixels[x, 2 * size // 3 + 1] = wall_light + (255,)

        # Trubka nahoře
        pipe_y = 6
        for x in range(size):
            pixels[x, pipe_y] = pipe_shadow + (255,)
            pixels[x, pipe_y + 1] = pipe_main + (255,)
            pixels[x, pipe_y + 2] = pipe_highlight + (255,)
            pixels[x, pipe_y + 3] = pipe_main + (255,)
            pixels[x, pipe_y + 4] = pipe_shadow + (255,)

        # Šrouby na trubce
        for bx in [10, 30, 50]:
            if bx < size:
                pixels[bx, pipe_y + 2] = bolt_color + (255,)
                pixels[bx + 1, pipe_y + 2] = bolt_color + (255,)

        # Malá obrazovka / monitor
        scr_x, scr_y = 6, size // 3 + 5
        scr_w, scr_h = 18, 12
        for sy in range(scr_y, scr_y + scr_h):
            for sx in range(scr_x, scr_x + scr_w):
                if sx < size and sy < size:
                    pixels[sx, sy] = screen_bg + (255,)
        # Okraj obrazovky
        for sx in range(scr_x - 1, scr_x + scr_w + 1):
            if 0 <= sx < size:
                if scr_y - 1 >= 0:
                    pixels[sx, scr_y - 1] = wall_light + (255,)
                if scr_y + scr_h < size:
                    pixels[sx, scr_y + scr_h] = wall_dark + (255,)
        for sy in range(scr_y - 1, scr_y + scr_h + 1):
            if 0 <= sy < size:
                if scr_x - 1 >= 0:
                    pixels[scr_x - 1, sy] = wall_light + (255,)
                if scr_x + scr_w < size:
                    pixels[scr_x + scr_w, sy] = wall_dark + (255,)
        # Text na obrazovce (pár svítících pixelů)
        screen_pixels = [
            (2, 3), (3, 3), (4, 3), (6, 3), (7, 3),
            (2, 5), (4, 5), (5, 5), (6, 5), (8, 5), (9, 5),
            (2, 7), (3, 7), (5, 7), (7, 7), (10, 7), (11, 7),
        ]
        for spx, spy in screen_pixels:
            px, py = scr_x + spx, scr_y + spy
            if 0 <= px < size and 0 <= py < size:
                pixels[px, py] = screen_text + (255,)
        # Glow kolem
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                gx, gy = scr_x + scr_w // 2 + dx, scr_y + scr_h + 1 + dy
                if 0 <= gx < size and 0 <= gy < size:
                    pixels[gx, gy] = screen_glow + (255,)

        # Výstražný pruh dole
        stripe_y = 2 * size // 3 + 4
        for x in range(size):
            for dy in range(4):
                if stripe_y + dy < size:
                    if ((x + dy) // 4) % 2 == 0:
                        pixels[x, stripe_y + dy] = warning_yellow + (255,)
                    else:
                        pixels[x, stripe_y + dy] = warning_dark + (255,)

        return pygame.image.fromstring(img.tobytes(), img.size, 'RGBA')

    @staticmethod
    def create_chair_texture(size=40):
        """Vytvoří texturu židle v řídícím centru"""
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        # Sedák
        draw.rectangle([size*0.15, size*0.35, size*0.85, size*0.65],
                       fill=(60, 60, 80), outline=(40, 40, 60), width=2)
        # Opěradlo
        draw.rectangle([size*0.2, size*0.05, size*0.8, size*0.38],
                       fill=(50, 50, 70), outline=(35, 35, 55), width=2)
        # Nohy
        draw.rectangle([size*0.25, size*0.65, size*0.35, size*0.95],
                       fill=(80, 80, 100), outline=(50, 50, 70))
        draw.rectangle([size*0.65, size*0.65, size*0.75, size*0.95],
                       fill=(80, 80, 100), outline=(50, 50, 70))
        return pygame.image.fromstring(img.tobytes(), img.size, 'RGBA')

    @staticmethod
    def create_screen_texture(size=40):
        """Vytvoří texturu monitoru/obrazovky"""
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        # Rám monitoru
        draw.rectangle([size*0.05, size*0.05, size*0.95, size*0.75],
                       fill=(30, 35, 50), outline=(20, 25, 40), width=2)
        # Obrazovka
        draw.rectangle([size*0.12, size*0.12, size*0.88, size*0.68],
                       fill=(10, 30, 45))
        # Text / data na obrazovce
        for i in range(3):
            y = size * 0.2 + i * size * 0.15
            draw.rectangle([size*0.18, y, size*0.18 + size*(0.4 - i*0.08), y + size*0.06],
                           fill=(30, 200, 170))
        # Stoček
        draw.rectangle([size*0.4, size*0.75, size*0.6, size*0.95],
                       fill=(60, 65, 80), outline=(40, 45, 60))
        return pygame.image.fromstring(img.tobytes(), img.size, 'RGBA')

    @staticmethod
    def create_keyboard_texture(size=40):
        """Vytvoří texturu klávesnice"""
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        # Tělo klávesnice
        draw.rectangle([size*0.05, size*0.3, size*0.95, size*0.7],
                       fill=(50, 55, 70), outline=(35, 40, 55), width=2)
        # Klávesy (mřížka)
        for row in range(3):
            for col in range(6):
                kx = size*0.12 + col * size*0.13
                ky = size*0.35 + row * size*0.1
                draw.rectangle([kx, ky, kx + size*0.1, ky + size*0.07],
                               fill=(70, 75, 90), outline=(40, 45, 60))
        return pygame.image.fromstring(img.tobytes(), img.size, 'RGBA')

    @staticmethod
    def create_cable_texture(size=30):
        """Vytvoří texturu kabelu"""
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        # Křivka kabelu
        points = []
        for i in range(size):
            x = i
            y = int(size * 0.5 + math.sin(i * 0.4) * size * 0.25)
            points.append((x, y))
        if len(points) > 1:
            draw.line(points, fill=(180, 50, 50), width=3)
            # Konektory
            draw.ellipse([0, size*0.35, size*0.15, size*0.65],
                         fill=(120, 120, 140), outline=(80, 80, 100))
            draw.ellipse([size*0.85, size*0.25, size, size*0.55],
                         fill=(120, 120, 140), outline=(80, 80, 100))
        return pygame.image.fromstring(img.tobytes(), img.size, 'RGBA')

    @staticmethod
    def create_datapad_texture(size=35):
        """Vytvoří texturu datapadu/tabletu"""
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        # Tělo
        draw.rectangle([size*0.15, size*0.05, size*0.85, size*0.95],
                       fill=(45, 50, 65), outline=(30, 35, 50), width=2)
        # Display
        draw.rectangle([size*0.22, size*0.12, size*0.78, size*0.75],
                       fill=(15, 40, 55))
        # Data čáry
        for i in range(4):
            y = size * 0.2 + i * size * 0.12
            draw.rectangle([size*0.28, y, size*0.28 + size*(0.35 - i*0.05), y + size*0.05],
                           fill=(50, 220, 180))
        # Tlačítko
        draw.ellipse([size*0.4, size*0.8, size*0.6, size*0.9],
                     fill=(80, 85, 100), outline=(60, 65, 80))
        return pygame.image.fromstring(img.tobytes(), img.size, 'RGBA')

    @staticmethod
    def create_cc_floor_texture(size=64):
        """Vytvoří pixel-art texturu podlahy řídícího centra"""
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        pixels = img.load()

        base = (35, 40, 55)
        light = (50, 55, 72)
        dark = (25, 28, 42)
        glow_blue = (30, 100, 200)
        glow_dim = (20, 60, 120)

        for y in range(size):
            for x in range(size):
                noise = ((x * 5 + y * 9) % 4) - 1
                r = max(0, min(255, base[0] + noise))
                g = max(0, min(255, base[1] + noise))
                b = max(0, min(255, base[2] + noise))
                pixels[x, y] = (r, g, b, 255)

        # Mřížka
        for i in range(size):
            pixels[i, 0] = dark + (255,)
            pixels[i, size-1] = dark + (255,)
            pixels[0, i] = dark + (255,)
            pixels[size-1, i] = dark + (255,)

        # Středová světelná linka (modrá)
        half = size // 2
        for i in range(4, size - 4):
            pixels[i, half] = glow_blue + (255,)
            pixels[i, half - 1] = glow_dim + (255,)
            pixels[i, half + 1] = glow_dim + (255,)

        # Rohové indikátory
        for cx, cy in [(4, 4), (size-6, 4), (4, size-6), (size-6, size-6)]:
            pixels[cx, cy] = glow_blue + (255,)
            pixels[cx+1, cy] = glow_blue + (255,)
            pixels[cx, cy+1] = glow_blue + (255,)
            pixels[cx+1, cy+1] = glow_dim + (255,)

        return pygame.image.fromstring(img.tobytes(), img.size, 'RGBA')

    @staticmethod
    def create_cc_wall_texture(size=64):
        """Vytvoří pixel-art texturu stěny řídícího centra"""
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        pixels = img.load()

        base = (25, 30, 50)
        light = (40, 45, 68)
        dark = (15, 18, 35)
        screen_bg = (5, 15, 30)
        screen_glow = (20, 150, 255)
        screen_data = (40, 200, 255)
        indicator_red = (200, 40, 40)
        indicator_green = (40, 200, 80)

        for y in range(size):
            for x in range(size):
                noise = ((x * 7 + y * 3) % 3) - 1
                r = max(0, min(255, base[0] + noise))
                g = max(0, min(255, base[1] + noise))
                b = max(0, min(255, base[2] + noise))
                pixels[x, y] = (r, g, b, 255)

        # Panel čáry
        for x in range(size):
            pixels[x, size // 4] = dark + (255,)
            pixels[x, size // 4 + 1] = light + (255,)
            pixels[x, 3 * size // 4] = dark + (255,)
            pixels[x, 3 * size // 4 + 1] = light + (255,)

        # Velká obrazovka uprostřed
        scr_x, scr_y = 8, size // 4 + 5
        scr_w, scr_h = size - 16, size // 3
        for sy in range(scr_y, min(scr_y + scr_h, size)):
            for sx in range(scr_x, min(scr_x + scr_w, size)):
                pixels[sx, sy] = screen_bg + (255,)
        # Data čáry
        for row in range(4):
            dy = scr_y + 3 + row * 5
            length = scr_w - 8 - row * 6
            for dx in range(scr_x + 3, min(scr_x + 3 + length, size)):
                if dy < size:
                    pixels[dx, dy] = screen_data + (255,)
        # Glow okraj
        for sx in range(scr_x - 1, min(scr_x + scr_w + 1, size)):
            if scr_y - 1 >= 0 and sx >= 0:
                pixels[sx, scr_y - 1] = screen_glow + (255,)
            if scr_y + scr_h < size and sx >= 0:
                pixels[sx, scr_y + scr_h] = screen_glow + (255,)

        # Indikátory nahoře
        for ix, color in [(10, indicator_green), (16, indicator_green), (22, indicator_red),
                          (size - 12, indicator_green), (size - 18, indicator_red)]:
            if 0 <= ix < size:
                for dy in range(3):
                    iy = 5 + dy
                    if iy < size:
                        pixels[ix, iy] = color + (255,)
                        if ix + 1 < size:
                            pixels[ix + 1, iy] = color + (255,)

        return pygame.image.fromstring(img.tobytes(), img.size, 'RGBA')

class TextureManager:
    """Správa textur"""
    def __init__(self):
        self.textures = {}
        self.assets_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
        self.load_or_generate_textures()
    
    def load_or_generate_textures(self):
        """Načte nebo vygeneruje textury"""
        texture_configs = {
            "cat": (100, TextureGenerator.create_cat_texture),
            "bug": (20, TextureGenerator.create_bug_texture),
            "mouse": (20, TextureGenerator.create_mouse_texture),
            "container": (20, TextureGenerator.create_container_texture),
            "plant": (20, TextureGenerator.create_plant_texture),
            "lab_floor": (64, TextureGenerator.create_lab_floor_texture),
            "lab_wall": (64, TextureGenerator.create_lab_wall_texture),
            "chair": (40, TextureGenerator.create_chair_texture),
            "screen": (40, TextureGenerator.create_screen_texture),
            "keyboard": (40, TextureGenerator.create_keyboard_texture),
            "cable": (30, TextureGenerator.create_cable_texture),
            "datapad": (35, TextureGenerator.create_datapad_texture),
            "cc_floor": (64, TextureGenerator.create_cc_floor_texture),
            "cc_wall": (64, TextureGenerator.create_cc_wall_texture),
        }
        
        for name, (size, generator_func) in texture_configs.items():
            # Pokus se nahrát ze složky assets
            if os.path.exists(self.assets_path):
                path = os.path.join(self.assets_path, f"{name}.png")
                try:
                    texture = pygame.image.load(path).convert_alpha()
                    self.textures[name] = texture
                    print(f"[OK] Textura '{name}' nahrana ze souboru: {path}")
                    continue
                except:
                    pass
            
            # Vygeneruj texturu
            try:
                texture = generator_func(size)
                self.textures[name] = texture
                print(f"[OK] Textura '{name}' vygenerovana")
            except Exception as e:
                print(f"[CHYBA] Chyba pri generovani textury '{name}': {e}")
                self.textures[name] = None
    
    def get_texture(self, name):
        """Vrátí texturu"""
        return self.textures.get(name)
    
    def scale_texture(self, name, width, height):
        """Vrátí zmenšenou texturu"""
        texture = self.get_texture(name)
        if texture:
            return pygame.transform.scale(texture, (int(width), int(height)))
        return None

class Button:
    """Tlačítko"""
    def __init__(self, x, y, width, height, text, font, text_color, button_color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.text_color = text_color
        self.button_color = button_color
        self.hover_color = hover_color
        self.is_hovered = False
    
    def draw(self, screen):
        color = self.hover_color if self.is_hovered else self.button_color
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 3)
        
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
    
    def check_hover(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)
    
    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

class Menu:
    """Hlavní menu"""
    def __init__(self, texture_manager):
        self.screen = pygame.display.get_surface()
        self.clock = pygame.time.Clock()
        self.running = True
        self.texture_manager = texture_manager
        
        self.font_title = pygame.font.Font(None, 80)
        self.font_button = pygame.font.Font(None, 50)
        
        button_width = 300
        button_height = 80
        button_x = (SCREEN_WIDTH - button_width) // 2
        button_y = (SCREEN_HEIGHT - button_height) // 2 + 100
        
        self.start_button = Button(
            button_x, button_y, button_width, button_height,
            "PLAY",
            self.font_button,
            WHITE,
            ALIEN_GREEN_MAIN,
            ALIEN_GREEN_LIGHT
        )
    
    def draw_background(self):
        for y in range(SCREEN_HEIGHT):
            color = (
                int(100 + (150 - 100) * (y / SCREEN_HEIGHT)),
                int(150 + (200 - 150) * (y / SCREEN_HEIGHT)),
                int(100 + (150 - 100) * (y / SCREEN_HEIGHT))
            )
            pygame.draw.line(self.screen, color, (0, y), (SCREEN_WIDTH, y))
    
    def draw_alien_cat_menu(self):
        cat_texture = self.texture_manager.get_texture("cat")
        if cat_texture:
            scaled_cat = pygame.transform.scale(cat_texture, (150, 150))
            cat_rect = scaled_cat.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
            self.screen.blit(scaled_cat, cat_rect)
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return None
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.start_button.is_clicked(pygame.mouse.get_pos()):
                    return "play"
        return None
    
    def update(self):
        self.start_button.check_hover(pygame.mouse.get_pos())
    
    def draw(self):
        self.draw_background()
        self.draw_alien_cat_menu()
        
        title_text = self.font_title.render("Mimozemská Kočka", True, WHITE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 50))
        self.screen.blit(title_text, title_rect)
        
        self.start_button.draw(self.screen)
        
        pygame.display.flip()
    
    def run(self):
        while self.running:
            result = self.handle_events()
            if result == "play":
                return "play"
            self.update()
            self.draw()
            self.clock.tick(FPS)
        return None

class LevelSelect:
    """Výběr levelu"""
    def __init__(self, texture_manager):
        self.screen = pygame.display.get_surface()
        self.clock = pygame.time.Clock()
        self.running = True
        self.texture_manager = texture_manager
        
        self.font_title = pygame.font.Font(None, 70)
        self.font_button = pygame.font.Font(None, 42)
        self.font_desc = pygame.font.Font(None, 28)
        
        button_width = 350
        button_height = 90
        center_x = SCREEN_WIDTH // 2
        
        self.level1_button = Button(
            center_x - button_width - 30, 300, button_width, button_height,
            "Level 1: Laboratoř",
            self.font_button,
            WHITE,
            (60, 130, 80),
            (80, 180, 100)
        )
        
        self.level2_button = Button(
            center_x + 30, 300, button_width, button_height,
            "Level 2: Řídící Centrum",
            self.font_button,
            WHITE,
            (40, 80, 160),
            (60, 120, 200)
        )
        
        self.back_button = Button(
            center_x - 100, 520, 200, 60,
            "ZPĚT",
            self.font_button,
            WHITE,
            (120, 60, 60),
            (180, 80, 80)
        )
        
        # Pulsující hvězdy na pozadí
        self.stars = [(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT),
                       random.random() * 2 + 0.5) for _ in range(120)]
        self.star_timer = 0
    
    def draw_background(self):
        # Tmavý vesmírný gradient
        for y in range(SCREEN_HEIGHT):
            r = int(10 + 20 * (y / SCREEN_HEIGHT))
            g = int(12 + 25 * (y / SCREEN_HEIGHT))
            b = int(30 + 40 * (y / SCREEN_HEIGHT))
            pygame.draw.line(self.screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))
        
        # Hvězdy
        self.star_timer += 0.02
        for sx, sy, brightness in self.stars:
            alpha = int(128 + 127 * math.sin(self.star_timer * brightness))
            star_color = (alpha, alpha, min(255, alpha + 30))
            self.screen.set_at((sx, sy), star_color)
            if brightness > 1.5:
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nx, ny = sx + dx, sy + dy
                    if 0 <= nx < SCREEN_WIDTH and 0 <= ny < SCREEN_HEIGHT:
                        dim = max(0, alpha // 3)
                        self.screen.set_at((nx, ny), (dim, dim, min(255, dim + 15)))
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return "quit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if self.level1_button.is_clicked(pos):
                    return "level1"
                if self.level2_button.is_clicked(pos):
                    return "level2"
                if self.back_button.is_clicked(pos):
                    return "back"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "back"
        return None
    
    def update(self):
        pos = pygame.mouse.get_pos()
        self.level1_button.check_hover(pos)
        self.level2_button.check_hover(pos)
        self.back_button.check_hover(pos)
    
    def draw(self):
        self.draw_background()
        
        title_text = self.font_title.render("Vyber si Level", True, WHITE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 80))
        self.screen.blit(title_text, title_rect)
        
        # Ikonka kočky
        cat_texture = self.texture_manager.get_texture("cat")
        if cat_texture:
            scaled_cat = pygame.transform.scale(cat_texture, (100, 100))
            cat_rect = scaled_cat.get_rect(center=(SCREEN_WIDTH // 2, 190))
            self.screen.blit(scaled_cat, cat_rect)
        
        self.level1_button.draw(self.screen)
        self.level2_button.draw(self.screen)
        self.back_button.draw(self.screen)
        
        # Popisy levelů
        desc1 = self.font_desc.render("Sněz 50 malých věcí v laboratoři", True, (180, 200, 180))
        desc1_rect = desc1.get_rect(center=(self.level1_button.rect.centerx, 410))
        self.screen.blit(desc1, desc1_rect)
        
        desc2 = self.font_desc.render("Sněz 50 velkých věcí v řídícím centru", True, (160, 180, 220))
        desc2_rect = desc2.get_rect(center=(self.level2_button.rect.centerx, 410))
        self.screen.blit(desc2, desc2_rect)
        
        pygame.display.flip()
    
    def run(self):
        while self.running:
            result = self.handle_events()
            if result in ("level1", "level2", "back", "quit"):
                return result
            self.update()
            self.draw()
            self.clock.tick(FPS)
        return "quit"

class Food:
    """Jídlo"""
    def __init__(self, x, y, food_type, texture_manager):
        self.x = x
        self.y = y
        self.food_type = food_type
        self.width = random.randint(35, 50)
        self.height = random.randint(35, 50)
        self.eaten = False
        self.texture_manager = texture_manager
    
    def draw(self, screen):
        if self.eaten:
            return
        
        texture = self.texture_manager.get_texture(self.food_type)
        if texture:
            scaled_texture = self.texture_manager.scale_texture(self.food_type, self.width, self.height)
            if scaled_texture:
                screen.blit(scaled_texture, (self.x, self.y))
    
    def is_eaten_by(self, cat):
        cat_left = cat.x - cat.size
        cat_right = cat.x + cat.size
        cat_top = cat.y - cat.size
        cat_bottom = cat.y + cat.size
        
        food_left = self.x
        food_right = self.x + self.width
        food_top = self.y
        food_bottom = self.y + self.height
        
        return not (food_right < cat_left or food_left > cat_right or 
                   food_bottom < cat_top or food_top > cat_bottom)

class AlienCat:
    """Mimozemská kočka"""
    def __init__(self, x, y, texture_manager):
        self.x = x
        self.y = y
        self.size = BASE_CAT_SIZE
        self.vx = 0
        self.vy = 0
        self.speed = 5
        self.food_eaten = 0
        self.animation_counter = 0
        self.animation_walk = 0
        self.texture_manager = texture_manager
    
    def handle_input(self, keys):
        self.vx = 0
        self.vy = 0
        
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vx = -self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vx = self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.vy = -self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.vy = self.speed
    
    def update(self):
        self.x += self.vx
        self.y += self.vy
        
        self.x = max(self.size, min(self.x, SCREEN_WIDTH - self.size))
        self.y = max(self.size, min(self.y, SCREEN_HEIGHT - self.size))
        
        self.animation_counter += 1
        if self.vx != 0 or self.vy != 0:
            self.animation_walk += 0.2
    
    def eat_food(self, food):
        if self.size < MAX_CAT_SIZE:
            self.size += 3
            self.food_eaten += 1
            self.speed = max(2.5, 5 - (self.size - BASE_CAT_SIZE) / 60)
        else:
            self.food_eaten += 1
        food.eaten = True
    
    def draw(self, screen):
        """Kreslí POUZE texturu kočky - nic vykresleného!"""
        cat_texture = self.texture_manager.get_texture("cat")
        
        if cat_texture:
            scaled_cat = pygame.transform.scale(cat_texture, (int(self.size * 2), int(self.size * 2)))
            cat_rect = scaled_cat.get_rect(center=(int(self.x), int(self.y)))
            screen.blit(scaled_cat, cat_rect)

class Game:
    """Level 1 - Laboratoř (sněz 50 věcí)"""
    FOOD_GOAL = 50
    
    def __init__(self, texture_manager):
        self.screen = pygame.display.get_surface()
        self.clock = pygame.time.Clock()
        self.running = True
        self.won = False
        self.texture_manager = texture_manager
        
        self.cat = AlienCat(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, texture_manager)
        self.foods = []
        self.bg_surface = self._build_background()
        self.spawn_food()
    
    def spawn_food(self):
        for _ in range(12):
            x = random.randint(50, SCREEN_WIDTH - 50)
            y = random.randint(150, SCREEN_HEIGHT - 50)
            food_type = random.choice(["bug", "mouse", "container", "plant"])
            self.foods.append(Food(x, y, food_type, self.texture_manager))
    
    def _build_background(self):
        """Sestaví předrenderované pozadí z pixel-art textur"""
        bg = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        
        floor_tile = self.texture_manager.get_texture("lab_floor")
        wall_tile = self.texture_manager.get_texture("lab_wall")
        
        tile_size = 64
        wall_height = 128  # 2 řady tile pro stěnu
        
        # Stěna (horní část)
        if wall_tile:
            for x in range(0, SCREEN_WIDTH, tile_size):
                for y in range(0, wall_height, tile_size):
                    bg.blit(wall_tile, (x, y))
        else:
            bg.fill((55, 60, 78), (0, 0, SCREEN_WIDTH, wall_height))
        
        # Přechodová linka stěna → podlaha
        pygame.draw.line(bg, (30, 200, 170), (0, wall_height), (SCREEN_WIDTH, wall_height), 2)
        pygame.draw.line(bg, (20, 120, 100), (0, wall_height + 2), (SCREEN_WIDTH, wall_height + 2), 1)
        
        # Podlaha (zbytek)
        if floor_tile:
            for x in range(0, SCREEN_WIDTH, tile_size):
                for y in range(wall_height + 3, SCREEN_HEIGHT, tile_size):
                    bg.blit(floor_tile, (x, y))
        else:
            bg.fill(LAB_FLOOR, (0, wall_height + 3, SCREEN_WIDTH, SCREEN_HEIGHT - wall_height - 3))
        
        return bg

    def draw_laboratory(self):
        # Vykreslí předrenderované pixel-art pozadí
        self.screen.blit(self.bg_surface, (0, 0))
        
        font_small = pygame.font.Font(None, 28)
        font_title = pygame.font.Font(None, 36)
        
        title_text = font_title.render("Level 1: Laboratoř", True, WHITE)
        self.screen.blit(title_text, (20, 10))
        
        size_text = font_small.render(f"Velikost: {self.cat.size:.0f} / {MAX_CAT_SIZE}", True, WHITE)
        self.screen.blit(size_text, (SCREEN_WIDTH - 350, 15))
        
        food_text = font_small.render(f"Snědeno: {self.cat.food_eaten} / {self.FOOD_GOAL}", True, WHITE)
        self.screen.blit(food_text, (SCREEN_WIDTH - 350, 45))
        
        progress_width = 300
        progress_height = 15
        progress_x = SCREEN_WIDTH - 350
        progress_y = 75
        
        pygame.draw.rect(self.screen, LIGHT_GRAY, 
                        (progress_x, progress_y, progress_width, progress_height))
        
        filled_width = min(1.0, self.cat.food_eaten / self.FOOD_GOAL) * progress_width
        pygame.draw.rect(self.screen, (80, 180, 100), 
                        (progress_x, progress_y, filled_width, progress_height))
        
        pygame.draw.rect(self.screen, WHITE, 
                        (progress_x, progress_y, progress_width, progress_height), 2)
        
        controls_text = font_small.render("WASD nebo Šipky = Pohyb | ESC = Zpět", True, (180, 200, 180))
        self.screen.blit(controls_text, (20, SCREEN_HEIGHT - 30))
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
    
    def update(self):
        keys = pygame.key.get_pressed()
        self.cat.handle_input(keys)
        self.cat.update()
        
        for food in self.foods:
            if not food.eaten and food.is_eaten_by(self.cat):
                self.cat.eat_food(food)
        
        # Win podmínka
        if self.cat.food_eaten >= self.FOOD_GOAL:
            self.won = True
            self.running = False
            return
        
        alive_foods = sum(1 for f in self.foods if not f.eaten)
        if alive_foods < 5:
            self.spawn_food()
    
    def draw(self):
        self.screen.fill(LAB_FLOOR)
        self.draw_laboratory()
        
        for food in self.foods:
            food.draw(self.screen)
        
        self.cat.draw(self.screen)
        
        pygame.display.flip()
    
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        return "won" if self.won else "quit"

class GameLevel2:
    """Level 2 - Řídící Centrum (sněz 50 větších věcí)"""
    FOOD_GOAL = 50
    
    def __init__(self, texture_manager):
        self.screen = pygame.display.get_surface()
        self.clock = pygame.time.Clock()
        self.running = True
        self.won = False
        self.texture_manager = texture_manager
        
        self.cat = AlienCat(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, texture_manager)
        self.cat.size = 50  # Větší počáteční velikost
        self.cat.speed = 4
        self.foods = []
        self.bg_surface = self._build_background()
        self.spawn_food()
    
    def spawn_food(self):
        for _ in range(8):
            x = random.randint(80, SCREEN_WIDTH - 80)
            y = random.randint(160, SCREEN_HEIGHT - 80)
            food_type = random.choice(["chair", "screen", "keyboard", "cable", "datapad"])
            food = Food(x, y, food_type, self.texture_manager)
            food.width = random.randint(50, 75)  # Větší jídlo
            food.height = random.randint(50, 75)
            self.foods.append(food)
    
    def _build_background(self):
        """Sestaví pozadí řídícího centra"""
        bg = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        
        floor_tile = self.texture_manager.get_texture("cc_floor")
        wall_tile = self.texture_manager.get_texture("cc_wall")
        
        tile_size = 64
        wall_height = 128
        
        if wall_tile:
            for x in range(0, SCREEN_WIDTH, tile_size):
                for y in range(0, wall_height, tile_size):
                    bg.blit(wall_tile, (x, y))
        else:
            bg.fill((25, 30, 50), (0, 0, SCREEN_WIDTH, wall_height))
        
        # Přechodová linka - modrý glow
        pygame.draw.line(bg, (20, 100, 255), (0, wall_height), (SCREEN_WIDTH, wall_height), 2)
        pygame.draw.line(bg, (15, 60, 150), (0, wall_height + 2), (SCREEN_WIDTH, wall_height + 2), 1)
        
        if floor_tile:
            for x in range(0, SCREEN_WIDTH, tile_size):
                for y in range(wall_height + 3, SCREEN_HEIGHT, tile_size):
                    bg.blit(floor_tile, (x, y))
        else:
            bg.fill((35, 40, 55), (0, wall_height + 3, SCREEN_WIDTH, SCREEN_HEIGHT - wall_height - 3))
        
        return bg

    def draw_command_center(self):
        self.screen.blit(self.bg_surface, (0, 0))
        
        font_small = pygame.font.Font(None, 28)
        font_title = pygame.font.Font(None, 36)
        
        title_text = font_title.render("Level 2: Řídící Centrum", True, (40, 200, 255))
        self.screen.blit(title_text, (20, 10))
        
        size_text = font_small.render(f"Velikost: {self.cat.size:.0f} / {MAX_CAT_SIZE}", True, (180, 200, 255))
        self.screen.blit(size_text, (SCREEN_WIDTH - 350, 15))
        
        food_text = font_small.render(f"Snědeno: {self.cat.food_eaten} / {self.FOOD_GOAL}", True, (180, 200, 255))
        self.screen.blit(food_text, (SCREEN_WIDTH - 350, 45))
        
        progress_width = 300
        progress_height = 15
        progress_x = SCREEN_WIDTH - 350
        progress_y = 75
        
        pygame.draw.rect(self.screen, (30, 40, 60), 
                        (progress_x, progress_y, progress_width, progress_height))
        
        filled_width = min(1.0, self.cat.food_eaten / self.FOOD_GOAL) * progress_width
        pygame.draw.rect(self.screen, (30, 150, 255), 
                        (progress_x, progress_y, filled_width, progress_height))
        
        pygame.draw.rect(self.screen, (40, 200, 255), 
                        (progress_x, progress_y, progress_width, progress_height), 2)
        
        controls_text = font_small.render("WASD nebo Šipky = Pohyb | ESC = Zpět", True, (100, 120, 160))
        self.screen.blit(controls_text, (20, SCREEN_HEIGHT - 30))
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
    
    def update(self):
        keys = pygame.key.get_pressed()
        self.cat.handle_input(keys)
        self.cat.update()
        
        for food in self.foods:
            if not food.eaten and food.is_eaten_by(self.cat):
                self.cat.eat_food(food)
        
        # Win podmínka
        if self.cat.food_eaten >= self.FOOD_GOAL:
            self.won = True
            self.running = False
            return
        
        alive_foods = sum(1 for f in self.foods if not f.eaten)
        if alive_foods < 3:
            self.spawn_food()
    
    def draw(self):
        self.screen.fill((25, 30, 50))
        self.draw_command_center()
        
        for food in self.foods:
            food.draw(self.screen)
        
        self.cat.draw(self.screen)
        
        pygame.display.flip()
    
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        return "won" if self.won else "quit"

class LevelComplete:
    """Obrazovka dokončení levelu"""
    def __init__(self, texture_manager, level_name, food_eaten):
        self.screen = pygame.display.get_surface()
        self.clock = pygame.time.Clock()
        self.running = True
        self.texture_manager = texture_manager
        self.level_name = level_name
        self.food_eaten = food_eaten
        
        self.font_title = pygame.font.Font(None, 80)
        self.font_info = pygame.font.Font(None, 45)
        self.font_button = pygame.font.Font(None, 42)
        
        center_x = SCREEN_WIDTH // 2
        
        self.continue_button = Button(
            center_x - 150, 450, 300, 70,
            "ZPĚT NA LEVELY",
            self.font_button,
            WHITE,
            ALIEN_GREEN_MAIN,
            ALIEN_GREEN_LIGHT
        )
        
        self.pulse_timer = 0
        self.stars = [(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT),
                       random.random() * 2 + 0.5) for _ in range(80)]
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return "quit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.continue_button.is_clicked(pygame.mouse.get_pos()):
                    return "levels"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    return "levels"
        return None
    
    def draw(self):
        # Pozadí
        for y in range(SCREEN_HEIGHT):
            r = int(5 + 15 * (y / SCREEN_HEIGHT))
            g = int(15 + 30 * (y / SCREEN_HEIGHT))
            b = int(10 + 25 * (y / SCREEN_HEIGHT))
            pygame.draw.line(self.screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))
        
        self.pulse_timer += 0.03
        for sx, sy, brightness in self.stars:
            alpha = int(128 + 127 * math.sin(self.pulse_timer * brightness))
            self.screen.set_at((sx, sy), (alpha, alpha, min(255, alpha + 20)))
        
        # Velká kočka
        cat_texture = self.texture_manager.get_texture("cat")
        if cat_texture:
            cat_size = int(180 + 10 * math.sin(self.pulse_timer * 2))
            scaled_cat = pygame.transform.scale(cat_texture, (cat_size, cat_size))
            cat_rect = scaled_cat.get_rect(center=(SCREEN_WIDTH // 2, 200))
            self.screen.blit(scaled_cat, cat_rect)
        
        # Gratulace
        glow = int(200 + 55 * math.sin(self.pulse_timer * 3))
        title = self.font_title.render("LEVEL DOKONČEN!", True, (glow, 255, glow))
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 330))
        self.screen.blit(title, title_rect)
        
        info = self.font_info.render(f"{self.level_name} — Snědeno: {self.food_eaten}", True, (180, 200, 180))
        info_rect = info.get_rect(center=(SCREEN_WIDTH // 2, 390))
        self.screen.blit(info, info_rect)
        
        self.continue_button.check_hover(pygame.mouse.get_pos())
        self.continue_button.draw(self.screen)
        
        pygame.display.flip()
    
    def run(self):
        while self.running:
            result = self.handle_events()
            if result in ("levels", "quit"):
                return result
            self.draw()
            self.clock.tick(FPS)
        return "quit"

class ComicCutscene:
    """Komiks cutscéna - loď selhala a spadla na planetu"""
    
    # Barvy pro komiks
    PANEL_BG = (12, 15, 28)
    PANEL_BORDER = (200, 200, 200)
    BUBBLE_BG = (255, 255, 255)
    BUBBLE_BORDER = (40, 40, 40)
    BUBBLE_TEXT = (20, 20, 20)
    NARRATION_BG = (40, 35, 20)
    NARRATION_TEXT = (255, 230, 150)
    SFX_COLOR = (255, 80, 50)
    
    def __init__(self, texture_manager):
        self.screen = pygame.display.get_surface()
        self.clock = pygame.time.Clock()
        self.running = True
        self.texture_manager = texture_manager
        
        self.font_narration = pygame.font.Font(None, 28)
        self.font_dialog = pygame.font.Font(None, 26)
        self.font_sfx = pygame.font.Font(None, 72)
        self.font_sfx_small = pygame.font.Font(None, 48)
        self.font_hint = pygame.font.Font(None, 24)
        self.font_title = pygame.font.Font(None, 60)
        
        self.current_panel = 0
        self.panel_timer = 0
        self.shake_offset = (0, 0)
        self.flash_alpha = 0
        
        # Hvězdy pro vesmírné panely
        self.stars = [(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT),
                       random.random() * 2 + 0.5) for _ in range(200)]
        
        # Definice panelů: (draw_function, duration_or_click)
        self.panels = [
            self._draw_panel_1,  # Loď letí vesmírem
            self._draw_panel_2,  # Alarm! Systémy selhávají
            self._draw_panel_3,  # Kočka u ovládacího panelu
            self._draw_panel_4,  # Exploze a pád
            self._draw_panel_5,  # Loď padá na planetu
            self._draw_panel_6,  # Dopad - prášek a kráter
        ]
    
    def _draw_starfield(self, surface, rect, speed_mult=1.0):
        """Kreslí hvězdnou oblohu do obdélníku"""
        for sx, sy, br in self.stars:
            # Posún hvězdy do prostoru panelu
            px = rect.x + (sx % rect.width)
            py = rect.y + (sy % rect.height)
            if rect.collidepoint(px, py):
                alpha = int(100 + 100 * math.sin(self.panel_timer * br * speed_mult))
                alpha = max(0, min(255, alpha))
                surface.set_at((px, py), (alpha, alpha, min(255, alpha + 30)))
    
    def _draw_speech_bubble(self, surface, text, x, y, width=220, tail_dir="down"):
        """Kreslí řečovou bublinu"""
        lines = []
        words = text.split()
        current_line = ""
        for word in words:
            test = current_line + (" " if current_line else "") + word
            if self.font_dialog.size(test)[0] < width - 20:
                current_line = test
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        if current_line:
            lines.append(current_line)
        
        height = len(lines) * 24 + 20
        bubble_rect = pygame.Rect(x - width // 2, y - height, width, height)
        
        # Bublina
        pygame.draw.rect(surface, self.BUBBLE_BG, bubble_rect, border_radius=12)
        pygame.draw.rect(surface, self.BUBBLE_BORDER, bubble_rect, 2, border_radius=12)
        
        # Ocas bubliny
        if tail_dir == "down":
            tail = [
                (bubble_rect.centerx - 8, bubble_rect.bottom),
                (bubble_rect.centerx + 8, bubble_rect.bottom),
                (bubble_rect.centerx + 5, bubble_rect.bottom + 15)
            ]
        else:
            tail = [
                (bubble_rect.centerx - 8, bubble_rect.top),
                (bubble_rect.centerx + 8, bubble_rect.top),
                (bubble_rect.centerx + 5, bubble_rect.top - 15)
            ]
        pygame.draw.polygon(surface, self.BUBBLE_BG, tail)
        pygame.draw.polygon(surface, self.BUBBLE_BORDER, tail, 2)
        
        # Text
        for i, line in enumerate(lines):
            txt = self.font_dialog.render(line, True, self.BUBBLE_TEXT)
            txt_rect = txt.get_rect(center=(bubble_rect.centerx, bubble_rect.y + 15 + i * 24))
            surface.blit(txt, txt_rect)
    
    def _draw_narration_box(self, surface, text, x, y, width=300):
        """Kreslí narační box (obdelník s textem nahoře)"""
        lines = []
        words = text.split()
        current_line = ""
        for word in words:
            test = current_line + (" " if current_line else "") + word
            if self.font_narration.size(test)[0] < width - 16:
                current_line = test
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        if current_line:
            lines.append(current_line)
        
        height = len(lines) * 26 + 14
        box_rect = pygame.Rect(x, y, width, height)
        
        pygame.draw.rect(surface, self.NARRATION_BG, box_rect)
        pygame.draw.rect(surface, self.NARRATION_TEXT, box_rect, 2)
        
        for i, line in enumerate(lines):
            txt = self.font_narration.render(line, True, self.NARRATION_TEXT)
            surface.blit(txt, (box_rect.x + 8, box_rect.y + 7 + i * 26))
    
    def _draw_sfx(self, surface, text, x, y, color=None, font=None, angle=0):
        """Kreslí zvukový efekt (velký text)"""
        if color is None:
            color = self.SFX_COLOR
        if font is None:
            font = self.font_sfx
        txt = font.render(text, True, color)
        if angle != 0:
            txt = pygame.transform.rotate(txt, angle)
        txt_rect = txt.get_rect(center=(x, y))
        surface.blit(txt, txt_rect)
    
    def _draw_simple_ship(self, surface, cx, cy, size=80, damage=0):
        """Kreslí jednoduchou pixel-art vesmírnou loď"""
        # Tělo lodi
        body_color = (120, 130, 150) if damage < 1 else (100, 80, 70)
        pygame.draw.ellipse(surface, body_color,
                           (cx - size, cy - size // 3, size * 2, size * 2 // 3))
        # Kokpit
        pygame.draw.ellipse(surface, (40, 180, 200),
                           (cx + size // 3, cy - size // 6, size // 3, size // 4))
        # Křídla
        wing_color = (90, 100, 120) if damage < 1 else (80, 60, 50)
        pygame.draw.polygon(surface, wing_color, [
            (cx - size // 2, cy - size // 3),
            (cx - size // 3, cy - size),
            (cx + size // 4, cy - size // 3)
        ])
        pygame.draw.polygon(surface, wing_color, [
            (cx - size // 2, cy + size // 3),
            (cx - size // 3, cy + size),
            (cx + size // 4, cy + size // 3)
        ])
        # Motor
        engine_color = (60, 70, 90) if damage < 2 else (50, 40, 35)
        pygame.draw.rect(surface, engine_color,
                        (cx - size - size // 4, cy - size // 5, size // 3, size * 2 // 5))
        
        # Plamínky z motoru (pokud letí)
        if damage < 2:
            flame_colors = [(255, 200, 50), (255, 120, 30), (255, 60, 20)]
            for i, fc in enumerate(flame_colors):
                fl_w = size // 4 - i * 4 + int(math.sin(self.panel_timer * 10 + i) * 5)
                fl_h = size // 6 - i * 2
                fx = cx - size - size // 4 - fl_w
                fy = cy - fl_h // 2
                pygame.draw.ellipse(surface, fc, (fx, fy, fl_w, fl_h))
        
        # Poškození - praskliny a plamínky
        if damage >= 1:
            # Praskliny
            crack_color = (200, 60, 30)
            pygame.draw.line(surface, crack_color,
                           (cx - size // 4, cy - size // 4),
                           (cx + size // 6, cy + size // 6), 2)
            pygame.draw.line(surface, crack_color,
                           (cx, cy - size // 5),
                           (cx - size // 3, cy + size // 4), 2)
        if damage >= 2:
            # Oheň a kouř
            for _ in range(3):
                ex = cx + random.randint(-size // 2, size // 2)
                ey = cy + random.randint(-size // 4, size // 4)
                er = random.randint(4, 12)
                ec = random.choice([(255, 100, 30), (255, 180, 50), (200, 50, 20)])
                pygame.draw.circle(surface, ec, (ex, ey), er)
            # Kouř
            for _ in range(5):
                sx = cx + random.randint(-size, 0)
                sy = cy + random.randint(-size // 3, size // 3)
                sr = random.randint(6, 18)
                smoke_val = random.randint(40, 80)
                pygame.draw.circle(surface, (smoke_val, smoke_val, smoke_val + 10), (sx, sy), sr)
    
    def _draw_planet(self, surface, cx, cy, radius, color1, color2):
        """Kreslí jednoduchou planetu"""
        pygame.draw.circle(surface, color1, (cx, cy), radius)
        # Kruhá stínování
        for i in range(radius // 4):
            alpha_surf = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(alpha_surf, (*color2, 30),
                             (radius + i * 2, radius - i), radius - i * 2)
            surface.blit(alpha_surf, (cx - radius, cy - radius))
        # Atmosféra
        pygame.draw.circle(surface, (*color2, 80) if len(color2) == 3 else color2,
                          (cx, cy), radius + 3, 3)
    
    def _draw_panel_frame(self, rect, title=None):
        """Kreslí rámec panelu"""
        pygame.draw.rect(self.screen, self.PANEL_BG, rect)
        pygame.draw.rect(self.screen, self.PANEL_BORDER, rect, 3)
        if title:
            txt = self.font_hint.render(title, True, (150, 150, 150))
            self.screen.blit(txt, (rect.x + 5, rect.y + 5))
    
    # ===== PANELY =====
    
    def _draw_panel_1(self):
        """Panel 1: Loď letí vesmírem - klidná scéna"""
        # Velký panel přes celou obrazovku
        panel = pygame.Rect(40, 40, SCREEN_WIDTH - 80, SCREEN_HEIGHT - 80)
        self._draw_panel_frame(panel)
        self._draw_starfield(self.screen, panel)
        
        # Loď
        ship_x = panel.centerx - 50 + int(math.sin(self.panel_timer * 0.5) * 10)
        ship_y = panel.centery + int(math.cos(self.panel_timer * 0.3) * 5)
        self._draw_simple_ship(self.screen, ship_x, ship_y, size=90, damage=0)
        
        # Narrace
        self._draw_narration_box(self.screen,
            "Po všech těch hodech v řídícím centru loď nervózně pípala...",
            panel.x + 15, panel.y + 10, panel.width - 30)
        
        # Malá planeta v dálce
        self._draw_planet(self.screen, panel.right - 100, panel.bottom - 100,
                         35, (80, 140, 80), (50, 100, 50))
    
    def _draw_panel_2(self):
        """Panel 2: Alarm - systémy selhávají"""
        # Dva panely vedle sebe
        left = pygame.Rect(40, 40, SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT - 80)
        right = pygame.Rect(SCREEN_WIDTH // 2 + 10, 40, SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT - 80)
        
        # Levý panel - blikání alarmu
        self._draw_panel_frame(left)
        alarm_flash = int(abs(math.sin(self.panel_timer * 4)) * 40)
        alarm_bg = (30 + alarm_flash, 10, 10)
        pygame.draw.rect(self.screen, alarm_bg, left.inflate(-6, -6))
        self._draw_starfield(self.screen, left, 2.0)
        
        # Varovné texty
        warn_y = left.centery - 60
        for i, txt in enumerate(["! VAROVÁNÍ !", "SYSTÉMY SELHÁVAJÍ", "MOTOR POŠKOZEN", "NAVIGACE OFFLINE"]):
            blink = abs(math.sin(self.panel_timer * 3 + i * 0.8))
            if blink > 0.3:
                color = (255, int(60 + 100 * blink), 50)
                t = self.font_narration.render(txt, True, color)
                tr = t.get_rect(center=(left.centerx, warn_y + i * 40))
                self.screen.blit(t, tr)
        
        # Pravý panel - kočka se dívá na obrazovku
        self._draw_panel_frame(right)
        pygame.draw.rect(self.screen, (20, 25, 40), right.inflate(-6, -6))
        
        # Kočka (velká, vyjídá velkou část panelu)
        cat_tex = self.texture_manager.get_texture("cat")
        if cat_tex:
            cs = min(right.width - 40, right.height - 120)
            scaled = pygame.transform.scale(cat_tex, (cs, cs))
            cr = scaled.get_rect(center=(right.centerx, right.centery + 20))
            self.screen.blit(scaled, cr)
        
        self._draw_speech_bubble(self.screen,
            "MŇau?! Co se děje?!",
            right.centerx, right.centery - 130, width=200)
    
    def _draw_panel_3(self):
        """Panel 3: Kočka zkouší ovládat loď"""
        # Tři panely nad sebou
        h = (SCREEN_HEIGHT - 100) // 3
        top = pygame.Rect(40, 40, SCREEN_WIDTH - 80, h - 5)
        mid = pygame.Rect(40, 40 + h + 5, SCREEN_WIDTH - 80, h - 5)
        bot = pygame.Rect(40, 40 + 2 * (h + 5), SCREEN_WIDTH - 80, h - 5)
        
        # Horní - kočka máčká tlačítka
        self._draw_panel_frame(top)
        pygame.draw.rect(self.screen, (25, 30, 50), top.inflate(-6, -6))
        
        cat_tex = self.texture_manager.get_texture("cat")
        if cat_tex:
            cs = top.height - 30
            scaled = pygame.transform.scale(cat_tex, (cs, cs))
            self.screen.blit(scaled, (top.x + 30, top.y + 15))
        
        # Ovládací panel (obdélníky jako tlačítka)
        for i in range(6):
            bx = top.centerx + i * 50 - 50
            by = top.centery - 15
            pressed = (i == int(self.panel_timer * 3) % 6)
            bc = (200, 60, 60) if pressed else (60, 70, 90)
            pygame.draw.rect(self.screen, bc, (bx, by, 35, 30), border_radius=4)
            pygame.draw.rect(self.screen, (100, 110, 130), (bx, by, 35, 30), 2, border_radius=4)
        
        self._draw_narration_box(self.screen,
            "Kočka zoufale máčkala všechna tlačítka...",
            top.right - 310, top.y + 8, 300)
        
        # Střední - SFX
        self._draw_panel_frame(mid)
        shake = int(math.sin(self.panel_timer * 15) * 3)
        pygame.draw.rect(self.screen, (15, 10, 8), mid.inflate(-6, -6))
        self._draw_sfx(self.screen, "BZZZT!", mid.centerx - 150 + shake, mid.centery,
                       color=(255, 255, 80), angle=5)
        self._draw_sfx(self.screen, "KRRR!", mid.centerx + 150 + shake, mid.centery,
                       color=(255, 120, 40), font=self.font_sfx_small, angle=-8)
        
        # Spodní - narrace
        self._draw_panel_frame(bot)
        pygame.draw.rect(self.screen, (20, 15, 30), bot.inflate(-6, -6))
        
        self._draw_narration_box(self.screen,
            "...ale nic nepomáhalo. Motor definitivně zhasl.",
            bot.x + 20, bot.y + 10, bot.width - 40)
        
        # Hasičí scéna - loď s poškozením
        self._draw_simple_ship(self.screen, bot.centerx, bot.centery + 30, size=70, damage=1)
    
    def _draw_panel_4(self):
        """Panel 4: VELKÁ EXPLOZE"""
        panel = pygame.Rect(40, 40, SCREEN_WIDTH - 80, SCREEN_HEIGHT - 80)
        self._draw_panel_frame(panel)
        
        # Blikající pozadí - exploze
        flash = abs(math.sin(self.panel_timer * 6))
        bg_r = int(40 + 100 * flash)
        bg_g = int(15 + 40 * flash)
        pygame.draw.rect(self.screen, (bg_r, bg_g, 5), panel.inflate(-6, -6))
        
        self._draw_starfield(self.screen, panel, 3.0)
        
        # Exploze - kruhy
        for i in range(8):
            angle = self.panel_timer * 2 + i * 0.8
            dist = 30 + i * 20 + math.sin(self.panel_timer * 3 + i) * 15
            ex = panel.centerx + int(math.cos(angle) * dist)
            ey = panel.centery + int(math.sin(angle) * dist)
            er = int(15 + 20 * abs(math.sin(self.panel_timer * 4 + i)))
            ec = random.choice([(255, 200, 50), (255, 120, 30), (255, 60, 20), (255, 255, 100)])
            pygame.draw.circle(self.screen, ec, (ex, ey), er)
        
        # Loď uprostřed - poškozená
        shake_x = int(math.sin(self.panel_timer * 20) * 8)
        shake_y = int(math.cos(self.panel_timer * 17) * 5)
        self._draw_simple_ship(self.screen,
                              panel.centerx + shake_x, panel.centery + shake_y,
                              size=80, damage=2)
        
        # Velký SFX
        self._draw_sfx(self.screen, "BOOOM!",
                       panel.centerx, panel.y + 80,
                       color=(255, 255, 80))
        self._draw_sfx(self.screen, "KRAAAK!",
                       panel.centerx + 100, panel.bottom - 80,
                       color=(255, 160, 40), font=self.font_sfx_small, angle=-12)
    
    def _draw_panel_5(self):
        """Panel 5: Loď padá na planetu"""
        # Dva panely - levý (vesmír) a pravý (z pohledu planety)
        left = pygame.Rect(40, 40, SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT - 80)
        right = pygame.Rect(SCREEN_WIDTH // 2 + 10, 40, SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT - 80)
        
        # Levý - pohled z vesmíru
        self._draw_panel_frame(left)
        pygame.draw.rect(self.screen, (5, 8, 18), left.inflate(-6, -6))
        self._draw_starfield(self.screen, left)
        
        # Planeta dole
        planet_y = left.bottom - 40
        self._draw_planet(self.screen, left.centerx, planet_y,
                         120, (70, 130, 70), (40, 90, 40))
        
        # Loď padá - diagonální poz
        fall_progress = min(1.0, (self.panel_timer % 3) / 2.5)
        ship_x = int(left.centerx - 60 + fall_progress * 80)
        ship_y = int(left.y + 60 + fall_progress * (left.height - 180))
        
        # Oěň stópka za lodí
        trail_color = (200, 100, 30)
        for i in range(8):
            tx = ship_x - i * 12 - random.randint(0, 5)
            ty = ship_y - i * 8 - random.randint(0, 5)
            tr = max(2, 10 - i)
            tc_val = max(0, 200 - i * 25)
            if left.collidepoint(tx, ty):
                pygame.draw.circle(self.screen, (tc_val, tc_val // 2, 10), (tx, ty), tr)
        
        self._draw_simple_ship(self.screen, ship_x, ship_y, size=50, damage=2)
        
        self._draw_narration_box(self.screen,
            "Gravitační pole planety získalo loď do své moci...",
            left.x + 10, left.y + 10, left.width - 20)
        
        # Pravý - pohled ze země nahořu
        self._draw_panel_frame(right)
        # Zeleno-hnědá krajina
        for y in range(right.y + 3, right.bottom - 3):
            green = int(60 + 40 * ((y - right.y) / right.height))
            brown = int(40 + 30 * ((y - right.y) / right.height))
            pygame.draw.line(self.screen, (brown, green, 20),
                           (right.x + 3, y), (right.right - 3, y))
        
        # Obloha nahoře
        sky_height = right.height // 3
        for y in range(right.y + 3, right.y + sky_height):
            factor = (y - right.y) / sky_height
            r = int(40 + 60 * factor)
            g = int(60 + 80 * factor)
            b = int(120 - 50 * factor)
            pygame.draw.line(self.screen, (r, g, b),
                           (right.x + 3, y), (right.right - 3, y))
        
        # Padající loď - malá s kouřem
        fx = right.centerx + int(math.sin(self.panel_timer) * 30)
        fy = right.y + right.height // 4
        pygame.draw.circle(self.screen, (255, 160, 50), (fx, fy), 15)
        pygame.draw.circle(self.screen, (255, 255, 100), (fx, fy), 8)
        # Kouřová stopa
        for i in range(12):
            sx = fx - i * 3 + random.randint(-3, 3)
            sy = fy - i * 6
            sr = max(2, 8 - i)
            sv = min(180, 60 + i * 15)
            if right.collidepoint(sx, sy):
                pygame.draw.circle(self.screen, (sv, sv, sv + 10), (sx, sy), sr)
        
        self._draw_speech_bubble(self.screen,
            "MŇAAAAU!!!",
            right.centerx, right.centery + 30, width=180)
    
    def _draw_panel_6(self):
        """Panel 6: Dopad na planetu - kráter a prašina"""
        panel = pygame.Rect(40, 40, SCREEN_WIDTH - 80, SCREEN_HEIGHT - 80)
        self._draw_panel_frame(panel)
        
        # Krajina
        for y in range(panel.y + 3, panel.bottom - 3):
            factor = (y - panel.y) / panel.height
            g = int(50 + 50 * factor)
            b = int(30 + 20 * factor)
            r = int(40 + 40 * factor)
            pygame.draw.line(self.screen, (r, g, b),
                           (panel.x + 3, y), (panel.right - 3, y))
        
        # Obloha
        for y in range(panel.y + 3, panel.y + panel.height // 3):
            factor = (y - panel.y) / (panel.height // 3)
            pygame.draw.line(self.screen, (int(30 + 40*factor), int(50 + 60*factor), int(100 - 30*factor)),
                           (panel.x + 3, y), (panel.right - 3, y))
        
        # Kráter uprostřed
        crater_cx = panel.centerx
        crater_cy = panel.centery + 60
        crater_r = 90
        # Okraj kráteru
        pygame.draw.ellipse(self.screen, (60, 50, 30),
                           (crater_cx - crater_r, crater_cy - crater_r // 2,
                            crater_r * 2, crater_r))
        pygame.draw.ellipse(self.screen, (40, 35, 20),
                           (crater_cx - crater_r + 15, crater_cy - crater_r // 2 + 10,
                            crater_r * 2 - 30, crater_r - 20))
        
        # Zbytky lodi v kráteru
        self._draw_simple_ship(self.screen, crater_cx, crater_cy, size=45, damage=2)
        
        # Prašné oblaka kolem
        dust_timer = self.panel_timer * 0.5
        for i in range(15):
            angle = i * 0.42 + dust_timer
            dist = crater_r + 20 + math.sin(dust_timer + i) * 30
            dx = crater_cx + int(math.cos(angle) * dist)
            dy = crater_cy + int(math.sin(angle) * dist * 0.5)
            dr = int(15 + 10 * abs(math.sin(dust_timer + i * 0.7)))
            dv = random.randint(100, 160)
            if panel.collidepoint(dx, dy):
                dust_surf = pygame.Surface((dr * 2, dr * 2), pygame.SRCALPHA)
                pygame.draw.circle(dust_surf, (dv, dv - 20, dv - 40, 100), (dr, dr), dr)
                self.screen.blit(dust_surf, (dx - dr, dy - dr))
        
        # SFX
        self._draw_sfx(self.screen, "KRRRACH!",
                       panel.centerx, panel.y + 60,
                       color=(255, 200, 80))
        
        # Kočka vyleza z trosek
        cat_tex = self.texture_manager.get_texture("cat")
        if cat_tex:
            cs = 60
            scaled = pygame.transform.scale(cat_tex, (cs, cs))
            self.screen.blit(scaled, (crater_cx + crater_r - 10, crater_cy - 50))
        
        self._draw_speech_bubble(self.screen,
            "...mňau. Kde to jsem?",
            crater_cx + crater_r + 30, crater_cy - 65, width=190)
        
        self._draw_narration_box(self.screen,
            "Loď havarovala na neznámé planetě. Nové dobrodružství začíná...",
            panel.x + 15, panel.bottom - 65, panel.width - 30)
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return "quit"
            if event.type == pygame.MOUSEBUTTONDOWN or (
                event.type == pygame.KEYDOWN and event.key in
                (pygame.K_SPACE, pygame.K_RETURN, pygame.K_RIGHT)):
                self.current_panel += 1
                self.panel_timer = 0
                if self.current_panel >= len(self.panels):
                    return "done"
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "done"
        return None
    
    def draw(self):
        self.screen.fill((5, 5, 15))
        self.panel_timer += 1 / FPS
        
        # Vykresli aktuální panel
        if self.current_panel < len(self.panels):
            self.panels[self.current_panel]()
        
        # Hint
        hint_alpha = int(128 + 127 * math.sin(self.panel_timer * 2))
        hint_color = (hint_alpha // 2, hint_alpha // 2, hint_alpha)
        panel_num = f"Panel {self.current_panel + 1}/{len(self.panels)}"
        hint = self.font_hint.render(
            f"{panel_num}  —  Klikni nebo stiskni SPACE pro další panel",
            True, hint_color)
        self.screen.blit(hint, (SCREEN_WIDTH // 2 - hint.get_width() // 2, SCREEN_HEIGHT - 25))
        
        pygame.display.flip()
    
    def run(self):
        while self.running:
            result = self.handle_events()
            if result in ("done", "quit"):
                return result
            self.draw()
            self.clock.tick(FPS)
        return "quit"

if __name__ == "__main__":
    print("Inicializuji hru...")
    pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Mimozemská Kočka")
    texture_manager = TextureManager()
    print("\nSpouštím menu...")
    
    state = "menu"
    
    while state != "quit":
        if state == "menu":
            menu = Menu(texture_manager)
            result = menu.run()
            if result == "play":
                state = "levels"
            else:
                state = "quit"
        
        elif state == "levels":
            level_select = LevelSelect(texture_manager)
            result = level_select.run()
            if result == "level1":
                state = "game1"
            elif result == "level2":
                state = "game2"
            elif result == "back":
                state = "menu"
            else:
                state = "quit"
        
        elif state == "game1":
            game = Game(texture_manager)
            result = game.run()
            if result == "won":
                lc = LevelComplete(texture_manager, "Laboratoř", game.cat.food_eaten)
                lc_result = lc.run()
                state = "levels" if lc_result == "levels" else "quit"
            else:
                state = "levels"
        
        elif state == "game2":
            game2 = GameLevel2(texture_manager)
            result = game2.run()
            if result == "won":
                lc = LevelComplete(texture_manager, "Řídící Centrum", game2.cat.food_eaten)
                lc_result = lc.run()
                if lc_result != "quit":
                    # Cutscéna po Level 2
                    cutscene = ComicCutscene(texture_manager)
                    cs_result = cutscene.run()
                    state = "levels" if cs_result == "done" else "quit"
                else:
                    state = "quit"
            else:
                state = "levels"
    
    pygame.quit()