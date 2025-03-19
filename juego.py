import pygame
import sys

# Inicializamos pygame
pygame.init()

# Definimos el tamaño de la pantalla y otras variables
SCREEN_WIDTH, SCREEN_HEIGHT = 1366, 768
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Menú Torrente Vice")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)

# Cargamos la imagen de fondo del menú
background_image = pygame.image.load('assets/images.jpeg')
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Fuente para los textos del menú
font = pygame.font.Font(None, 74)
credits_font = pygame.font.Font(None, 50)

# Imagen de créditos
credits_image = pygame.image.load('assets/images.jpeg')
credits_image = pygame.transform.scale(credits_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Texto de créditos
credits_text = [
    "Desarrollado por: Equipo Torrente Vice",
    "Programación: Juan Pérez",
    "Arte: María López",
    "Música: Carlos Sánchez",
    "Año: 2025",
    "Gracias por jugar!"
]


# Función para mostrar el menú
def show_menu():
    screen.blit(background_image, (0, 0))  # Fondo del menú

    # Mostrar el título
    title_text = font.render("Menú Principal", True, WHITE)
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 150))

    # Mostrar opciones
    options = ["1 - Jugar", "2 - Salir", "3 - Créditos"]
    for i, option in enumerate(options):
        option_text = font.render(option, True, WHITE)
        screen.blit(option_text, (SCREEN_WIDTH // 2 - option_text.get_width() // 2, 350 + i * 100))

    pygame.display.flip()


# Función para mostrar los créditos
def show_credits():
    screen.blit(credits_image, (0, 0))  # Fondo de créditos
    y_offset = SCREEN_HEIGHT  # Comienza fuera de la pantalla

    running = True
    while running:
        screen.blit(credits_image, (0, 0))  # Volvemos a poner la imagen de fondo

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Salir de los créditos con ESC
                    running = False

        # Dibujar cada línea de créditos con desplazamiento
        for i, line in enumerate(credits_text):
            text = credits_font.render(line, True, WHITE)
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, y_offset + i * 60))

        y_offset -= 2  # Movimiento hacia arriba

        pygame.display.flip()
        pygame.time.delay(30)  # Pequeño retraso para el efecto de scroll


# Función principal
def main():
    while True:
        show_menu()  # Mostrar menú siempre

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    print("Cargando juego...")  # Aquí iría la lógica del juego
                elif event.key == pygame.K_2:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_3:
                    show_credits()  # Mostrar créditos


if __name__ == "__main__":
    main()
