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