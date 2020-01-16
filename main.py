import sys
from go import Player, Background, Meteorite
import pygame


pygame.init()
pygame.display.set_caption('Asteroid Destroyer')
screen = pygame.display.set_mode((900, 720))
clock = pygame.time.Clock()


pygame.mixer.music.load('data/music1.mp3')
pygame.mixer_music.play(-1)

all_object = pygame.sprite.Group()
plasmoids = pygame.sprite.Group()
meteors = pygame.sprite.Group()

player = Player(clock, plasmoids)
background = Background()
meteorite = Meteorite()

score_count = 0
life = 1

all_object.add(background)
all_object.add(player)
all_object.add(meteorite)

run = True

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((255, 255, 255))
    Meteorite.process_meteors(clock, meteors)

    all_object.update()
    plasmoids.update()
    meteors.update()

    plasmoids_and_meteors_collided = pygame.sprite.groupcollide(meteors, plasmoids, True, True)
    player_and_meteors_collided = pygame.sprite.spritecollide(player, meteors, False)

    if plasmoids_and_meteors_collided:
        score_count += 1
    all_object.draw(screen)
    plasmoids.draw(screen)
    meteors.draw(screen)
    if player_and_meteors_collided:
        all_object.remove(player)
        life = 0
    if life == 0:
        font = pygame.font.Font('data/cosmic.otf', 33)
        scoretext = font.render(f"Your score: {score_count}", 1, (255, 100, 0))
        screen.blit(scoretext, (280, 300))
        dead = font.render("You lose! Press W to restart.", 1, (255, 100, 0))
        screen.blit(dead, (900 / 2 - 380, 720 / 2))
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        all_object.add(player)
        life = 1
        score_count = 0
    if keys[pygame.K_p] and life != 0:
        pause()
    font = pygame.font.Font('data/cosmic.otf', 35)
    score = font.render(f"Score: {score_count}", 1, (255, 255, 255))
    screen.blit(score, (650, 20))
    pygame.display.flip()
    clock.tick(75)

    def pause():
        pygame.mixer_music.pause()
        paused = True
        while paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            keys = pygame.key.get_pressed()
            font = pygame.font.Font('data/cosmic.otf', 30)
            pausetext = font.render("Game is paused! Press W to continue", 1, (255, 100, 0))
            screen.blit(pausetext, (60, 300))
            if keys[pygame.K_w]:
                pygame.mixer_music.unpause()
                paused = False
            pygame.display.flip()
            clock.tick(15)
