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
pygame.mixer.music.load("assets/music/Apatrullando.mp3")  # Asegúrate de tener este archivo
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

def fade_in_text(text, duration, big=False):
    font = font_big if big else font_medium
    for alpha in range(0, 255, 5):
        screen.fill(BLACK)
        rendered_text = font.render(text, True, WHITE)
        rendered_text.set_alpha(alpha)
        text_rect = rendered_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(rendered_text, text_rect)
        pygame.display.update()
        clock.tick(30)

    time.sleep(duration)

def run_trailer():
    for scene in scenes:
        fade_in_text(scene["text"], scene["duration"], scene.get("big", False))
        screen.fill(BLACK)
        pygame.display.update()
        time.sleep(1)

    pygame.mixer.music.fadeout(2000)
    time.sleep(2)

    pygame.quit()
    subprocess.run(["python3", "main.py"])  # O usa "python3" según tu entorno
    sys.exit()

# Loop principal
try:
    run_trailer()
except KeyboardInterrupt:
    pygame.quit()
    sys.exit()
