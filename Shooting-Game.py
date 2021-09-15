import math
import random
import pygame
from pygame import mixer
# Intialize the pygame
pygame.init()
# Create the screen
screen = pygame.display.set_mode((800, 1500))
# Background
background = pygame.image.load("background.png")
#Background Sound
mixer.music.load("background.wav")
mixer.music.play(-1)
# Caption and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)
# Player
playerImg = pygame.image.load("player.png")
playerX = 1500
playerY = 500
playerX_change = 0
# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 10


for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load("Enemy.png"))
    enemyX.append(random.randint(0, 800))
    enemyY.append(random.randint(50, 300))
    enemyX_change.append(2)
    enemyY_change .append(40)

# Bullet
bulletImg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

#Font
score_value = 0
font = pygame.font.Font("freesansbold.ttf", 32)

textX = 10
testY = 10
#Game over text
over_font = pygame.font.Font("freesansbold.ttf", 64)

def show_score(x, y):
    score = font.render("Score :" + str(score_value), True, (255, 0, 0))
    screen.blit(score, (x, y))
def game_over_text(x, y):
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))
def player(x, y):
    screen.blit(playerImg, (x, y))


def Enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))

def isCollision(enemyX,enemyY,bulletX,bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY,2)))
    if distance < 27:
        return True
    else:
        return False
# Game loop
running = True
while running:
    screen.fill((0, 0, 0))
    # Background image
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # if key stroke is pressed check weather it is right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                playerX_change = -2
            if event.key == pygame.K_p:
                playerX_change = 2
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_Sound = mixer.Sound("laser.wav")
                    bullet_Sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)



        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
    # Checking for boundaries of space ship so it is dosn't go out of bounds
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736
    # Enemy Movement
    for i in range(num_of_enemies):
        #Game over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text(220, 250)
            break


        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 2
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -2
            enemyY[i] += enemyY_change[i]
        #Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_Sound = mixer.Sound("explosion.wav")
            explosion_Sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)


        Enemy(enemyX[i], enemyY[i], i)


    #Bullet Movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, testY)
    pygame.display.update()
