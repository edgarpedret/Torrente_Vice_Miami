import pygame
import sys
import time
import subprocess

# Configuración inicial
pygame.init()
WIDTH, HEIGHT = 1366, 768
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game Intro Trailer")
clock = pygame.time.Clock()

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Fuentes
font_big = pygame.font.SysFont("georgia", 74, bold=True)
font_medium = pygame.font.SysFont("arial", 40)

# Música de fondo
pygame.mixer.music.load("assets/music/Apatrullando.mp3")  # Asegúrate de que exista el archivo
pygame.mixer.music.play(-1)

# Frases del tráiler
scenes = [
    {"text": "En un mundo sin esperanza...", "duration": 3},
    {"text": "Donde el caos reina sin control...", "duration": 3},
    {"text": "Solo un buen policía puede...", "duration": 3},
    {"text": "Ponerle remedio a esta situación", "duration": 3},
    {"text": "Prepárate para cumplir la ley", "duration": 3},
    {"text": "El Brazo Tonto De La Ley", "duration": 5, "big": True},
]

# Efecto fade-in del texto
def fade_in_text(text, duration, big=False):
    font = font_big if big else font_medium
    rendered_text = font.render(text, True, WHITE)
    text_rect = rendered_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    start_ticks = pygame.time.get_ticks()  # Marcamos el tiempo de inicio
    while pygame.time.get_ticks() - start_ticks < duration * 1000:  # Duración en milisegundos
        for alpha in range(0, 256, 5):
            screen.fill(BLACK)
            text_surface = font.render(text, True, WHITE)
            text_surface.set_alpha(alpha)
            screen.blit(text_surface, text_rect)
            pygame.display.update()
            clock.tick(30)
        pygame.event.pump()  # Procesa eventos para evitar que la app se "congele"

# Efecto fade-out del texto
def fade_out_text(text, big=False):
    font = font_big if big else font_medium
    rendered_text = font.render(text, True, WHITE)
    text_rect = rendered_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    for alpha in range(255, -1, -5):
        screen.fill(BLACK)
        text_surface = font.render(text, True, WHITE)
        text_surface.set_alpha(alpha)
        screen.blit(text_surface, text_rect)
        pygame.display.update()
        clock.tick(30)

# Efecto de flash blanco
def flash_effect():
    flash = pygame.Surface((WIDTH, HEIGHT))
    flash.fill(WHITE)
    for alpha in range(255, 0, -25):
        flash.set_alpha(alpha)
        screen.blit(flash, (0, 0))
        pygame.display.update()
        clock.tick(60)

# Efecto zoom dramático final
def dramatic_final():
    text = scenes[-1]["text"]
    for size in range(74, 94, 2):
        font_dynamic = pygame.font.SysFont("georgia", size, bold=True)
        screen.fill(BLACK)
        text_surface = font_dynamic.render(text, True, WHITE)
        rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text_surface, rect)
        pygame.display.update()
        clock.tick(15)
    time.sleep(2)  # Mantener por un par de segundos antes de continuar

# Ejecutar intro
def run_trailer():
    for i, scene in enumerate(scenes[:-1]):  # Todas menos la última
        fade_in_text(scene["text"], scene["duration"], scene.get("big", False))
        fade_out_text(scene["text"], scene.get("big", False))
        flash_effect()

    # Última escena con zoom especial
    dramatic_final()
    pygame.mixer.music.fadeout(2000)
    time.sleep(2)

    pygame.quit()

    # Llamada al siguiente script sin que bloquee el hilo actual
    subprocess.Popen(["python3", "main.py"])  # Ejecuta "main.py" de forma no bloqueante
    sys.exit()

# Main loop
try:
    run_trailer()
except KeyboardInterrupt:
    pygame.quit()
    sys.exit()


