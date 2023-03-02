from Maze import Maze

# Test du constructeur de la classe Maze
laby = Maze(4, 4, empty = True)
laby.add_wall((0, 0), (0, 1))
laby.remove_wall((0, 1), (0, 0))
print(laby)