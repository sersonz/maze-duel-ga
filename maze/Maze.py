import turtle
import types
import itertools
import random
import sys, os
import matplotlib.pyplot as plt
from Solver import Solver

current = os.path.dirname(os.path.realpath(__file__))
parent_directory = os.path.dirname(current)
sys.path.append(parent_directory + "/common")
from common import Common

class Maze:
	def __init__(self, x, y):
		'''
		Creates a new Maze instance.
		Parameters:
			x: The horizontal size of the maze
			y: The vertical size of the maze
		'''
		if x < 1 or x < 1:
			raise ValueError("Maze of size " + str(self.size) + " is invalid")
		else:
			self.x = 2*x + 1
			self.y = 2*y + 1
			self.maze = [[1 for i in range(self.x)] for j in range(self.y)]
			self.initialized = False
			self.valid = False
			self.start = None
			self.end = None
			self.popSize = None
			self.genLimit = None

	def initMaze(self, method="depth", popSize=None, genLimit=None):
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
		self.end = random.choice(potentialPoints)
		# re-generate start and end points if they are on a wall

		# For some reason, we have to pass the parameter in manually
		# or trying to initialize this again won't work
		match method:
			case "depth":
				self.depthGenerate(self.start, [])
				self.initialized = True
			case "genetic":
				self.geneticGenerate(popSize=popSize, genLimit=genLimit)
				self.initialized = True
		while self.maze[self.start[0]][self.start[1]] == 1:
			self.start = random.choice(potentialPoints)
		while self.maze[self.end[0]][self.end[1]] == 1:
			self.end = random.choice(potentialPoints)

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

	def parentSelection(self, fitnessValues, matingPoolSize):
		'''
		Selects two parents using random uniform selection.
		'''
		selectedParents = []
		# Select two parents
		for _ in range(matingPoolSize):
			# Select a random individual
			selectedParents.append(random.randint(0, len(fitnessValues)-1))
		return selectedParents

	def getBestIndividual(self, population, fitnessValues):
		bestIndividual = None
		bestFitness = 0
		for i in range(len(population)):
			if fitnessValues[i] >= bestFitness:
				bestIndividual = population[i]
				bestFitness = fitnessValues[i]
		return bestIndividual

	def createInitialPopulation(self, popSize):
		population = []
		# randomly generate a population of individuals with 0s and 1s
		for _ in range(popSize):
			individual = [[random.randint(0, 1) for _ in range(
				self.x)] for __ in range(self.y)]
			population.append(individual)
		return population

	def survivorSelection(self, currentPop, currentFitness, offspring, offspringFitness):
		# mu, lambda
		population = []
		fitness = []

		currentPopFitness = list(zip(currentPop, currentFitness))
		rankedPopFitness = sorted(
			currentPopFitness, key=lambda x: x[1], reverse=True)

		for i in range(len(offspring)):
			population.append(rankedPopFitness[i][0])
			fitness.append(rankedPopFitness[i][1])

		population = population + offspring
		fitness = fitness + offspringFitness

		return population, fitness

	def evalFitness(self, individual):
		# currently implemented to use DFS as a reference
		solver = Solver(individual, self.x, self.y, self.start, self.end)
		path = solver.DFS()
		if path:
			return len(solver.finalPath)
		else:
			return 1

	def crossover(self, parent1, parent2):
		# print("parent1: " + str(len(parent1)))
		# print("parent2: " + str(len(parent2)))
		# return offspring1, offspring2
		offspring1 = []
		offspring2 = []

		for i in range(len(parent1)):
			if random.random() < 0.5:  # 50% chance of selecting from parent1
				if parent1[i] not in offspring1:
					offspring1.append(parent1[i])
				if parent2[i] not in offspring2:
					offspring2.append(parent2[i])
			else:  # 50% chance of selecting from parent2
				if parent2[i] not in offspring1:
					offspring1.append(parent2[i])
				if parent1[i] not in offspring2:
					offspring2.append(parent1[i])

		return offspring1, offspring2

	def mutation(self, individual):
		# print("here")
		# print("individual" + str(individual))
		# Put the entire maze into a long string and swap an empty tile with a wall

		# Choose a random wall and random empty tile, below are the x and y coordinates
		empty = (random.randrange(self.x), random.randrange(self.y))
		tile = (random.randrange(self.x), random.randrange(self.y))

		while individual[empty[1]][empty[0]] != 0:
			empty = (random.randrange(self.x), random.randrange(self.y))

		while individual[tile[1]][tile[0]] != 1:
			tile = (random.randrange(self.x), random.randrange(self.y))

		# Create a temporary copy and swap the two values
		temp = [row[:] for row in individual]

		temp[empty[1]][empty[0]] = 1
		temp[tile[1]][tile[0]] = 0

		# Check if maze is still solvable
		solver = Solver(temp, self.x, self.y, self.start, self.end)
		path = solver.DFS()
		if path:
			return temp
		else:
			return individual

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

		replacement = []
		for i in range(self.y):
			replacement.append(
				[total_string[i * self.x: (i * self.x) + self.x]])

		self.maze = replacement

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
