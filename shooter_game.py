#Создай собственный Шутер!

from pygame import *
from random import randint
from time import time as mytime


class GameSprite(sprite.Sprite):
    def __init__(self, img, x, y, w, h, speed):
        super().__init__()
        self.image = transform.scale(image.load(img), (w, h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

    def collidepoint(self, x, y):
        return self.rect.collidepoint(x, y)

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x>5:
            self.rect.x -= self.speed
        if keys[K_s] and self.rect.x<700-5-self.rect.width:
            self.rect.x += self.speed

    def fire(self):
        y = self.rect.y
        x = self.rect.centerx
        r = randint(0,1)
        if r == 0:
            bullet = Bullet('patron.png', x-47, y, 30, 50, 3)
        elif r == 1:
            bullet = Bullet('bulka.png', x-47, y, 30, 50, 3)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y>500-self.rect.height:
            self.rect.x = randint(2, 700-5-self.rect.width)
            self.rect.y = -self.rect.height
            self.speed = randint(1,3)
            lost += 1

class Enemy1(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y>500-self.rect.height:
            self.rect.x = randint(2, 700-5-self.rect.width)
            self.rect.y = -self.rect.height
            self.speed = randint(1,3)

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y<0:
            self.kill()



window = display.set_mode((700, 500))
display.set_caption('Шутер')


background = transform.scale(image.load('fon.png'), (700, 500))
button = GameSprite('start.png', 280, 250, 150, 50, 0)

mixer.init()
mixer.music.load('music.ogg')
mixer.music.play()

font.init()
font1 = font.Font(None, 36)


player = Player('shaurmist.png', 316, 400, 100, 100, 5)

enemy_count = 3
enemyes = sprite.Group()
for i in range(enemy_count):
    enemy = Enemy('sob.png', randint(5, 700-5-70), -50, 40, 66, 2)
    enemyes.add(enemy)

asteroid_count = 2
asteroids = sprite.Group()
for i in range(asteroid_count):
    asteroid = Enemy1('golub.png', randint(5, 700-5-70), -50, 40, 66, 1)
    asteroids.add(asteroid)

bullets = sprite.Group()



game = True
finish = True
menu = True
lost = 0
score = 0
text = 0
font_lose = font1.render('GAME OVER!', 1, (255, 0, 0))
font_win = font1.render('ШАУРМА ТВОЯ!', 1, (0, 255, 0))
font_lose1 = font1.render('ТЕБЯ ЗАКЛЕВАЛИ!', 1, (255, 255, 0))


clock = time.Clock()
FPS = 100

while game:

    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                player.fire()
            if e.key == K_d:
                menu = False
                finish = False
                start_time = mytime()

    if menu == True:
        window.blit(background, (0, 0))
        button.reset()
        pressed = mouse.get_pressed()
        pos = mouse.get_pos()
        if pressed[0]:
            if button.collidepoint(pos[0], pos[1]):
                menu = False
                finish = False
                start_time = mytime()
        if text == 1:
            window.blit(font_win, (255,225))
        elif text == 2:
            window.blit(font_lose, (280, 225))
        elif text == 3:
            window.blit(font_lose1, (245, 225))
        if text != 0:
            font_time = font1.render('Время на уровне: '+str(int(end_time-start_time))+' сек', 1, (255, 255, 255))
            window.blit(font_time, (225, 300))
        lost = 0
        score = 0
        enemyes.empty()
        for i in range(enemy_count):
            enemy = Enemy('sob.png', randint(5, 700-5-70), -50, 40, 66, 1)
            enemyes.add(enemy)
        asteroids.empty()
        for i in range(asteroid_count):
            asteroid = Enemy1('golub.png', randint(5, 700-5-70), -50, 40, 66, 2)
            asteroids.add(asteroid)
        bullets.empty()

    if finish != True:


        window.blit(background, (0, 0))
        player.update()
        enemyes.update()
        bullets.update()
        asteroids.update()
        player.reset()
        enemyes.draw(window)
        bullets.draw(window)
        asteroids.draw(window)

        sprite_list1 = sprite.spritecollide(player, enemyes, False)
        if lost>6:
            text = 2
            finish = True
            menu = True
            end_time = mytime()

        sprite_list2 = sprite.spritecollide(player, asteroids, False)
        if len(sprite_list2)>0:
            text = 3
            finish = True
            menu = True
            end_time = mytime()

        sprite_list = sprite.groupcollide(enemyes, bullets, True, True)
        for m in sprite_list:
            score += 1
            enemy = Enemy('sob.png', randint(5, 700-5-70), -50, 50, 76, 1)
            enemyes.add(enemy)
        if score > 29:
            text = 1
            finish = True
            menu = True
            end_time = mytime()

        font_lost = font1.render('Убежало собак: '+ str(lost), 1, (255, 0, 0))
        window.blit(font_lost, (4, 4))

        font_score = font1.render('Поймано собак: '+ str(score), 1, (0, 255, 0))
        window.blit(font_score, (4, 30))

    display.update()
    clock.tick(FPS)


