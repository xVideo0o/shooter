from pygame import *
from random import choice

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
    def update1(self):
        keys = key.get_pressed()
        if keys[K_w] and self.rect.y>5:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y<500-5-self.rect.height:
            self.rect.y += self.speed

    def update2(self):
        keys = key.get_pressed()
        if keys[K_UP] and self.rect.y>5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y<500-5-self.rect.height:
            self.rect.y += self.speed


class Ball(GameSprite):
    def __init__(self, img, x, y, w, h, speed):
        super().__init__(img, x, y, w, h, speed)
        self.speed_x = 0
        self.speed_y = 0
    
    def set_direction(self, speed_x, speed_y):
        self.speed_x = speed_x
        self.speed_y = speed_y
    def update(self):
        self.rect.x += self.speed_x*self.speed
        self.rect.y += self.speed_y*self.speed

    def check_direction(self, pl1, pl2):
        global point_l, point_r
        if self.rect.y<=0:
            self.speed_y*=-1
        elif self.rect.y >= 500 - self.rect.height:
            self.speed_y*=-1
        elif self.rect.colliderect(pl1.rect):
            self.speed_x *=-1
        elif self.rect.colliderect(pl2.rect):
            self.speed_x *=-1

        elif self.rect.x <= 0:
            point_r +=1
            self.rect.x = 700/2-self.rect.width/2
            self.rect.y = 500/2-self.rect.height/2
            self.set_direction(choice([-1,1]), choice([-1,1]))

        elif self.rect.x >=  700 - self.rect.width:
            point_l +=1
            self.rect.x = 700/2-self.rect.width/2
            self.rect.y = 500/2-self.rect.height/2
            self.set_direction(choice([-1,1]), choice([-1,1]))


point_l = 0
point_r = 0

direction = [-1,1]
ball = Ball('Player.png', 700/2-25, 700/2-25, 50, 50, 2)
ball.set_direction(choice(direction), choice(direction))
player1 = Player('liana.png', 20, 250, 75, 150, 6)
player2 = Player('liana.png', 625, 250, 75, 150, 6)

window = display.set_mode((700, 500))
display.set_caption('ПингПонг')
background = transform.scale(image.load('fon.jpg'), (700, 500))


clock = time.Clock()
FPS = 100

game = True

while game:

    for e in event.get():
        if e.type == QUIT:
            game = False
    window.blit(background,(0,0))
    ball.update()
    ball.reset()
    ball.check_direction(player1, player2)
    player1.update1()
    player1.reset()
    player2.update2()
    player2.reset()
    


    display.update()
    clock.tick(FPS)