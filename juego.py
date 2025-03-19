import pygame
import sys

# Inicializar Pygame
pygame.init()

# Definir dimensiones de la ventana
width, height = 800, 600
screen = pygame.display.set_mode((width, height))

# Cargar la imagen de fondo
fondo = pygame.image.load("1.png")

# Ajustar la imagen al tamaño de la ventana
fondo = pygame.transform.scale(fondo, (width, height))

# Bucle principal del juego
running = True
while running:
    # Revisar eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Dibujar el fondo en la pantalla
    screen.blit(fondo, (0, 0))

    # Actualizar la pantalla
    pygame.display.flip()

# Salir de Pygame
pygame.quit()
sys.exit()
