from Maze import Maze

# Test de la classe Maze
"""
laby = Maze(4, 4, empty = False)
laby.empty()
laby.add_wall((0, 0), (0, 1))
laby.add_wall((1, 1), (1, 0))
laby.add_wall((1, 1), (0, 1))
print(laby)
print(laby.get_walls())
"""

# Test des méthodes de générations
laby = Maze.gen_btree(4, 4)
laby = Maze.gen_sidewinder(4, 4)
laby = Maze.gen_fusion(4, 4)
laby = Maze.gen_exploration(4, 4)
print(laby)