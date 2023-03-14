import types
import itertools
import random
import sys
sys.path.insert(1, "../common")
from common import Common

class Maze:
	def __init__(self, size):
		'''
		Creates a new Maze instance.
		Parameters:
			size: A tuple representing the size of the maze
		'''
		if size[0] < 1 or size[1] < 1:
			raise ValueError("Maze of size " + str(self.size) + " is invalid")
		else:
			self.size = (2*size[0] + 1, 2*size[1] + 1)
			self.maze = [[1 for i in range(self.size[0])] for j in range(self.size[1])]
			self.initialized = False
			self.valid = False
			
	def initMaze(self, method="random"):
		'''
		Initializes this maze.
		'''
		if self.initialized:
			self.maze = [[1 for i in range(self.size[0])] for j in range(self.size[1])]
		if method == "ab":
			visited_cells = 1
			curCell = (random.randrange(1, self.size[0], 2), random.randrange(1, self.size[1], 2))
			while visited_cells < (self.size[0] - 1)/2 * (self.size[1] - 1)/2:
				neighbors = []
				if curCell[0] > 1 and self.maze[curCell[0] - 2][curCell[1]] == 1:
					neighbors.append((curCell[0] - 2, curCell[1]))
				if curCell[0] < self.size[0] - 2 and self.maze[curCell[0] + 2][curCell[1]] == 1:
					neighbors.append((curCell[0] + 2, curCell[1]))
				if curCell[1] > 1 and self.maze[curCell[0]][curCell[1] - 2] == 1:
					neighbors.append((curCell[0], curCell[1] - 2))
				if curCell[1] < self.size[1] - 2 and self.maze[curCell[0]][curCell[1] + 2] == 1:
					neighbors.append((curCell[0], curCell[1] + 2))
				if len(neighbors) == 0:
					if curCell[0] > 1 and self.maze[curCell[0] - 2][curCell[1]] == 0:
						neighbors.append((curCell[0] - 2, curCell[1]))
					if curCell[0] < self.size[0] - 2 and self.maze[curCell[0] + 2][curCell[1]] == 0:
						neighbors.append((curCell[0] + 2, curCell[1]))
					if curCell[1] > 1 and self.maze[curCell[0]][curCell[1] - 2] == 0:
						neighbors.append((curCell[0], curCell[1] - 2))
					if curCell[1] < self.size[1] - 2 and self.maze[curCell[0]][curCell[1] + 2] == 0:
						neighbors.append((curCell[0], curCell[1] + 2))
					curCell = random.choice(neighbors)
					continue
				random.shuffle(neighbors)
				for (x, y) in neighbors:
					if self.maze[x][y] > 0:
						self.maze[(curCell[0] + x) // 2][(curCell[1] + y) // 2] = 0
						self.maze[x][y] = 0
						visited_cells += 1
						curCell = (x, y)
						break
			self.initialized = True
		elif method == "random":
			for i in range(self.size[0]):
				for j in range(self.size[1]):
					self.maze[i][j] = random.randrange(0, 2)
		else:
			raise NotImplementedError("Invalid maze init method " + str(method))
		
	def asTextObject(self):
		string = ""
		for i in range(self.size[0]):
			for j in range(self.size[1]):
				string = string + str(self.maze[i][j])
			string = string + "\n"
		return string
	
	def printTextObject(self):
		print(self.asTextObject())
		
	def asGeneticObject(self):
		string = ""
		for i in range(self.size[0]):
			for j in range(self.size[1]):
				string = string + str(self.maze[i][j])
		return string