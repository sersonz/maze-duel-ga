from Maze import Maze
import os
import sys
import random
current = os.path.dirname(os.path.realpath(__file__))
parent_directory = os.path.dirname(current)
sys.path.append(parent_directory + "/solver")
from GeneticSolver import GeneticSolver

class CoEvolver:

	def __init__(self, x, y, mazeCount, solverCount, initialLength, lengthenPeriod):
		if x < 1 or x < 1:
			raise ValueError("Maze of size " + str(self.size) + " is invalid")
		else:
			self.mazes = []
			self.solvers = []
			for i in range(mazeCount):
				maze = Maze(x, y)
				maze.initMaze(method="depth")
				self.mazes.append(maze)
			for j in range(solverCount):
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
		return total_fitness / len(self.solvers)
		
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
				parent1 = random.choice(self.mazes)
				parent2 = random.choice(self.mazes)
			case "ms":
				parent1 = random.choice(self.solvers)
				parent2 = random.choice(self.solvers)
		return parent1, parent2
		
	def step(self, mgRatchet=5, msRatchet=5):
		for i in range(mgRatchet):
			mgParent1, mgParent2 = self.parentSelection(algorithm="mg")
			mgChild1, mgChild2 = mgParent1.crossover(mgParent2)
			mgChild1 = mgChild1.mutate()
			mgChild2 = mgChild2.mutate()
			for child in [mgChild1, mgChild2]:
				if child != None:
					self.mazes.append(child)
		for i in range(msRatchet):
			msParent1, msParent2 = self.parentSelection(algorithm="ms")
			msChild1, msChild2 = msParent1.crossover(msParent2)
			msChild1 = msChild1.mutate()
			msChild2 = msChild2.mutate()
			# Step 4: Add to population
			for child in [msChild1, msChild2]:
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
		print(fitnesses_ms)
		self.currentGen += 1
		
	def showAllMazes(self):
		for maze in self.mazes:
			maze.display()
			
	def stepMulti(self, steps=1):
		for i in range(steps):
			self.step()
		
		

if __name__ == "__main__":

	coevolveGen = 5
	mazeGen = 100
	mazePop = 100
	mazeSize = 10
	# generate maze
	evolver = CoEvolver(10, 10, 5, 25, 10, 10)

	# DFSPath = Solver(mazeSize, mazeSize, maze.start, maze.end, maze.maze)
	# DFSPath.DFS()
	# DFSPath = DFSPath.path

	# for i in range(coevolveGen):
	#	  # evaluate fitness of solver on maze and DFS
	#	  fitness = evaluate(maze, solver, DFSPath)
