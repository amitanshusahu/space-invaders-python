import pygame
import random
import math
from pygame import mixer
pygame.init()

#screen 
screen = pygame.display.set_mode() 
pygame.display.set_caption("Space Invader - mission to save earth")

#screen size
screenX , screenY = screen.get_size()

#background image
bgimg = "./img/bg1.jpg"
background = pygame.image.load(bgimg)

#background music
mixer.music.load("./audio/bgm2.wav")
mixer.music.play(-1)

#player
playerImg = pygame.image.load('./img/spaceship1.png')
playerImgHight = playerImg.get_height()
playerImgWidth = playerImg.get_width()
playerX = (screenX / 2) - playerImgWidth
playerY = screenY-(playerImgHight * 2)
playerSpeed = (1/200) * screenX
playerX_change = 0

def player(playerX , playerY):
    screen.blit(playerImg , (playerX , playerY))

#enemy 
enemyImg = []
enemyImgHeight = []
enemyImgwidth = []
enemyX_position = []
enemyY_position = []
enemyX = []
enemyY = []
enemySpeed = []
enemyX_change = []
num_of_enemy = 6
for i in range(num_of_enemy):
    enemyImg.append(pygame.image.load('./img/ufo1.png'))
    enemyImgHeight.append(enemyImg[i].get_height())
    enemyImgwidth.append(enemyImg[i].get_width())
    enemyX_position.append(screenX - enemyImgwidth[i])
    enemyY_position.append(screenY - enemyImgHeight[i])
    enemyX.append(random.randint(0,enemyX_position[i]-30))
    enemyY.append(random.randint(0,int(enemyY_position[i]/2)))
    enemySpeed.append(int((1/400) * screenX))
    enemyX_change.append(enemySpeed[i])

def enemy(enemyX , enemyY , i):
    screen.blit(enemyImg[i] , (enemyX,enemyY))

#bullet
bulletImg = pygame.image.load('./img/bullet1.png')
bulletX = (screenX / 2) - playerImgWidth
bulletY = screenY-(playerImgHight * 2)
bulletSpeed = int((1/200) * screenX)
bulletY_change = bulletSpeed;
bulletSound = "./audio/bullet2.wav"
isfire = False
def fire(bulletX , bulletY):
    global isfire
    isfire = True
    screen.blit(bulletImg , (bulletX+(playerImgHight/2)-15, bulletY-(10)))

#bullet number
isOnce2 = True
isOnce4 = True
isOnce6 = True
isOnce8 = True
isOnce10 = True
isOnce12 = True
isOnce14 = True
bullet_number = 3
bulletFont = pygame.font.Font("freesansbold.ttf", 32)
def show_bullet():
    bullet_num = bulletFont.render("X" + str(bullet_number), True, (255, 255, 255))
    screen.blit(bullet_num , (200, 20))

#collision
def iscollision(enemyX,enemyY,bulletX,bulletY , i):
    distance = math.sqrt((math.pow(enemyX-bulletX , 2)) + (math.pow(enemyY-bulletY , 2)))
    if distance < (enemyImgwidth[i]/2):
        return True
    return False

#score
score_value = 0
scoreFont = pygame.font.Font('freesansbold.ttf' , 30)
def show_score(scoreX, scoreY):
    score = scoreFont.render("Score: " + str(score_value) , True , (255,255,255))
    screen.blit(score, (scoreX, scoreY))

#level
level_count = 0
levelFont = pygame.font.Font('freesansbold.ttf' , 30)
def show_level(levelX, levelY):
    level = levelFont.render("Level: " + str(level_count) , True , (255,255,255))
    screen.blit(level, (levelX, levelY))

#game over
def game_over():
    gameOverFont = pygame.font.Font("freesansbold.ttf" , 50)
    gameOver = gameOverFont.render("Mission Fail", True , (255 , 255, 255) )
    tab = gameOverFont.render("tab to restart" , True , (255, 255, 255))
    screen.blit(gameOver , ((screenX/2)-150 , screenY/3))
    screen.blit(tab , ((screenX/2)-170 , (screenY/3)+80))

isWarning = True

#game loop
exit = False
while not exit:
     #fill screen color
    screen.fill((0,0,0))

    #use background image
    screen.blit(background , (0,0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit = True
    
    #key events
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
            playerX_change = 0 - playerSpeed
        if event.key == pygame.K_RIGHT:
            playerX_change = playerSpeed
        if event.key == pygame.K_UP:
            if not isfire:
                bulletX = playerX
                fire(bulletX , bulletY)
                fireSound = mixer.Sound(bulletSound)
                fireSound.play()
                bullet_number -= 1
                if score_value > 0:
                    level_count = int(score_value/2)
    if event.type == pygame.KEYUP:
        playerX_change = 0

    #movement restriction of player
    playerX += playerX_change
    if playerX <= (0-playerImgWidth):
        playerX= screenX-playerImgWidth
    if playerX >= screenX:
        playerX = 0 - playerImgWidth

    #player
    player(playerX,playerY)

    #movement of enemy automatic
    for i in range(num_of_enemy):
        #warning
        if enemyY[i] > (screenY-(playerImgHight* 3)) and isWarning:
            alrmsound = mixer.Sound("./audio/alram.wav")
            alrmsound.play()
            bgimg = "./img/bg2.jpg"
            background = pygame.image.load(bgimg)
            isWarning = False

        #game over
        if enemyY[i] > ((screenY-(playerImgHight* 2)-enemyImgHeight[i]/2)) or bullet_number < 0:
            for i in range(num_of_enemy):
                enemyY[i] = screenY+(enemyImgHeight[i]*2)
            game_over()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = enemySpeed[i]
            enemyY[i] += enemyImgHeight[i]
        if enemyX[i] >= (screenX-(enemyImgwidth[i] + 30)):
            enemyX_change[i] = 0 - enemySpeed[i]
            enemyY[i] += enemyImgHeight[i]

        #check collision
        collision = iscollision(enemyX[i],enemyY[i],bulletX,bulletY,i)
        if collision:
            bulletY = screenY-(playerImgHight * 2)
            isfire = False
            score_value += 1
            enemyX[i] = random.randint(0,enemyX_position[i]-30);
            enemyY[i] = random.randint(0,int(enemyY_position[i]/2))
            collisionSound = mixer.Sound("./audio/explosion.wav")
            collisionSound.play()
            isWarning = True
            if bullet_number < 3:
                bullet_number += 1

        #enemy
        enemy(enemyX[i], enemyY[i], i)

        # --- level logic ----
        # level 2
        if level_count == 2 and isOnce2:
            enemySpeed[i-1] += 1
            isOnce2 = False
        # level 4
        elif level_count == 4 and isOnce4:
            levelSound = mixer.Sound('./audio/new-level.wav')
            levelSound.play()
            enemySpeed[i] += 2
            enemyImg[i] = pygame.image.load("./img/ufo2.png")
            playerImg = pygame.image.load("./img/spaceship2.png")
            bulletY_change += 5
            bullet_number = 3
            bulletSound = "./audio/bullet1.wav"
            bulletImg = pygame.image.load('./img/bullet2.png')
            isOnce4 = False
        #level 6
        elif level_count == 6 and isOnce6:
            enemyImg[i+1] = pygame.image.load("./img/ufo2.png")
            enemySpeed[i+1] += 2
            isOnce6 = False
        #level 8
        elif level_count == 8 and isOnce8:
            levelSound = mixer.Sound('./audio/new-level.wav')
            levelSound.play()
            if i < num_of_enemy-2:
                enemySpeed[i+2] += 3
                enemyImg[i+2] = pygame.image.load("./img/ufo3.png")
            elif i > 1:
                enemySpeed[i-2] += 3
                enemyImg[i-2] = pygame.image.load("./img/ufo3.png")
            playerSpeed += 1
            playerImg = pygame.image.load("./img/spaceship3.png")
            bulletY_change += 10
            bullet_number = 3
            bulletSound = "./audio/laser.wav"
            bulletImg = pygame.image.load('./img/laser.png')
            isOnce8 = False
        #level 10
        elif level_count == 10 and isOnce10:
            if i < num_of_enemy-3:
                enemySpeed[i+3] += 4
                enemyImg[i+3] = pygame.image.load("./img/ufo2.png")
            elif i > 2:
                enemySpeed[i-3] += 4
                enemyImg[i-3] = pygame.image.load("./img/ufo2.png")
            playerSpeed += 1
            bullet_number = 3
            isOnce10 = False
        #level 12
        elif level_count == 12 and isOnce12:
            if i < num_of_enemy-4:
                enemySpeed[i+4] += 4
                enemyImg[i+4] = pygame.image.load("./img/ufo3.png")
                enemyY[i] += enemyImgHeight[i]*2
            elif i > 3:
                enemySpeed[i-4] += 4
                enemyImg[i-4] = pygame.image.load("./img/ufo3.png")
                enemyY[i] += enemyImgHeight[i]*2
            playerSpeed += 1
            bulletY_change += 20
            bullet_number = 3
            isOnce12 = False
        #level 14
        elif level_count == 14 and isOnce14:
            if i < num_of_enemy-5:
                enemySpeed[i+5] += 4
                enemyImg[i+5] = pygame.image.load("./img/ufo3.png")
                enemyY[i+5] += enemyImgHeight[i]*2
            elif i > 4:
                enemySpeed[i-5] += 4
                enemyImg[i-5] = pygame.image.load("./img/ufo3.png")
                enemyY[i+5] += enemyImgHeight[i]*2
            playerSpeed += 1
            bullet_number = 3
            isOnce14 = False
            


    #movement of bullet
    if bulletY <= 0:
        bulletY = screenY-(playerImgHight * 2)
        isfire = False
    if isfire:
        fire(bulletX, bulletY)
        bulletY -= bulletY_change

    #score
    show_score(20,20)

    #level
    show_level((screenX-150) , 20)
    if score_value == 10:
        level_count = 2

    #show bullet number
    show_bullet()

    pygame.display.update()
