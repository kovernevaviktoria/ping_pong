from pygame import *
from random import randint
import random
mixer.init()
font.init()

class GameSprite(sprite.Sprite):
    def __init__(self,player_image,player_speed, player_x, player_y, size_x, size_y):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect() #прямоугольник
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image,(self.rect.x, self.rect.y))

class Player(GameSprite):
    def update_r(self):
        keys = key.get_pressed()
        if keys[K_UP] and self.rect.y > 0:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < 350:
            self.rect.y += self.speed
    def update_l(self):
        keys = key.get_pressed()
        if keys[K_w] and self.rect.y > 0:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < 350:
            self.rect.y += self.speed


#окно игры и фон
window = display.set_mode((700, 500))
display.set_caption("Ping-pong")
background = transform.scale(image.load("background.jpeg"),(700,500)) #создать фон картинку и адаптировать под размер окна

#переменные
clock = time.Clock()
FPS = 60
finish = False #конец партии
score_1 = 0 
score_2 = 0
font1 = font.SysFont('Arial', 36)
num_fire = 0
rel_time = False #конец всего матча (match_over)
run = True #физическое окно
speed_x = random.choice([-2,2])
speed_y = random.choice([-2,2])
score1 = 0
score2 = 0
max_score = 3
font1 = font.Font(None, 35)
kick = mixer.Sound('sound.mp3')


#спрайты
pl1 = Player("line.png", 5, 25, 250, 15, 100)
pl2 = Player("line.png", 5, 670, 250, 15, 100)
ball = GameSprite("ball.png", 1, 350, 250, 40,40)

pl2_text = font1.render('Игрок 2 победил', True, (0,0,0))
pl1_text = font1.render('Игрок 1 победил', True, (0,0,0))
 

while run == True:
    for e in event.get():
        if e.type == QUIT:
            run = False       
    if not finish and not rel_time:
        window.blit(background,(0,0))
        pl1.reset()
        pl1.update_l()
        pl2.reset()
        pl2.update_r()
        ball.reset()
        ball.rect.x += speed_x
        ball.rect.y += speed_y
        
        #гол игрока 2 (мяч ушел за левую границу)
        if ball.rect.x <= 0:
            kick.play()
            score2 += 1
            finish = True
            

        #гол игрока 1 (за правую границу)
        if ball.rect.x >= 660:
            kick.play()
            score1 += 1
            finish = True


        #проверка победы в матче
        if score1 == max_score or score2 == max_score:
            rel_time = True
        if rel_time and score1 == max_score:
            window.blit(pl1_text, (250,230))
        if rel_time and score2 == max_score:
            window.blit(pl2_text, (250,230))

    elif finish and not rel_time:
        ball.rect.x = 350
        ball.rect.y = 250
        pl1.rect.y = 250
        pl2.rect.y = 250

        pl1.reset()
        pl1.update_l()
        pl2.reset()
        pl2.update_r()
        ball.reset()

        #пауза
        time.wait(2000)

        #случайное направление мяча
        finish = False

    if ball.rect.y > 450 or ball.rect.y < 0:
        speed_y *= -1.01
    if sprite.collide_rect(pl1,ball) or sprite.collide_rect(pl2, ball):
        speed_x *= -1.01
    
    score_text = font1.render(str(score1) + ' : ' + str(score2), True, (0,0,0))
    window.blit(score_text, (310,20))
    display.update()
    clock.tick(FPS)
