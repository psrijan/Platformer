import pygame
from pygame.surface import Surface

def clip(surface: Surface, x, y, x_size, y_size):
    copied_surface = surface.copy()
    clip = pygame.Rect(x, y, x_size, y_size)
    copied_surface.set_clip(clip)
    img = surface.subsurface(copied_surface.get_clip())
    return img.copy()

def clip2(surface, x, y, x_size, y_size): #Get a part of the image
    handle_surface = surface.copy() #Sprite that will get process later
    clipRect = pygame.Rect(x,y,x_size,y_size) #Part of the image
    handle_surface.set_clip(clipRect) #Clip or you can call cropped
    image = surface.subsurface(handle_surface.get_clip()) #Get subsurface
    return image.copy() #Return


def generate_coins(screen, imgLoc, startX, startY, count, scale=1):
    img = pygame.image.load(imgLoc).convert_alpha()
    img = clip2(img, 0, 0, 20, 20)
    img = pygame.transform.scale(img, (img.get_width() * scale, img.get_height() * scale))
    offset = 22 # keeping a default offset of 20px
    for i in range(0, count):
        rect = img.get_rect()
        rect.centerx = startX + offset * i
        rect.centery = startY
        screen.blit(img, rect)

def generate_bar(screen, imgLoc, startX, startY, amountLeft, totalAmount, bar_type, text='', scale=1):
    pass
    # ft = pygame.font.SysFont('Comic Sans MS', 30)
    # font_surface = ft.render("hello world", False, (200, 200, 200))
    # screen.blit(font_surface, (10, 10))
    img = pygame.image.load(imgLoc).convert_alpha()
    img = pygame.transform.scale(img, (img.get_width() * scale, img.get_height() * scale))
    img.get_rect()

    img_rect = img.get_rect()
    img_rect.center = (startX, startY)
    screen.blit(img, img_rect)
    width = 100
    height = 10
    actual_width = int((amountLeft * width) / totalAmount)

    if bar_type == 'BAR':
        pygame.draw.rect(screen, "white",  [startX + 14, startY - 2, width + 4, 10 + 4])
        pygame.draw.rect(screen, "red", [startX + 16, startY, width, height])
        pygame.draw.rect(screen, "green", [startX + 16, startY, actual_width, height])
    elif bar_type == 'xTEXT':
        ft = pygame.font.SysFont('Comic Sans MS', 11)
        font_surface = ft.render('X {}'.format(text), False, (200, 200, 200))
        screen.blit(font_surface, (startX + 30, startY))

