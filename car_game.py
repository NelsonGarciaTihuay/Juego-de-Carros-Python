import pygame
from pygame.locals import *
import random

# Inicializar Pygame
pygame.init()

# Configuracion de la ventana 
width = 500
height = 600
screen_size = (width, height)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption('Juego de Carreras con Obstáculos')

# colores de la pista
gray = (100, 100, 100)
green = (76, 208, 56)
red = (200, 0, 0)
white = (255, 255, 255)
yellow = (255, 232, 0)

# tamaños de carreteras y marcadores
road_width = 300
marker_width = 10
marker_height = 50

# coordenadas del carril
left_lane = 150
center_lane = 250
right_lane = 350
lanes = [left_lane, center_lane, right_lane]

# marcadores de caminos y bordes
road = (100, 0, road_width, height)
left_edge_marker = (95, 0, marker_width, height)
right_edge_marker = (395, 0, marker_width, height)

# animar el movimiento de los marcadores de carril
lane_marker_move_y = 0

# coordenadas iniciales del jugador
player_x = 250
player_y = 400

# FPS
clock = pygame.time.Clock()
fps = 60

# Configuracion del juegp
gameover = False
speed = 2
score = 0

# Clase para el Vehículo
class Vehicle(pygame.sprite.Sprite):
    
    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)
        
        # Ancho del carril
        image_scale = 45 / image.get_rect().width
        new_width = image.get_rect().width * image_scale
        new_height = image.get_rect().height * image_scale
        self.image = pygame.transform.scale(image, (new_width, new_height))
        
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

     

# vehiculo principal 
class PlayerVehicle(Vehicle):
    
    def __init__(self, x, y):
        image = pygame.image.load('images/car.png')
        super().__init__(image, x, y)

        
# grupos de sprites
player_group = pygame.sprite.Group()
vehicle_group = pygame.sprite.Group()

# auto del jugador
player = PlayerVehicle(player_x, player_y)
player_group.add(player)

# imagenes de los vehiculos xd
image_filenames = ['pickup_truck.png', 'semi_trailer.png', 'taxi.png', 'van.png']
vehicle_images = []
for image_filename in image_filenames:
    image = pygame.image.load('images/' + image_filename)
    vehicle_images.append(image)
    
# imagen de la explocion 
crash = pygame.image.load('images/crash.png')
crash_rect = crash.get_rect()

# bucle del juego
running = True
while running:
    
    clock.tick(fps)
    
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
            
        # asignacion de teclas 
        if event.type == KEYDOWN:
            
            if event.key == K_LEFT and player.rect.center[0] > left_lane:
                player.rect.x -= 100
            elif event.key == K_RIGHT and player.rect.center[0] < right_lane:
                player.rect.x += 100
                
            # comprobar si hay una colisión lateral después de cambiar de carril
            for vehicle in vehicle_group:
                if pygame.sprite.collide_rect(player, vehicle):
                    
                    gameover = True
                    
                    # coloca el auto del jugador al lado de otro vehículo
                    # y determine dónde colocar la imagen del accidente
                    if event.key == K_LEFT:
                        player.rect.left = vehicle.rect.right
                        crash_rect.center = [player.rect.left, (player.rect.center[1] + vehicle.rect.center[1]) / 2]
                    elif event.key == K_RIGHT:
                        player.rect.right = vehicle.rect.left
                        crash_rect.center = [player.rect.right, (player.rect.center[1] + vehicle.rect.center[1]) / 2]
            
            
    # dibujar la hierba
    screen.fill(green)
    
    # dibuja el camino
    pygame.draw.rect(screen, gray, road)
    
    # dibujar los marcadores de borde
    pygame.draw.rect(screen, yellow, left_edge_marker)
    pygame.draw.rect(screen, yellow, right_edge_marker)
    
    # dibujar los marcadores de carril
    lane_marker_move_y += speed * 2
    if lane_marker_move_y >= marker_height * 2:
        lane_marker_move_y = 0
    for y in range(marker_height * -2, height, marker_height * 2):
        pygame.draw.rect(screen, white, (left_lane + 45, y + lane_marker_move_y, marker_width, marker_height))
        pygame.draw.rect(screen, white, (center_lane + 45, y + lane_marker_move_y, marker_width, marker_height))
        
    # dibuja el auto del jugador
    player_group.draw(screen)
    
    # añadir vehiculo
    if len(vehicle_group) < 2:
        
        # espacio entre los vehículos.
        add_vehicle = True
        for vehicle in vehicle_group:
            if vehicle.rect.top < vehicle.rect.height * 1.5:
                add_vehicle = False
                
        if add_vehicle:
            
            # seleccione un carril aleatorio
            lane = random.choice(lanes)
            
            # seleccione una imagen de vehículo aleatoria
            image = random.choice(vehicle_images)
            vehicle = Vehicle(image, lane, height / -2)
            vehicle_group.add(vehicle)
    
    # hacer que los vehículos se muevan
    for vehicle in vehicle_group:
        vehicle.rect.y += speed
        
        # eliminar el vehículo una vez que salga de la pantalla
        if vehicle.rect.top >= height:
            vehicle.kill()
            
            # añadir puntuación
            score += 1
            
            # acelera el juego después de pasar 3 vehículos
            if score > 0 and score % 3 == 0:
                speed += 1
    
    # dibujar el vehiculo
    vehicle_group.draw(screen)
    
    # mostrar la puntuación
    font = pygame.font.Font(pygame.font.get_default_font(), 16)
    text = font.render('Puntaje: ' + str(score), True, red)
    text_rect = text.get_rect()
    text_rect.center = (50, 400)
    screen.blit(text, text_rect)
    
    # comprobar si hay una colisión frontal
    if pygame.sprite.spritecollide(player, vehicle_group, True):
        gameover = True
        crash_rect.center = [player.rect.center[0], player.rect.top]
            
    sound = pygame.mixer.Sound("explocion.mp3")

    # mostrar game over
    if gameover:
        screen.blit(crash, crash_rect)
        
        pygame.draw.rect(screen, red, (0, 50, width, 100))
        
        font = pygame.font.Font(pygame.font.get_default_font(), 16)
        text = font.render('Game over. Jugar de nuevo? (Precione S o N)', True, white)
        text_rect = text.get_rect()
        text_rect.center = (width / 2, 100)
        screen.blit(text, text_rect)
        sound.play()
            
    pygame.display.update()

    # esperar la eleccion del jugador
    while gameover:
        
        clock.tick(fps)
        
        for event in pygame.event.get():
            
            if event.type == QUIT:
                gameover = False
                running = False
                
            # Precionar la tecla S o N
            if event.type == KEYDOWN:
                if event.key == K_s:
                    # Reinicar juego
                    gameover = False
                    speed = 2
                    score = 0
                    vehicle_group.empty()
                    player.rect.center = [player_x, player_y]
                elif event.key == K_n:
                    # Salir del juego
                    gameover = False
                    running = False

pygame.quit()