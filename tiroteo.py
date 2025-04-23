import pygame
import random

# Inicializar Pygame
pygame.init()

# Definir dimensiones de la pantalla
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Space Invaders con Personas")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Cargar imágenes
background = pygame.image.load("assets/background_images/1fondo.png")  # Cambia esto con la ruta de tu imagen de fondo
player_img = pygame.image.load("assets/sprites/right0.png")  # Cambia esto con la ruta de tu personaje
bullet_img = pygame.image.load("assets/objects/bala.png")  # Cambia esto con la ruta de tu imagen de bala
enemy_img = pygame.image.load("assets/sprites/left0.png")  # Cambia esto con la ruta de tu imagen de enemigo

# Redimensionar imágenes
player_width, player_height = 50, 50
player_img = pygame.transform.scale(player_img, (player_width, player_height))
enemy_width, enemy_height = 50, 50
enemy_img = pygame.transform.scale(enemy_img, (enemy_width, enemy_height))
bullet_width, bullet_height = 10, 20
bullet_img = pygame.transform.scale(bullet_img, (bullet_width, bullet_height))

# Reloj para controlar la tasa de fotogramas
clock = pygame.time.Clock()

# Variables del jugador
player_x = screen_width // 4
player_y = screen_height - 70
player_speed = 5

# Velocidad de disparo
shoot_delay = 500  # tiempo entre disparos en milisegundos
last_shot_time = pygame.time.get_ticks()

# Listas de enemigos y balas
enemies = []
player_bullets = []
enemy_bullets = []

# Variables para el movimiento suave
player_dx = 0  # Desplazamiento horizontal
player_dy = 0  # Desplazamiento vertical

# Clase de Enemigos
class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = random.randint(2, 5)
        self.is_stopped = False  # Nuevo atributo para detenerse

    def move(self):
        if not self.is_stopped:  # Solo se mueve si no está detenido
            self.y += self.speed

    def stop(self):
        self.is_stopped = True  # Detener el movimiento del enemigo

    def draw(self):
        screen.blit(enemy_img, (self.x, self.y))

    def shoot(self):
        bullet_x = self.x + enemy_width // 2 - bullet_width // 2
        bullet_y = self.y + enemy_height
        enemy_bullets.append(Bullet(bullet_x, bullet_y, "enemy"))

# Clase de Balas
class Bullet:
    def __init__(self, x, y, owner):
        self.x = x
        self.y = y
        self.speed = 7 if owner == "player" else 5
        self.owner = owner

    def move(self):
        if self.owner == "player":
            self.y -= self.speed
        else:  # Balas de enemigo
            self.y += self.speed

    def draw(self):
        screen.blit(bullet_img, (self.x, self.y))

# Función para crear enemigos
def create_enemy():
    x = random.randint(0, screen_width - enemy_width)
    y = random.randint(-150, -50)
    enemies.append(Enemy(x, y))

# Función para manejar los disparos del jugador
def shoot_bullet():
    global last_shot_time
    current_time = pygame.time.get_ticks()
    if current_time - last_shot_time >= shoot_delay:
        x = player_x + player_width // 2 - bullet_width // 2
        y = player_y
        player_bullets.append(Bullet(x, y, "player"))
        last_shot_time = current_time

# Función para verificar colisiones entre balas y enemigos
def check_collisions():
    global enemies, player_bullets
    for bullet in player_bullets:
        for enemy in enemies:
            if (enemy.x < bullet.x < enemy.x + enemy_width and
                    enemy.y < bullet.y < enemy.y + enemy_height):
                enemies.remove(enemy)
                player_bullets.remove(bullet)
                break

# Función para verificar colisiones entre balas del jugador y las balas de los enemigos
def check_bullet_collisions():
    global enemy_bullets
    for bullet in enemy_bullets:
        if bullet.owner == "enemy":
            if bullet.x >= player_x and bullet.x <= player_x + player_width and bullet.y >= player_y and bullet.y <= player_y + player_height:
                print("¡Te han dado!")
                enemy_bullets.remove(bullet)
                break

# Main game loop
running = True
while running:
    screen.fill(BLACK)
    screen.blit(background, (0, 0))  # Dibuja el fondo

    # Capturar eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_dx = -player_speed  # Mover a la izquierda
            elif event.key == pygame.K_RIGHT:
                player_dx = player_speed  # Mover a la derecha
            elif event.key == pygame.K_UP:
                player_dy = -player_speed  # Mover hacia arriba
            elif event.key == pygame.K_DOWN:
                player_dy = player_speed  # Mover hacia abajo
            elif event.key == pygame.K_SPACE:
                shoot_bullet()  # Disparar una bala
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_dx = 0  # Dejar de mover horizontalmente
            elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                player_dy = 0  # Dejar de mover verticalmente

    # Mover el jugador
    player_x += player_dx
    player_y += player_dy

    # Evitar que el jugador se mueva fuera de los límites
    player_x = max(0, min(screen_width - player_width, player_x))
    player_y = max(0, min(screen_height - player_height, player_y))

    # Mover y dibujar balas del jugador
    for bullet in player_bullets:
        bullet.move()
        bullet.draw()
        if bullet.y < 0:
            player_bullets.remove(bullet)

    # Mover y dibujar balas de los enemigos
    for bullet in enemy_bullets:
        bullet.move()
        bullet.draw()
        if bullet.y > screen_height:
            enemy_bullets.remove(bullet)

    # Mover y dibujar enemigos
    for enemy in enemies:
        # Detener a los enemigos cuando lleguen al 1/4 de la pantalla
        if enemy.y >= screen_height // 4 and not enemy.is_stopped:
            enemy.stop()  # Detener el enemigo
        enemy.move()
        enemy.draw()
        if enemy.y > screen_height:
            enemies.remove(enemy)
        # Los enemigos disparan con una probabilidad
        if random.random() < 0.01:  # Menos enemigos, menor probabilidad de disparo
            enemy.shoot()

    # Verificar colisiones entre balas del jugador y enemigos
    check_collisions()

    # Verificar colisiones entre balas de los enemigos y el jugador
    check_bullet_collisions()

    # Dibujar el jugador
    screen.blit(player_img, (player_x, player_y))

    # Crear nuevos enemigos con menos probabilidad
    if random.random() < 0.01:  # Probabilidad reducida para crear enemigos
        create_enemy()

    # Actualizar pantalla
    pygame.display.update()

    # Controlar la velocidad de los fotogramas
    clock.tick(60)

pygame.quit()
