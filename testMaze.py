from Maze import Maze

# Test du constructeur de la classe Maze
laby = Maze(4, 4, empty = False)
laby.empty()
print(laby)
print(laby.get_walls())
