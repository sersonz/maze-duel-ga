import types
import itertools
import random
import sys
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
		Initializes this maze.
		'''
		if self.initialized:
			self.maze = [[1 for i in range(self.x)] for j in range(self.y)]
		if method=="depth":
			self.start = (random.randrange(0, self.x, 2), random.randrange(0, self.y, 2))
			self.depthGenerate(self.start, [])
			self.initialized = True
		else:
			raise NotImplementedError("Invalid maze init method " + str(method))
			
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