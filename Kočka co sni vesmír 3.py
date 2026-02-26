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
MAX_CAT_SIZE = 150

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
            "plant": (20, TextureGenerator.create_plant_texture)
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
            "START",
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
                    return "start"
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
            if result == "start":
                return True
            self.update()
            self.draw()
            self.clock.tick(FPS)
        return False

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
            self.size += 2
            self.food_eaten += 1
            self.speed = max(2, 5 - (self.size - BASE_CAT_SIZE) / 30)
        food.eaten = True
    
    def draw(self, screen):
        """Kreslí POUZE texturu kočky - nic vykresleného!"""
        cat_texture = self.texture_manager.get_texture("cat")
        
        if cat_texture:
            scaled_cat = pygame.transform.scale(cat_texture, (int(self.size * 2), int(self.size * 2)))
            cat_rect = scaled_cat.get_rect(center=(int(self.x), int(self.y)))
            screen.blit(scaled_cat, cat_rect)

class Game:
    """Hlavní hra"""
    def __init__(self, texture_manager):
        self.screen = pygame.display.get_surface()
        self.clock = pygame.time.Clock()
        self.running = True
        self.texture_manager = texture_manager
        
        self.cat = AlienCat(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, texture_manager)
        self.foods = []
        self.spawn_food()
    
    def spawn_food(self):
        for _ in range(12):
            x = random.randint(50, SCREEN_WIDTH - 50)
            y = random.randint(150, SCREEN_HEIGHT - 50)
            food_type = random.choice(["bug", "mouse", "container", "plant"])
            self.foods.append(Food(x, y, food_type, self.texture_manager))
    
    def draw_laboratory(self):
        pygame.draw.rect(self.screen, LAB_FLOOR, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
        
        tile_size = 60
        for x in range(0, SCREEN_WIDTH, tile_size):
            for y in range(0, SCREEN_HEIGHT, tile_size):
                if (x // tile_size + y // tile_size) % 2 == 0:
                    pygame.draw.rect(self.screen, (210, 210, 210), (x, y, tile_size, tile_size))
        
        wall_color = (180, 180, 200)
        pygame.draw.rect(self.screen, wall_color, (0, 0, SCREEN_WIDTH, 100))
        pygame.draw.line(self.screen, DARK_GRAY, (0, 100), (SCREEN_WIDTH, 100), 3)
        
        shelf_y = 30
        pygame.draw.rect(self.screen, (150, 100, 50), (50, shelf_y, 200, 50))
        pygame.draw.circle(self.screen, (100, 100, 150), (100, shelf_y - 10), 12)
        pygame.draw.rect(self.screen, (200, 150, 100), (140, shelf_y - 15, 20, 20))
        pygame.draw.circle(self.screen, (100, 150, 100), (180, shelf_y - 12), 10)
        
        pygame.draw.rect(self.screen, (150, 100, 50), (SCREEN_WIDTH - 220, 50, 200, 60))
        for i in range(3):
            pygame.draw.circle(self.screen, (100, 150, 200), 
                              (SCREEN_WIDTH - 200 + i * 50, 40), 8)
        
        font_small = pygame.font.Font(None, 28)
        font_title = pygame.font.Font(None, 36)
        
        title_text = font_title.render("Mimozemská Kočka v Laboratoři", True, BLACK)
        self.screen.blit(title_text, (20, 10))
        
        size_text = font_small.render(f"Velikost: {self.cat.size:.0f} / {MAX_CAT_SIZE}", True, BLACK)
        self.screen.blit(size_text, (SCREEN_WIDTH - 350, 15))
        
        food_text = font_small.render(f"Snědeno: {self.cat.food_eaten}", True, BLACK)
        self.screen.blit(food_text, (SCREEN_WIDTH - 350, 45))
        
        progress_width = 300
        progress_height = 15
        progress_x = SCREEN_WIDTH - 350
        progress_y = 75
        
        pygame.draw.rect(self.screen, LIGHT_GRAY, 
                        (progress_x, progress_y, progress_width, progress_height))
        
        filled_width = (self.cat.size - BASE_CAT_SIZE) / (MAX_CAT_SIZE - BASE_CAT_SIZE) * progress_width
        pygame.draw.rect(self.screen, (80, 180, 100), 
                        (progress_x, progress_y, filled_width, progress_height))
        
        pygame.draw.rect(self.screen, BLACK, 
                        (progress_x, progress_y, progress_width, progress_height), 2)
        
        controls_text = font_small.render("WASD nebo Šipky = Pohyb", True, DARK_GRAY)
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
        
        pygame.quit()

if __name__ == "__main__":
    print("Inicializuji hru...")
    pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Mimozemská Kočka - Laboratoř")
    texture_manager = TextureManager()
    print("\nSpouštím menu...")
    
    menu = Menu(texture_manager)
    if menu.run():
        game = Game(texture_manager)
        game.run()