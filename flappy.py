import pygame, random
from pygame.locals import *

LARGURA_TELA = 400
ALTURA_TELA = 800
LARGURA_SOLO = 2 * LARGURA_TELA
ALTURA_SOLO = 100
LARGURA_CANO = 80
ALTURA_CANO = 500
DISTANCIA_CANO = 200
VELOCIDADE = 10
GRAVITY = 1
VELOCIDADE_GERAL = 10


class Bird(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.images = [pygame.image.load('bluebird-upflap.png').convert_alpha(),
                       pygame.image.load('bluebird-midflap.png').convert_alpha(),
                       pygame.image.load('bluebird-downflap.png').convert_alpha()]

        self.velocidade = VELOCIDADE

        self.current_image = 0

        self.image = pygame.image.load('bluebird-upflap.png').convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect[0] = LARGURA_TELA / 2
        self.rect[1] = ALTURA_TELA / 2

    def update(self):
        self.current_image = (self.current_image + 1) % 3
        self.image = self.images[ self.current_image ]

        self.velocidade += GRAVITY

        self.rect[1] += self.velocidade
    
    def bump(self):
        self.velocidade = -VELOCIDADE

class Pipe(pygame.sprite.Sprite):

    def __init__(self, inverted, xpos, ysize):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('pipe-red.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (LARGURA_CANO,ALTURA_CANO))

        self.rect = self.image.get_rect()
        self.rect[0] = xpos

        if inverted:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect[1] = - (self.rect[3] - ysize)
        else:
            self.rect[1] = ALTURA_TELA - ysize

        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect[0] -= VELOCIDADE_GERAL

class Ground(pygame.sprite.Sprite):

    def __init__(self, xpos):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('base.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (LARGURA_SOLO, ALTURA_SOLO))

        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect[0] = xpos
        self.rect[1] = ALTURA_TELA - ALTURA_SOLO
    
    def update(self):
        self.rect[0] -= VELOCIDADE_GERAL

def fora_da_tela(sprite):
    return sprite.rect[0] < -(sprite.rect[2])

def tamanho_cano(xpos):
    size = random.randint(100, 300)
    pipe = Pipe(False, xpos, size)
    pipe_inverted = Pipe(True, xpos, ALTURA_TELA - size - DISTANCIA_CANO)
    return (pipe, pipe_inverted)


pygame.init()
screen = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))

BACKGROUND = pygame.image.load('background.png')
BACKGROUND = pygame.transform.scale(BACKGROUND, (LARGURA_TELA, ALTURA_TELA))

bird_group = pygame.sprite.Group()
bird = Bird()
bird_group.add(bird)

ground_group = pygame.sprite.Group()
for i in range(2):
    ground = Ground(LARGURA_SOLO * i)
    ground_group.add(ground)

pipe_group = pygame.sprite.Group()
for i in range(2):
    pipes = tamanho_cano(LARGURA_TELA * i + 800)
    pipe_group.add(pipes[0])
    pipe_group.add(pipes[1])


clock = pygame.time.Clock()

while True:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()

        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                bird.bump()

    screen.blit(BACKGROUND, (0, 0))

    if fora_da_tela(ground_group.sprites()[0]):
        ground_group.remove(ground_group.sprites()[0])

        new_ground = Ground(LARGURA_SOLO - 20)
        ground_group.add(new_ground)

    if fora_da_tela(pipe_group.sprites()[0]):
        pipe_group.remove(pipe_group.sprites()[0])
        pipe_group.remove(pipe_group.sprites()[0])

        pipes = tamanho_cano(LARGURA_TELA * 2)

        pipe_group.add(pipes[0])
        pipe_group.add(pipes[1])

    bird_group.update()
    ground_group.update()
    pipe_group.update()

    bird_group.draw(screen)
    pipe_group.draw(screen)
    ground_group.draw(screen)

    pygame.display.update()

    if (pygame.sprite.groupcollide(bird_group, ground_group, False, False, pygame.sprite.collide_mask) or
       pygame.sprite.groupcollide(bird_group, pipe_group, False, False, pygame.sprite.collide_mask)):
        pygame.quit()
