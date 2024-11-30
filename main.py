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
            cambio_random = random.randint(-1, 1)
            self.x = 400
            self.y = 300
            if cambio_random == 0:
                cambio_random = random.randint(-1, 1)
            else:
                if cambio_random == -1:
                    self.x_change = -0.7
                    self.y_change = -0.7
                else:
                    self.x_change = 0.7
                    self.y_change = 0.7



def es_colision(player_x, player_y, pelota_x, pelota_y):
    #distancia = math.sqrt(math.pow((player_x - pelota_x), 2) + math.pow((player_y - pelota_y), 2)) # Distancia entre dos puntos
    #return distancia <= 50 # Valor fijo de la distancia maxima o lo suficientemente cerca para considerarlo una colision

    # Comprobar si la pelota está dentro del área de la paleta en X y Y
    if player_x < pelota_x + 20 < player_x + 20 and player_y < pelota_y + 20 < player_y + 100:
        return True
    return False

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



# Fondo del juego.
fondo = pygame.image.load("fondo.png")
# Puntuacion inicial , fuente y victoria
score1 = 0
score2 = 0
font = pygame.font.Font(None, 150)
player_font = pygame.font.Font(None, 64)
victory_font = pygame.font.Font(None, 126)
# Creo el jugador
player1 = Player(280, 100)
player2 = Player(280, 700)
# Creo la pelota
speed = 0.7
pelota = Pelota(speed)
# Cargar Sonidos
punto = pygame.mixer.Sound("punto.mp3")
raqueta = pygame.mixer.Sound("raqueta.mp3")
victoria = pygame.mixer.Sound("victoria.mp3")

running = True
while running:
    screen.blit(fondo, (0, 0)) #Fondo Negro 

    if score1 == 10:
        pygame.mixer.Sound.play(victoria)
        game_over_text_1()
        pygame.display.flip()
        pygame.time.delay(3000)
        running = False
    elif score2 == 10:
        pygame.mixer.Sound.play(victoria)
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

    if es_colision(player1.x, player1.y, pelota.x, pelota.y):
        pygame.mixer.Sound.play(raqueta)
    # Si la pelota colisiona con la paleta del jugador 1
        if pelota.y > player1.y and pelota.y < player1.y + 100:  # Golpeó la paleta
        # Calcular la diferencia de posición con el centro de la paleta
            medio_paleta = (pelota.y - (player1.y + 50)) / 50  # 50 es el centro de la paleta
            pelota.x_change *= -1  # Invertir la dirección en X
            pelota.y_change += medio_paleta * 0.5  # Ajustar la dirección en Y, según dónde golpeó la paleta
        # Asegurarse de que la pelota no se mueva dentro de la paleta
        if pelota.x <= player1.x + 20:
            pelota.x = player1.x + 20  # Evitar que la pelota quede "pegada" al borde de la paleta

    if es_colision(player2.x, player2.y, pelota.x, pelota.y):
        pygame.mixer.Sound.play(raqueta)
    # Si la pelota colisiona con la paleta del jugador 2
        if pelota.y > player2.y and pelota.y < player2.y + 100:  # Golpeó la paleta
        # Calcular la diferencia de posición con el centro de la paleta
            medio_paleta = (pelota.y - (player2.y + 50)) / 50  # 50 es el centro de la paleta
            pelota.x_change *= -1  # Invertir la dirección en X
            pelota.y_change += medio_paleta *0.5  # Ajustar la dirección en Y, según dónde golpeó la paleta
        # Asegurarse de que la pelota no se mueva dentro de la paleta
        if pelota.x >= player2.x - 20:
            pelota.x = player2.x - 20  # Evitar que la pelota quede "pegada" al borde de la paleta

    if not es_colision(pelota.x, pelota.y, player1.x, player1.y):
        if pelota.x < 90:
            pygame.mixer.Sound.play(punto)
            score2 +=1
            pelota.reset_posision()
    if not es_colision(pelota.x, pelota.y, player2.x, player2.y):
        if pelota.x > 710:
            pygame.mixer.Sound.play(punto)
            score1 += 1
            pelota.reset_posision()
    print(pelota.x_change)
    print(pelota.y_change)
    # Mostar la puntuacion en pantalla
    score_text1 = font.render(f"{score1}", True, (255, 255, 255))
    screen.blit(score_text1, (85, 10))
    score_text2 = font.render(f"{score2}", True, (255, 255, 255))
    screen.blit(score_text2, (676, 10))


    pygame.display.flip()
pygame.quit()