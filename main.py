import pygame
import math
import random

pygame.init()

# Configuramos la resolucion de la pantalla
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Ping Pong")

class Player:
    def __init__(self, y, x):
        self.y = y
        self.x = x
        self.y_change = 0

    def draw(self):
        pygame.draw.rect(screen, (255, 255, 255), (self.x, self.y,20, 100))
    
    def move(self):
        # Actualizar la posicion
        self.y += self.y_change
        # Limitar el moviento dentro de los limites de la pantalla
        if self.y <= 0:
            self.y = 0
        elif self.y >= 500: # 800 - ancho del personaje 64 px
            self.y = 500
    
    def reset_posision(self, y, x):
            self.y = y
            self.x = x

class Pelota:
    def __init__(self, speed):
        self.y = 300
        self.x = 400
        self.y_change = speed
        self.x_change = speed

    def draw(self):
        pygame.draw.rect(screen, (255, 255, 0), (self.x, self.y,20, 20))

    def move(self):
        self.x += self.x_change
        self.y += self.y_change
        # Cambiar de direccion
        if self.x <= 0 or self.x >= 780:
            self.x_change *= -1 # Cambio de direcion opuesta
        elif self.y <= 0 or self.y >= 580:
            self.y_change *= -1 # Cambio de direcion opuesta
    
    def reset_posision(self):
            self.x = 400
            self.y = 300
            self.x_change = speed
            self.y_change = speed


def es_colision(player_x, player_y, pelota_x, pelota_y):
    distancia = math.sqrt(math.pow((player_x - pelota_x), 2) + math.pow((player_y - pelota_y), 2)) # Distancia entre dos puntos
    return distancia <= 50 # Valor fijo de la distancia maxima o lo suficientemente cerca para considerarlo una colision

def game_over_text_1():
    victoria_text = victory_font.render("VICTORIA!" , True ,(0,204,0))
    screen.blit(victoria_text,(150,100))
    over_text = player_font.render("Jugador 1" , True ,(0,204,0))
    screen.blit(over_text,(255,250))

def game_over_text_2():
    victoria_text = victory_font.render("VICTORIA!" , True ,(0,204,0))
    screen.blit(victoria_text,(150,100))
    over_text = player_font.render("Jugador 2" , True ,(0,204,0))
    screen.blit(over_text,(255,250))



# Puntuacion inicial , fuente y victoria
score1 = 0
score2 = 0
font = pygame.font.Font(None, 150)
player_font = pygame.font.Font(None,64)
victory_font = pygame.font.Font(None,126)
# Creo el jugador
player1 = Player(280, 100)
player2 = Player(280, 700)
# Creo la pelota
speed = 0.5
pelota = Pelota(speed)

running = True
while running:
    screen.fill((0, 0, 0)) #Fondo Negro 

    if score1 == 10:
        game_over_text_1()
        pygame.display.flip()
        pygame.time.delay(3000)
        running = False
    elif score2 == 10:
        game_over_text_2()
        pygame.display.flip()
        pygame.time.delay(3000)
        running = False
    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
    # Detectar si se presiona una tecla
        if event.type == pygame.KEYDOWN: # Solo teclas
            if event.key == pygame.K_w:
                player1.y_change = -1 # Valor de velocidad
            elif event.key == pygame.K_s:
                player1.y_change = 1 # Velocidad de jugador
            elif event.key == pygame.K_UP:
                player2.y_change = -1 # Valor de velocidad
            elif event.key == pygame.K_DOWN:
                player2.y_change = 1 # Velocidad de jugador
            elif event.key == pygame.K_r:
                score1 = 0
                score2 = 0
                speed = 0.5
                pelota.reset_posision()
                player1.reset_posision(280, 100)
                player2.reset_posision(280, 700)

        # Detectar si se suelta la tecla
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w or event.key == pygame.K_s:
                player1.y_change = 0
            elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                player2.y_change = 0
        
    #Mover y dibujar el jugador 1
    player1.move()
    player1.draw()
    #Mover y dibujar el jugador 2
    player2.move()
    player2.draw()
    #Dibujar Pelota
    pelota.move()
    pelota.draw()

    if es_colision(pelota.x, pelota.y, player1.x -5, player1.y + 40) or es_colision(pelota.x, pelota.y, player2.x -5 , player2.y + 40):
        pelota.x_change *= -1  # Cambiar la dirección en el eje X

    if not es_colision(pelota.x, pelota.y, player1.x, player1.y):
        if pelota.x < 90:
            score2 +=1
            if score1 % 2 == 0:
                speed += 0.2
            pelota.reset_posision()
    if not es_colision(pelota.x, pelota.y, player2.x, player2.y):
        if pelota.x > 710:
            score1 += 1
            if score2 % 2 == 0:
                speed += 0.1
            pelota.reset_posision()
    print(speed)
    # Mostar la puntuacion en pantalla
    score_text1 = font.render(f"{score1}", True, (255, 255, 255))
    screen.blit(score_text1, (10, 10))
    score_text2 = font.render(f"{score2}", True, (255, 255, 255))
    screen.blit(score_text2, (676, 10))
    print(score1)
    print(score2)


    pygame.display.flip()
pygame.quit()