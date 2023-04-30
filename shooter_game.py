#Создай собственный Шутер!

from pygame import *
from random import (
    randint,uniform
)
from time import time as timer


class GameSprite(sprite.Sprite):
    def __init__ (self,player_image,player_x,player_y,x_size,y_size,player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image),(x_size,y_size))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < 620:
            self.rect.x += self.speed

    def fire(self):
        bullets.add(Bullet("bullet.png",self.rect.centerx-7,self.rect.top-15,15,20,-15))
    def rice_speed(self):
        self.speed += 1
    def one_lose(self):
        self.speed = randint(1,3)
lost = 0

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        #исчезает, если дойдёт до края экрана
        if self.rect.y > 525:
           self.rect.x = randint(50, 650)
           self.rect.y = 0
           lost = lost + 1
        '''if self.rect.y < 525:
            self.rect.y += self.speed
        else:
            global lost
            self.speed = uniform(self.speed,self.speed+2)
            self.rect.x = randint(50,650)
            self.rect.y = -25
            lost += 1'''
    def rice_speed(self):
        self.speed += 1.5
    def one_lose(self):
        self.speed = randint(1,3)

class Bullet (GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < -5:
            self.kill()



#создай окно игры
window = display.set_mode((700,500))
display.set_caption("Шутер")

#задай фон сцены
background = transform.scale(image.load("galaxy.jpg"),(700,500))
clock = time.Clock()
FPS = 50
game = True
finish = False

#персонажи игры
rocket = Player("rocket.png",350,400,80,100,10)
monsters = sprite.Group()
for i in range(5):
    monsters.add(Enemy("ufo.png",randint(50,650),0,80,50,randint(1,3)))
asteroids = sprite.Group()
for i in range(3):
    asteroids.add(Enemy("asteroid.png",randint(50,650),0,80,50,randint(1,3)))
bullets = sprite.Group()

#подключение музыки
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_song = mixer.Sound('fire.ogg')


#
font.init()

life = 3
speed_control = 0
point = 0
speed = 1
rel_time = False
num_fire = 0

while game:
    if finish == False:
        window.blit(background,(0,0))
        text_lost = font.SysFont('Arial',30).render('Пропущено:'+str(lost),1,(255,255,255))
        text_kill = font.SysFont('Arial',30).render('Убито:'+str(point),1,(255,255,255))
        window.blit(text_lost,(10,10))
        window.blit(text_kill,(10,30))
        rocket.reset()
        monsters.draw(window)
        asteroids.draw(window)
        bullets.draw(window)
        rocket.update()
        monsters.update()
        asteroids.update()
        bullets.update()
        speed_control += 1

        if rel_time == True:
            now_time = timer()
        
            if now_time - last_time < 3:
                reload_text = font.SysFont('Arial',20).render('Пожалуйста, подождите!',1,(255,255,255))
                window.blit(reload_text,(220,460))
            else:
                num_fire = 0
                rel_time = False


        if len(sprite.groupcollide(monsters,bullets,False,False)) > 0:
            collide = sprite.groupcollide(
                monsters,bullets,True,True
            )
            point += 1
            monsters.add(Enemy("ufo.png",randint(50,650),0,80,50,uniform(speed,speed+2)))

        if len(sprite.spritecollide(rocket,monsters,False)) > 0 or len(sprite.spritecollide(rocket,asteroids,False)) > 0:
            finish = True
            kill = font.SysFont('Arial',45).render('Поздравляю! Сохраняй результат!',1,(255,255,255))
            window.blit(kill,(100,240))
            

        if speed_control == 50:
            for monster in monsters:
                monster.rice_speed()
            for asteroid in asteroids:
                asteroid.rice_speed()
            rocket.rice_speed()
            speed_control = 0
    else:
        finish = False
        score = 0
        lost = 0
        num_fire = 0
        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()
        for a in asteroids:
            a.kill()

        time.delay(3000)
        for i in range(5):
            monster = Enemy("ufo.png",randint(50,650),0,80,50,randint(1,3))
            monsters.add(monster)
        for i in range(3):
            asteroid = Enemy("asteroid.png",randint(50,650),0,80,50,randint(1,3))
            asteroids.add(asteroid)
    

    for e in event.get():
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time != True:
                    rocket.fire()
                    fire_song.play()
                    num_fire += 1
                if num_fire >= 5 and rel_time != True:
                    rel_time = True
                    last_time = timer()
        if e.type == QUIT:
            game = False
    display.update()
    clock.tick(FPS)