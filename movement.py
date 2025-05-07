import time
import pygame
from pygame.locals import *
import os

# Inicializar pygame
pygame.init()
pygame.mixer.init()

# Música
pygame.mixer.music.load("assets/music/Apatrullando.mp3")
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)

# Ventana
VIEW_WIDTH = 1366
VIEW_HEIGHT = 768

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)

# Inicializar pantalla
pantalla = pygame.display.set_mode((VIEW_WIDTH, VIEW_HEIGHT))
pygame.display.set_caption("Torrente Vice")

# Fuentes
titulo_font = pygame.font.SysFont("georgia", 74, bold=True)
menu_font = pygame.font.Font(None, 36)

# Fondo
background_image = pygame.image.load('assets/background_images/mapa.jpg').convert()
background_width = background_image.get_width()
background_height = background_image.get_height()

# Personaje
player_image = pygame.image.load('assets/sprites/down0.png')
protagonist_speed = 4
player_rect = player_image.get_rect(midbottom=(VIEW_WIDTH // 2, VIEW_HEIGHT // 2))

# Posición del fondo
bg_x, bg_y = 0, 0
MARGIN_X, MARGIN_Y = VIEW_WIDTH // 2, VIEW_HEIGHT // 2

# FPS
clock = pygame.time.Clock()
fps = 30

# Animación
sprite_direction = "down"
sprite_index = 0
animation_protagonist_speed = 200
sprite_frame_number = 3
last_change_frame_time = 0
idle = False

# Zonas del mapa (ajusta según escala real de tu imagen)
# Son coordenadas absolutas dentro del mapa, no de la pantalla
edificio_amarillo_rect = pygame.Rect(710, 720, 470, 475)
puerta_amarilla_rect = pygame.Rect(915, 850, 53, 380)

# Información de que hacer
def mostrar_intro():
    intro_duracion = 10000  # milisegundos
    inicio_intro = pygame.time.get_ticks()

    texto_intro = menu_font.render("Dirígete al New Dreams a por tabaquillo pa fuma, que vienes del casino de ganar dinero y tienes mono", True, BLANCO)
    overlay_negro = pygame.Surface((VIEW_WIDTH, VIEW_HEIGHT))
    overlay_negro.set_alpha(180)  # Opacidad (0-255)
    overlay_negro.fill((0, 0, 0))

    while pygame.time.get_ticks() - inicio_intro < intro_duracion:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        imprimir_pantalla_fons(bg_x, bg_y)  # Dibuja el fondo
        pantalla.blit(overlay_negro, (0, 0))  # Dibuja el overlay negro opaco
        pantalla.blit(texto_intro, (VIEW_WIDTH // 2 - texto_intro.get_width() // 2, VIEW_HEIGHT // 2 - 20))  # Centrar texto

        pygame.display.update()
        clock.tick(fps)



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

# INTRO DE INFO
mostrar_intro()

# Bucle principal
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
    dx, dy = 0, 0

    if keys[K_UP]:
        idle = False
        sprite_direction = "up"
        dy = -protagonist_speed
    if keys[K_DOWN]:
        idle = False
        sprite_direction = "down"
        dy = protagonist_speed
    if keys[K_RIGHT]:
        idle = False
        sprite_direction = "right"
        dx = protagonist_speed
    if keys[K_LEFT]:
        idle = False
        sprite_direction = "left"
        dx = -protagonist_speed

    # Movimiento y scroll
    new_rect = player_rect.move(dx, dy)

    map_player_x = new_rect.centerx - bg_x
    map_player_y = new_rect.centery - bg_y
    map_player_rect = pygame.Rect(map_player_x - 16, map_player_y - 32, 32, 64)

    # Colisión con edificio amarillo
    if edificio_amarillo_rect.colliderect(map_player_rect) and not puerta_amarilla_rect.colliderect(map_player_rect):
        dx = dy = 0  # Bloquear movimiento

    # Entrada al edificio por la puerta
    if puerta_amarilla_rect.colliderect(map_player_rect):
        pygame.quit()
        os.system("python3 tiroteo.py")
        exit()

    # Aplicar movimiento con scroll
    if dx != 0:
        if dx > 0:  # Derecha
            if player_rect.x < VIEW_WIDTH - MARGIN_X or bg_x <= VIEW_WIDTH - background_width:
                player_rect.x += dx
            else:
                bg_x = max(bg_x - dx, VIEW_WIDTH - background_width)
        else:  # Izquierda
            if player_rect.x > MARGIN_X or bg_x >= 0:
                player_rect.x += dx
            else:
                bg_x = min(bg_x - dx, 0)

    if dy != 0:
        if dy > 0:  # Abajo
            if player_rect.y < VIEW_HEIGHT - MARGIN_Y or bg_y <= VIEW_HEIGHT - background_height:
                player_rect.y += dy
            else:
                bg_y = max(bg_y - dy, VIEW_HEIGHT - background_height)
        else:  # Arriba
            if player_rect.y > MARGIN_Y or bg_y >= 0:
                player_rect.y += dy
            else:
                bg_y = min(bg_y - dy, 0)

    imprimir_pantalla_fons(bg_x, bg_y)

    if not idle:
        if current_time - last_change_frame_time >= animation_protagonist_speed:
            last_change_frame_time = current_time
            sprite_index = (sprite_index + 1) % sprite_frame_number
    else:
        sprite_index = 0

    player_image = pygame.image.load(f'assets/sprites/{sprite_direction}{sprite_index}.png')
    pantalla.blit(player_image, player_rect)

    pygame.display.update()
    clock.tick(fps)
