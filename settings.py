WIDTH = 1280
HEIGHT = 720
FPS = 60
TITLE = "Goats also have dreams"


# Dimensions du labyrinthe
CELL_SIZE = 150
STARTPOS = (WIDTH//2-0.25*CELL_SIZE, HEIGHT//2-0.25*CELL_SIZE)
# STARTPOS = (CELL_SIZE*1.25,CELL_SIZE*1.25)

# Vitesse du joueur
VELOCITY = CELL_SIZE

# Taille du joueur
PLAYER_WIDTH = CELL_SIZE//2
PLAYER_HEIGHT = CELL_SIZE//2

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 150, 150)
WALL_COLOR = (20, 20, 20)

# Item info

ITEM_WIDTH = CELL_SIZE/2
ITEM_HEIGHT = CELL_SIZE/2

# Wall and path info
WALL = 0
PATH = 1
SOLUCE = 2
