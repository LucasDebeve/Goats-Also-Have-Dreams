import pygame
from settings import *

vec = pygame.math.Vector2

class Item(pygame.sprite.Sprite):
    def __init__(self, game, x, y, itemtype, name):
        super().__init__()
        self.x = x
        self.y = y
        self.game = game
        self.id = itemtype
        self.image = pygame.image.load(name).convert_alpha()
        self.image = pygame.transform.scale(self.image, (ITEM_WIDTH, ITEM_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.pos = vec(x, y)

    def render(self, display):
        display.blit(self.image, self.pos)


# ID = 0 : Point d'arrivée
# ID = 1 : Fil d'Ariane
# ID = 2 : Potion de vie
# ID = 3 : Bombe