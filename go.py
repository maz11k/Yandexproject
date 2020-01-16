import pygame
from random import randint


pygame.init()


pew = pygame.mixer.Sound('data/pew.wav')


class Player(pygame.sprite.Sprite):
    def __init__(self, clock, plasmoids):
        super(Player, self).__init__()
        self.image = pygame.image.load('data/spaceship.png')
        self.clock = clock
        self.plasmoids = plasmoids
        self.rect = self.image.get_rect()
        self.rect.centerx = 900 / 2
        self.rect.bottom = 720 - 10
        self.max_speed = 10
        self.current_speed = 0
        self.shooting_cooldown = 450
        self.current_shooting_cooldown = 0

    def update(self, *args):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and self.rect.centerx > 0:
            self.current_speed = - self.max_speed
        elif keys[pygame.K_d] and self.rect.centerx < 900:
            self.current_speed = self.max_speed
        else:
            self.current_speed = 0
        self.rect.move_ip((self.current_speed, 0))
        self.process_shooting()

    def process_shooting(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.current_shooting_cooldown <= 0:
            self.plasmoids.add(Plasmoid(self.rect.midtop))
            self.current_shooting_cooldown = self.shooting_cooldown
            pygame.mixer.Sound.play(pew)
        else:
            self.current_shooting_cooldown -= self.clock.get_time()
        for plasmoid in list(self.plasmoids):
            if plasmoid.rect.bottom < 0:
                self.plasmoids.remove(plasmoid)


class Background(pygame.sprite.Sprite):
    def __init__(self):
        super(Background, self).__init__()
        self.image = pygame.image.load('data/space.jpeg')
        self.rect = self.image.get_rect()
        self.rect.bottom = 720

    def update(self, *args):
        self.rect.bottom += 5
        if self.rect.bottom >= self.rect.height:
            self.rect.bottom = 720


class Plasmoid(pygame.sprite.Sprite):
    def __init__(self, position):
        super(Plasmoid, self).__init__()
        self.image = pygame.image.load('data/plasmoid.png')
        self.rect = self.image.get_rect()
        self.rect.midbottom = position
        self.speed = - 15

    def update(self, *args):
        self.rect.move_ip((0, self.speed))


class Meteorite(pygame.sprite.Sprite):
    cooldown = 250
    current_cooldown = 0
    speed = 10

    def __init__(self):
        super(Meteorite, self).__init__()
        self.image = pygame.image.load('data/meteorite.png')
        self.rect = self.image.get_rect()
        self.rect.midbottom = (randint(0, 900), 0)

    def update(self, *args):
        self.rect.move_ip((0, self.speed))

    @staticmethod
    def process_meteors(clock, meteorites):
        if Meteorite.current_cooldown <= 0:
            meteorites.add(Meteorite())
            Meteorite.current_cooldown = Meteorite.cooldown
        else:
            Meteorite.current_cooldown -= clock.get_time()
        for m in list(meteorites):
            if m.rect.right < 0 or m.rect.left > 900 or m.rect.top > 720:
                meteorites.remove(m)

