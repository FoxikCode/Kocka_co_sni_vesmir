import pygame
import random
import math
import os

# Inicializace Pygame
pygame.init()

# Konstanty
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
FPS = 60
BASE_CAT_SIZE = 40
MAX_CAT_SIZE = 500

# Barvy
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARK_GRAY = (40, 40, 40)
LIGHT_GRAY = (200, 200, 200)
LAB_FLOOR = (220, 220, 220)

ALIEN_GREEN_DARK = (30, 120, 60)
ALIEN_GREEN_MAIN = (80, 180, 100)
ALIEN_GREEN_LIGHT = (120, 220, 140)

class TextureManager:
    """Správa textur - načítá PNG ze složky assets"""
    TEXTURE_NAMES = [
        "cat", "bug", "mouse", "container", "plant",
        "lab_floor", "lab_wall", "chair", "screen", "keyboard",
        "cable", "datapad", "cc_floor", "cc_wall",
        "alien_mushroom", "alien_vine", "alien_crystal_flower",
        "alien_bulb", "alien_tentacle_plant",
        "planet_floor", "planet_sky", "village_ground", "village_sky",
        "alien_villager", "alien_guard", "alien_child",
        "alien_farmer", "alien_merchant",
        "alien_building", "alien_tower", "alien_dome", "alien_factory",
        "mountain_chunk", "giant_tree", "giant_crystal", "lake",
        "meteorite", "asteroid", "planet_food",
        "small_planet", "gas_planet", "ice_planet", "lava_planet",
    ]

    def __init__(self):
        self.textures = {}
        self.assets_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
        self.load_textures()

    def load_textures(self):
        """Načte všechny textury z assets/"""
        for name in self.TEXTURE_NAMES:
            path = os.path.join(self.assets_path, f"{name}.png")
            if os.path.exists(path):
                try:
                    self.textures[name] = pygame.image.load(path).convert_alpha()
                except Exception as e:
                    print(f"[CHYBA] Nelze nacist '{name}': {e}")
                    self.textures[name] = None
            else:
                print(f"[CHYBA] Textura '{name}' nenalezena: {path}")
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
        
        self.font_title = pygame.font.Font(None, 60)
        self.font_button = pygame.font.Font(None, 32)
        self.font_desc = pygame.font.Font(None, 22)
        
        button_width = 300
        button_height = 55
        center_x = SCREEN_WIDTH // 2
        gap = 16
        row_gap = 72
        start_y = 100
        
        level_data = [
            ("Level 1: Laboratoř", (60, 130, 80), (80, 180, 100)),
            ("Level 2: Řídící Centrum", (40, 80, 160), (60, 120, 200)),
            ("Level 3: Cizí Planeta", (140, 60, 160), (180, 90, 200)),
            ("Level 4: Vesnice", (180, 100, 40), (220, 140, 60)),
            ("Level 5: Mimoz. Město", (120, 40, 140), (160, 70, 180)),
            ("Level 6: Obří Kočka", (60, 140, 50), (90, 180, 70)),
            ("Level 7: Vesmír", (40, 50, 140), (60, 80, 200)),
            ("Level 8: Požírač Planet", (180, 80, 20), (220, 120, 40)),
        ]
        
        self.level_buttons = []
        for i, (text, color, hover) in enumerate(level_data):
            row = i // 2
            col = i % 2
            bx = center_x - button_width - gap // 2 if col == 0 else center_x + gap // 2
            by = start_y + row * row_gap
            self.level_buttons.append(Button(
                bx, by, button_width, button_height, text,
                self.font_button, WHITE, color, hover
            ))
        
        self.back_button = Button(
            center_x - 100, start_y + 4 * row_gap + 10, 200, 50,
            "ZPĚT",
            self.font_button,
            WHITE,
            (120, 60, 60),
            (180, 80, 80)
        )
        
        self.level_descs = [
            "Sněz 50 malých věcí v laboratoři",
            "Sněz 50 velkých věcí v řídícím centru",
            "Sněz 50 zvláštních rostlin na planetě",
            "Sežer 50 mimozemšťanů ve vesnici!",
            "Žer baráky v mimozemském městě!",
            "Obří kočka jí hory, stromy a jezera!",
            "Jez meteority, na vel. 40 sněz planetu!",
            "Sežer všechny okolní planety!",
        ]
        self.desc_colors = [
            (180, 200, 180), (160, 180, 220), (200, 170, 220), (240, 180, 100),
            (220, 150, 240), (180, 240, 160), (160, 170, 255), (255, 180, 100),
        ]
        
        self.stars = [(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT),
                       random.random() * 2 + 0.5) for _ in range(120)]
        self.star_timer = 0
    
    def draw_background(self):
        for y in range(SCREEN_HEIGHT):
            r = int(10 + 20 * (y / SCREEN_HEIGHT))
            g = int(12 + 25 * (y / SCREEN_HEIGHT))
            b = int(30 + 40 * (y / SCREEN_HEIGHT))
            pygame.draw.line(self.screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))
        
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
                for i, btn in enumerate(self.level_buttons):
                    if btn.is_clicked(pos):
                        return f"level{i + 1}"
                if self.back_button.is_clicked(pos):
                    return "back"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "back"
        return None
    
    def update(self):
        pos = pygame.mouse.get_pos()
        for btn in self.level_buttons:
            btn.check_hover(pos)
        self.back_button.check_hover(pos)
    
    def draw(self):
        self.draw_background()
        
        title_text = self.font_title.render("Vyber si Level", True, WHITE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 50))
        self.screen.blit(title_text, title_rect)
        
        for btn in self.level_buttons:
            btn.draw(self.screen)
        self.back_button.draw(self.screen)
        
        # Popisy levelů
        for i, btn in enumerate(self.level_buttons):
            desc = self.font_desc.render(self.level_descs[i], True, self.desc_colors[i])
            desc_rect = desc.get_rect(center=(btn.rect.centerx, btn.rect.bottom + 10))
            self.screen.blit(desc, desc_rect)
        
        pygame.display.flip()
    
    def run(self):
        while self.running:
            result = self.handle_events()
            if result and (result.startswith("level") or result in ("back", "quit")):
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
        # Střed jídla
        food_cx = self.x + self.width / 2
        food_cy = self.y + self.height / 2
        food_radius = min(self.width, self.height) * 0.3
        
        # Kočka - střed je cat.x, cat.y, hodně zmenšený poloměr aby se musela opravdu dotknout
        cat_radius = cat.size * 0.35
        
        # Vzdálenost středů
        dx = cat.x - food_cx
        dy = cat.y - food_cy
        dist = math.sqrt(dx * dx + dy * dy)
        
        # Kolize nastane jen když se středy hodně přiblíží
        return dist < (cat_radius + food_radius)

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
        self.max_size = MAX_CAT_SIZE
        self.growth_per_food = 3
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
        
        # Omezení na okraj obrazovky (střed kočky nesmí přesáhnout okraj)
        self.x = max(0, min(self.x, SCREEN_WIDTH))
        self.y = max(0, min(self.y, SCREEN_HEIGHT))
        
        self.animation_counter += 1
        if self.vx != 0 or self.vy != 0:
            self.animation_walk += 0.2
    
    def eat_food(self, food):
        if self.size < self.max_size:
            self.size += self.growth_per_food
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
        
        # Animované efekty laboratoře
        self.lab_light_timer = 0
        self.lab_sparks = []
        for _ in range(8):
            self.lab_sparks.append([
                random.randint(50, SCREEN_WIDTH - 50),
                random.randint(140, SCREEN_HEIGHT - 50),
                random.random() * 3 + 1,
                random.randint(150, 255)
            ])
    
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
        
        # Laboratorní vybavení na stěně - nádrže
        for tx, tw, th in [(80, 60, 80), (300, 50, 90), (700, 70, 75), (1050, 55, 85)]:
            tank_y = wall_height - th + 10
            # Sklo nádrže
            tank_surf = pygame.Surface((tw, th), pygame.SRCALPHA)
            pygame.draw.rect(tank_surf, (20, 80, 70, 100), (0, 0, tw, th), border_radius=5)
            pygame.draw.rect(tank_surf, (30, 180, 150, 150), (0, 0, tw, th), 2, border_radius=5)
            # Tekutina uvnitř
            liquid_h = int(th * 0.6)
            pygame.draw.rect(tank_surf, (20, 160, 120, 80), (3, th - liquid_h, tw - 6, liquid_h - 3))
            # Bubliny
            for _ in range(3):
                bx = random.randint(8, tw - 8)
                by = random.randint(th - liquid_h + 5, th - 8)
                pygame.draw.circle(tank_surf, (40, 220, 180, 120), (bx, by), random.randint(2, 5))
            bg.blit(tank_surf, (tx, tank_y))
        
        # Regály / police na stěně
        for sx in [180, 500, 870]:
            shelf_y = wall_height - 40
            pygame.draw.rect(bg, (70, 75, 88), (sx, shelf_y, 90, 6))
            pygame.draw.rect(bg, (50, 55, 68), (sx, shelf_y, 90, 6), 1)
            # Předměty na polici
            for ox in range(0, 80, 20):
                oh = random.randint(10, 25)
                color = random.choice([(180, 60, 60), (60, 180, 80), (60, 80, 180), (180, 180, 60)])
                pygame.draw.rect(bg, color, (sx + 5 + ox, shelf_y - oh, 14, oh))
        
        # Stropní světla (pásy)
        for lx in [150, 400, 650, 900, 1100]:
            # Tělo světla
            pygame.draw.rect(bg, (160, 165, 175), (lx - 30, wall_height + 5, 60, 4))
            pygame.draw.rect(bg, (200, 210, 220), (lx - 25, wall_height + 6, 50, 2))
            # Kužel světla (jemný)
            light_surf = pygame.Surface((120, 80), pygame.SRCALPHA)
            for ly in range(80):
                alpha = max(0, 25 - ly // 3)
                width = 20 + ly
                pygame.draw.line(light_surf, (180, 220, 200, alpha),
                               (60 - width // 2, ly), (60 + width // 2, ly))
            bg.blit(light_surf, (lx - 60, wall_height + 10))
        
        # Potrubí podél spodní hrany stěny
        pipe_y = wall_height - 8
        pygame.draw.line(bg, (100, 105, 115), (0, pipe_y), (SCREEN_WIDTH, pipe_y), 4)
        pygame.draw.line(bg, (130, 135, 145), (0, pipe_y - 1), (SCREEN_WIDTH, pipe_y - 1), 1)
        # Spoje potrubí
        for jx in range(0, SCREEN_WIDTH, 120):
            pygame.draw.circle(bg, (140, 145, 155), (jx, pipe_y + 1), 5)
            pygame.draw.circle(bg, (80, 85, 95), (jx, pipe_y + 1), 5, 1)
        
        return bg

    def draw_laboratory(self):
        # Vykreslí předrenderované pixel-art pozadí
        self.screen.blit(self.bg_surface, (0, 0))
        
        # Animované efekty - blikající jiskry u přístrojů
        self.lab_light_timer += 0.04
        for spark in self.lab_sparks:
            spark[3] = int(120 + 100 * math.sin(self.lab_light_timer * spark[2]))
            spark_surf = pygame.Surface((6, 6), pygame.SRCALPHA)
            alpha = max(0, min(255, spark[3]))
            pygame.draw.circle(spark_surf, (30, 200, 170, alpha), (3, 3), 3)
            self.screen.blit(spark_surf, (int(spark[0]) - 3, int(spark[1]) - 3))
        
        # Zelený ambientní glow na podlaze (pulsující)
        glow_alpha = int(15 + 10 * math.sin(self.lab_light_timer * 0.5))
        for gx, gy, gr in [(200, 400, 80), (600, 350, 100), (900, 500, 70), (400, 550, 90)]:
            glow_surf = pygame.Surface((gr * 2, gr * 2), pygame.SRCALPHA)
            pygame.draw.circle(glow_surf, (30, 180, 150, glow_alpha), (gr, gr), gr)
            self.screen.blit(glow_surf, (gx - gr, gy - gr))
        
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
        
        # Animované efekty řídícího centra
        self.holo_timer = 0
        self.holo_particles = []
        for _ in range(15):
            self.holo_particles.append([
                random.randint(100, SCREEN_WIDTH - 100),
                random.randint(150, SCREEN_HEIGHT - 100),
                random.random() * 2 + 0.5,
                random.randint(0, 360)
            ])
        # Hvězdy ve výhledu
        self.viewport_stars = [(random.randint(0, 400), random.randint(0, 80),
                                random.random() * 2 + 0.5) for _ in range(60)]
    
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
        
        # Velké panoramatické okno s výhledem do vesmíru
        viewport_x, viewport_w, viewport_h = 400, 400, 90
        viewport_y = 15
        # Vesmírné pozadí v okně
        for vy in range(viewport_h):
            factor = vy / viewport_h
            r = int(5 + 10 * factor)
            g = int(5 + 15 * factor)
            b = int(20 + 30 * (1 - factor))
            pygame.draw.line(bg, (r, g, b),
                           (viewport_x, viewport_y + vy),
                           (viewport_x + viewport_w, viewport_y + vy))
        # Statické hvězdy v okně
        for _ in range(40):
            sx = viewport_x + random.randint(5, viewport_w - 5)
            sy = viewport_y + random.randint(5, viewport_h - 5)
            brightness = random.randint(120, 255)
            bg.set_at((sx, sy), (brightness, brightness, min(255, brightness + 30)))
        # Vzdálená mlhovina
        nebula_surf = pygame.Surface((120, 50), pygame.SRCALPHA)
        pygame.draw.ellipse(nebula_surf, (40, 20, 80, 30), (0, 0, 120, 50))
        pygame.draw.ellipse(nebula_surf, (60, 30, 100, 20), (20, 10, 80, 30))
        bg.blit(nebula_surf, (viewport_x + 50, viewport_y + 20))
        # Rám okna
        pygame.draw.rect(bg, (60, 70, 100), (viewport_x, viewport_y, viewport_w, viewport_h), 3)
        pygame.draw.rect(bg, (30, 120, 200), (viewport_x + 1, viewport_y + 1, viewport_w - 2, viewport_h - 2), 1)
        # Příčky okna
        pygame.draw.line(bg, (50, 60, 90), (viewport_x + viewport_w // 3, viewport_y),
                        (viewport_x + viewport_w // 3, viewport_y + viewport_h), 2)
        pygame.draw.line(bg, (50, 60, 90), (viewport_x + 2 * viewport_w // 3, viewport_y),
                        (viewport_x + 2 * viewport_w // 3, viewport_y + viewport_h), 2)
        
        # Přechodová linka - modrý glow
        pygame.draw.line(bg, (20, 100, 255), (0, wall_height), (SCREEN_WIDTH, wall_height), 2)
        pygame.draw.line(bg, (15, 60, 150), (0, wall_height + 2), (SCREEN_WIDTH, wall_height + 2), 1)
        
        if floor_tile:
            for x in range(0, SCREEN_WIDTH, tile_size):
                for y in range(wall_height + 3, SCREEN_HEIGHT, tile_size):
                    bg.blit(floor_tile, (x, y))
        else:
            bg.fill((35, 40, 55), (0, wall_height + 3, SCREEN_WIDTH, SCREEN_HEIGHT - wall_height - 3))
        
        # Konzolové stanice po stranách  
        for cx, cw in [(20, 100), (SCREEN_WIDTH - 120, 100)]:
            console_y = wall_height + 10
            # Tělo konzole
            pygame.draw.rect(bg, (40, 45, 65), (cx, console_y, cw, 60))
            pygame.draw.rect(bg, (55, 60, 80), (cx, console_y, cw, 60), 2)
            # Displej
            pygame.draw.rect(bg, (5, 15, 30), (cx + 8, console_y + 5, cw - 16, 30))
            # Data na displeji
            for row in range(3):
                line_w = random.randint(20, cw - 30)
                pygame.draw.line(bg, (20, 150, 220),
                               (cx + 12, console_y + 12 + row * 8),
                               (cx + 12 + line_w, console_y + 12 + row * 8), 1)
            # Indikátory
            for ix in range(4):
                color = random.choice([(40, 200, 80), (200, 40, 40), (40, 150, 255)])
                pygame.draw.circle(bg, color, (cx + 15 + ix * 20, console_y + 48), 3)
        
        # Holografický projektor na podlaze (kruhová platforma)
        holo_cx, holo_cy = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80
        pygame.draw.ellipse(bg, (30, 40, 60), (holo_cx - 60, holo_cy - 15, 120, 30))
        pygame.draw.ellipse(bg, (20, 80, 180), (holo_cx - 60, holo_cy - 15, 120, 30), 2)
        pygame.draw.ellipse(bg, (15, 60, 140), (holo_cx - 50, holo_cy - 10, 100, 20), 1)
        
        # Podlahové LED pásy
        for ly in [wall_height + 80, SCREEN_HEIGHT - 60]:
            for lx in range(0, SCREEN_WIDTH, 8):
                blue_val = 60 + (lx % 40)
                pygame.draw.rect(bg, (10, 30, blue_val), (lx, ly, 5, 2))
        
        return bg

    def draw_command_center(self):
        self.screen.blit(self.bg_surface, (0, 0))
        
        # Animovaný holografický efekt
        self.holo_timer += 0.03
        holo_cx, holo_cy = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80
        # Holografické kroužky
        for i in range(3):
            radius = 30 + i * 15 + int(5 * math.sin(self.holo_timer * 2 + i))
            alpha = int(40 + 30 * math.sin(self.holo_timer * 1.5 + i * 2))
            holo_ring = pygame.Surface((radius * 2, radius), pygame.SRCALPHA)
            pygame.draw.ellipse(holo_ring, (20, 120, 255, alpha), (0, 0, radius * 2, radius), 1)
            self.screen.blit(holo_ring, (holo_cx - radius, holo_cy - 40 - i * 20 - radius // 2))
        
        # Holografické částice stoupající vzhůru
        for p in self.holo_particles:
            p[1] -= p[2] * 0.3
            p[3] += 2
            if p[1] < holo_cy - 120:
                p[1] = holo_cy - 10
                p[0] = holo_cx + random.randint(-40, 40)
            alpha = int(60 + 40 * math.sin(self.holo_timer * p[2]))
            psf = pygame.Surface((4, 4), pygame.SRCALPHA)
            pygame.draw.circle(psf, (30, 150, 255, max(0, min(255, alpha))), (2, 2), 2)
            self.screen.blit(psf, (int(p[0]) - 2, int(p[1]) - 2))
        
        # Animované hvězdičky ve výhledu
        viewport_x, viewport_y, viewport_w, viewport_h = 400, 15, 400, 90
        for sx, sy, spd in self.viewport_stars:
            sx_anim = (sx + self.holo_timer * spd * 8) % viewport_w
            screen_sx = viewport_x + int(sx_anim)
            screen_sy = viewport_y + sy
            brightness = int(150 + 80 * math.sin(self.holo_timer * spd))
            brightness = max(0, min(255, brightness))
            if viewport_x + 3 < screen_sx < viewport_x + viewport_w - 3:
                self.screen.set_at((screen_sx, screen_sy), (brightness, brightness, min(255, brightness + 30)))
        
        # Modrý ambientní glow
        glow_alpha = int(10 + 8 * math.sin(self.holo_timer * 0.7))
        for gx, gy, gr in [(150, 300, 70), (SCREEN_WIDTH - 150, 300, 70), (SCREEN_WIDTH // 2, 450, 100)]:
            glow_surf = pygame.Surface((gr * 2, gr * 2), pygame.SRCALPHA)
            pygame.draw.circle(glow_surf, (20, 80, 200, glow_alpha), (gr, gr), gr)
            self.screen.blit(glow_surf, (gx - gr, gy - gr))
        
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

class GameLevel3:
    """Level 3 - Cizí Planeta (sněz 50 zvláštních rostlin)"""
    FOOD_GOAL = 50
    
    def __init__(self, texture_manager):
        self.screen = pygame.display.get_surface()
        self.clock = pygame.time.Clock()
        self.running = True
        self.won = False
        self.texture_manager = texture_manager
        
        self.cat = AlienCat(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, texture_manager)
        self.cat.size = 35  # Menší na planetě
        self.cat.speed = 5.5
        self.foods = []
        self.bg_surface = self._build_background()
        self.spawn_food()
        
        # Efekty planety
        self.wind_particles = []
        self.ambient_timer = 0
        for _ in range(30):
            self.wind_particles.append([
                random.randint(0, SCREEN_WIDTH),
                random.randint(0, SCREEN_HEIGHT),
                random.random() * 2 + 1,
                random.choice([(100, 255, 100, 40), (200, 150, 255, 30), (255, 255, 100, 35)])
            ])
        # Plovoucí kameny v obloze
        self.floating_rocks = []
        for _ in range(6):
            self.floating_rocks.append([
                random.randint(50, SCREEN_WIDTH - 50),
                random.randint(20, 100),
                random.randint(10, 25),
                random.random() * 2 + 0.5
            ])
        # Aurora efekt
        self.aurora_points = []
        for i in range(20):
            self.aurora_points.append(i * (SCREEN_WIDTH // 20))
    
    def spawn_food(self):
        for _ in range(10):
            x = random.randint(60, SCREEN_WIDTH - 60)
            y = random.randint(160, SCREEN_HEIGHT - 60)
            food_type = random.choice([
                "alien_mushroom", "alien_vine", "alien_crystal_flower",
                "alien_bulb", "alien_tentacle_plant"
            ])
            food = Food(x, y, food_type, self.texture_manager)
            food.width = random.randint(40, 65)
            food.height = random.randint(40, 65)
            self.foods.append(food)
    
    def _build_background(self):
        """Sestaví pozadí mimozemské planety"""
        bg = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        
        floor_tile = self.texture_manager.get_texture("planet_floor")
        sky_tile = self.texture_manager.get_texture("planet_sky")
        
        tile_size = 64
        sky_height = 128
        
        # Obloha
        if sky_tile:
            for x in range(0, SCREEN_WIDTH, tile_size):
                for y in range(0, sky_height, tile_size):
                    bg.blit(sky_tile, (x, y))
        else:
            for y in range(sky_height):
                factor = y / sky_height
                r = int(25 + 35 * factor)
                g = int(15 + 50 * factor)
                b = int(45 + 30 * (1 - factor))
                pygame.draw.line(bg, (r, g, b), (0, y), (SCREEN_WIDTH, y))
        
        # Vzdálená mlhovina na obloze
        nebula_surf = pygame.Surface((200, 60), pygame.SRCALPHA)
        pygame.draw.ellipse(nebula_surf, (80, 20, 120, 25), (0, 0, 200, 60))
        pygame.draw.ellipse(nebula_surf, (100, 40, 150, 15), (40, 15, 120, 30))
        bg.blit(nebula_surf, (100, 10))
        nebula_surf2 = pygame.Surface((150, 45), pygame.SRCALPHA)
        pygame.draw.ellipse(nebula_surf2, (20, 80, 60, 20), (0, 0, 150, 45))
        bg.blit(nebula_surf2, (800, 25))
        
        # Měsíc
        moon_surf = pygame.Surface((40, 40), pygame.SRCALPHA)
        pygame.draw.circle(moon_surf, (200, 160, 100, 180), (20, 20), 18)
        pygame.draw.circle(moon_surf, (220, 190, 130, 100), (16, 16), 12)
        bg.blit(moon_surf, (900, 15))
        
        # Přechodová linka - zelený glow (hezčí gradient přechod)
        for dy in range(8):
            alpha = 255 - dy * 30
            green = max(0, 255 - dy * 25)
            pygame.draw.line(bg, (30, min(255, green), 30),
                           (0, sky_height - 2 + dy), (SCREEN_WIDTH, sky_height - 2 + dy))
        pygame.draw.line(bg, (80, 255, 80), (0, sky_height), (SCREEN_WIDTH, sky_height), 2)
        
        # Povrch planety
        if floor_tile:
            for x in range(0, SCREEN_WIDTH, tile_size):
                for y in range(sky_height + 3, SCREEN_HEIGHT, tile_size):
                    bg.blit(floor_tile, (x, y))
        else:
            bg.fill((55, 85, 45), (0, sky_height + 3, SCREEN_WIDTH, SCREEN_HEIGHT - sky_height - 3))
        
        # Vzdálené horoviny na horizontu
        mountains = [(0, 50), (80, 30), (200, 55), (300, 20), (420, 45), (520, 15),
                     (640, 50), (750, 25), (860, 55), (960, 30), (1060, 45), (1160, 35)]
        for i in range(len(mountains) - 1):
            mx1, mh1 = mountains[i]
            mx2, mh2 = mountains[i + 1]
            pts = [(mx1, sky_height + 10), (mx1 + (mx2 - mx1) // 2, sky_height + 10 - max(mh1, mh2)),
                   (mx2, sky_height + 10)]
            pygame.draw.polygon(bg, (35, 55, 30), pts)
            pygame.draw.polygon(bg, (40, 65, 35), pts, 1)
        
        # Dekorativní velké kameny a kopce na pozadí
        for cx, cy, r in [(150, sky_height + 30, 40), (500, sky_height + 20, 55),
                          (900, sky_height + 35, 35), (1100, sky_height + 25, 45)]:
            pygame.draw.ellipse(bg, (45, 70, 35),
                              (cx - r, cy - r // 2, r * 2, r))
            pygame.draw.ellipse(bg, (55, 85, 45),
                              (cx - r + 5, cy - r // 2 + 3, r * 2 - 10, r - 6))
        
        # Mimozemské stromy/houby na pozadí (siluety)
        for tx, th in [(100, 45), (350, 60), (550, 40), (800, 55), (1050, 50)]:
            ty = sky_height + 15
            # Kmen
            pygame.draw.rect(bg, (40, 60, 35), (tx - 3, ty, 6, th))
            # Koruna (svítivá)
            crown_surf = pygame.Surface((40, 30), pygame.SRCALPHA)
            pygame.draw.ellipse(crown_surf, (50, 100, 40, 120), (0, 0, 40, 30))
            pygame.draw.ellipse(crown_surf, (60, 130, 50, 60), (5, 5, 30, 20))
            bg.blit(crown_surf, (tx - 20, ty - 25))
        
        # Svítivé krystaly na zemi
        for kx, ky, kh in [(250, sky_height + 70, 20), (600, sky_height + 90, 15),
                           (850, sky_height + 75, 18), (1000, sky_height + 100, 12)]:
            crystal_surf = pygame.Surface((12, kh + 10), pygame.SRCALPHA)
            pygame.draw.polygon(crystal_surf, (80, 220, 255, 80),
                              [(6, 0), (0, kh), (12, kh)])
            pygame.draw.polygon(crystal_surf, (100, 240, 255, 120),
                              [(6, 0), (0, kh), (12, kh)], 1)
            bg.blit(crystal_surf, (kx, ky))
        
        return bg

    def draw_planet_hud(self):
        self.screen.blit(self.bg_surface, (0, 0))
        
        # Animované částice větru
        self.ambient_timer += 0.02
        for p in self.wind_particles:
            p[0] += p[2]
            p[1] += math.sin(self.ambient_timer + p[0] * 0.01) * 0.5
            if p[0] > SCREEN_WIDTH:
                p[0] = 0
                p[1] = random.randint(0, SCREEN_HEIGHT)
            particle_surf = pygame.Surface((4, 4), pygame.SRCALPHA)
            pygame.draw.circle(particle_surf, p[3], (2, 2), 2)
            self.screen.blit(particle_surf, (int(p[0]), int(p[1])))
        
        # Aurora efekt na obloze
        aurora_surf = pygame.Surface((SCREEN_WIDTH, 60), pygame.SRCALPHA)
        for i in range(len(self.aurora_points) - 1):
            x1 = self.aurora_points[i]
            x2 = self.aurora_points[i + 1]
            y1 = 30 + int(15 * math.sin(self.ambient_timer * 0.8 + i * 0.5))
            y2 = 30 + int(15 * math.sin(self.ambient_timer * 0.8 + (i + 1) * 0.5))
            alpha = int(20 + 15 * math.sin(self.ambient_timer + i * 0.3))
            # Fialovo-zelená aurora
            r = int(60 + 40 * math.sin(self.ambient_timer * 0.3 + i))
            g = int(150 + 60 * math.sin(self.ambient_timer * 0.5 + i * 0.7))
            b = int(100 + 50 * math.sin(self.ambient_timer * 0.4 + i * 1.2))
            pygame.draw.line(aurora_surf, (r, g, b, max(0, min(255, alpha))),
                           (x1, y1), (x2, y2), 4)
            pygame.draw.line(aurora_surf, (r, g, b, max(0, min(255, alpha // 2))),
                           (x1, y1 - 5), (x2, y2 - 5), 6)
        self.screen.blit(aurora_surf, (0, 15))
        
        # Plovoucí kameny
        for rock in self.floating_rocks:
            rock[1] = rock[1] + math.sin(self.ambient_timer * rock[3]) * 0.2
            rx, ry, rs = int(rock[0]), int(rock[1]), rock[2]
            rock_surf = pygame.Surface((rs * 2, rs * 2), pygame.SRCALPHA)
            pygame.draw.ellipse(rock_surf, (70, 60, 50, 160), (0, rs // 3, rs * 2, rs))
            pygame.draw.ellipse(rock_surf, (90, 80, 65, 100), (3, rs // 3 + 3, rs * 2 - 6, rs - 6))
            # Glow pod kamenem
            pygame.draw.ellipse(rock_surf, (80, 200, 100, 30), (rs // 2, rs + rs // 2, rs, rs // 3))
            self.screen.blit(rock_surf, (rx - rs, ry - rs))
        
        font_small = pygame.font.Font(None, 28)
        font_title = pygame.font.Font(None, 36)
        
        title_text = font_title.render("Level 3: Cizí Planeta", True, (180, 120, 255))
        self.screen.blit(title_text, (20, 10))
        
        size_text = font_small.render(f"Velikost: {self.cat.size:.0f} / {MAX_CAT_SIZE}", True, (200, 180, 255))
        self.screen.blit(size_text, (SCREEN_WIDTH - 350, 15))
        
        food_text = font_small.render(f"Rostliny snědeny: {self.cat.food_eaten} / {self.FOOD_GOAL}", True, (200, 180, 255))
        self.screen.blit(food_text, (SCREEN_WIDTH - 350, 45))
        
        progress_width = 300
        progress_height = 15
        progress_x = SCREEN_WIDTH - 350
        progress_y = 75
        
        pygame.draw.rect(self.screen, (40, 25, 50),
                        (progress_x, progress_y, progress_width, progress_height))
        
        filled_width = min(1.0, self.cat.food_eaten / self.FOOD_GOAL) * progress_width
        # Gradient fialovo-zelený
        green_part = self.cat.food_eaten / self.FOOD_GOAL
        bar_color = (int(160 - 80 * green_part), int(80 + 150 * green_part), int(200 - 100 * green_part))
        pygame.draw.rect(self.screen, bar_color,
                        (progress_x, progress_y, filled_width, progress_height))
        
        pygame.draw.rect(self.screen, (180, 120, 255),
                        (progress_x, progress_y, progress_width, progress_height), 2)
        
        controls_text = font_small.render("WASD nebo Šipky = Pohyb | ESC = Zpět", True, (120, 100, 140))
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
        if alive_foods < 4:
            self.spawn_food()
    
    def draw(self):
        self.screen.fill((30, 50, 25))
        self.draw_planet_hud()
        
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


class Guard:
    """Nepřátelský strážce, který pronásleduje kočku"""
    def __init__(self, x, y, texture_manager):
        self.x = x
        self.y = y
        self.width = 60
        self.height = 60
        self.speed = 2.0
        self.alive = True
        self.texture_manager = texture_manager
        self.damage_cooldown = 0

    def update(self, cat):
        if not self.alive:
            return
        # Pronásledování kočky
        dx = cat.x - self.x
        dy = cat.y - self.y
        dist = math.hypot(dx, dy)
        if dist > 0:
            self.x += (dx / dist) * self.speed
            self.y += (dy / dist) * self.speed
        if self.damage_cooldown > 0:
            self.damage_cooldown -= 1

    def collides_with(self, cat):
        cat_left = cat.x - cat.size
        cat_right = cat.x + cat.size
        cat_top = cat.y - cat.size
        cat_bottom = cat.y + cat.size
        # Menší hitbox než vizuální velikost (60% šířky/výšky)
        hb_w = self.width * 0.6
        hb_h = self.height * 0.6
        g_left = self.x - hb_w / 2
        g_right = self.x + hb_w / 2
        g_top = self.y - hb_h / 2
        g_bottom = self.y + hb_h / 2
        return not (g_right < cat_left or g_left > cat_right or
                    g_bottom < cat_top or g_top > cat_bottom)

    def draw(self, screen):
        if not self.alive:
            return
        texture = self.texture_manager.get_texture("alien_guard")
        if texture:
            scaled = pygame.transform.scale(texture, (self.width, self.height))
            rect = scaled.get_rect(center=(int(self.x), int(self.y)))
            screen.blit(scaled, rect)


class GameLevel4:
    """Level 4 - Vesnice mimozemšťanů (sežer 50 mimozemšťanů)"""
    FOOD_GOAL = 50
    
    def __init__(self, texture_manager):
        self.screen = pygame.display.get_surface()
        self.clock = pygame.time.Clock()
        self.running = True
        self.won = False
        self.texture_manager = texture_manager
        
        self.cat = AlienCat(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, texture_manager)
        self.cat.size = 45  # Kočka je už dost velká
        self.cat.speed = 5
        self.cat.hp = 100
        self.cat.max_hp = 100
        self.foods = []
        self.guards = []
        self.bg_surface = self._build_background()
        self.spawn_food()
        self.spawn_guards()
        self.guard_spawn_timer = 0
        self.damage_flash = 0
        
        # Efekty vesnice - světélkující částice a kouř z chatek
        self.smoke_particles = []
        self.ambient_timer = 0
        self.fireflies = []
        for _ in range(25):
            self.fireflies.append([
                random.randint(0, SCREEN_WIDTH),
                random.randint(0, SCREEN_HEIGHT),
                random.random() * 2 + 0.5,
                random.choice([(255, 200, 80, 50), (100, 255, 150, 40), (200, 150, 255, 45)])
            ])
        # Kouřové body nad chatkami
        self.hut_positions = [(150, 155), (400, 145), (700, 150), (950, 148)]
        for hx, hy in self.hut_positions:
            for _ in range(3):
                self.smoke_particles.append([
                    hx + random.randint(-10, 10),
                    hy,
                    random.random() * 0.5 + 0.3,
                    random.randint(60, 100)
                ])
    
    def spawn_guards(self):
        """Spawnuje strážce na okrajích mapy"""
        for _ in range(3):
            side = random.choice(["left", "right", "top", "bottom"])
            if side == "left":
                x, y = 30, random.randint(170, SCREEN_HEIGHT - 60)
            elif side == "right":
                x, y = SCREEN_WIDTH - 30, random.randint(170, SCREEN_HEIGHT - 60)
            elif side == "top":
                x, y = random.randint(60, SCREEN_WIDTH - 60), 170
            else:
                x, y = random.randint(60, SCREEN_WIDTH - 60), SCREEN_HEIGHT - 30
            self.guards.append(Guard(x, y, self.texture_manager))

    def spawn_food(self):
        for _ in range(8):
            x = random.randint(60, SCREEN_WIDTH - 60)
            y = random.randint(170, SCREEN_HEIGHT - 60)
            food_type = random.choice([
                "alien_villager", "alien_villager",
                "alien_child", "alien_farmer", "alien_merchant"
            ])
            food = Food(x, y, food_type, self.texture_manager)
            if food_type == "alien_child":
                food.width = random.randint(25, 35)
                food.height = random.randint(25, 35)
            elif food_type == "alien_merchant":
                food.width = random.randint(50, 65)
                food.height = random.randint(50, 65)
            else:
                food.width = random.randint(40, 55)
                food.height = random.randint(40, 55)
            self.foods.append(food)
    
    def _build_background(self):
        """Sestaví pozadí mimozemské vesnice"""
        bg = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        
        floor_tile = self.texture_manager.get_texture("village_ground")
        sky_tile = self.texture_manager.get_texture("village_sky")
        
        tile_size = 64
        sky_height = 128
        
        # Obloha
        if sky_tile:
            for x in range(0, SCREEN_WIDTH, tile_size):
                for y in range(0, sky_height, tile_size):
                    bg.blit(sky_tile, (x, y))
        else:
            for y in range(sky_height):
                factor = y / sky_height
                r = int(30 + 50 * factor)
                g = int(15 + 30 * factor)
                b = int(60 + 40 * (1 - factor))
                pygame.draw.line(bg, (r, g, b), (0, y), (SCREEN_WIDTH, y))
        
        # Mlhovina na obloze
        nebula_surf = pygame.Surface((180, 50), pygame.SRCALPHA)
        pygame.draw.ellipse(nebula_surf, (120, 50, 80, 20), (0, 0, 180, 50))
        pygame.draw.ellipse(nebula_surf, (150, 70, 100, 12), (30, 10, 120, 30))
        bg.blit(nebula_surf, (600, 8))
        
        # Vzdálené hory na horizontu
        mountain_pts = [(0, sky_height - 5)]
        for mx in range(0, SCREEN_WIDTH + 50, 60):
            mh = random.randint(20, 55)
            mountain_pts.append((mx + 30, sky_height - 5 - mh))
            mountain_pts.append((mx + 60, sky_height - 5))
        mountain_pts.append((SCREEN_WIDTH, sky_height - 5))
        pygame.draw.polygon(bg, (50, 35, 55), mountain_pts)
        # Světlejší vrstva hor
        mountain_pts2 = [(0, sky_height - 2)]
        for mx in range(0, SCREEN_WIDTH + 50, 80):
            mh = random.randint(10, 35)
            mountain_pts2.append((mx + 40, sky_height - 2 - mh))
            mountain_pts2.append((mx + 80, sky_height - 2))
        mountain_pts2.append((SCREEN_WIDTH, sky_height - 2))
        pygame.draw.polygon(bg, (60, 45, 40), mountain_pts2)
        
        # Přechodová linka - žluto-oranžový glow (gradient)
        for dy in range(6):
            r_val = max(0, 200 - dy * 20)
            g_val = max(0, 150 - dy * 20)
            b_val = max(0, 60 - dy * 10)
            pygame.draw.line(bg, (r_val, g_val, b_val),
                           (0, sky_height - 1 + dy), (SCREEN_WIDTH, sky_height - 1 + dy))
        pygame.draw.line(bg, (200, 150, 60), (0, sky_height), (SCREEN_WIDTH, sky_height), 2)
        
        # Povrch vesnice
        if floor_tile:
            for x in range(0, SCREEN_WIDTH, tile_size):
                for y in range(sky_height + 3, SCREEN_HEIGHT, tile_size):
                    bg.blit(floor_tile, (x, y))
        else:
            bg.fill((70, 55, 40), (0, sky_height + 3, SCREEN_WIDTH, SCREEN_HEIGHT - sky_height - 3))
        
        # Chatky na pozadí (dekorace) - bohatší
        for hx, hy in [(150, sky_height + 10), (400, sky_height + 5),
                        (700, sky_height + 12), (950, sky_height + 8)]:
            # Stěna chatky
            hw, hh = 80, 50
            pygame.draw.rect(bg, (120, 100, 60), (hx - hw // 2, hy, hw, hh))
            pygame.draw.rect(bg, (90, 75, 45), (hx - hw // 2, hy, hw, hh), 2)
            # Vzory na stěně (mimozemské symboly)
            for sy in range(hy + 5, hy + hh - 5, 12):
                symbol_color = (140, 120, 70)
                pygame.draw.line(bg, symbol_color,
                               (hx - hw // 2 + 5, sy), (hx - hw // 2 + 15, sy), 1)
                pygame.draw.line(bg, symbol_color,
                               (hx + hw // 2 - 15, sy), (hx + hw // 2 - 5, sy), 1)
            # Střecha (trojúhelník) - lepší
            pygame.draw.polygon(bg, (160, 80, 40), [
                (hx - hw // 2 - 10, hy),
                (hx + hw // 2 + 10, hy),
                (hx, hy - 35)
            ])
            pygame.draw.polygon(bg, (130, 60, 30), [
                (hx - hw // 2 - 10, hy),
                (hx + hw // 2 + 10, hy),
                (hx, hy - 35)
            ], 2)
            # Dekorace na střeše
            pygame.draw.circle(bg, (200, 160, 50), (hx, hy - 30), 4)
            # Dveře
            pygame.draw.rect(bg, (80, 60, 35), (hx - 10, hy + 15, 20, 35))
            pygame.draw.rect(bg, (60, 45, 25), (hx - 10, hy + 15, 20, 35), 1)
            # Klika
            pygame.draw.circle(bg, (160, 140, 80), (hx + 6, hy + 32), 2)
            # Okno - svítivé
            pygame.draw.rect(bg, (180, 200, 100), (hx + 18, hy + 12, 15, 15))
            pygame.draw.rect(bg, (100, 80, 50), (hx + 18, hy + 12, 15, 15), 1)
            pygame.draw.rect(bg, (220, 230, 150), (hx + 20, hy + 14, 11, 11))
            # Glow kolem okna
            window_glow = pygame.Surface((25, 25), pygame.SRCALPHA)
            pygame.draw.rect(window_glow, (220, 200, 100, 25), (0, 0, 25, 25))
            bg.blit(window_glow, (hx + 15, hy + 9))
        
        # Plůtky mezi chatkami
        for fx in range(0, SCREEN_WIDTH, 40):
            fy = sky_height + 65
            pygame.draw.line(bg, (100, 80, 50), (fx, fy), (fx, fy + 20), 2)
            pygame.draw.line(bg, (100, 80, 50), (fx, fy + 5), (fx + 38, fy + 5), 1)
            pygame.draw.line(bg, (100, 80, 50), (fx, fy + 15), (fx + 38, fy + 15), 1)
        
        # Pochodně / svítidla podél cesty
        for tx in [250, 550, 850, 1100]:
            torch_y = sky_height + 55
            # Sloup
            pygame.draw.rect(bg, (80, 65, 45), (tx - 2, torch_y, 4, 30))
            # Plamen (statická oranžová záře)
            flame_surf = pygame.Surface((20, 20), pygame.SRCALPHA)
            pygame.draw.circle(flame_surf, (255, 180, 50, 120), (10, 10), 8)
            pygame.draw.circle(flame_surf, (255, 220, 100, 80), (10, 8), 5)
            bg.blit(flame_surf, (tx - 10, torch_y - 15))
            # Glow na zemi
            ground_glow = pygame.Surface((60, 20), pygame.SRCALPHA)
            pygame.draw.ellipse(ground_glow, (200, 150, 50, 20), (0, 0, 60, 20))
            bg.blit(ground_glow, (tx - 30, torch_y + 28))
        
        # Svítivé houby na zemi
        for mx, my in [(180, sky_height + 100), (460, sky_height + 120),
                       (720, sky_height + 95), (1020, sky_height + 110)]:
            mush_surf = pygame.Surface((16, 16), pygame.SRCALPHA)
            pygame.draw.rect(mush_surf, (100, 60, 140), (6, 8, 4, 8))
            pygame.draw.ellipse(mush_surf, (160, 80, 200, 120), (0, 0, 16, 10))
            pygame.draw.ellipse(mush_surf, (200, 120, 240, 60), (3, 2, 10, 6))
            bg.blit(mush_surf, (mx, my))
        
        # Mimozemská vegetace - trsy trávy
        for gx in range(0, SCREEN_WIDTH, 45):
            if random.random() > 0.4:
                gy = sky_height + random.randint(85, SCREEN_HEIGHT - sky_height - 30)
                for blade in range(3):
                    bx = gx + blade * 4
                    bh = random.randint(8, 18)
                    tilt = random.randint(-3, 3)
                    pygame.draw.line(bg, (50, 120 + random.randint(0, 40), 60),
                                   (bx, gy), (bx + tilt, gy - bh), 1)
        
        return bg

    def draw_village_hud(self):
        self.screen.blit(self.bg_surface, (0, 0))
        
        # Animované pochodně
        self.ambient_timer += 0.03
        sky_height = 128
        for tx in [250, 550, 850, 1100]:
            torch_y = sky_height + 55
            # Animovaný plamen
            flame_size = 8 + int(3 * math.sin(self.ambient_timer * 5 + tx))
            flame_surf = pygame.Surface((flame_size * 3, flame_size * 3), pygame.SRCALPHA)
            alpha = int(150 + 60 * math.sin(self.ambient_timer * 4 + tx * 0.1))
            pygame.draw.circle(flame_surf, (255, 180, 50, max(0, min(255, alpha))),
                             (flame_size * 3 // 2, flame_size * 3 // 2), flame_size)
            pygame.draw.circle(flame_surf, (255, 230, 120, max(0, min(255, alpha // 2))),
                             (flame_size * 3 // 2, flame_size * 3 // 2 - 2), flame_size // 2)
            self.screen.blit(flame_surf, (tx - flame_size * 3 // 2, torch_y - 15 - flame_size))
        
        # Kouř z chatek
        for p in self.smoke_particles:
            p[1] -= p[2]
            p[0] += math.sin(self.ambient_timer + p[0] * 0.01) * 0.3
            if p[1] < 80:
                # Resetuj kouř
                hx, hy = random.choice(self.hut_positions)
                p[0] = hx + random.randint(-10, 10)
                p[1] = hy
                p[3] = random.randint(60, 100)
            smoke_surf = pygame.Surface((10, 10), pygame.SRCALPHA)
            alpha = max(0, min(200, p[3] - int((self.hut_positions[0][1] - p[1]) * 0.8)))
            pygame.draw.circle(smoke_surf, (p[3], p[3], p[3] + 10, alpha), (5, 5), 5)
            self.screen.blit(smoke_surf, (int(p[0]) - 5, int(p[1]) - 5))
        
        # Světlušky / broučci
        for f in self.fireflies:
            f[0] += math.sin(self.ambient_timer * f[2] + f[1] * 0.01) * 1.5
            f[1] += math.cos(self.ambient_timer * f[2] * 0.7 + f[0] * 0.01) * 0.8
            if f[0] > SCREEN_WIDTH:
                f[0] = 0
            if f[0] < 0:
                f[0] = SCREEN_WIDTH
            if f[1] > SCREEN_HEIGHT:
                f[1] = 100
            if f[1] < 100:
                f[1] = SCREEN_HEIGHT
            glow_alpha = int(120 + 100 * math.sin(self.ambient_timer * f[2] * 2))
            firefly_surf = pygame.Surface((8, 8), pygame.SRCALPHA)
            pygame.draw.circle(firefly_surf, (*f[3][:3], min(255, glow_alpha)), (4, 4), 4)
            self.screen.blit(firefly_surf, (int(f[0]) - 4, int(f[1]) - 4))
        
        font_small = pygame.font.Font(None, 28)
        font_title = pygame.font.Font(None, 36)
        
        title_text = font_title.render("Level 4: Vesnice Mimozemšťanů", True, (255, 200, 100))
        self.screen.blit(title_text, (20, 10))
        
        size_text = font_small.render(f"Velikost: {self.cat.size:.0f} / {MAX_CAT_SIZE}", True, (240, 200, 140))
        self.screen.blit(size_text, (SCREEN_WIDTH - 350, 15))
        
        food_text = font_small.render(f"Mimozemšťané sežráni: {self.cat.food_eaten} / {self.FOOD_GOAL}", True, (240, 200, 140))
        self.screen.blit(food_text, (SCREEN_WIDTH - 350, 45))
        
        progress_width = 300
        progress_height = 15
        progress_x = SCREEN_WIDTH - 350
        progress_y = 75
        
        pygame.draw.rect(self.screen, (50, 35, 20),
                        (progress_x, progress_y, progress_width, progress_height))
        
        filled_width = min(1.0, self.cat.food_eaten / self.FOOD_GOAL) * progress_width
        hunger = self.cat.food_eaten / self.FOOD_GOAL
        bar_color = (int(200 + 55 * hunger), int(140 - 40 * hunger), int(40 + 20 * hunger))
        pygame.draw.rect(self.screen, bar_color,
                        (progress_x, progress_y, filled_width, progress_height))
        
        pygame.draw.rect(self.screen, (255, 200, 100),
                        (progress_x, progress_y, progress_width, progress_height), 2)
        
        controls_text = font_small.render("WASD nebo Šipky = Pohyb | ESC = Zpět", True, (150, 120, 80))
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
        
        # Strážci - pronásledování a kolize
        for guard in self.guards:
            if not guard.alive:
                continue
            guard.update(self.cat)
            if guard.collides_with(self.cat):
                if self.cat.food_eaten >= 20:
                    # Kočka sežrala dost mimozemšťanů - sežere strážce
                    guard.alive = False
                    self.cat.food_eaten += 1
                    self.cat.size += 5
                else:
                    # Strážce zraní kočku
                    if guard.damage_cooldown <= 0:
                        self.cat.hp -= 10
                        guard.damage_cooldown = 30  # Cooldown 0.5s při 60 FPS
                        self.damage_flash = 10
        
        # Odstraň mrtvé strážce
        self.guards = [g for g in self.guards if g.alive]
        
        # Spawn nových strážců
        self.guard_spawn_timer += 1
        if self.guard_spawn_timer >= 300:  # Každých 5 sekund
            self.guard_spawn_timer = 0
            if len(self.guards) < 6:
                self.spawn_guards_single()
        
        # Game over - HP vyčerpáno
        if self.cat.hp <= 0:
            self.running = False
            return
        
        if self.damage_flash > 0:
            self.damage_flash -= 1
        
        # Win podmínka
        if self.cat.food_eaten >= self.FOOD_GOAL:
            self.won = True
            self.running = False
            return
        
        alive_foods = sum(1 for f in self.foods if not f.eaten)
        if alive_foods < 3:
            self.spawn_food()
    
    def spawn_guards_single(self):
        """Spawnuje jednoho strážce na kraji mapy"""
        side = random.choice(["left", "right", "top", "bottom"])
        if side == "left":
            x, y = 30, random.randint(170, SCREEN_HEIGHT - 60)
        elif side == "right":
            x, y = SCREEN_WIDTH - 30, random.randint(170, SCREEN_HEIGHT - 60)
        elif side == "top":
            x, y = random.randint(60, SCREEN_WIDTH - 60), 170
        else:
            x, y = random.randint(60, SCREEN_WIDTH - 60), SCREEN_HEIGHT - 30
        self.guards.append(Guard(x, y, self.texture_manager))
    
    def draw(self):
        self.screen.fill((40, 30, 20))
        self.draw_village_hud()
        
        for food in self.foods:
            food.draw(self.screen)
        
        # Strážci
        for guard in self.guards:
            guard.draw(self.screen)
        
        self.cat.draw(self.screen)
        
        # Červený flash při zásahu
        if self.damage_flash > 0:
            flash_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            flash_surf.fill((255, 0, 0, int(40 * (self.damage_flash / 10))))
            self.screen.blit(flash_surf, (0, 0))
        
        # HP bar
        hp_ratio = max(0, self.cat.hp / self.cat.max_hp)
        bar_w, bar_h = 200, 16
        bar_x, bar_y = 20, 45
        pygame.draw.rect(self.screen, (60, 20, 20), (bar_x, bar_y, bar_w, bar_h))
        hp_color = (50, 200, 50) if hp_ratio > 0.5 else (200, 200, 50) if hp_ratio > 0.25 else (200, 50, 50)
        pygame.draw.rect(self.screen, hp_color, (bar_x, bar_y, int(bar_w * hp_ratio), bar_h))
        pygame.draw.rect(self.screen, (255, 200, 100), (bar_x, bar_y, bar_w, bar_h), 2)
        font_hp = pygame.font.Font(None, 24)
        hp_text = font_hp.render(f"HP: {max(0, self.cat.hp)} / {self.cat.max_hp}", True, (255, 255, 255))
        self.screen.blit(hp_text, (bar_x + 5, bar_y + 1))
        
        # Nápověda k počtu sežraných
        if self.cat.food_eaten < 20:
            font_hint = pygame.font.Font(None, 26)
            hint = font_hint.render(f"Sežer 20 mimozemšťanů abys mohl sežrat strážce! ({self.cat.food_eaten}/20)", True, (255, 150, 100))
            self.screen.blit(hint, (20, SCREEN_HEIGHT - 55))
        
        pygame.display.flip()
    
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        return "won" if self.won else "quit"


class GameLevel5:
    """Level 5 - Mimozemské Město (kočka žere baráky)"""
    FOOD_GOAL = 50

    def __init__(self, texture_manager):
        self.screen = pygame.display.get_surface()
        self.clock = pygame.time.Clock()
        self.running = True
        self.won = False
        self.texture_manager = texture_manager

        self.cat = AlienCat(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, texture_manager)
        self.cat.size = 55
        self.cat.speed = 4.5
        self.cat.max_size = 300
        self.foods = []
        self.bg_surface = self._build_background()
        self.spawn_food()

        self.neon_timer = 0
        self.neon_signs = []
        for _ in range(10):
            self.neon_signs.append([
                random.randint(50, SCREEN_WIDTH - 50),
                random.randint(135, 155),
                random.random() * 3 + 1,
                random.choice([(255, 50, 200), (50, 255, 200), (255, 255, 50), (50, 200, 255)])
            ])

    def spawn_food(self):
        for _ in range(8):
            x = random.randint(60, SCREEN_WIDTH - 60)
            y = random.randint(170, SCREEN_HEIGHT - 60)
            food_type = random.choice(["alien_building", "alien_tower", "alien_dome", "alien_factory"])
            food = Food(x, y, food_type, self.texture_manager)
            food.width = random.randint(55, 85)
            food.height = random.randint(55, 85)
            self.foods.append(food)

    def _build_background(self):
        bg = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        sky_height = 130

        # Fialová obloha města
        for y in range(sky_height):
            factor = y / sky_height
            r = int(30 + 60 * factor)
            g = int(10 + 20 * factor)
            b = int(60 + 50 * (1 - factor))
            pygame.draw.line(bg, (r, g, b), (0, y), (SCREEN_WIDTH, y))

        # Hvězdy
        for _ in range(60):
            sx = random.randint(0, SCREEN_WIDTH)
            sy = random.randint(0, sky_height - 10)
            brightness = random.randint(100, 255)
            bg.set_at((sx, sy), (brightness, brightness, min(255, brightness + 30)))

        # Siluety vzdálených budov na horizontu
        for bx in range(0, SCREEN_WIDTH, 40):
            bh = random.randint(20, 70)
            bw = random.randint(25, 38)
            pygame.draw.rect(bg, (40, 25, 60), (bx, sky_height - bh, bw, bh))
            pygame.draw.rect(bg, (50, 30, 70), (bx, sky_height - bh, bw, bh), 1)
            # Okna
            for wy in range(sky_height - bh + 4, sky_height - 4, 10):
                for wx in range(bx + 3, bx + bw - 5, 8):
                    if random.random() > 0.3:
                        wc = random.choice([(200, 255, 180), (255, 200, 100), (150, 200, 255)])
                        bg.set_at((wx, wy), wc)
                        bg.set_at((wx + 1, wy), wc)
                        bg.set_at((wx, wy + 1), wc)
                        bg.set_at((wx + 1, wy + 1), wc)

        pygame.draw.line(bg, (150, 50, 200), (0, sky_height), (SCREEN_WIDTH, sky_height), 2)

        # Podlaha města - kovový povrch
        for y in range(sky_height + 2, SCREEN_HEIGHT):
            noise = random.randint(-3, 3)
            r = max(0, min(255, 50 + noise))
            g = max(0, min(255, 40 + noise))
            b = max(0, min(255, 65 + noise))
            pygame.draw.line(bg, (r, g, b), (0, y), (SCREEN_WIDTH, y))

        # Silnice/cesty
        road_y = SCREEN_HEIGHT // 2 + 50
        pygame.draw.rect(bg, (35, 30, 45), (0, road_y, SCREEN_WIDTH, 30))
        for lx in range(0, SCREEN_WIDTH, 40):
            pygame.draw.rect(bg, (200, 180, 50), (lx, road_y + 13, 20, 4))

        return bg

    def draw_city_hud(self):
        self.screen.blit(self.bg_surface, (0, 0))

        self.neon_timer += 0.03
        for s in self.neon_signs:
            alpha = int(150 + 100 * math.sin(self.neon_timer * s[2]))
            neon_surf = pygame.Surface((12, 12), pygame.SRCALPHA)
            pygame.draw.circle(neon_surf, (*s[3][:3], max(0, min(255, alpha))), (6, 6), 6)
            self.screen.blit(neon_surf, (int(s[0]) - 6, int(s[1]) - 6))

        font_small = pygame.font.Font(None, 28)
        font_title = pygame.font.Font(None, 36)

        title_text = font_title.render("Level 5: Mimozemské Město", True, (255, 100, 255))
        self.screen.blit(title_text, (20, 10))

        size_text = font_small.render(f"Velikost: {self.cat.size:.0f} / {self.cat.max_size}", True, (255, 180, 255))
        self.screen.blit(size_text, (SCREEN_WIDTH - 350, 15))

        food_text = font_small.render(f"Baráky sežrány: {self.cat.food_eaten} / {self.FOOD_GOAL}", True, (255, 180, 255))
        self.screen.blit(food_text, (SCREEN_WIDTH - 350, 45))

        progress_width = 300
        progress_x = SCREEN_WIDTH - 350
        progress_y = 75
        pygame.draw.rect(self.screen, (40, 20, 50), (progress_x, progress_y, progress_width, 15))
        filled_width = min(1.0, self.cat.food_eaten / self.FOOD_GOAL) * progress_width
        pygame.draw.rect(self.screen, (200, 80, 255), (progress_x, progress_y, filled_width, 15))
        pygame.draw.rect(self.screen, (255, 100, 255), (progress_x, progress_y, progress_width, 15), 2)

        controls_text = font_small.render("WASD nebo Šipky = Pohyb | ESC = Zpět", True, (140, 100, 160))
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
        if self.cat.food_eaten >= self.FOOD_GOAL:
            self.won = True
            self.running = False
            return
        alive_foods = sum(1 for f in self.foods if not f.eaten)
        if alive_foods < 3:
            self.spawn_food()

    def draw(self):
        self.screen.fill((30, 20, 45))
        self.draw_city_hud()
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


class GameLevel6:
    """Level 6 - Obří Kočka (jí velké věci na planetě - hory, stromy, jezera)"""
    FOOD_GOAL = 50

    def __init__(self, texture_manager):
        self.screen = pygame.display.get_surface()
        self.clock = pygame.time.Clock()
        self.running = True
        self.won = False
        self.texture_manager = texture_manager

        self.cat = AlienCat(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, texture_manager)
        self.cat.size = 80
        self.cat.speed = 4
        self.cat.max_size = 400
        self.cat.growth_per_food = 5
        self.foods = []
        self.bg_surface = self._build_background()
        self.spawn_food()
        self.quake_timer = 0

    def spawn_food(self):
        for _ in range(6):
            x = random.randint(60, SCREEN_WIDTH - 60)
            y = random.randint(130, SCREEN_HEIGHT - 60)
            food_type = random.choice(["mountain_chunk", "giant_tree", "giant_crystal", "lake"])
            food = Food(x, y, food_type, self.texture_manager)
            food.width = random.randint(70, 110)
            food.height = random.randint(70, 110)
            self.foods.append(food)

    def _build_background(self):
        bg = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        # Pohled z výšky - zeleno-hnědý terén
        for y in range(SCREEN_HEIGHT):
            factor = y / SCREEN_HEIGHT
            r = int(40 + 30 * factor)
            g = int(80 + 40 * math.sin(factor * 3))
            b = int(30 + 20 * factor)
            pygame.draw.line(bg, (r, g, b), (0, y), (SCREEN_WIDTH, y))

        # Terénní skvrny
        for _ in range(40):
            sx = random.randint(0, SCREEN_WIDTH)
            sy = random.randint(0, SCREEN_HEIGHT)
            sr = random.randint(20, 60)
            sc = random.choice([(50, 100, 40), (60, 90, 35), (35, 70, 25), (70, 110, 50)])
            terrain_surf = pygame.Surface((sr * 2, sr * 2), pygame.SRCALPHA)
            pygame.draw.ellipse(terrain_surf, (*sc, 60), (0, 0, sr * 2, sr * 2))
            bg.blit(terrain_surf, (sx - sr, sy - sr))

        # Řeky
        for river_x_base in [300, 800]:
            for y in range(0, SCREEN_HEIGHT, 2):
                rx = river_x_base + int(30 * math.sin(y * 0.02))
                pygame.draw.line(bg, (30, 80, 140), (rx, y), (rx + 8, y), 3)

        return bg

    def draw_giant_hud(self):
        self.screen.blit(self.bg_surface, (0, 0))
        self.quake_timer += 0.02

        # Otřesy země při pohybu
        if self.cat.vx != 0 or self.cat.vy != 0:
            shake = int(math.sin(self.quake_timer * 20) * 2)
            self.screen.scroll(shake, 0)

        font_small = pygame.font.Font(None, 28)
        font_title = pygame.font.Font(None, 36)

        title_text = font_title.render("Level 6: Obří Kočka", True, (200, 255, 150))
        self.screen.blit(title_text, (20, 10))

        size_text = font_small.render(f"Velikost: {self.cat.size:.0f} / {self.cat.max_size}", True, (200, 255, 150))
        self.screen.blit(size_text, (SCREEN_WIDTH - 350, 15))

        food_text = font_small.render(f"Sežráno: {self.cat.food_eaten} / {self.FOOD_GOAL}", True, (200, 255, 150))
        self.screen.blit(food_text, (SCREEN_WIDTH - 350, 45))

        progress_width = 300
        progress_x = SCREEN_WIDTH - 350
        progress_y = 75
        pygame.draw.rect(self.screen, (30, 50, 20), (progress_x, progress_y, progress_width, 15))
        filled_width = min(1.0, self.cat.food_eaten / self.FOOD_GOAL) * progress_width
        pygame.draw.rect(self.screen, (100, 200, 80), (progress_x, progress_y, filled_width, 15))
        pygame.draw.rect(self.screen, (150, 255, 100), (progress_x, progress_y, progress_width, 15), 2)

        controls_text = font_small.render("WASD nebo Šipky = Pohyb | ESC = Zpět", True, (120, 160, 100))
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
        if self.cat.food_eaten >= self.FOOD_GOAL:
            self.won = True
            self.running = False
            return
        alive_foods = sum(1 for f in self.foods if not f.eaten)
        if alive_foods < 3:
            self.spawn_food()

    def draw(self):
        self.screen.fill((35, 60, 25))
        self.draw_giant_hud()
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


class GameLevel7:
    """Level 7 - Vesmír (jí meteority, na velikosti 80 sní planetu → 120)"""

    def __init__(self, texture_manager):
        self.screen = pygame.display.get_surface()
        self.clock = pygame.time.Clock()
        self.running = True
        self.won = False
        self.texture_manager = texture_manager

        self.cat = AlienCat(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, texture_manager)
        self.cat.size = 40
        self.cat.speed = 6
        self.cat.max_size = 120
        self.cat.growth_per_food = 2
        self.foods = []
        self.planet_spawned = False
        self.planet_eaten = False
        self.bg_surface = self._build_background()
        self.spawn_food()

        self.star_timer = 0
        self.bg_stars = [(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT),
                          random.random() * 2 + 0.5) for _ in range(150)]

    def spawn_food(self):
        for _ in range(15):
            x = random.randint(60, SCREEN_WIDTH - 60)
            y = random.randint(60, SCREEN_HEIGHT - 60)
            food_type = random.choice(["meteorite", "asteroid"])
            food = Food(x, y, food_type, self.texture_manager)
            food.width = random.randint(30, 55)
            food.height = random.randint(30, 55)
            self.foods.append(food)

    def spawn_planet(self):
        """Spawne planetu když je kočka dost velká"""
        x = random.randint(100, SCREEN_WIDTH - 100)
        y = random.randint(100, SCREEN_HEIGHT - 100)
        food = Food(x, y, "planet_food", self.texture_manager)
        food.width = 140
        food.height = 140
        self.foods.append(food)
        self.planet_spawned = True

    def _build_background(self):
        bg = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        # Hluboký vesmír
        for y in range(SCREEN_HEIGHT):
            factor = y / SCREEN_HEIGHT
            r = int(3 + 8 * factor)
            g = int(2 + 5 * factor)
            b = int(12 + 15 * (1 - factor))
            pygame.draw.line(bg, (r, g, b), (0, y), (SCREEN_WIDTH, y))

        # Hvězdy
        for _ in range(200):
            sx = random.randint(0, SCREEN_WIDTH)
            sy = random.randint(0, SCREEN_HEIGHT)
            brightness = random.randint(60, 255)
            color_shift = random.choice([(0, 0, 30), (20, 0, 0), (0, 20, 0), (0, 0, 0)])
            bg.set_at((sx, sy), (min(255, brightness + color_shift[0]),
                                  min(255, brightness + color_shift[1]),
                                  min(255, brightness + color_shift[2])))

        # Mlhoviny
        for nx, ny, nr in [(200, 150, 80), (800, 400, 100), (500, 550, 70)]:
            neb_surf = pygame.Surface((nr * 2, nr * 2), pygame.SRCALPHA)
            neb_color = random.choice([(60, 20, 80, 15), (20, 40, 80, 15), (80, 30, 40, 12)])
            pygame.draw.ellipse(neb_surf, neb_color, (0, 0, nr * 2, nr * 2))
            bg.blit(neb_surf, (nx - nr, ny - nr))

        return bg

    def draw_space_hud(self):
        self.screen.blit(self.bg_surface, (0, 0))
        self.star_timer += 0.02

        # Blikající hvězdy
        for sx, sy, br in self.bg_stars:
            alpha = int(80 + 80 * math.sin(self.star_timer * br))
            alpha = max(0, min(255, alpha))
            self.screen.set_at((int(sx), int(sy)), (alpha, alpha, min(255, alpha + 20)))

        font_small = pygame.font.Font(None, 28)
        font_title = pygame.font.Font(None, 36)

        title_text = font_title.render("Level 7: Vesmír", True, (200, 200, 255))
        self.screen.blit(title_text, (20, 10))

        size_text = font_small.render(f"Velikost: {self.cat.size:.0f}", True, (180, 180, 255))
        self.screen.blit(size_text, (SCREEN_WIDTH - 350, 15))

        if not self.planet_eaten:
            if self.cat.size >= 80:
                hint = font_small.render("! PLANETA SE OBJEVILA - SEŽER JI !", True, (255, 255, 100))
            else:
                hint = font_small.render(f"Jez meteority! Na vel. 80 sníš planetu (nyní: {self.cat.size:.0f})", True, (180, 180, 255))
            self.screen.blit(hint, (SCREEN_WIDTH - 550, 45))
        else:
            hint = font_small.render("Planeta sežrána! Velikost 120!", True, (100, 255, 100))
            self.screen.blit(hint, (SCREEN_WIDTH - 380, 45))

        # Progress bar k velikosti 40 (pak k 50)
        progress_width = 300
        progress_x = SCREEN_WIDTH - 350
        progress_y = 75
        pygame.draw.rect(self.screen, (15, 15, 40), (progress_x, progress_y, progress_width, 15))
        if self.cat.size < 80:
            filled = min(1.0, (self.cat.size - 40) / 40) * progress_width
            pygame.draw.rect(self.screen, (100, 100, 255), (progress_x, progress_y, filled, 15))
        else:
            filled = min(1.0, (self.cat.size - 40) / 80) * progress_width
            pygame.draw.rect(self.screen, (100, 255, 100), (progress_x, progress_y, filled, 15))
        pygame.draw.rect(self.screen, (150, 150, 255), (progress_x, progress_y, progress_width, 15), 2)
        # Značka na 80
        mark_x = progress_x + int((40 / 80) * progress_width)
        pygame.draw.line(self.screen, (255, 255, 100), (mark_x, progress_y - 3), (mark_x, progress_y + 18), 2)

        controls_text = font_small.render("WASD nebo Šipky = Pohyb | ESC = Zpět", True, (100, 100, 140))
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
            if food.eaten:
                continue
            if food.food_type == "planet_food":
                # Planetu lze sníst jen při velikosti >= 80
                if self.cat.size >= 80 and food.is_eaten_by(self.cat):
                    food.eaten = True
                    self.cat.size = 120
                    self.cat.food_eaten += 1
                    self.planet_eaten = True
            else:
                if food.is_eaten_by(self.cat):
                    self.cat.eat_food(food)

        # Spawn planety když kočka >= 80
        if self.cat.size >= 80 and not self.planet_spawned:
            self.spawn_planet()

        # Win: kočka sežrala planetu (velikost >= 50)
        if self.planet_eaten:
            self.won = True
            self.running = False
            return

        alive_foods = sum(1 for f in self.foods if not f.eaten and f.food_type != "planet_food")
        if alive_foods < 8:
            self.spawn_food()

    def draw(self):
        self.screen.fill((5, 3, 15))
        self.draw_space_hud()
        for food in self.foods:
            if not food.eaten and food.food_type == "planet_food":
                # Pulzující záře kolem planety
                glow_r = 60 + int(10 * math.sin(self.star_timer * 3))
                glow_surf = pygame.Surface((glow_r * 2, glow_r * 2), pygame.SRCALPHA)
                pygame.draw.circle(glow_surf, (100, 255, 100, 30), (glow_r, glow_r), glow_r)
                self.screen.blit(glow_surf, (food.x + food.width // 2 - glow_r,
                                              food.y + food.height // 2 - glow_r))
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


class GameLevel8:
    """Level 8 - Požírač Planet (kočka jí okolní planety)"""
    FOOD_GOAL = 30

    def __init__(self, texture_manager):
        self.screen = pygame.display.get_surface()
        self.clock = pygame.time.Clock()
        self.running = True
        self.won = False
        self.texture_manager = texture_manager

        self.cat = AlienCat(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, texture_manager)
        self.cat.size = 50
        self.cat.speed = 5
        self.cat.max_size = 500
        self.cat.growth_per_food = 8
        self.foods = []
        self.bg_surface = self._build_background()
        self.spawn_food()

        self.star_timer = 0
        self.bg_stars = [(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT),
                          random.random() * 2 + 0.5) for _ in range(200)]
        # Centrální hvězda (slunce)
        self.sun_x = SCREEN_WIDTH // 2
        self.sun_y = SCREEN_HEIGHT // 2

    def spawn_food(self):
        for _ in range(5):
            x = random.randint(80, SCREEN_WIDTH - 80)
            y = random.randint(80, SCREEN_HEIGHT - 80)
            food_type = random.choice(["small_planet", "gas_planet", "ice_planet", "lava_planet"])
            food = Food(x, y, food_type, self.texture_manager)
            if food_type == "gas_planet":
                food.width = random.randint(70, 100)
                food.height = random.randint(70, 100)
            else:
                food.width = random.randint(50, 80)
                food.height = random.randint(50, 80)
            self.foods.append(food)

    def _build_background(self):
        bg = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        # Temný vesmír
        bg.fill((2, 1, 8))

        # Hvězdy
        for _ in range(300):
            sx = random.randint(0, SCREEN_WIDTH)
            sy = random.randint(0, SCREEN_HEIGHT)
            brightness = random.randint(40, 255)
            color = random.choice([(brightness, brightness, min(255, brightness + 30)),
                                    (min(255, brightness + 20), brightness, brightness),
                                    (brightness, brightness, brightness)])
            bg.set_at((sx, sy), color)

        # Centrální hvězda (slunce systému)
        sun_cx, sun_cy = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        for r in range(60, 0, -1):
            alpha = int(255 * (1 - r / 60))
            glow_surf = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
            pygame.draw.circle(glow_surf, (255, 200, 50, min(255, alpha // 3)), (r, r), r)
            bg.blit(glow_surf, (sun_cx - r, sun_cy - r))
        pygame.draw.circle(bg, (255, 240, 150), (sun_cx, sun_cy), 18)
        pygame.draw.circle(bg, (255, 255, 220), (sun_cx, sun_cy), 10)

        # Orbitální dráhy
        for orbit_r in [120, 200, 300, 420]:
            orbit_surf = pygame.Surface((orbit_r * 2, orbit_r * 2), pygame.SRCALPHA)
            pygame.draw.circle(orbit_surf, (40, 40, 60, 40), (orbit_r, orbit_r), orbit_r, 1)
            bg.blit(orbit_surf, (sun_cx - orbit_r, sun_cy - orbit_r))

        return bg

    def draw_devourer_hud(self):
        self.screen.blit(self.bg_surface, (0, 0))
        self.star_timer += 0.02

        # Blikající hvězdy
        for sx, sy, br in self.bg_stars:
            alpha = int(60 + 60 * math.sin(self.star_timer * br))
            alpha = max(0, min(255, alpha))
            self.screen.set_at((int(sx), int(sy)), (alpha, alpha, min(255, alpha + 15)))

        # Pulzující záře centrální hvězdy
        pulse = int(5 * math.sin(self.star_timer * 2))
        glow_r = 30 + pulse
        glow_surf = pygame.Surface((glow_r * 2, glow_r * 2), pygame.SRCALPHA)
        pygame.draw.circle(glow_surf, (255, 200, 50, 40), (glow_r, glow_r), glow_r)
        self.screen.blit(glow_surf, (self.sun_x - glow_r, self.sun_y - glow_r))

        font_small = pygame.font.Font(None, 28)
        font_title = pygame.font.Font(None, 36)

        title_text = font_title.render("Level 8: Požírač Planet", True, (255, 150, 50))
        self.screen.blit(title_text, (20, 10))

        size_text = font_small.render(f"Velikost: {self.cat.size:.0f}", True, (255, 200, 100))
        self.screen.blit(size_text, (SCREEN_WIDTH - 350, 15))

        food_text = font_small.render(f"Planety sežrány: {self.cat.food_eaten} / {self.FOOD_GOAL}", True, (255, 200, 100))
        self.screen.blit(food_text, (SCREEN_WIDTH - 350, 45))

        progress_width = 300
        progress_x = SCREEN_WIDTH - 350
        progress_y = 75
        pygame.draw.rect(self.screen, (30, 20, 10), (progress_x, progress_y, progress_width, 15))
        filled_width = min(1.0, self.cat.food_eaten / self.FOOD_GOAL) * progress_width
        hunger = min(1.0, self.cat.food_eaten / self.FOOD_GOAL)
        bar_color = (int(255), int(150 - 100 * hunger), int(50 - 40 * hunger))
        pygame.draw.rect(self.screen, bar_color, (progress_x, progress_y, filled_width, 15))
        pygame.draw.rect(self.screen, (255, 180, 80), (progress_x, progress_y, progress_width, 15), 2)

        controls_text = font_small.render("WASD nebo Šipky = Pohyb | ESC = Zpět", True, (120, 100, 60))
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
        if self.cat.food_eaten >= self.FOOD_GOAL:
            self.won = True
            self.running = False
            return
        alive_foods = sum(1 for f in self.foods if not f.eaten)
        if alive_foods < 2:
            self.spawn_food()

    def draw(self):
        self.screen.fill((2, 1, 8))
        self.draw_devourer_hud()

        # Glow kolem planet
        for food in self.foods:
            if not food.eaten:
                gr = max(food.width, food.height) // 2 + 10
                glow_surf = pygame.Surface((gr * 2, gr * 2), pygame.SRCALPHA)
                color_map = {
                    "lava_planet": (255, 80, 20, 20),
                    "ice_planet": (100, 180, 255, 20),
                    "gas_planet": (200, 170, 80, 20),
                    "small_planet": (200, 150, 80, 20),
                }
                gc = color_map.get(food.food_type, (200, 200, 200, 20))
                pygame.draw.circle(glow_surf, gc, (gr, gr), gr)
                self.screen.blit(glow_surf, (food.x + food.width // 2 - gr,
                                              food.y + food.height // 2 - gr))
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


class ExplosionCutscene:
    """Cutscéna - kočka se přejedla a vybouchla"""
    def __init__(self, texture_manager):
        self.screen = pygame.display.get_surface()
        self.clock = pygame.time.Clock()
        self.texture_manager = texture_manager
        self.timer = 0
        self.phase = "growing"  # growing -> shake -> explode -> text
        self.cat_size = 200
        self.shake_offset = [0, 0]
        self.particles = []
        self.flash_alpha = 0
        self.stars = [(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT),
                       random.random() * 2 + 0.5) for _ in range(100)]
        self.star_timer = 0
        self.text_alpha = 0
        self.font_big = pygame.font.Font(None, 100)
        self.font_medium = pygame.font.Font(None, 60)
        self.font_small = pygame.font.Font(None, 40)
        self.font_hint = pygame.font.Font(None, 30)
        # Barvy částic exploze
        self.particle_colors = [
            (255, 100, 50), (255, 180, 30), (255, 60, 60),
            (80, 180, 100), (120, 220, 140), (60, 255, 80),
            (255, 255, 100), (255, 200, 50), (200, 80, 200)
        ]

    def spawn_explosion_particles(self):
        cx, cy = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30
        for _ in range(200):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2, 15)
            size = random.randint(3, 20)
            color = random.choice(self.particle_colors)
            life = random.randint(60, 180)
            self.particles.append({
                'x': cx, 'y': cy,
                'vx': math.cos(angle) * speed,
                'vy': math.sin(angle) * speed,
                'size': size, 'color': color,
                'life': life, 'max_life': life,
                'rotation': random.uniform(0, 360),
                'rot_speed': random.uniform(-5, 5)
            })

    def update(self):
        self.timer += 1
        self.star_timer += 0.02

        if self.phase == "growing":
            # Kočka roste a nafoukne se
            self.cat_size = 200 + self.timer * 1.5
            if self.cat_size > 450:
                self.phase = "shake"
                self.timer = 0

        elif self.phase == "shake":
            # Kočka se třese
            intensity = min(self.timer / 30, 1.0) * 15
            self.shake_offset[0] = random.uniform(-intensity, intensity)
            self.shake_offset[1] = random.uniform(-intensity, intensity)
            # Kočka pulzuje
            self.cat_size = 450 + math.sin(self.timer * 0.5) * 20
            if self.timer > 90:
                self.phase = "explode"
                self.timer = 0
                self.spawn_explosion_particles()
                self.flash_alpha = 255

        elif self.phase == "explode":
            self.flash_alpha = max(0, self.flash_alpha - 8)
            # Update částic
            for p in self.particles:
                p['x'] += p['vx']
                p['y'] += p['vy']
                p['vy'] += 0.05  # gravitace
                p['vx'] *= 0.99
                p['life'] -= 1
                p['rotation'] += p['rot_speed']
            self.particles = [p for p in self.particles if p['life'] > 0]
            if self.timer > 120:
                self.phase = "text"
                self.timer = 0

        elif self.phase == "text":
            self.text_alpha = min(255, self.text_alpha + 3)
            # Částice stále padají
            for p in self.particles:
                p['x'] += p['vx']
                p['y'] += p['vy']
                p['vy'] += 0.05
                p['life'] -= 1
                p['rotation'] += p['rot_speed']
            self.particles = [p for p in self.particles if p['life'] > 0]

    def draw_background(self):
        for y in range(SCREEN_HEIGHT):
            r = int(5 + 10 * (y / SCREEN_HEIGHT))
            g = int(3 + 8 * (y / SCREEN_HEIGHT))
            b = int(15 + 20 * (1 - y / SCREEN_HEIGHT))
            pygame.draw.line(self.screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))
        for sx, sy, br in self.stars:
            alpha = int(80 + 80 * math.sin(self.star_timer * br))
            alpha = max(0, min(255, alpha))
            self.screen.set_at((int(sx), int(sy)), (alpha, alpha, min(255, alpha + 20)))

    def draw(self):
        self.draw_background()
        cx, cy = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30

        if self.phase in ("growing", "shake"):
            # Kresli kočku (nafouklou)
            cat_texture = self.texture_manager.get_texture("cat")
            if cat_texture:
                sx = int(self.cat_size + self.shake_offset[0])
                sy = int(self.cat_size + self.shake_offset[1])
                scaled = pygame.transform.scale(cat_texture, (sx, sy))
                rect = scaled.get_rect(center=(cx, cy))
                self.screen.blit(scaled, rect)

            # Červená záře při třásní
            if self.phase == "shake":
                glow_alpha = int(40 + 30 * math.sin(self.timer * 0.3))
                glow_r = int(self.cat_size * 0.7)
                glow_surf = pygame.Surface((glow_r * 2, glow_r * 2), pygame.SRCALPHA)
                pygame.draw.circle(glow_surf, (255, 50, 30, glow_alpha), (glow_r, glow_r), glow_r)
                self.screen.blit(glow_surf, (cx - glow_r, cy - glow_r))

            # Varovný text
            if self.phase == "growing":
                warn = self.font_small.render("Kočka se přejídá...", True, (255, 200, 100))
                self.screen.blit(warn, warn.get_rect(center=(cx, cy + self.cat_size // 2 + 40)))
            elif self.phase == "shake":
                blink = int(self.timer * 0.3) % 2 == 0
                if blink:
                    warn = self.font_medium.render("! POZOR !", True, (255, 50, 50))
                    self.screen.blit(warn, warn.get_rect(center=(cx, cy + self.cat_size // 2 + 40)))

        elif self.phase in ("explode", "text"):
            # Částice
            for p in self.particles:
                alpha = int(255 * (p['life'] / p['max_life']))
                alpha = max(0, min(255, alpha))
                size = max(1, int(p['size'] * (p['life'] / p['max_life'])))
                surf = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
                color = (*p['color'], alpha)
                pygame.draw.circle(surf, color, (size, size), size)
                rotated = pygame.transform.rotate(surf, p['rotation'])
                self.screen.blit(rotated, (int(p['x']) - size, int(p['y']) - size))

            # Bílý flash
            if self.flash_alpha > 0:
                flash = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
                flash.fill((255, 255, 255, self.flash_alpha))
                self.screen.blit(flash, (0, 0))

            # Texty po explozi
            if self.phase == "text":
                # BOOM!
                boom_color = (255, max(0, 100 - self.timer), max(0, 50 - self.timer))
                boom = self.font_big.render("BOOM!", True, boom_color)
                self.screen.blit(boom, boom.get_rect(center=(cx, 150)))

                # Hlavní text
                if self.text_alpha > 50:
                    txt_surf = pygame.Surface((700, 250), pygame.SRCALPHA)
                    lines = [
                        ("Kočka se přejedla...", self.font_medium, (255, 200, 100)),
                        ("a VYBOUCHLA!", self.font_medium, (255, 80, 60)),
                        ("", None, None),
                        ("Snědla celý vesmír.", self.font_small, (180, 180, 255)),
                        ("A pak i sebe.", self.font_small, (150, 255, 150)),
                    ]
                    y_off = 0
                    for text, font, color in lines:
                        if font is None:
                            y_off += 15
                            continue
                        a = min(self.text_alpha, 255)
                        rendered = font.render(text, True, (*color,))
                        rendered.set_alpha(a)
                        r = rendered.get_rect(center=(350, y_off + rendered.get_height() // 2))
                        txt_surf.blit(rendered, r)
                        y_off += rendered.get_height() + 8
                    self.screen.blit(txt_surf, (cx - 350, 280))

                if self.text_alpha > 200:
                    hint = self.font_hint.render("Stiskni ENTER nebo ESC", True, (120, 120, 150))
                    self.screen.blit(hint, hint.get_rect(center=(cx, SCREEN_HEIGHT - 50)))

        pygame.display.flip()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                if event.type == pygame.KEYDOWN:
                    if self.phase == "text" and self.text_alpha > 150:
                        if event.key in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_ESCAPE):
                            return "menu"
            self.update()
            self.draw()
            self.clock.tick(FPS)
        return "menu"


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
            if result and result.startswith("level"):
                level_num = result.replace("level", "")
                state = f"game{level_num}"
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
        
        elif state == "game3":
            game3 = GameLevel3(texture_manager)
            result = game3.run()
            if result == "won":
                lc = LevelComplete(texture_manager, "Cizí Planeta", game3.cat.food_eaten)
                lc_result = lc.run()
                state = "levels" if lc_result == "levels" else "quit"
            else:
                state = "levels"
        
        elif state == "game4":
            game4 = GameLevel4(texture_manager)
            result = game4.run()
            if result == "won":
                lc = LevelComplete(texture_manager, "Vesnice Mimozemšťanů", game4.cat.food_eaten)
                lc_result = lc.run()
                state = "levels" if lc_result == "levels" else "quit"
            else:
                state = "levels"
        
        elif state == "game5":
            game5 = GameLevel5(texture_manager)
            result = game5.run()
            if result == "won":
                lc = LevelComplete(texture_manager, "Mimozemské Město", game5.cat.food_eaten)
                lc_result = lc.run()
                state = "levels" if lc_result == "levels" else "quit"
            else:
                state = "levels"
        
        elif state == "game6":
            game6 = GameLevel6(texture_manager)
            result = game6.run()
            if result == "won":
                lc = LevelComplete(texture_manager, "Obří Kočka", game6.cat.food_eaten)
                lc_result = lc.run()
                state = "levels" if lc_result == "levels" else "quit"
            else:
                state = "levels"
        
        elif state == "game7":
            game7 = GameLevel7(texture_manager)
            result = game7.run()
            if result == "won":
                lc = LevelComplete(texture_manager, "Vesmír", game7.cat.food_eaten)
                lc_result = lc.run()
                state = "levels" if lc_result == "levels" else "quit"
            else:
                state = "levels"
        
        elif state == "game8":
            game8 = GameLevel8(texture_manager)
            result = game8.run()
            if result == "won":
                lc = LevelComplete(texture_manager, "Požírač Planet", game8.cat.food_eaten)
                lc_result = lc.run()
                # Po dokončení posledního levelu - cutscéna s explozí
                cutscene = ExplosionCutscene(texture_manager)
                cutscene.run()
                state = "menu"
            else:
                state = "levels"
    
    pygame.quit()
