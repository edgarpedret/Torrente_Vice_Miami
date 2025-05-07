import pygame
import random
import sys
import time
import os

# Inicializar Pygame
pygame.init()
WIDTH, HEIGHT = 1366, 768
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tiroteo Torrente")
clock = pygame.time.Clock()

# Tamany
VIEW_WIDTH = 1366
VIEW_HEIGHT = 768

# Fonts
titulo_font = pygame.font.SysFont("georgia", 74, bold=True)  
menu_font = pygame.font.Font(None, 36)

# Cargar imágenes
background = pygame.image.load("assets/background_images/dreams.png")
player_img = pygame.image.load("assets/sprites/up0.png")
enemy_imgs = [pygame.image.load(f"assets/sprites/down{i}.png") for i in range(4)]
life_img = pygame.transform.scale(pygame.image.load("assets/objects/vida1.png"), (20, 20))

# Colores y fuentes
WHITE = (255, 255, 255)
font = pygame.font.SysFont("arial", 24)

# Variables del jugador
player_x = WIDTH // 2
player_y = HEIGHT - 60
player_speed = 5
player_lives = 5
player_bullets = []

# Enemigos
enemies = []
enemy_bullets = []
enemy_spawn_delay = 40

# Tiempo
start_time = pygame.time.get_ticks()
game_duration = 120000  # 120 segundos / 2 Mins

# Colors
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)



# Disparo
bullet_speed = 7
enemy_bullet_speed = 4

# Función para mostrar el menú de pausa
def mostrar_menu():
    screen.fill(NEGRO)

    title_text = titulo_font.render("PAUSA", True, BLANCO)
    menu_text_1 = menu_font.render("1. Continuar", True, BLANCO)
    menu_text_2 = menu_font.render("2. Salir", True, BLANCO)

    screen.blit(title_text, (VIEW_WIDTH // 2 - title_text.get_width() // 2, 100))
    screen.blit(menu_text_1, (VIEW_WIDTH // 2 - 50, VIEW_HEIGHT // 2 - 20))
    screen.blit(menu_text_2, (VIEW_WIDTH // 2 - 50, VIEW_HEIGHT // 2 + 20))

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:  # Continuar
                    return
                elif event.key == pygame.K_2:  # Salir y volver al main
                    pygame.quit()
                    import os
                    os.system("python3 movement.py")
                    exit()



def spawn_enemy():
    enemy = {
        "x": random.randint(0, WIDTH - 50),
        "y": -50,
        "img": random.choice(enemy_imgs),
        "speed": random.randint(1, 3),
        "last_shot": pygame.time.get_ticks()
    }
    enemies.append(enemy)

def draw_lives():
    for i in range(player_lives):
        screen.blit(life_img, (10 + i * 25, 10))

def draw_timer():
    elapsed = pygame.time.get_ticks() - start_time
    remaining = max(0, game_duration - elapsed)
    seconds = remaining // 1000
    timer_surface = font.render(f"Tiempo: {seconds}s", True, WHITE)
    screen.blit(timer_surface, (WIDTH - 160, 10))
    return remaining <= 0

def show_victory():
    victory = font.render("¡Lo Has Conseguido!", True, WHITE)
    screen.blit(victory, (WIDTH // 2 - 100, HEIGHT // 2))

# Bucle principal
running = True
victory = False

while running:
    clock.tick(60)
    screen.blit(background, (0, 0))

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < WIDTH - player_img.get_width():
        player_x += player_speed
    if keys[pygame.K_SPACE]:
        if len(player_bullets) < 5:
            player_bullets.append([player_x + player_img.get_width()//2, player_y])
    if keys[pygame.K_ESCAPE]:
        mostrar_menu()


    # Dibujar jugador
    screen.blit(player_img, (player_x, player_y))

    # Dibujar y mover balas del jugador
    for bullet in player_bullets[:]:
        bullet[1] -= bullet_speed
        pygame.draw.rect(screen, WHITE, (*bullet, 4, 10))
        if bullet[1] < 0:
            player_bullets.remove(bullet)

    # Spawnear enemigos
    if random.randint(0, enemy_spawn_delay) == 0:
        spawn_enemy()

    # Mover enemigos y disparar
    for enemy in enemies[:]:
        if enemy["y"] < HEIGHT // 2:
            enemy["y"] += 0.5  # Bajada lenta

        screen.blit(enemy["img"], (enemy["x"], enemy["y"]))
        
        # Disparo enemigo
        now = pygame.time.get_ticks()
        if now - enemy["last_shot"] > 2000 and random.random() < 0.02:
            enemy_bullets.append([enemy["x"] + 20, enemy["y"] + 30])
            enemy["last_shot"] = now


    # Mover balas enemigas
    for e_bullet in enemy_bullets[:]:
        e_bullet[1] += enemy_bullet_speed
        pygame.draw.rect(screen, (255, 0, 0), (*e_bullet, 4, 10))
        if e_bullet[1] > HEIGHT:
            enemy_bullets.remove(e_bullet)

    # Colisiones: jugador golpeado
    for e_bullet in enemy_bullets[:]:
        if player_x < e_bullet[0] < player_x + player_img.get_width() and \
           player_y < e_bullet[1] < player_y + player_img.get_height():
            enemy_bullets.remove(e_bullet)
            player_lives -= 1
            if player_lives <= 0:
                running = False

    # Colisiones: balas del jugador golpean enemigos
    for bullet in player_bullets[:]:
        for enemy in enemies[:]:
            if enemy["x"] < bullet[0] < enemy["x"] + enemy["img"].get_width() and \
               enemy["y"] < bullet[1] < enemy["y"] + enemy["img"].get_height():
                try:
                    player_bullets.remove(bullet)
                except ValueError:
                    pass
                enemies.remove(enemy)
                break

    draw_lives()
    time_up = draw_timer()

    if time_up and player_lives > 0:
        show_victory()
        victory = True

    pygame.display.flip()

    if time_up:
        pygame.time.delay(3000)
        running = False

    # Manejar eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
sys.exit()
