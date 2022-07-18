import pygame, random
from pygame.locals import *
from sprites.asteroid import Asteroid
from sprites.alien import Alien
from sprites.space import Space
from sprites.ship import Ship
from sprites.shot import Shot
import os, sys

def fora_da_tela(sprite):
    return sprite.rect[0] < -(sprite.rect[2])

def asteroide_fora_da_tela(sprite):
    return sprite.rect[0] < -(sprite.rect[2]+300)

def tiro_fora_da_tela(sprite):
    return sprite.rect[0] > (400+sprite.rect[2])

def pos_asteroide(xpos):
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

background = pygame.image.load('src/images/newbackground.jpg')
background = pygame.transform.scale(background, (400,800))

space_group = pygame.sprite.Group()
for i in range(2):
    space = Space(800 * i)
    space_group.add(space)

Asteroid_group = pygame.sprite.Group()
for i in range(2):
    Asteroids = pos_asteroide(400 * i + 800)
    Asteroid_group.add(Asteroids[0])
    Asteroid_group.add(Asteroids[1])
    Asteroid_group.add(Asteroids[2])
    Asteroid_group.add(Asteroids[3])

alien_group = pygame.sprite.Group()
ypos = random.randint(200,600)
alien = Alien(400,ypos)
alien_group.add(alien) 

ship_group = pygame.sprite.Group()
ship = Ship()
ship_group.add(ship)

shot_group = pygame.sprite.Group()
enemy_shot_group = pygame.sprite.Group()

clock = pygame.time.Clock()

count = 0
max_count = 0
font = pygame.font.SysFont(None, 24)
is_dead = False

while True:
    clock.tick(30)

    if (is_dead):
        screen.blit(pygame.transform.scale(pygame.image.load('src/images/gameover.png'), (200,125)), (100, 300))
        screen.blit(font.render('Aperte ESPAÇO para continuar', True, (255,255,255)), (80, 450))


        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    is_dead = False
                    ship_group.empty()
                    ship = Ship()
                    ship_group.add(ship)
                    shot_group.empty()
                    Asteroid_group.empty()
                    alien_group.empty()
                    enemy_shot_group.empty()
                    count = 0
                    max_count = max(max_count, count)
                    Asteroids = pos_asteroide(400 * 2)
                    Asteroid_group.add(Asteroids[0])
                    Asteroid_group.add(Asteroids[1])
                    Asteroid_group.add(Asteroids[2])
                    Asteroid_group.add(Asteroids[3])

            if event.type == QUIT:
                pygame.quit()
                
        continue

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()

        if event.type == KEYDOWN:
            if event.key == K_UP:
                ship.up()

            if event.key == K_DOWN:
                ship.down()
        
            if event.key == K_LEFT:
                ship.left()
        
            if event.key == K_RIGHT:
                ship.right()
 
            if event.key == K_SPACE:
                shot = Shot(ship.rect[0], ship.rect[1], 'ship')
                shot_group.add(shot)

    if fora_da_tela(space_group.sprites()[0]):
        space_group.remove(space_group.sprites()[0])

        new_Space = Space(800 - 20)
        space_group.add(new_Space)

    if (Asteroid_group.sprites()):
        if asteroide_fora_da_tela(Asteroid_group.sprites()[0]): 
            Asteroid_group.remove(Asteroid_group.sprites()[0])
            Asteroid_group.remove(Asteroid_group.sprites()[0])
            Asteroid_group.remove(Asteroid_group.sprites()[0])
            Asteroid_group.remove(Asteroid_group.sprites()[0])

            Asteroids = pos_asteroide(400 * 2)

            Asteroid_group.add(Asteroids[0])
            Asteroid_group.add(Asteroids[1])
            Asteroid_group.add(Asteroids[2])
            Asteroid_group.add(Asteroids[3])
    
    if (shot_group.sprites()):
        if tiro_fora_da_tela(shot_group.sprites()[0]):
            shot_group.remove(shot_group.sprites()[0])
    
    if(alien_group.sprites()):
        if fora_da_tela(alien_group.sprites()[0]):
            alien_group.remove(alien_group.sprites()[0])

    else:
        ypos = random.randint(200,600)
        alien = Alien(400,ypos)
        alien_group.add(alien)
    
    space_group.update()
    Asteroid_group.update()
    ship_group.update()
    alien_group.update(enemy_shot_group)
    enemy_shot_group.update(ship.rect[0], ship.rect[1])
    shot_group.update()

    space_group.draw(screen)
    Asteroid_group.draw(screen)
    ship_group.draw(screen)
    alien_group.draw(screen)
    shot_group.draw(screen)
    enemy_shot_group.draw(screen)
    screen.blit(font.render(f'CONTADOR: {count}', True, (255,255,255)), (20, 20))
    screen.blit(font.render(f'MAXIMO: {max_count}', True, (255,255,255)), (20, 40))


    pygame.display.update()
  
    if pygame.sprite.groupcollide(ship_group, Asteroid_group, False, False, pygame.sprite.collide_mask) or pygame.sprite.groupcollide(ship_group, alien_group, True, False, pygame.sprite.collide_mask) or pygame.sprite.groupcollide(ship_group, enemy_shot_group, True, False, pygame.sprite.collide_mask):
        is_dead = True
        continue
        #pygame.quit()
        
             
    if pygame.sprite.groupcollide(shot_group, alien_group, True, True, pygame.sprite.collide_mask):
        count += 1

    pygame.sprite.groupcollide(shot_group, enemy_shot_group, True, True, pygame.sprite.collide_mask)

    max_count = max(max_count, count)

