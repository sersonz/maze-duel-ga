from Maze import Maze
from Solver import Solver
from GeneticSolver import GeneticSolver


def tracePath(solverPath, start):
    # trace path of solver on maze
    # 0 is stop, 1 is north, 2 is south, 3 is east, 4 is west
    path = []
    current = start
    print(current)
    for i in range(len(solverPath)):
        print(solverPath[i])
        if solverPath[i] == 0:
            break
        elif solverPath[i] == 1:
            nextMove = (current[0], current[1] - 1)
            if nextMove[1] < 0 or nextMove[1] > len(maze.maze[0]):
                pass
            else:
                current = nextMove
        elif solverPath[i] == 2:
            nextMove = (current[0], current[1] + 1)
            if nextMove[1] < 0 or nextMove[1] > len(maze.maze[0]):
                pass
            else:
                current = nextMove
        elif solverPath[i] == 3:
            nextMove = (current[0] + 1, current[1])
            if nextMove[0] < 0 or nextMove[0] > len(maze.maze):
                pass
            else:
                current = nextMove
        elif solverPath[i] == 4:
            nextMove = (current[0] - 1, current[1])
            if nextMove[0] < 0 or nextMove[0] > len(maze.maze):
                pass
            else:
                current = nextMove
        path.append(current)
    return path


def evaluate(maze, solver, DFSPath):
    # evaluate fitness of solver on maze and DFS
    fitness = 0
    for i in range(len(solverPath)):
        if solverPath[i] == DFSPath[i]:
            fitness += 1
    return fitness


if __name__ == "__main__":

    coevolveGen = 5
    mazeGen = 100
    mazePop = 100
    mazeSize = 10
    # generate maze
    maze = Maze(mazeSize, mazeSize)
    method = "genetic"
    maze.initMaze(method, mazePop, mazeGen)

    geneticMaze = maze.asGeneticObject()

    # generate solver
    solverLength = len(geneticMaze)
    solver = GeneticSolver(solverLength)
    solver.init()
    geneticPath = solver.string
    print(geneticPath)
    # trace path of solver on maze
    solverPath = tracePath(geneticPath, maze.start)
    print(solverPath)

    maze.display()

    # DFSPath = Solver(mazeSize, mazeSize, maze.start, maze.end, maze.maze)
    # DFSPath.DFS()
    # DFSPath = DFSPath.path

    # for i in range(coevolveGen):
    #     # evaluate fitness of solver on maze and DFS
    #     fitness = evaluate(maze, solver, DFSPath)
