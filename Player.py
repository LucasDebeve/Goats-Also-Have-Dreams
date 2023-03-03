import pygame
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self,game, x, y):
        super().__init__()
        self.game = game
        self.health = 3
        self.maxHelath = 3
        self.velocity = VELOCITY
        # Changer la taille de l'image
        self.image = pygame.image.load("./assets/anims/player/right1.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (PLAYER_WIDTH, PLAYER_HEIGHT))
        # Afficher les contours de l'image
        self.image.set_colorkey(BLACK)
        
        # Animation
        self.imagesRight = []
        self.imagesLeft = []
        self.imagesUp = []
        self.imagesDown = []
        for i in range(1,5):
            self.imagesRight.append(pygame.image.load(f"./assets/anims/player/right{str(i)}.png").convert_alpha())
            self.imagesLeft.append(pygame.image.load(f"./assets/anims/player/left{str(i)}.png").convert_alpha())
            self.imagesUp.append(pygame.image.load(f"./assets/anims/player/up{str(i)}.png").convert_alpha())
            self.imagesDown.append(pygame.image.load(f"./assets/anims/player/down{str(i)}.png").convert_alpha())
        self.facing = "RIGHT"

        self.index = 0

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    def update(self):
        self.index += 1
        pygame.time.delay(50)
        if self.facing == "RIGHT":
            self.index = self.index % len(self.imagesRight)
            self.image = self.imagesRight[self.index]
        elif self.facing == "LEFT":
            self.index = self.index % len(self.imagesLeft)
            self.image = self.imagesLeft[self.index]
        elif self.facing == "UP":
            self.index = self.index % len(self.imagesUp)
            self.image = self.imagesUp[self.index]
        elif self.facing == "DOWN":
            self.index = self.index % len(self.imagesDown)
            self.image = self.imagesDown[self.index]
        
        

    def move_up(self):
        self.facing = "UP"
        self.game.cam_y += self.velocity
    
    def move_down(self):
        self.facing = "DOWN"
        self.game.cam_y -= self.velocity
    
    def move_left(self):
        self.facing = "LEFT"
        self.game.cam_x += self.velocity
    
    def move_right(self):
        self.facing = "RIGHT"
        self.game.cam_x -= self.velocity

    def dead(self):
        # Respawn du joueur
        if self.health > 1:
            self.health -= 1
            self.game.cam_x = STARTPOS[0]-1.2*CELL_SIZE
            self.game.cam_y = STARTPOS[1]-1.2*CELL_SIZE
            # Afficher un message de mort
            self.game.display_message(f"/tp @p 0 0 : {self.health} vies", (255,0,0), size=100)
            pygame.time.delay(1000)
        else:
            # Afficher un message de game over
            self.game.display_message("VOUS AVEZ PERI", (255,0,0), size=100)
            self.game.display_message("RATIO SANDRON", (255,0,255), size=30, delay=400)
            self.game.running = False
    
    def addLife(self):
        if (self.health > 0 and self.health < self.maxHelath):
            self.health += 1
            self.game.display_message("VIE +1", (255, 255, 0), size=50, delay=500)
        else:
            self.game.display_message("VIE MAX", (255, 200, 0), size=50, delay=500)
