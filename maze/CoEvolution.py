from Maze import Maze
from Solver import Solver
import os
import sys
current = os.path.dirname(os.path.realpath(__file__))
parent_directory = os.path.dirname(current)
sys.path.append(parent_directory + "/solver")
from GeneticSolver import GeneticSolver

class CoEvolver:

	def __init__(self, x, y, mazeCount, solverCount, initialLength, lengthenPeriod, mu, lam):
		if x < 1 or x < 1:
			raise ValueError("Maze of size " + str(self.size) + " is invalid")
		else:
			self.mazes = []
			self.solvers = []
			for i in range(mazeCount):
				self.mazes.append(Maze(x, y))
			for j in range(solverCount):
				self.solvers.append(GeneticSolver(initialLength))
			self.lengthenPeriod = lengthenPeriod
			self.mu = mu
			self.lam = lam
			self.mazeCount = mazeCount
			self.solverCount = solverCount


	def tracePath(self, solverPath, maze, start):
		# trace path of solver on maze
		# 0 is stop, 1 is north, 2 is south, 3 is east, 4 is west
		path = []
		current = start
		print(current)
		for i in range(len(solverPath)):
			print(solverPath[i])
			if solverPath[i] == 0:
				continue
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
	
	def evaluateMaze(self, maze):
		euc = lambda x1, x2, y1, y2: ((x1-x2)**2 + (y1-y2)**2)**0.5
		initial_distance = euc(maze.start[0], maze.end[0], maze.start[1], maze.end[1])
		total_fitness = 0
		for solver in self.solvers:
			
			path = self.tracePath(solver.asGeneticObject(), maze, maze.start)
			lastOnGoal = -1
			for i in range(len(path)):
				if path[i] == maze.end:
					if lastOnGoal == -1:
						lastOnGoal = i
				else:
					lastOnGoal = -1
			total_distance = euc(path[-1][0], maze.end[0], path[-1][1], maze.end[1])
			total_fitness += (lastToGoal if lastToGoal != -1 else len(path)) / (2 - (total_distance / initial_distance))
		return total_fitness / len(self.solvers)
		
	def survivorSelection(self, algorithm="mg"):
		match algorithm:
			case "mg":
				# Will use mu+lambda selection just to test
				# We have 2 weeks to revise if this is a bad choice,
				# but we're under a bit of time pressure
				mazes = []
				for maze in self.mazes:
					mazes.append((maze, self.evaluateMaze(maze)))
				fitness = sorted(mazes, key=lambda x: x[1], reverse=True)
				self.mazes = [x[0] for x in fitness][:self.mazeCount]
			case "ms":
				# Will use mu+lambda selection just to test
				# We have 2 weeks to revise if this is a bad choice,
				# but we're under a bit of time pressure
				solvers = []
				for solver in self.solvers:
					solvers.append((solver, self.evaluateSolver(solver)))
				fitness = sorted(solvers, key=lambda x: x[1], reverse=True)
				self.solvers = [x[0] for x in fitness][:self.solverCount]				
				
	def parentSelection(self, algorithm="mg"):
		match algorithm:
			case "mg":
				parent1 = random.choice(self.mazes)
				parent2 = random.choice(self.mazes)
			case "ms":
				parent1 = random.choice(self.solvers)
				parent2 = random.choice(self.solvers)
		return parent1, parent2


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
	evolver = CoEvolver(10, 10, 100, 100, 25, 5)

	maze.display()

	# DFSPath = Solver(mazeSize, mazeSize, maze.start, maze.end, maze.maze)
	# DFSPath.DFS()
	# DFSPath = DFSPath.path

	# for i in range(coevolveGen):
	#	  # evaluate fitness of solver on maze and DFS
	#	  fitness = evaluate(maze, solver, DFSPath)
