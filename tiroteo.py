import pygame
import random
import subprocess
import sys
import os

# Configuración de pantalla
SCREEN_WIDTH, SCREEN_HEIGHT = 1366, 768

# Inicialización
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Torrente Vice")

# Colores
WHITE, BLACK = (255, 255, 255), (0, 0, 0)

# Reloj
clock = pygame.time.Clock()

# Fuentes
font_wasted = pygame.font.SysFont("impact", 120)
font_menu = pygame.font.SysFont("arial", 40)

# Recursos visuales
try:
    background = pygame.image.load("assets/background_images/1fondo.png").convert()
except:
    background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    background.fill(BLACK)

player_img = pygame.transform.scale(pygame.image.load("assets/sprites/right0.png"), (50, 50))
enemy_img = pygame.transform.scale(pygame.image.load("assets/sprites/left0.png"), (50, 50))
bullet_img = pygame.transform.scale(pygame.image.load("assets/objects/bala.png"), (10, 20))
life_img = pygame.transform.scale(pygame.image.load("assets/objects/vida1.png"), (40, 40))

# Jugador
player_x, player_y = SCREEN_WIDTH // 4, SCREEN_HEIGHT - 70
player_speed = 5
player_lives = 5

# Movimiento
moving_left = moving_right = moving_up = moving_down = False

# Balas y enemigos
shoot_delay = 500
last_shot = 0
player_bullets, enemy_bullets, enemies = [], [], []

class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = random.randint(2, 5)
        self.is_stopped = False

    def move(self):
        if not self.is_stopped:
            self.y += self.speed

    def draw(self):
        screen.blit(enemy_img, (self.x, self.y))

    def shoot(self):
        enemy_bullets.append(Bullet(self.x + 20, self.y + 50, "enemy"))

class Bullet:
    def __init__(self, x, y, owner):
        self.x = x
        self.y = y
        self.speed = 7 if owner == "player" else 5
        self.owner = owner

    def move(self):
        self.y += -self.speed if self.owner == "player" else self.speed

    def draw(self):
        screen.blit(bullet_img, (self.x, self.y))

def shoot_bullet():
    global last_shot
    now = pygame.time.get_ticks()
    if now - last_shot > shoot_delay:
        player_bullets.append(Bullet(player_x + 22, player_y, "player"))
        last_shot = now

def create_enemy():
    enemies.append(Enemy(random.randint(0, SCREEN_WIDTH - 50), random.randint(-150, -50)))

def draw_lives():
    for i in range(player_lives):
        screen.blit(life_img, (10 + i * 45, 10))

def check_collisions():
    global player_bullets
    for bullet in player_bullets[:]:
        for enemy in enemies[:]:
            if enemy.x < bullet.x < enemy.x + 50 and enemy.y < bullet.y < enemy.y + 50:
                enemies.remove(enemy)
                player_bullets.remove(bullet)
                break

def check_bullet_collisions():
    global player_lives
    for bullet in enemy_bullets[:]:
        if player_x <= bullet.x <= player_x + 50 and player_y <= bullet.y <= player_y + 50:
            enemy_bullets.remove(bullet)
            player_lives -= 1
            if player_lives <= 0:
                show_game_over_screen()

def restart_game():
    global player_x, player_y, player_lives, enemies, player_bullets, enemy_bullets
    player_x, player_y = SCREEN_WIDTH // 4, SCREEN_HEIGHT - 70
    player_lives = 5
    enemies.clear()
    player_bullets.clear()
    enemy_bullets.clear()

def show_game_over_screen():
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.set_alpha(180)
    overlay.fill(BLACK)
    screen.blit(background, (0, 0))
    screen.blit(overlay, (0, 0))

    wasted = font_wasted.render("WASTED", True, (255, 0, 0))
    restart = font_menu.render("Pulsa R para reiniciar o M para volver al menú", True, WHITE)

    screen.blit(wasted, wasted.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)))
    screen.blit(restart, restart.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60)))
    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    waiting = False
                    restart_game()
                elif event.key == pygame.K_m:
                    pygame.quit()
                    subprocess.run(["python", "main.py"] if os.name == 'nt' else ["python3", "main.py"])
                    sys.exit()
