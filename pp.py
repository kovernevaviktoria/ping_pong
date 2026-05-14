from pygame import *
from random import randint
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
background = transform.scale(image.load("bg.jpeg"),(700,500)) #создать фон картинку и адаптировать под размер окна

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
speed_x = 1
speed_y = 1
score1 = 0
score2 = 0
max_score = 3
font1 = font.Font(None, 35)


#спрайты
pl1 = Player("line.png", 5, 15, 250, 17, 100)
pl2 = Player("line.png", 5, 650, 250, 17, 100)
ball = GameSprite("ball.png", 1, 350, 250, 40,40)
 

while run == True:
    for e in event.get():
        if e.type == QUIT:
            run = False       
    if finish != True:
        window.blit(background,(0,0))
        pl1.reset()
        pl1.update_l()
        pl2.reset()
        pl2.update_r()
        ball.reset()
        ball.rect.x += speed_x
        ball.rect.y += speed_y
        score_text = font1.render(str(score1) + ' : ' + str(score2), True, (0,0,0))
        window.blit(score_text, (310,20))
    if ball.rect.y > 450 or ball.rect.y < 0:
        speed_y *= -1.07
    if sprite.collide_rect(pl1,ball) or sprite.collide_rect(pl2, ball):
        speed_x *= -1.07
    

    display.update()
    clock.tick(FPS)



    '''
    from pygame import *
from random import randint
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
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < 600:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet("bullet.png",15, self.rect.centerx, self.rect.top, 15, 20)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 500:
            self.rect.y = -110
            self.rect.x = randint(5,615)
            lost += 1
            self.speed = randint(2,5)

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill() #безжалостно убиваем


#окно игры и фон
window = display.set_mode((700, 500))
display.set_caption("Шутер")
background = transform.scale(image.load("galaxy.jpg"),(700,500)) #создать фон картинку и адаптировать под размер окна

mixer.init()
mixer.music.load("space.ogg")
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

ship = Player("rocket.png", 5, 250, 400, 110, 110) #главный спрайт

clock = time.Clock()
FPS = 60
run = True
finish = False
lost = 0
score = 0 #безжалостно расстрелено
life = 3
num_fire = 0
rel_time = False

#GROUP 
rabbits = sprite.Group() #create a  group
for i in range(5):
    rabbit = Enemy("ufo.png",randint(1,3),randint(5,615),-80,80,50)
    rabbits.add(rabbit)
#GROUP 2
bullets = sprite.Group()
asts = sprite.Group()
for s in range (3):
    ast = Enemy("asteroid.png",randint(1,3),randint(5,615),-80,80,50)
    asts.add(ast)
#FONT
font1 = font.SysFont('Arial', 36)
font2 = font.SysFont('Arial', 80) 

while run == True:
    for e in event.get():
        if e.type == QUIT:
            run = False       
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    num_fire += 1
                    ship.fire()
                    fire_sound.play()
                elif num_fire>=5 and rel_time == False:
                    last_time = time.get_ticks()
                    rel_time = True

    if finish != True:
        window.blit(background,(0,0))
        ship.reset()
        ship.update()
        rabbits.draw(window)
        rabbits.update()
        bullets.draw(window)
        bullets.update()
        collides = sprite.groupcollide(rabbits,bullets,True,True) #список трагически умерших
        for s in collides:
            score += 1
            rabbit = Enemy("ufo.png",randint(1,3),randint(5,615),-80,80,50)
            rabbits.add(rabbit)
        asts.draw(window)
        asts.update()
        list1 = sprite.spritecollide(ship, rabbits, True)
        for I in list1:
            life -= 1
            rabbit = Enemy("ufo.png",randint(1,3),randint(5,615),-80,80,50)
            rabbits.add(rabbit)
        list2 = sprite.spritecollide(ship, asts, True)
        for I in list2:
            life -= 1
            ast = Enemy("asteroid.png",randint(1,3),randint(5,615),-80,80,50)
            asts.add(ast)
        if life<= 0 or lost >=5:
            finish = True
            game_over = font2.render("YOU LOSE", 1, (255,255,255))
            window.blit(game_over,(320,250))
        if rel_time == True:
            new_time = time.get_ticks()
            if new_time - last_time < 1000:
                wait = font1.render("Wait, reload...", 1, (255,255,255))
                window.blit(wait,(320,250))
            else:
                num_fire = 0
                rel_time = False
        
        if score >= 5:
            game_win = font2.render("YOU WIN", 1, (255,255,255))
            window.blit(game_win,(320,250))
            finish = True

        text_lose = font1.render("Пропущено:" + str(lost), 1, (255,255,255))
        window.blit(text_lose,(10,10))
        text_win = font1.render("Убито:" + str(score), 1, (255,255,255))
        window.blit(text_win,(10,35))
        text_life = font1.render("Жизни:" + str(life), 1, (255,255,255))
        window.blit(text_life,(10,60))
    
    display.update()
    clock.tick(FPS)
    '''
