import pygame
import sys
import subprocess

# Inicializamos pygame
pygame.init()

# Inicializar el mezclador de sonido
pygame.mixer.init()

# Cargar la canción (debe estar en la carpeta del proyecto o indicar la ruta completa)
pygame.mixer.music.load("assets/music/vaquilla_intro.mp3")  # Reemplaza con la ruta correcta

# Ajustar volumen (opcional, valor entre 0.0 y 1.0)
pygame.mixer.music.set_volume(1)

# Reproducir la música en bucle infinito (-1)
pygame.mixer.music.play(-1)


# Definimos el tamaño de la pantalla y otras variables
SCREEN_WIDTH, SCREEN_HEIGHT = 1366, 768  # Dimensiones de la pantalla
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # Crear pantalla
pygame.display.set_caption("Torrente Vice Main")  # Título de la ventana

# Colores definidos en RGB
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (200, 0, 0)
AMARILLO_TITULO = (215, 150, 0)
AMARILLO_SUBSTITULO = (198, 119, 0)

# Cargar la imagen de inicio
start_image = pygame.image.load('assets/background_images/1fondo.png')
start_image = pygame.transform.scale(start_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Cargar la imagen de fondo del menú
background_image = pygame.image.load('assets/background_images/1fondo.png')
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Fuentes para los textos del menú
titulo_font = pygame.font.SysFont("georgia", 74, bold=True)  # Fuente para el título
font_entrar = pygame.font.SysFont("arial", 50)  # Fuente para el texto de "Presiona Enter"
subtitulo_font = pygame.font.SysFont("arial", 50, bold=True)  # Fuente para subtítulos
menu_font = pygame.font.Font(None, 74)  # Fuente para el menú
credits_font = pygame.font.SysFont("georgia", 50)  # Fuente para los créditos

# Cargar la imagen de créditos
credits_image = pygame.image.load('assets/background_images/1fondo.png')
credits_image = pygame.transform.scale(credits_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Texto de créditos
credits_text = [
    "Desarrollado por: Institut Antoni Ballester",
    "Programación: Edgar Pedret y Javier Jaca",
    "Arte: Kristopher Gonzalez",
    "Música: El Fary, Los Chichos",
    "Guión: Kristopher Gonzalez, Javier Jaca y Edgar Pedret",
    "Gracias por jugar a nuestro juego, esperemos que hayas disfrutado!!!"
]


# Función para mostrar la pantalla con la sinopsis del juego
def show_sinopsis_screen():
    screen.fill(NEGRO)  # Fondo negro para la pantalla de sinopsis

    # Sinopsis del juego
    story_text = [
        "Era se una vez Torrente, orgulloso agente de la policía local de ",
        "Miami Platja, pasó de hacer rondas a hacer el ridículo en 2018, cuando lo ",
        "encontraron patrullando borracho como una cuba. Pero no estaba ",
        "solo. Lo acompañaban unos chavales de 12 años a los que, en un ",
        "acto de genialidad suprema, les dejó su pistola reglamentaria para ",
        "que “no le molestaran mientras intentaba dormir en un banco ",
        "delante del colegio”. Como si fuera poco, intentó venderles ",
        "cocaína y éxtasis asegurando que eran caramelos Sugus. Desde ",
        "entonces, la justicia, los medios y su propia madre lo conocen ",
        "como “El Brazo Tonto de la Ley”. Ahora se dedica a trabajar ",
        "por libre en los peores lugares de la ciudad."
    ]

    # Fuente para el texto de la historia
    sinopsis_font = pygame.font.SysFont("timesnewroman", 30)

    y_offset = SCREEN_HEIGHT // 2 - 250  # Iniciar en el centro vertical
    for line in story_text:
        text = sinopsis_font.render(line, True, BLANCO)
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, y_offset))
        y_offset += 40  # Espaciado entre líneas

    # Mostrar "Presiona Enter para continuar"
    continue_text = pygame.font.SysFont("arial", 40).render("Presiona Enter para continuar", True, BLANCO)
    screen.blit(continue_text, (SCREEN_WIDTH // 2 - continue_text.get_width() // 2, SCREEN_HEIGHT - 100))

    pygame.display.flip()

    # Esperar que el jugador presione Enter para continuar
    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting_for_input = False  # Salir de la pantalla de historia


# Función para mostrar la pantalla de inicio
def show_start_screen():
    while True:
        screen.blit(start_image, (0, 0))  # Mostrar imagen de inicio


        # Relieve hacia abajo
        text = font_entrar.render("Presiona Enter para empezar", True, (0, 0, 0))
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT - 98))
        # Relieve hacia derecha
        text = font_entrar.render("Presiona Enter para empezar", True, (0, 0, 0))
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2 + 3, SCREEN_HEIGHT - 100))
        # Mostrar el mensaje "Presiona Enter para empezar"
        text = font_entrar.render("Presiona Enter para empezar", True, BLANCO)
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT - 100))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return  # Salir de la pantalla de inicio


# Función para mostrar el menú
def show_menu():
    screen.blit(background_image, (0, 0))  # Fondo del menú
    # Mostrar opciones
    options = ["1 - Jugar", "2 - Creditos", "3 - Salir"]
    for i, option in enumerate(options):
        option_text = menu_font.render(option, True, BLANCO)
        screen.blit(option_text, (SCREEN_WIDTH // 8 - option_text.get_width() // 30, 350 + i * 100))

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
            # Relieve hacia derecha
            text = credits_font.render(line, True, (30, 30, 30))
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2 + 2, y_offset + i * 60))
            # Izquierda relieve
            text = credits_font.render(line, True, (200, 200, 200))
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2 - 2, y_offset + i * 60))
            # Relieve hacia arriba
            text = credits_font.render(line, True, (0, 0, 0))
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, y_offset + i * 60 - 2))
            # Credito
            text = credits_font.render(line, True, BLANCO)
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, y_offset + i * 60))

        y_offset -= 2  # Movimiento hacia arriba

        pygame.display.flip()
        pygame.time.delay(30)  # Pequeño retraso para el efecto de scroll


# Función principal
def main():
    show_start_screen()  # Muestra la pantalla de inicio antes del menú
    show_sinopsis_screen()  # Muestra la sinopsis antes del menú
    while True:
        show_menu()  # Mostrar menú siempre

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    print("Cargando juego...")  # Aquí iría la lógica del juego
                    pygame.quit()
                    subprocess.run([sys.executable, "movement.py"]) # El sys.executable es perque utilitzi la mateixxa versió de python que el codi actual de main
                    sys.exit()
                elif event.key == pygame.K_2:
                    show_credits()  # Mostrar créditos
                elif event.key == pygame.K_3:
                    pygame.quit()
                    sys.exit()


if __name__ == "__main__":
    main()

