from Maze import Maze

# Test du constructeur de la classe Maze
laby = Maze(4, 4, empty = False)
laby.empty()
laby.add_wall((0, 0), (0, 1))
laby.add_wall((1, 1), (1, 0))
laby.add_wall((1, 1), (0, 1))
print(laby)
print(laby.get_contiguous_cells((0, 0)))