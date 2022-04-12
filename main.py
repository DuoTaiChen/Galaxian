import pygame
import random
import math
from pygame import mixer

pygame.init()

# Crate screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load("background.jpg")

# Background Sound
mixer.music.load('background.wav')
mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption("Space Invader")
icon = pygame.image.load('dragonman.png')
pygame.display.set_icon(icon)

# Player
playerIMG = pygame.image.load('space-invaders.png')
playerX = 370
playerY = 520
playerX_change = 0
speed: float = 0.6
directR = False
directL = False

# Enemy
enemyIMG = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemy = 6

# Score

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

# Game Over text
over_font = pygame.font.Font('freesansbold.ttf', 64)


def show_score(x, y):
    score = font.render("Score :" + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("Game Over", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


for i in range(num_of_enemy):
    enemyIMG.append(pygame.image.load('alien.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(0.5)
    enemyY_change.append(40)

# Bullet

# Ready - You can't the bullet on the screen
# Fire - The bullet is moving
bulletIMG = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 520
bulletX_change = 0
bulletY_change = 1.6
bullet_state = "ready"


def player(x, y):
    screen.blit(playerIMG, (x, y))


def enemy(x, y, i):
    screen.blit(enemyIMG[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletIMG, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(
        math.pow(
            enemyX -
            bulletX,
            2) +
        math.pow(
            enemyY -
            bulletY,
            2))
    if distance < 27:
        return True
    else:
        return False


# Game loop
running = True
while running:

    # R G B
    screen.fill((255, 255, 255))
    # Background Image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                directL = True
            if event.key == pygame.K_RIGHT:
                directR = True
            if event.key == pygame.K_SPACE and bullet_state == "ready":
                bullet_Sound = mixer.Sound('laser.wav')
                bullet_Sound.play()
                bulletX = playerX
                fire_bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                directL = False
            if event.key == pygame.K_RIGHT:
                directR = False

    if directL and directR:
        playerX_change = 0
    elif directL:
        playerX_change = -speed
    elif directR:
        playerX_change = speed
    else:
        playerX_change = 0

    # Checking fo boundaries of spaceship
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy movements
    for i in range(num_of_enemy):

        # Game Over
        if enemyY[i] > 400:
            for j in range(num_of_enemy):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]

        if enemyX[i] <= 0:
            enemyX_change[i] = 0.5
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -0.5
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_Sound = mixer.Sound('explosion.wav')
            explosion_Sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # Bullet movements
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change
        if bulletY <= 0:
            bullet_state = "ready"
            bulletY = playerY

    # Refresh screen
    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
