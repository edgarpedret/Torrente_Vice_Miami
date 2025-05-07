import time
import pygame
from pygame.locals import *
import os

pygame.init()
pygame.mixer.init()

pygame.mixer.music.load("assets/music/Apatrullando.mp3")
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)

VIEW_WIDTH = 1366
VIEW_HEIGHT = 768

BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)

pantalla = pygame.display.set_mode((VIEW_WIDTH, VIEW_HEIGHT))
pygame.display.set_caption("Torrente Vice")

titulo_font = pygame.font.SysFont("georgia", 74, bold=True)
menu_font = pygame.font.Font(None, 36)

background_image = pygame.image.load('assets/background_images/mapa.jpg').convert()
background_width = background_image.get_width()
background_height = background_image.get_height()

player_image = pygame.image.load('assets/sprites/down0.png')
protagonist_speed = 4
player_rect = player_image.get_rect(midbottom=(VIEW_WIDTH // 2, VIEW_HEIGHT // 2))

bg_x, bg_y = 0, 0
MARGIN_X, MARGIN_Y = VIEW_WIDTH // 2, VIEW_HEIGHT // 2

clock = pygame.time.Clock()
fps = 30

sprite_direction = "down"
sprite_index = 0
animation_protagonist_speed = 200
sprite_frame_number = 3
last_change_frame_time = 0
idle = False

# === ZONAS PROHIBIDAS: coordenadas basadas en el personaje en pantalla ===
zona_mar = pygame.Rect(0, 0, 1366, 150)
#casa_izquierda = pygame.Rect(430, 280, 160, 160)
#casa_derecha = pygame.Rect(770, 280, 160, 160)
zonas_prohibidas = [zona_mar]


def imprimir_pantalla_fons(x, y):
    pantalla.blit(background_image, (x, y))


def mostrar_menu():
    pantalla.fill(NEGRO)
    title_text = titulo_font.render("Torrente Vice", True, BLANCO)
    menu_text_1 = menu_font.render("1. Salir", True, BLANCO)
    menu_text_2 = menu_font.render("2. Continuar", True, BLANCO)

    pantalla.blit(title_text, (VIEW_WIDTH // 2 - title_text.get_width() // 2, 100))
    pantalla.blit(menu_text_1, (VIEW_WIDTH // 2 - 50, VIEW_HEIGHT // 2 - 20))
    pantalla.blit(menu_text_2, (VIEW_WIDTH // 2 - 50, VIEW_HEIGHT // 2 + 20))

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    pygame.quit()
                    os.system("python3 main.py")
                    exit()
                elif event.key == pygame.K_2:
                    return


# === BUCLE PRINCIPAL ===
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            mostrar_menu()

    current_time = pygame.time.get_ticks()
    idle = True
    keys = pygame.key.get_pressed()

    # Guardamos la posición previa
    prev_pos = player_rect.topleft

    if keys[K_UP]:
        idle = False
        sprite_direction = "up"
        player_rect.y -= protagonist_speed

    if keys[K_DOWN]:
        idle = False
        sprite_direction = "down"
        player_rect.y += protagonist_speed

    if keys[K_RIGHT]:
        idle = False
        sprite_direction = "right"
        player_rect.x += protagonist_speed

    if keys[K_LEFT]:
        idle = False
        sprite_direction = "left"
        player_rect.x -= protagonist_speed

    # Detectar colisiones y revertir si choca
    for zona in zonas_prohibidas:
        if player_rect.colliderect(zona):
            player_rect.topleft = prev_pos
            break

    imprimir_pantalla_fons(bg_x, bg_y)

    if not idle:
        if current_time - last_change_frame_time >= animation_protagonist_speed:
            last_change_frame_time = current_time
            sprite_index = (sprite_index + 1) % sprite_frame_number
    else:
        sprite_index = 0

    player_image = pygame.image.load(f'assets/sprites/{sprite_direction}{sprite_index}.png')
    pantalla.blit(player_image, player_rect)
    player_rect.clamp_ip(pantalla.get_rect())

    pygame.display.update()
    clock.tick(fps)

