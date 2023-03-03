import pygame
from pygame import mixer
import sys
from random import randrange
# Importation des constantes
from settings import *
# Importation des classes
from Maze import Maze
from Player import Player
from Item import Item
from debug import *


class Game:
    def __init__(self, width : int, height : int) -> None:
        """
        Constructeur de la classe Game
        Args:
            width (int): largeur de départ du labyrinthe
            height (int): hauteur de départ du labyrinthe
        """
        pygame.init()
        pygame.display.set_caption(TITLE)
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.width = width
        self.height = height
        self.nLevel = 0
        self.newLevel(0)
        # Ajout de la musique - A ajouter
        mixer.music.load("./assets/sounds/music.wav")
        mixer.music.play(-1)

        # Lancer le jeu
        self.run()
    
    def newLevel(self, difficulty : float) -> None:
        if self.nLevel == 14:
            # Ecran de fin
            self.display_message("Fin du jeu", (255, 255, 0), size=150, delay=1000)
        else:
            # Verifie l'existance d'un niveau precedent
            if difficulty != 0:
                # Jouer le son de victoire
                Sound = mixer.Sound(f"./assets/sounds/{self.nLevel}.mp3")
                mixer.Sound.play(Sound)
                # Recuperer la durée de la musique
                duration = mixer.Sound.get_length(Sound)
                # Afficher le message de victoire
                self.display_message(
                "Niveau suivant", (255, 255, 0), size=150, delay=int(duration*1000+500))
            else:
                self.difficulty = 0
            self.nLevel += 1
            self.items_sprites = pygame.sprite.Group()
            # Génération du labyrinthe
            i = 0
            while self.difficulty <= difficulty:
                i += 1
                if i < 20:
                    self.maze = Maze.gen_fusion(self.height, self.width)
                    print(self.maze)
                    self.difficulty = round(self.maze.distance_geo(
                        (0, 0), (self.height-1, self.width-1)) / self.maze.distance_man((0, 0), (self.height-1, self.width-1)), 2)
                    print(self.difficulty)
                else:
                    self.width += 1
                    self.height += 1
                    i = 0
            self.maze_surface = pygame.Surface(
                (2*self.width * CELL_SIZE, 2*self.height * CELL_SIZE))
            self.maze_surface.fill((50, 50, 50))
            self.mat = self.maze.get_mat()

            # Ajout du joueur
            self.player = Player(
                self, STARTPOS[0], STARTPOS[1])
            self.obstacles_sprites = pygame.sprite.Group()

            # Ajout de la fin du niveau
            self.endPoint = Item(self, 2*self.width*CELL_SIZE-0.75*CELL_SIZE,
                                2*self.height*CELL_SIZE-0.75*CELL_SIZE, 0, "assets/endPoint.png")
            self.items_sprites.add(self.endPoint)
            self.cam_x = 0
            self.cam_y = 0
            self.isPaused = False

            # Ajout des items de vie
            self.potion = []
            for i in range(0, self.width * self.height // 10):
                x = randrange(1, 2*self.width-1, 2)
                y = randrange(1, 2*self.height-1, 2)
                while (x,y) == (1,1) or (x,y) == (2*self.width-1,2*self.height-1):
                    x = randrange(1, 2*self.width-1, 2)
                    y = randrange(1, 2*self.height-1, 2)
                self.potion.append(Item(self, CELL_SIZE*x+0.25*CELL_SIZE,
                                CELL_SIZE*y+0.25*CELL_SIZE, 2, "assets/potion.png"))
                self.items_sprites.add(self.potion[-1])
    
    def run(self) -> None:
        # Boucle du jeu
        while self.running:
            self.clock.tick(FPS)
            self.handling_event()
            self.update()
            self.display()
    
    def handling_event(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if self.running:
                    self.running = False

            # Input de déplacement du joueur
            elif event.type == pygame.KEYDOWN:
                if not self.isPaused and event.key == pygame.K_UP:
                    self.player.move_up()
                elif not self.isPaused and event.key == pygame.K_DOWN:
                    self.player.move_down()
                elif not self.isPaused and event.key == pygame.K_LEFT:
                    self.player.move_left()
                elif not self.isPaused and event.key == pygame.K_RIGHT:
                    self.player.move_right()

    def update(self):
        # Music loop
        if not mixer.music.get_busy():
            mixer.music.play(-1)
        
        self.player.update()
        self.endPoint.update()
        # Vérifier la collision avec les obstacles
        if pygame.sprite.spritecollide(self.player, self.obstacles_sprites, False):
            self.isPaused = True
            self.player.dead()
            self.isPaused = False
        # Vérifier la collision avec les items
        hits = pygame.sprite.spritecollide(
            self.player, self.items_sprites, False)
        if hits:
            for hit in hits:
                if hit.id == 0:
                    self.isPaused = True
                    self.newLevel(self.difficulty)
                elif hit.id == 1:
                    # Fil d'ariane
                    pass
                elif hit.id == 2:
                    self.player.addLife()
                elif hit.id == 3:
                    self.player.dead()

                hit.kill()
    
    def display(self):
        self.screen.fill((0, 0, 0))
        self.obstacles_sprites.empty()
        # Dessiner le labyrinthe
        for i in range(len(self.mat)):
            for j in range(len(self.mat[i])):
                if self.mat[i][j] == WALL:

                    pygame.draw.rect(self.maze_surface, BLACK, (j * CELL_SIZE,
                                                                i * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                    # Création des obstacles
                    obstacle = pygame.sprite.Sprite()
                    obstacle.image = pygame.Surface((CELL_SIZE, CELL_SIZE))
                    obstacle.rect = obstacle.image.get_rect()
                    obstacle.rect.x = j * CELL_SIZE + self.cam_x
                    obstacle.rect.y = i * CELL_SIZE + self.cam_y
                    self.obstacles_sprites.add(obstacle)
                elif self.mat[i][j] == PATH:
                    pygame.draw.rect(self.maze_surface, WHITE, (j * CELL_SIZE,
                                                                i * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        for item in self.items_sprites:
            item.rect.x = item.x + self.cam_x
            item.rect.y = item.y + self.cam_y
            item.render(self.maze_surface)
        # Debug FPS
        debug(str(int(self.clock.get_fps())), 10, 10)

        # Afficher le labyrinthe
        self.screen.blit(self.maze_surface, (self.cam_x, self.cam_y))
        # Appliquer l'image du joueur
        self.screen.blit(self.player.image, self.player.rect)
        pygame.display.flip()

    def display_message(self, message, color=(255, 255, 255), background=(0, 0, 0), size=30, delay=2000):
        font = pygame.font.SysFont("timesnewroman", size)
        text = font.render(message, 1, color, background)
        self.screen.blit(text, (WIDTH/2 - text.get_width() /
                         2, HEIGHT/2 - text.get_height()/2))
        pygame.display.flip()
        pygame.time.delay(delay)



if __name__ == "__main__":
    g = Game(5,5)
    pygame.quit()
    sys.exit()