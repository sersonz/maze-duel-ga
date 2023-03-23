import turtle
import types
import itertools
import random
import sys
import matplotlib.pyplot as plt

sys.path.insert(1, "../common")
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
			
	def initMaze(self, method="depth"):
		'''
		Initializes this maze using DFS as a reference.
		'''
		if self.initialized:
			self.maze = [[1 for i in range(self.x)] for j in range(self.y)]
		self.start = (random.randrange(0, self.x, 2), random.randrange(0, self.y, 2))
		# For some reason, we have to pass the parameter in manually
		# or trying to initialize this again won't work
		self.depthGenerate(self.start, [])
		self.initialized = True
		# From the outer ring, select a random start and end point
		potentialPoints = [(0, i) for i in range(self.y)] + [(self.x - 1, i) for i in range(self.y)] \
			+ [(i, 0) for i in range(self.x)] + [(i, self.y - 1) for i in range(self.x)]
		self.start = random.choice(potentialPoints)
		self.end = random.choice(potentialPoints)
			
	def depthGenerate(self, pos, visited=[]):
		visited.append(pos)
		nextPos = self.randomNeighbor(pos, visited)
		while nextPos != None:
			posBetween = ((pos[0] + nextPos[0])//2, (pos[1] + nextPos[1])//2)
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
					string = string + ("█" if self.maze[i][j] == 1 else " ")
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
		plt.imshow(self.maze, cmap=plt.cm.binary)
		plt.plot(self.start[0], self.start[1], 'go')
		plt.plot(self.end[0], self.end[1], 'ro')
		plt.title('Maze', size=12)
		plt.show()





if __name__ == "__main__":
	maze = Maze(20, 20)
	maze.initMaze()
	maze.printTextObject()
	maze.display()
	# print(maze.asGeneticObject())
