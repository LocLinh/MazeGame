from mazelib import Maze
from mazelib.generate.Prims import Prims
from mazelib.solve.BacktrackingSolver import BacktrackingSolver
import numpy as np
from numpy.lib.function_base import iterable

maze_name = 'maze.txt'

def readMaze(filename='maze.txt'):
    file = open(filename, 'r')
    maze = [[]]
    for x in file:
        for item in x:
            if item == '\n':
                maze.append([])
            elif item == '#':
                maze[-1].append(1)
            elif item == ' ':
                maze[-1].append(0)
            elif item == 'S':
                maze[-1].append(1)
            elif item == 'E':
                maze[-1].append(1)
    file.close()
    return np.array(maze)

def mazeGenerate(dimX, dimY):
    m = Maze()
    m.generator = Prims(dimX, dimY)
    m.generate()
    m.solver = BacktrackingSolver()
    m.start = (1, 1)
    m.end = (dimX-1, dimY-1)
    m.generate_entrances(True, True)
    maze = open('maze.txt', 'w')
    maze.write(m.__str__())
    final_maze = readMaze(filename=maze_name)
    return final_maze

# mazeGenerate(15, 15)