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
from time import time


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
        if self.nLevel == 10:
            # Écran de fin
            self.display_message("Fin du jeu", (255, 255, 0), size=150, delay=1000)
        else:
            # Vérifie l’existante d'un niveau precedent
            if difficulty != 0:
                # Jouer le son de victoire
                Sound = mixer.Sound(f"./assets/sounds/{self.nLevel}.mp3")
                mixer.Sound.play(Sound)
                # Récupérer la durée de la musique
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
            while self.difficulty <= difficulty or (difficulty != 0 and self.difficulty > difficulty + 0.1) or (difficulty == 0 and self.difficulty > 1.05):
                i += 1
                if i < 100:
                    self.maze = Maze.gen_fusion(self.height, self.width)
                    self.difficulty = round(self.maze.distance_geo(
                        (0, 0), (self.height-1, self.width-1)) / self.maze.distance_man((0, 0), (self.height-1, self.width-1)), 2)
                else:
                    self.width += 2
                    self.height += 2
                    i = 0
            
            # Affichage de la solution dans le terminal
            solution = self.maze.solve_bfs((0, 0), (self.height-1, self.width-1))
            str_solution = {c:'*' for c in solution}

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
            self.cam_x = int(STARTPOS[0]-1.2*CELL_SIZE)
            self.cam_y = int(STARTPOS[1]-1.2*CELL_SIZE)
            self.isPaused = False

            # Ajout des items
            self.potion = []
            self.ariane = []
            itemsCoords = [(1,1), (2*self.width-1,2*self.height-1)]
            for i in range(0, self.width * self.height // 10):
                # Potion de vie
                x = randrange(1, 2*self.width-1, 2)
                y = randrange(1, 2*self.height-1, 2)
                while (x,y) in itemsCoords:
                    x = randrange(1, 2*self.width-1, 2)
                    y = randrange(1, 2*self.height-1, 2)
                itemsCoords.append((x,y))
                self.potion.append(Item(self, CELL_SIZE*x+0.25*CELL_SIZE,
                                CELL_SIZE*y+0.25*CELL_SIZE, 2, "assets/potion.png"))
                self.items_sprites.add(self.potion[-1])
                
                # Fil d'Ariane
                if i % 5 == 1:
                    x1 = randrange(1, 2*self.width-1, 2)
                    y1 = randrange(1, 2*self.height-1, 2)
                    while (x1,y1) in itemsCoords:
                        x1 = randrange(1, 2*self.width-1, 2)
                        y1 = randrange(1, 2*self.height-1, 2)
                    itemsCoords.append((x1,y1))
                    str_solution[(int(y1/2),int(x1/2))] = "@"
                    self.ariane.append(Item(self, CELL_SIZE*x1+0.25*CELL_SIZE,
                                    CELL_SIZE*y1+0.25*CELL_SIZE, 1, "assets/ariane.png"))
                    self.items_sprites.add(self.ariane[-1])

            
            print(self.maze.overlay(str_solution))
            print(self.difficulty)


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
                    print(int( abs(self.cam_y-int(STARTPOS[1]-1.2*CELL_SIZE))//(2*CELL_SIZE)), int( abs((self.cam_x-int(STARTPOS[0]-1.2*CELL_SIZE))//(2*CELL_SIZE)) ) )
                    soluce = self.maze.solve_dfs((int( abs(self.cam_y-int(STARTPOS[1]-1.2*CELL_SIZE))//(2*CELL_SIZE)), int( abs((self.cam_x-int(STARTPOS[0]-1.2*CELL_SIZE))//(2*CELL_SIZE)) ) ), (self.width-1, self.height-1))
                    self.start_time = time()
                    self.display_soluce(soluce)
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
                else:
                    pygame.draw.rect(self.maze_surface, WHITE, (j * CELL_SIZE,
                                                                i * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                if SOLUCE in self.mat[i]:
                    if self.mat[i][j] == SOLUCE:
                        pygame.draw.rect(self.maze_surface, RED, (j * CELL_SIZE+1/3*CELL_SIZE,
                                                                    i * CELL_SIZE+1/3*CELL_SIZE, CELL_SIZE//3, CELL_SIZE//3))
                    if time() - self.start_time >= 2:
                        self.hideSoluce()

        for item in self.items_sprites:
            item.rect.x = item.x + self.cam_x
            item.rect.y = item.y + self.cam_y
            item.render(self.maze_surface)
        # Debug FPS
        debug(f"{self.cam_x} {self.cam_y}", 10, 10)

        # Afficher le labyrinthe
        self.screen.blit(self.maze_surface, (self.cam_x, self.cam_y))
        # Appliquer l'image du joueur
        self.screen.blit(self.player.image, self.player.rect)
        pygame.display.flip()

    def display_message(self, message, color=(255, 255, 255), background=(0, 0, 0), size=30, delay=2000):
        font = pygame.font.SysFont("timesnewroman", size)
        text = font.render(message, 1, color, background)
        self.screen.blit(text, (WIDTH/2 - text.get_width() /
                         2, HEIGHT/3 - text.get_height()/2))
        pygame.display.flip()
        pygame.time.delay(delay)

    def display_soluce(self, soluce : list) -> None:
        self.hideSoluce()
        print(soluce)
        for i in range(len(soluce)-1):
            self.mat[(soluce[i][0])*2+1][(soluce[i][1])*2+1] = SOLUCE
            print("(",((soluce[i][0]*2+1)+(soluce[i+1][0])*2+1)//2, ((soluce[i][1]*2+1)+(soluce[i+1][1])*2+1)//2,")")
            # Moyenne entre les deux coordonnées adjacentes
            self.mat[((soluce[i][0]*2+1)+(soluce[i+1][0])*2+1)//2] [((soluce[i][1]*2+1)+(soluce[i+1][1])*2+1)//2] = SOLUCE

    def hideSoluce(self) -> None:
        for i in range(len(self.mat)):
            for j in range(len(self.mat[i])):
                if self.mat[j][i] == SOLUCE:
                    self.mat[j][i] = PATH


if __name__ == "__main__":
    g = Game(5,5)
    pygame.quit()
    sys.exit()