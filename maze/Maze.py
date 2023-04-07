import turtle
import types
import itertools
import random
import numpy as np
import sys, os
import matplotlib.pyplot as plt
from Solver import Solver

current = os.path.dirname(os.path.realpath(__file__))
parent_directory = os.path.dirname(current)
sys.path.append(parent_directory + "/common")
from common import Common

class Maze:
	def __init__(self, x, y, maze=None, start=None, end=None):
		'''
		Creates a new Maze instance.
		Parameters:
			x: The horizontal size of the maze
			y: The vertical size of the maze
		'''
		if x < 1 or x < 1:
			raise ValueError("Maze of size " + str(self.size) + " is invalid")
		else:
			self.x = (2*x + 1 if maze==None else x)
			self.y = (2*y + 1 if maze==None else y)
			self.maze = ([[1 for i in range(self.x)] for j in range(self.y)]) if maze == None else maze
			self.initialized = False
			self.valid = False
			self.start = start
			self.end = end
			self.popSize = None
			self.genLimit = None

	def initMaze(self, method="depth", popSize=None, genLimit=None, maze=None):
		'''
		Initializes this maze using DFS as a reference.
		'''
		if self.initialized:
			self.maze = [[1 for i in range(self.x)] for j in range(self.y)]
		self.start = (random.randrange(0, self.x, 2),
					  random.randrange(0, self.y, 2))

		# From the outer ring, select a random start and end point
		potentialPoints = [(0, i) for i in range(self.y)] + [(self.x - 1, i) for i in range(self.y)] \
			+ [(i, 0) for i in range(self.x)] + [(i, self.y - 1)
												 for i in range(self.x)]
		self.start = random.choice(potentialPoints)
		potentialPoints.remove(self.start)
		self.end = random.choice(potentialPoints)
		# re-generate start and end points if they are on a wall

		# For some reason, we have to pass the parameter in manually
		# or trying to initialize this again won't work
		match method:
			case "depth":
				self.depthGenerate(self.start, [])
				self.initialized = True
			case "genetic":
				raise NotImplementedError("Genetic generation method not currently working")
			case "existing":
				self.maze = maze.maze
				self.start = maze.start
				self.end = maze.end
				self.popSize = maze.popSize
				self.genLimit = maze.genLimit
		while self.maze[self.start[0]][self.start[1]] == 1:
			self.start = random.choice(potentialPoints)
		while self.maze[self.end[0]][self.end[1]] == 1:
			self.end = random.choice(potentialPoints)

	'''
	def geneticGenerate(self, popSize, genLimit):
		population = self.createInitialPopulation(popSize)
		generation = 0
		xoverRate = 0.9
		mutationRate = 0.2
		matingPoolSize = int(popSize*0.5)
		fitnessValues = []
		for individual in population:
			fitnessValues.append(self.evalFitness(individual))
		# print("Fitness values: " + str(fitnessValues))
		while generation < genLimit:
			# pick parents
			parentsIndex = self.parentSelection(fitnessValues, matingPoolSize)
			random.shuffle(parentsIndex)

			offspring = []
			offspringFitness = []
			i = 0
			while len(offspring) < matingPoolSize and i+1 < len(parentsIndex):

				if random.random() < xoverRate:
					offspring1, offspring2 = self.crossover(
						population[parentsIndex[i]], population[parentsIndex[i+1]])
				else:
					offspring1 = population[parentsIndex[i]].copy()
					offspring2 = population[parentsIndex[i+1]].copy()

				if random.random() < mutationRate:
					offspring1 = self.mutation(offspring1)
				if random.random() < mutationRate:
					offspring2 = self.mutation(offspring2)

				offspring.append(offspring1)
				offspringFitness.append(self.evalFitness(offspring1))
				offspring.append(offspring2)
				offspringFitness.append(self.evalFitness(offspring2))
				i = i+2

			population, fitnessValues = self.survivorSelection(
				population, fitnessValues, offspring, offspringFitness)
			generation = generation + 1

		bestIndividual = self.getBestIndividual(population, fitnessValues)
		print("Best individual: " + str(bestIndividual))
		self.maze = bestIndividual
	'''

	def createInitialPopulation(self, popSize):
		population = []
		# randomly generate a population of individuals with 0s and 1s
		for _ in range(popSize):
			individual = [[random.randint(0, 1) for _ in range(
				self.x)] for __ in range(self.y)]
			population.append(individual)
		return population

	def evalFitness(self, individual):
		# currently implemented to use DFS as a reference
		solver = Solver(individual, self.x, self.y, self.start, self.end)
		path = solver.DFS()
		if path:
			return len(solver.finalPath)
		else:
			return 1

	def crossover(self, parent2):
		# print("parent1: " + str(len(parent1)))
		# print("parent2: " + str(len(parent2)))
		# return offspring1, offspring2
		offspring1 = ([[0 for i in range(self.x)] for j in range(self.y)])
		offspring2 = ([[0 for i in range(self.x)] for j in range(self.y)])

		for x in range(self.x):
			for y in range(self.y):
				if random.random() < 0.5:  # 50% chance of selecting from parent1
					offspring1[x][y] = self.maze[x][y]
					offspring2[x][y] = parent2.maze[x][y]
				else:  # 50% chance of selecting from parent2
					offspring1[x][y] = parent2.maze[x][y]
					offspring2[x][y] = self.maze[x][y]

		return Maze(self.x, self.y, offspring1, self.start, self.end), Maze(self.x, self.y, offspring2, self.start, self.end)

	def mutate(self):
		# print("here")
		# print("individual" + str(individual))
		# Put the entire maze into a long string and swap an empty tile with a wall

		# Choose a random wall and random empty tile, below are the x and y coordinates
		for i in range(60):
			empties = list(zip(*np.where(np.asarray(self.maze) == 0)))
			tiles = list(zip(*np.where(np.asarray(self.maze) == 1)))
			
			empty = random.choice(empties)
			tile = random.choice(tiles)
			
	
			# Create a temporary copy and swap the two values
			temp = [row[:] for row in self.maze]
	
			temp[empty[0]][empty[1]] = 1
			temp[tile[0]][tile[1]] = 0
	
			# Check if maze is still solvable
		solver = Solver(temp, self.x, self.y, self.start, self.end)
		path = solver.DFS()
		if path:
			return Maze(self.x, self.y, temp, self.start, self.end)
		else:
			return None

	def depthGenerate(self, pos, visited=[]):
		visited.append(pos)
		nextPos = self.randomNeighbor(pos, visited)
		while nextPos != None:
			posBetween = ((pos[0] + nextPos[0])//2,
						  (pos[1] + nextPos[1])//2)
			self.maze[posBetween[0]][posBetween[1]] = 0
			self.maze[nextPos[0]][nextPos[1]] = 0
			self.maze[pos[0]][pos[1]] = 0
			self.depthGenerate(nextPos, visited)
			nextPos = self.randomNeighbor(pos, visited)

	def randomNeighbor(self, pos, visited):
		neighbors = []
		if pos[0] > 1 and (pos[0] - 2, pos[1]) not in visited:
			neighbors.append((pos[0] - 2, pos[1]))
		if pos[0] < self.x - 2 and (pos[0] + 2, pos[1]) not in visited:
			neighbors.append((pos[0] + 2, pos[1]))
		if pos[1] > 1 and (pos[0], pos[1] - 2) not in visited:
			neighbors.append((pos[0], pos[1] - 2))
		if pos[1] < self.y - 2 and (pos[0], pos[1] + 2) not in visited:
			neighbors.append((pos[0], pos[1] + 2))
		if len(neighbors) == 0:
			return None
		random.shuffle(neighbors)
		return random.choice(neighbors)

	def asTextObject(self):
		string = ""
		for i in range(self.x):
			for j in range(self.y):
				if (i, j) == self.start:
					string = string + str(0)
				elif (i, j) == self.end:
					string = string + str(1)
				else:
					string = string + \
						("█" if self.maze[i][j] == 1 else " ")
			string = string + "\n"
		return string

	def printTextObject(self):
		print(self.asTextObject())

	def asGeneticObject(self):
		string = ""
		for i in range(self.x):
			for j in range(self.y):
				string = string + str(self.maze[i][j])
		return string

	def display(self):
		# print(self.maze)
		# print(self.start)
		# print(self.end)
		plt.imshow(self.maze, cmap=plt.cm.binary)
		plt.plot(self.start[1], self.start[0], 'go')
		plt.plot(self.end[1], self.end[0], 'ro')
		plt.title('Maze', size=12)
		plt.show()


if __name__ == "__main__":
	method = "genetic"
	population = 100
	generations = 100
	maze = Maze(10, 10)
	maze.initMaze(method, population, generations)
	maze.display()
	# maze.mutation()
	# maze.display()
	# print(maze.start)
	# print(type(maze.asGeneticObject()))
