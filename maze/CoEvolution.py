from Maze import Maze
import os
import sys
import random
import math
current = os.path.dirname(os.path.realpath(__file__))
parent_directory = os.path.dirname(current)
sys.path.append(parent_directory + "/solver")
from GeneticSolver import GeneticSolver
from Solver import Solver

PROB_TOURNAMENT_SELECTION_NEXT_HIGHEST = 0.75

class CoEvolver:
	def __init__(self, x, y, mazeCount, solverCount, initialLength, lengthenPeriod):
		"""
		CoEvolver initialization method generates a population of mazes and solvers
		:param x: width of maze
		:param y: height of maze
		:param mazeCount: number of mazes to generate
		:param solverCount: number of solvers to generate
		:param initialLength: initial length of solver (to be extended across generations)
		:param lengthenPeriod: number of generations before length of solver is extended
		"""
		if x < 1 or y < 1:
			raise ValueError("Maze of size " + str(self.size) + " is invalid")
		else:
			self.mazes = []
			self.solvers = []
			for i in range(mazeCount):
				maze = Maze(x, y)
				maze.initMaze(method="depth")
				self.mazes.append(maze)
			for j in range(solverCount):
				# set initial length of solver to be euclidean distance between start and end
				initialLength = int(math.sqrt((self.mazes[0].start[0] - self.mazes[0].end[0])**2 + (
				self.mazes[0].start[1] - self.mazes[0].end[1])**2))
				solver = GeneticSolver(initialLength)
				solver.init()
				self.solvers.append(solver)
			self.lengthenPeriod = lengthenPeriod
			self.mazeCount = mazeCount
			self.solverCount = solverCount
			self.currentGen = 1


	def tracePath(self, solverPath, maze, start):
		"""
		Trace the path of a solver on a maze
		:param solverPath: path of solver (a string of 0s, 1s, 2s, 3s, 4s)
		:param maze: maze to trace path on
		:param start: start position of solver
		:return: path of solver on maze
		"""
		# trace path of solver on maze
		# 0 is stop, 1 is north, 2 is south, 3 is east, 4 is west
		path = []
		current = start
		prevMove = current
		for i in range(len(solverPath)):
			direction = int(solverPath[i])
			if direction == 0:
				continue
			elif direction == 1:
				nextMove = (current[0], current[1] - 1)
				if nextMove[1] < 0 or nextMove[1] >= len(maze.maze[0]):
					pass
				else:
					current = nextMove
			elif direction == 2:
				nextMove = (current[0], current[1] + 1)
				if nextMove[1] < 0 or nextMove[1] >= len(maze.maze[0]):
					pass
				else:
					current = nextMove
			elif direction == 3:
				nextMove = (current[0] + 1, current[1])
				if nextMove[0] < 0 or nextMove[0] >= len(maze.maze[1]):
					pass
				else:
					current = nextMove
			elif direction == 4:
				nextMove = (current[0] - 1, current[1])
				if nextMove[0] < 0 or nextMove[0] >= len(maze.maze[1]):
					pass
				else:
					current = nextMove
			if maze.maze[nextMove[0]][nextMove[1]] == 0:
				path.append(current)
			else:
				current = prevMove
		return path
	
	def evaluateMaze(self, maze):
		"""
		Evaluates the fitness of a maze
		Calculates the fitness of a maze by running it against a solver and
		calculating the euclidean distance between the end of the path
		and the end of the maze

		:param maze: maze to be evaluated
		:return: fitness of maze
		"""
		solver = Solver(maze.maze, maze.x, maze.y, maze.start, maze.end)
		dfsPath = solver.DFS()
		# If the maze is unsolvable,
		# assign it a fitness of 1
		if not dfsPath:
			return 1
		euc = lambda x1, x2, y1, y2: ((x1-x2)**2 + (y1-y2)**2)**0.5
		total_fitness = 0
		for solver in self.solvers:
			atEnd = False
			path = self.tracePath(solver.asGeneticObject(), maze, maze.start)
			for i in range(len(path)):
				if path[i] == maze.end:
					atEnd = True
					total_fitness += i
					break
			if not atEnd:	
				total_distance = euc(path[-1][0], maze.end[0], path[-1][1], maze.end[1])
				total_fitness += len(path) * (1 + 1/total_distance)
		return (total_fitness / len(self.solvers)) * maze.radiation
		
	def evaluateSolver(self, solver):
		"""
		Evaluates the fitness of a solver
		Calculates the fitness of a solver by running it on a maze and 
		calculating the euclidean distance between the end of the path 
		and the end of the maze
		
		:param solver: solver to be evaluated
		:return: fitness of solver
		"""
		euc = lambda x1, x2, y1, y2: ((x2-x1)**2 + (y2-y1)**2)**0.5
		total_fitness = 0
		# if the last move of the solver is on the end of the maze,
		# assign it a fitness of 1
		if solver.asGeneticObject()[-1] == 0:
			return 100
		for maze in self.mazes:
			atEnd = False
			path = self.tracePath(solver.asGeneticObject(), maze, maze.start)
			for i in range(len(path)):
				if path[i] == maze.end:
					atEnd = True
					total_fitness += (1 / i)
					break
			if not atEnd:
				total_distance = euc(path[-1][0], maze.end[0], path[-1][1], maze.end[1])
				total_fitness += total_distance / len(path)
		return (total_fitness / len(self.mazes)) 
		
	def survivorSelection(self, algorithm="mg"):
		"""
		Survivor selection algorithm for both mg and ms algorithms
		Both algorithms use mu + lambda selection
		:param algorithm: "mg" or "ms"
		
		"""
		match algorithm:
			case "mg":
				mazes = []
				for maze in self.mazes:
					mazes.append((maze, self.evaluateMaze(maze)))
				fitness = sorted(mazes, key=lambda x: x[1], reverse=True)
				self.mazes = [x[0] for x in fitness][:self.mazeCount]


				# mu = []
				# lambda_ = []
				# for i in range((self.mazeCount)):
				# 	mu.append((self.mazes[i], self.evaluateMaze(self.mazes[i])))
				# for i in range((self.mazeCount), len(self.mazes)):
				# 	lambda_.append((self.mazes[i], self.evaluateMaze(self.mazes[i])))
				# # use mu > lambda selection where lambda offspreing replace the worst lambda individuals in mu
				# mu = sorted(mu, key=lambda x: x[1])
				# lambda_ = sorted(lambda_, key=lambda x: x[1])
				# self.mazes = [x[0] for x in mu[:self.mazeCount]] + [x[0] for x in lambda_[:self.mazeCount]]
			case "ms":
				solvers = []
				for solver in self.solvers:
					solvers.append((solver, self.evaluateSolver(solver)))
				fitness = sorted(solvers, key=lambda x: x[1])
				self.solvers = [x[0] for x in fitness][:self.solverCount]				
				
	def parentSelection(self, algorithm="mg"):
		"""
		Parent selection algorithm for both mg and ms algorithms
		Both algorithms use tournament selection
		:param algorithm: "mg" or "ms"
		:return: list of parents
		"""
		match algorithm:
			case "mg":
				result = []
				mating_pool_size = len(self.mazes)
				tournament_size = 10
				for i in range(mating_pool_size):
					members = random.sample(self.mazes, tournament_size)
					fitnesses = [(x, self.evaluateMaze(x)) for x in members]
					fitnesses = sorted(fitnesses, key=lambda x: x[1], reverse=True)
					selection = random.random()
					winnerIndex = 0
					while(selection != PROB_TOURNAMENT_SELECTION_NEXT_HIGHEST * (1 - PROB_TOURNAMENT_SELECTION_NEXT_HIGHEST) ** winnerIndex):
						winnerIndex += 1
						if winnerIndex == len(fitnesses) - 1:
							break
					result.append(fitnesses[winnerIndex][0])
			case "ms":
				result = []
				mating_pool_size = len(self.solvers)
				tournament_size = 10
				for i in range(mating_pool_size):
					members = random.sample(self.solvers, tournament_size)
					fitnesses = [(x, self.evaluateSolver(x)) for x in members]
					fitnesses = sorted(fitnesses, key=lambda x: x[1], reverse=True)
					result.append(fitnesses[0][0])
		return result
		
	def step(self):
		"""
		Driver function for a single step of the genetic algorithm
		For both mg and ms algorithms, this function does the following:
			1. Select parents
			2. Crossover parents
			3. Mutate children
			4. Add children to population
			5. Select survivors

		Calculates average fitnesses for all mazes and solvers in the population 

		"""
		parents = self.parentSelection(algorithm="mg")
		for j in range(len(parents) - 1):
			mgChild1, mgChild2 = parents[j].crossover(parents[j+1])
			mgChild1 = mgChild1.mutate()
			mgChild2 = mgChild2.mutate()
			for child in [mgChild1, mgChild2]:
				if child != None:
					self.mazes.append(child)
		parents = self.parentSelection(algorithm="ms")
		for j in range(len(parents) - 1):
			mgChild1, mgChild2 = parents[j].crossover(parents[j+1])
			mgChild1 = mgChild1.mutate()
			mgChild2 = mgChild2.mutate()
			for child in [mgChild1, mgChild2]:
				if child != None:
					self.solvers.append(child)
		self.survivorSelection(algorithm="mg")
		self.survivorSelection(algorithm="ms")
		# Step 6: If we are at the lengthen period, lengthen all current solvers
		if self.currentGen % self.lengthenPeriod == 0:
			for solver in self.solvers:
				solver.lengthen(1)
		# Show current figures
		fitness_mg = 0
		fitnesses_mg = []
		fitnesses_ms = []
		fitness_ms = 0
		for maze in self.mazes:
			fitness = self.evaluateMaze(maze)
			fitness_mg += fitness
			fitnesses_mg.append(fitness)
		for solver in self.solvers:
			fitness = self.evaluateSolver(solver)
			fitness_ms += fitness
			fitnesses_ms.append(fitness)
		# print("Generation " + str(self.currentGen) + ": " + str(fitness_mg / len(self.mazes)) + "/" + str(fitness_ms / len(self.solvers)))

		print("                 +--------+---------+")
		print(" Generation {:03d}: | Mazes  | Solvers |".format(self.currentGen))
		print("+----------------+--------+---------+")
		print("| Avg Fitness    | {:.3f} | {:.3f}   |".format(fitness_mg / len(self.mazes), fitness_ms / len(self.solvers)))
		print("+----------------+--------+---------+")
		self.currentGen += 1
		
	def showAllMazes(self):
		"""
		Displays all mazes and their solutions generated by DFS and the genetic solver
		"""
		for maze in self.mazes:
			for solver in self.solvers:
				solver = solver.asGeneticObject()
				geneticPath = self.tracePath(solver, maze, maze.start)
				solverDFS = Solver(maze.maze, maze.x, maze.y, maze.start, maze.end)
				solverDFS.DFS()
				DFSPath = solverDFS.finalPath
				if geneticPath != []:
					maze.display(DFSPath, geneticPath)
			
	def stepMulti(self, steps=1):
		for i in range(steps):
			self.step()
		
		

if __name__ == "__main__":

	coevolveGen = 5
	mazeGen = 100
	mazePop = 100
	mazeSize = 10
	# generate maze
	evolver = CoEvolver(10, 10, 25, 25, 10, 10)
	evolver.stepMulti(500)
	evolver.showAllMazes()

	# DFSPath = Solver(mazeSize, mazeSize, maze.start, maze.end, maze.maze)
	# DFSPath.DFS()
	# DFSPath = DFSPath.path

	# for i in range(coevolveGen):
	#	  # evaluate fitness of solver on maze and DFS
	#	  fitness = evaluate(maze, solver, DFSPath)
