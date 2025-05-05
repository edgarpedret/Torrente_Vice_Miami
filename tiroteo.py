import pygame
import random
import os
import sys
import subprocess

pygame.init()

# Configuración
WIDTH, HEIGHT = 1366, 768
FPS = 60
ENEMY_SPAWN_TIME = 1200
ENEMY_FIRE_TIME = 3000
GAME_DURATION = 50000
ENEMY_SPEED = 0.3
BULLET_SPEED = -5
ENEMY_BULLET_SPEED = 2

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Ventana
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Juego de Supervivencia")

# Cargar imágenes
enemy_img = pygame.transform.scale(pygame.image.load("assets/sprites/down0.png"), (50, 50))
heart_img = pygame.transform.scale(pygame.image.load("assets/objects/vida1.png"), (40, 40))
player_img = pygame.transform.scale(pygame.image.load("assets/sprites/up0.png"), (70, 70))

# Fuente
font = pygame.font.SysFont("Arial", 40)

# Jugador
player_rect = pygame.Rect(WIDTH // 2 - 35, HEIGHT - 80, 70, 70)

# Función para mostrar texto de temporizador
def draw_timer():
    elapsed = pygame.time.get_ticks() - start_time
    remaining = max(0, GAME_DURATION - elapsed)
    seconds = remaining // 1000
    text = font.render(f"Tiempo restante: {seconds}", True, WHITE)
    win.blit(text, (WIDTH - 300, 10))

# Función para mostrar pantalla de game over
def show_game_over():
    win.fill(BLACK)
    text = font.render("PERDEDOR", True, RED)
    win.blit(text, (WIDTH // 2 - 100, HEIGHT // 2 - 100))

    btn1 = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2, 300, 50)
    btn2 = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 + 70, 300, 50)

    pygame.draw.rect(win, WHITE, btn1)
    pygame.draw.rect(win, WHITE, btn2)

    txt1 = font.render("Ejecutar movement.py", True, BLACK)
    txt2 = font.render("Reiniciar Juego", True, BLACK)

    win.blit(txt1, (btn1.x + 10, btn1.y + 5))
    win.blit(txt2, (btn2.x + 35, btn2.y + 5))

    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn1.collidepoint(event.pos):
                    subprocess.run([sys.executable, "movement.py"])
                    waiting = False
                elif btn2.collidepoint(event.pos):
                    main()
                    waiting = False

# Función para dibujar todo
def draw_window(enemies, bullets, enemy_bullets, lives):
    win.fill(BLACK)

    # Jugador
    win.blit(player_img, player_rect)

    # Enemigos
    for enemy in enemies:
        win.blit(enemy_img, (enemy.x, enemy.y))  # Esto asegura que se vea

    # Balas del jugador
    for bullet in bullets:
        pygame.draw.rect(win, RED, bullet)

    # Balas enemigas
    for eb in enemy_bullets:
        pygame.draw.rect(win, WHITE, eb)

    # Vidas
    for i in range(lives):
        win.blit(heart_img, (10 + i * 45, 10))

    # Temporizador
    draw_timer()

    pygame.display.update()

# Función principal
def main():
    global start_time
    clock = pygame.time.Clock()
    enemies = []
    bullets = []
    enemy_bullets = []
    lives = 5
    last_spawn = pygame.time.get_ticks()
    last_enemy_fire = pygame.time.get_ticks()
    start_time = pygame.time.get_ticks()

    run = True
    while run:
        clock.tick(FPS)
        now = pygame.time.get_ticks()

        # Fin de tiempo
        if now - start_time > GAME_DURATION:
            run = False
            show_game_over()

        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_t:
                bullet = pygame.Rect(player_rect.centerx - 5, player_rect.top, 10, 20)
                bullets.append(bullet)

        # Movimiento jugador (izquierda/derecha solamente)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_rect.left > 0:
            player_rect.x -= 5
        if keys[pygame.K_RIGHT] and player_rect.right < WIDTH:
            player_rect.x += 5
        # Restringir eje Y
        player_rect.y = HEIGHT - 80

        # Spawneo de enemigos
        if now - last_spawn > ENEMY_SPAWN_TIME:
            x = random.randint(0, WIDTH - 50)
            new_enemy = pygame.Rect(x, -50, 50, 50)
            enemies.append(new_enemy)
            last_spawn = now

        # Disparos enemigos
        if now - last_enemy_fire > ENEMY_FIRE_TIME:
            for enemy in enemies:
                if random.random() < 0.4:
                    eb = pygame.Rect(enemy.centerx - 3, enemy.bottom, 6, 15)
                    enemy_bullets.append(eb)
            last_enemy_fire = now

        # Movimiento enemigos
        for enemy in enemies:
            enemy.y += ENEMY_SPEED

        # Movimiento balas jugador
        for bullet in bullets[:]:
            bullet.y += BULLET_SPEED
            if bullet.y < 0:
                bullets.remove(bullet)

        # Movimiento balas enemigas
        for eb in enemy_bullets[:]:
            eb.y += ENEMY_BULLET_SPEED
            if eb.colliderect(player_rect):
                enemy_bullets.remove(eb)
                lives -= 1
                if lives <= 0:
                    run = False
                    show_game_over()
            elif eb.y > HEIGHT:
                enemy_bullets.remove(eb)

        # Colisiones bala-jugador y enemigos
        for enemy in enemies[:]:
            for bullet in bullets[:]:
                if enemy.colliderect(bullet):
                    bullets.remove(bullet)
                    enemies.remove(enemy)
                    break

        draw_window(enemies, bullets, enemy_bullets, lives)

if __name__ == "__main__":
    main()
