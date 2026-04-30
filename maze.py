from pygame import *
from random import randint
font.init()
#фоновая музыка
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')


#нам нужны такие картинки:
img_back = "galaxy.jpg" #фон игры
img_hero = "rocket.png" #герой
img_ufo="ufo.png"
bullets=sprite.Group()
asteroids=sprite.Group()
font1=font.SysFont('Times new roman',36)
font2=font.SysFont('Times new roman',100)
lost=0
not_lost=0
count=0

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class Asteroid(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__(player_image, player_x, player_y, size_x, size_y, player_speed)
        self.life=5
    def update(self):
        self.rect.y+=self.speed
        if self.rect.y>=500:
            self.rect.y=0
            self.rect.x=randint(0,580)
            self.speed=randint(1,2)
        elif sprite.spritecollide(self, bullets, False):
            self.rect.y=0
            self.rect.x=randint(0,580)
            self.speed=randint(1,5)
            self.life-=1
        if self.rect.colliderect(ship.rect):
            self.rect.y=0
            self.rect.x=randint(0,580)
            self.speed=randint(1,5)
            self.life-=1
            global live
            live-=1
        if self.life==0:
            self.kill()
class Bullet(GameSprite):
    def update(self):
        self.rect.y-=self.speed
        if self.rect.y<=0 or sprite.spritecollide(self, ufos, False) or sprite.spritecollide(self, asteroids, False):
            self.kill()
class Enemy(GameSprite):
    def update(self):
        self.rect.y+=self.speed
        if self.rect.y>=500:
            self.rect.y=0
            self.rect.x=randint(0,580)
            self.speed=randint(1,5)
            global lost
            lost+=1
        elif sprite.spritecollide(self, bullets, False):
            self.rect.y=0
            self.rect.x=randint(0,580)
            self.speed=randint(1,5)
            global not_lost
            not_lost+=1
        if self.rect.colliderect(ship.rect):
            self.rect.y=0
            self.rect.x=randint(0,580)
            self.speed=randint(1,5)
            not_lost+=1
            global live
            live-=1
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    def fire(self):
        keys = key.get_pressed()
        global time1
        global count
        global reloady
        if keys[K_SPACE] and count<5 and reloady==False:
            bullet=Bullet("bullet.png",self.rect.centerx-7,self.rect.y,15,20,15)
            bullets.add(bullet)
            count+=1
        elif count>=5 and reloady==False:
            time1=time.get_ticks()
            reloady=True 
        if reloady==True and time.get_ticks()-time1>=500:
            reloady=False
            count=0

        bullets.update()
        bullets.draw(window)


win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))
clock = time.Clock()


ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)
ufos=sprite.Group()#создаем группу
for i in range(5):
    enemy1=Enemy(img_ufo,randint(0,580),0,120,75,randint(1,5))
    ufos.add(enemy1)

for i in range(3):
    asteroid1=Asteroid("asteroid.png",randint(0,580),0,96,60,randint(1,2))
    asteroids.add(asteroid1)

x=randint(0,255)
y=randint(0,255)
z=randint(0,255)
finish = False
run = True 
live=3
reloady=False
relcolor=False

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
    if not finish:
        window.blit(background,(0,0))
        
        ship.update()
        ship.reset()
        ship.fire()
        ufos.update()
        ufos.draw(window)
        
        asteroids.update()
        asteroids.draw(window)
        if not_lost==10:
            finish=True
            win=font1.render("Вы победили!" ,1,((x+y+z)/3,(x+y+z)/3,(x+y+z)/3))
            window.blit(win,(250,200))
        if lost>=3 or live<=0:
            finish=True
            loses=font1.render("Вы проиграли!" ,1,((x+y+z)/3,(x+y+z)/3,(x+y+z)/3))
            window.blit(loses,(250,200))
        lives1=font2.render("__",1,(abs(x-y),abs(y-z),abs(z-x)))
        lives2=font2.render(str(live),1,(abs(x-y),abs(y-z),abs(z-x)))
        lives3=font2.render("|  |",1,(abs(x-y),abs(y-z),abs(z-x)))
        lives4=font2.render("__",1,(abs(x-y),abs(y-z),abs(z-x)))
        window.blit(lives1,(626,-108))
        window.blit(lives2,(640,-9))
        window.blit(lives3,(618,-20))
        window.blit(lives4,(626,-17))
        
        text_lose=font1.render("Пропущено:"+str(lost),1,(x,y,z))
        text_not_lose=font1.render("Поймано:"+str(not_lost),1,(255-x,255-y,255-z))
        window.blit(text_lose,(0,0))
        window.blit(text_not_lose,(0,50))
        
       


    display.update()
    clock.tick(55)
