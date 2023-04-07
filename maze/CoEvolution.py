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
		maze.display()
		euc = lambda x1, x2, y1, y2: ((x1-x2)**2 + (y1-y2)**2)**0.5
		initial_distance = euc(maze.start[0], maze.end[0], maze.start[1], maze.end[1])
		print("Initial distance: " + str(initial_distance))
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
			print("Initial distance: " + str(initial_distance))
			print("Total distance: " + str(total_distance))
			total_fitness += (lastOnGoal if lastOnGoal != -1 else len(path)) / (2 - ((initial_distance - total_distance) / initial_distance))
		return total_fitness / len(self.solvers)
		
	def evaluateSolver(self, solver):
		euc = lambda x1, x2, y1, y2: ((x1-x2)**2 + (y1-y2)**2)**0.5
		total_fitness = 0
		for maze in self.mazes:
			path = self.tracePath(solver.asGeneticObject(), maze, maze.start)
			lastOnGoal = -1
			for i in range(len(path)):
				if path[i] == maze.end:
					if lastOnGoal == -1:
						lastOnGoal = i
				else:
					lastOnGoal = -1
			total_distance = euc(path[-1][0], maze.end[0], path[-1][1], maze.end[1])
			initial_distance = euc(maze.start[0], maze.end[0], maze.start[1], maze.end[1])
			total_fitness += (1 / lastOnGoal if lastOnGoal != -1 else (1 / len(path) * ((initial_distance - total_distance) / initial_distance)))
		return total_fitness / len(self.mazes)
		
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
		
	def step(self, mgRatchet=1, msRatchet=5):
		for i in range(mgRatchet):
			print("Started mgRatchet")
			mgParent1, mgParent2 = self.parentSelection(algorithm="mg")
			print("Finished computing mg fitness")
			mgChild1, mgChild2 = mgParent1.crossover(mgParent2)
			print("Finished mg crossover")
			mgChild1 = mgChild1.mutate()
			mgChild2 = mgChild2.mutate()
			print("Finished mg mutation")
			for child in [mgChild1, mgChild2]:
				if child != None:
					self.mazes.append(child)
		for i in range(msRatchet):
			print("Started msRatchet")
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
				solver.lengthen()
		

if __name__ == "__main__":

	coevolveGen = 5
	mazeGen = 100
	mazePop = 100
	mazeSize = 10
	# generate maze
	evolver = CoEvolver(10, 10, 100, 100, 25, 5)

	# DFSPath = Solver(mazeSize, mazeSize, maze.start, maze.end, maze.maze)
	# DFSPath.DFS()
	# DFSPath = DFSPath.path

	# for i in range(coevolveGen):
	#	  # evaluate fitness of solver on maze and DFS
	#	  fitness = evaluate(maze, solver, DFSPath)
