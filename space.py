import pygame, random
from pygame.locals import *

class Ship(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('Ship.png').convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)
        self.image = pygame.transform.scale(self.image, (45,40))

        self.rect = self.image.get_rect()
        self.rect[0] = 400 / 2
        self.rect[1] = 800 / 2
    
    def down(self):
        self.rect[1] += 20

    def up(self):
        self.rect[1] -= 20
    
    def left(self):
        self.rect[0] -= 20
    
    def right(self):
        self.rect[0] += 20
class Asteroid(pygame.sprite.Sprite):

    def __init__(self, xpos, ypos):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('asteroid.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (60,60))

        self.rect = self.image.get_rect()
        self.rect[0] = xpos
        self.rect[1] = 800 - ypos

        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect[0] -= 10

class Space(pygame.sprite.Sprite):

    def __init__(self, xpos):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('newbackground.jpg').convert_alpha()
        self.image = pygame.transform.scale(self.image, (800, 800))

        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect[0] = xpos
        self.rect[1] = 0
    
    def update(self):
        self.rect[0] -= 10

def fora_da_tela(sprite):
    return sprite.rect[0] < -(sprite.rect[2])

def asteroide_fora_da_tela(sprite):
    return sprite.rect[0] < -(sprite.rect[2]+300)

def tamanho_cano(xpos):
    size_1 = random.randint(650, 775)
    size_2 = random.randint(500, 600)
    size_3 = random.randint(300, 450)
    size_4 = random.randint(100, 250)
    dif1 = random.randint(0, 300)
    dif2 = random.randint(0, 300)
    dif3 = random.randint(0, 300)
    dif4 = random.randint(0, 300)
    Asteroid_1 = Asteroid(xpos - dif1, size_1)
    Asteroid_2 = Asteroid(xpos - dif2, size_2)
    Asteroid_3 = Asteroid(xpos - dif3, size_3)
    Asteroid_4 = Asteroid(xpos - dif4, size_4)
    return (Asteroid_1, Asteroid_2, Asteroid_3, Asteroid_4)


pygame.init()
screen = pygame.display.set_mode((400,800))

background = pygame.image.load('newbackground.jpg')
background = pygame.transform.scale(background, (400,800))

space_group = pygame.sprite.Group()
for i in range(2):
    space = Space(800 * i)
    space_group.add(space)

Asteroid_group = pygame.sprite.Group()
for i in range(2):
    Asteroids = tamanho_cano(400 * i + 800)
    Asteroid_group.add(Asteroids[0])
    Asteroid_group.add(Asteroids[1])
    Asteroid_group.add(Asteroids[2])
    Asteroid_group.add(Asteroids[3])

ship_group = pygame.sprite.Group()
ship = Ship()
ship_group.add(ship)

clock = pygame.time.Clock()

while True:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()

        if event.type == KEYDOWN:
            if event.key == K_UP:
                ship.up()

        if event.type == KEYDOWN:
            if event.key == K_DOWN:
                ship.down()
        
        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                ship.left()
        
        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                ship.right()

    if fora_da_tela(space_group.sprites()[0]):
        space_group.remove(space_group.sprites()[0])

        new_Space = Space(800 - 20)
        space_group.add(new_Space)

    if asteroide_fora_da_tela(Asteroid_group.sprites()[0]):
        Asteroid_group.remove(Asteroid_group.sprites()[0])
        Asteroid_group.remove(Asteroid_group.sprites()[0])
        Asteroid_group.remove(Asteroid_group.sprites()[0])
        Asteroid_group.remove(Asteroid_group.sprites()[0])

        Asteroids = tamanho_cano(400 * 2)

        Asteroid_group.add(Asteroids[0])
        Asteroid_group.add(Asteroids[1])
        Asteroid_group.add(Asteroids[2])
        Asteroid_group.add(Asteroids[3])

    space_group.update()
    Asteroid_group.update()
    ship_group.update()

    space_group.draw(screen)
    Asteroid_group.draw(screen)
    ship_group.draw(screen)

    pygame.display.update()

    if pygame.sprite.groupcollide(ship_group, Asteroid_group, False, False, pygame.sprite.collide_mask):
        pygame.quit()
