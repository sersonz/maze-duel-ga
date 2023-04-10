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

class CoEvolver:

	def __init__(self, x, y, mazeCount, solverCount, initialLength, lengthenPeriod):
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
		# trace path of solver on maze
		# 0 is stop, 1 is north, 2 is south, 3 is east, 4 is west
		path = []
		current = start
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
				if nextMove[0] < 0 or nextMove[0] >= len(maze.maze):
					pass
				else:
					current = nextMove
			elif direction == 4:
				nextMove = (current[0] - 1, current[1])
				if nextMove[0] < 0 or nextMove[0] >= len(maze.maze):
					pass
				else:
					current = nextMove
			path.append(current)
		return path
	
	def evaluateMaze(self, maze):
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
		euc = lambda x1, x2, y1, y2: ((x2-x1)**2 + (y2-y1)**2)**0.5
		total_fitness = 0
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
		return (total_fitness / len(self.mazes)) * solver.radiation
		
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
				fitness = sorted(solvers, key=lambda x: x[1])
				self.solvers = [x[0] for x in fitness][:self.solverCount]				
				
	def parentSelection(self, algorithm="mg"):
		match algorithm:
			case "mg":
				result = []
				mating_pool_size = len(self.mazes)
				tournament_size = 10
				for i in range(mating_pool_size):
					members = random.sample(self.mazes, tournament_size)
					fitnesses = [(x, self.evaluateMaze(x)) for x in members]
					fitnesses = sorted(fitnesses, key=lambda x: x[1], reverse=True)
					result.append(fitnesses[0][0])
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
		print("Generation " + str(self.currentGen) + ": " + str(fitness_mg / len(self.mazes)) + "/" + str(fitness_ms / len(self.solvers)))
		self.currentGen += 1
		
	def showAllMazes(self):
		# for maze in self.mazes:
			# maze.display()
		for maze in self.mazes:
			for solver in self.solvers:
				solver = solver.asGeneticObject()
				# path = self.getPath(solver, maze.start)
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
	evolver.stepMulti(250)
	evolver.showAllMazes()

	# DFSPath = Solver(mazeSize, mazeSize, maze.start, maze.end, maze.maze)
	# DFSPath.DFS()
	# DFSPath = DFSPath.path

	# for i in range(coevolveGen):
	#	  # evaluate fitness of solver on maze and DFS
	#	  fitness = evaluate(maze, solver, DFSPath)
