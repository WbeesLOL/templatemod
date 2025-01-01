

# Pygame initialisieren

try:
    import pygame
    pygame.init()
except Exception:
    print("pygame could not be initialized. Please make sure you have pygame installed.")

import sys
import samplemod
from random import randint



# Bildschirmgröße und Farben
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 500
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
RANDOM = (randint(0,255),randint(0,255),randint(0,255))

# Spielkonstanten
GRAVITY = 0.5
JUMP_STRENGTH = -10
OBSTACLE_SPEED = -6
FPS = 60
VERSION = "1.0"
LINK = "https://example.com/"



print(f"sucessfully loaded templatemod v{VERSION}!")
print("happy modding! :D")
print(f"for more information visit {LINK}")

# Shop-Konstanten
CUBE_COLORS = [BLUE, GREEN, YELLOW, RED, CYAN, MAGENTA, ORANGE, PURPLE]
CUBE_PRICES = [0, 500, 1000, 2000, 5000, 10000, 20000, 50000]  # Hohe Preise
BALL_SHAPES = [CYAN, MAGENTA, ORANGE, PURPLE]  # Farben für Bälle
BALL_PRICES = [100000, 200000, 300000, 500000]  # Sehr hohe Preise

selected_color = BLUE
selected_shape = "cube"

# Bildschirm erstellen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(f"Geometry Jump (modded with templatemod v{VERSION})")

# Clock für FPS
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)
title_font = pygame.font.Font(None, 72)


class get_element:
    def get_screen():
        return screen
    def get_width():
        return SCREEN_WIDTH
    def get_height():
        return SCREEN_HEIGHT
    def get_color(r, g, b):
        return r, g, b


def change_resolution(width, height):
    screen = pygame.display.set_mode((width, height))


# Spielerklasse
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill(selected_color)
        self.rect = self.image.get_rect(midbottom=(100, SCREEN_HEIGHT - 20))
        self.velocity = 0

    def update(self):
        # Bewegung
        self.velocity += GRAVITY
        self.rect.y += self.velocity

        # Begrenzung unten
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.velocity = 0

    def jump(self):
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.velocity = JUMP_STRENGTH

    def update_shape(self, shape, color):
        if shape == "cube":
            self.image = pygame.Surface((40, 40))
        elif shape == "ball":
            self.image = pygame.Surface((40, 40), pygame.SRCALPHA)
            pygame.draw.circle(self.image, color, (20, 20), 20)
        self.image.fill(color, special_flags=pygame.BLEND_RGBA_MULT)

# Hindernisklasse
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.image = pygame.Surface((30, 60))
        self.image.fill(RED)
        self.rect = self.image.get_rect(midbottom=(x, SCREEN_HEIGHT))

    def update(self):
        self.rect.x += OBSTACLE_SPEED
        if self.rect.right < 0:
            self.kill()

# Gruppen erstellen
player = Player()
player_group = pygame.sprite.GroupSingle(player)

obstacle_group = pygame.sprite.Group()

# Hindernisse erzeugen
def spawn_obstacle():
    x = randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 200)
    obstacle = Obstacle(x)
    obstacle_group.add(obstacle)

def title_screen(total_score):
    samplemod.events.ontitlescreen()
    secret_code = ["w", "a", "s", "d"]
    code_progress = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if start_button.collidepoint(mouse_pos):
                    return "start"
                if shop_button.collidepoint(mouse_pos):
                    return "shop"
                if modbutton.collidepoint(mouse_pos):
                    draw_custom_screen()
            if event.type == pygame.KEYDOWN:
                if event.unicode == secret_code[code_progress]:
                    code_progress += 1
                    if code_progress == len(secret_code):
                        return "secret_shop"
                else:
                    code_progress = 0

        screen.fill(WHITE)

        # Titel
        title_text = title_font.render("Geometry Jump (tm)", True, BLACK)
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 50))

        # Startknopf
        start_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, 150, 200, 50)
        pygame.draw.rect(screen, BLUE, start_button)
        start_text = font.render("Start", True, WHITE)
        screen.blit(start_text, (start_button.x + 70, start_button.y + 10))

        # Shopknopf
        shop_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, 250, 200, 50)
        pygame.draw.rect(screen, GREEN, shop_button)
        shop_text = font.render("Shop", True, WHITE)
        screen.blit(shop_text, (shop_button.x + 70, shop_button.y + 10))

        # Mod-Knopf
        modbutton = pygame.Rect(SCREEN_WIDTH // 2 - 100, 350, 200, 50)
        pygame.draw.rect(screen, RANDOM, modbutton)
        modbutton_text = font.render("Mods", True, WHITE)
        screen.blit(modbutton_text, (modbutton.x + modbutton.width / 2 - modbutton_text.get_width() / 2, modbutton.y + modbutton_text.get_height() / 2))

        # Punktestand anzeigen
        score_text = font.render(f"Punkte: {total_score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(FPS)

# Shop zeichnen
def draw_shop(score, shop_type):
    global selected_shape, selected_color, dialog
    items = BALL_SHAPES if shop_type == "secret" else CUBE_COLORS
    prices = BALL_PRICES if shop_type == "secret" else CUBE_PRICES
    dialog = "Wie bist du nach hier gekommen?" if shop_type == "secret" else "Willkommen im Shop!"
    
    if shop_type == "secret":
        
        # Geheimshop-Dialog
        screen.fill(WHITE)
        text = font.render(dialog, True, BLACK)
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - 20))
        pygame.display.flip()
        pygame.time.wait(2000)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return
            if event.type == pygame.KEYDOWN:
                try:
                    key_num = int(event.unicode) - 1
                    if 0 <= key_num < len(items):
                        if score >= prices[key_num]:
                            global selected_shape, selected_color
                            selected_shape = "ball" if shop_type == "secret" else "cube"
                            selected_color = items[key_num]
                            player.update_shape(selected_shape, selected_color)
                            score -= prices[key_num]
                except ValueError:
                    pass

        screen.fill(WHITE)
        shop_text = font.render(dialog, True, BLACK)
        screen.blit(shop_text, (20, 20))

        for i, (item, price) in enumerate(zip(items, prices)):
            x = 100 + (i % 4) * 150
            y = 100 + (i // 4) * 150
            if shop_type == "secret":
                pygame.draw.circle(screen, item, (x + 25, y + 25), 25)
            else:
                pygame.draw.rect(screen, item, (x, y, 50, 50))
            price_text = font.render(f"{price} Pkt", True, BLACK)
            screen.blit(price_text, (x - 10, y + 60))

        score_text = font.render(f"Deine Punkte: {score}", True, BLACK)
        screen.blit(score_text, (20, 350))
        pygame.display.flip()
        clock.tick(FPS)

# Spielhauptschleife
# Spielhauptschleife
def game_loop(total_score):
    samplemod.events.ongamestart()
    # Score und Hindernisse zurücksetzen
    score = 0
    spawn_timer = 0
    obstacle_group.empty()  # <--- Hindernisse zurücksetzen

    while True:
        samplemod.events.ongametick()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                player.jump()

        # Spielobjekte aktualisieren
        player_group.update()
        obstacle_group.update()

        # Hindernisse spawnen
        spawn_timer += 1
        if spawn_timer > 100:
            spawn_obstacle()
            spawn_timer = 0

        # Punkte erhöhen und Kollision überprüfen
        score += 1
        if pygame.sprite.spritecollide(player, obstacle_group, False):
            samplemod.events.ongameover()
            return total_score + score
            

        # Bildschirm zeichnen
        screen.fill(WHITE)
        player_group.draw(screen)
        obstacle_group.draw(screen)

        # Score anzeigen
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))
        pygame.display.flip()
        clock.tick(FPS)


def draw_custom_screen():
    

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return
        screen.fill(RANDOM)
        shop_text = font.render("Mods", True, BLACK)
        screen.blit(shop_text, (20, 20))
        untertext = font.render("Hier kannst du Mods sehen", True, BLACK)
        screen.blit(untertext, (20, 50))

        tutorial_link = font.render("Tutorial: example.com", True, BLUE)
        screen.blit(tutorial_link, (20, 100))

        mod_label = font.render("Deafault Mod     |   1.0", True, BLACK)
        mod_label2 = font.render("templatemod     |   1.0", True, BLACK)
        screen.blit(mod_label, (20, 150))
        screen.blit(mod_label2, (20, 200))

        score_text = font.render(f"templatemod v{VERSION}", True, BLACK)
        screen.blit(score_text, (20, 450))
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    total_score = 0
    while True:
        choice = title_screen(total_score)
        if choice == "start":
            total_score = game_loop(total_score)
        elif choice == "shop":
            samplemod.events.onopenshop()
            draw_shop(total_score, "regular")
            
        elif choice == "secret_shop":
            samplemod.events.onopensecretshop()
            draw_shop(total_score, "secret")
            
