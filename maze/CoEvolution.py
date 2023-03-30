from Maze import Maze
from Solver import Solver


if __name__ == "__main__":

    # GENERATIONS = 100
    # POPULATION = 100
    maze = Maze(20, 20)
    maze.initMaze()
    maze.display()
    geneticMaze = maze.asGeneticObject()

    solver = Solver(geneticMaze, maze.x, maze.y, maze.start, maze.end)
    pathDFS = solver.DFS()

    if pathDFS:
        solver.displayPath()

    else:
        print("No path found")
