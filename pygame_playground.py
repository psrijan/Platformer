import pygame
pygame.init()
running = True

size = (800, 500)
screen = pygame.display.set_mode(size)

pygame.mixer.init()
sountType = pygame.mixer.Sound("./assets/sounds/coin.wav")
sountType.set_volume(.2)
sountType.play()

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.set_caption("My Pygame Window")
    screen.fill((0,0,0))

    missle = pygame.image.load("./assets/objects/missile.gif").convert_alpha()
    missle.get_rect().center = (200, 200)


    missle2 = pygame.image.load("./assets/objects/granade.gif").convert_alpha()
    missle2.get_rect().center = (220, 200)

    screen.blit(missle, missle.get_rect())
    screen.blit(missle2, missle2.get_rect())

    pygame.draw.rect(screen, (0, 200, 0), (200, 300, 300, 300))
    pygame.draw.line(screen, (0, 0, 100), (100, 100), (700, 500), 5)
    pygame.display.flip()

    if missle.get_rect().colliderect(missle2.get_rect()):
        print('collision')
pygame.quit()

class Box(pygame.sprite.Sprite):

    def __init__(self):
        pass
