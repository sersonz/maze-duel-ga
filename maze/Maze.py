import types
import itertools
import random

class Maze:
	def __init__(self, size):
		'''
		Creates a new Maze instance.
		Parameters:
			size: A tuple representing the size of the maze
			tiles: A list of available tiles
		'''
		if size[0] < 1 or size[1] < 1:
			raise ValueError("Maze of size " + str(self.size) + " is invalid")
		else:
			self.size = size
			self.maze = [[0 for i in range(self.size[0])] for j in range(self.size[1])]
			
	def initMaze(self):
		'''
		Initializes this maze.
		'''
		dirs = {"E": 1, "W": 2, "N": 4, "S": 8}
		inv_dirs = {"E": 2, "W": 1, "N": 8, "S": 4}
		dx = {"E": 1, "W": -1, "N": 0, "S": 0}
		dy = {"E": 0, "W": 0, "N": -1, "S": 1}
		unvisited = list(itertools.product([i for i in range(self.size[0])], [i for i in range(self.size[1])]))
		remaining = (self.size[0] * self.size[1]) - 1
		curCell = random.choice(unvisited)
		while (remaining > 0):
			selectedDirection = random.choice(["N", "S", "E", "W"])
			nx = curCell[0] + dx[selectedDirection]
			ny = curCell[1] + dy[selectedDirection]
			while not (nx >= 0 and ny >= 0 and nx < self.size[0] and ny < self.size[1]):
				selectedDirection = random.choice(["E", "W", "N", "S"])
				nx = curCell[0] + dx[selectedDirection]
				ny = curCell[1] + dy[selectedDirection]
			if self.maze[nx][ny] == 0:
				self.maze[curCell[0]][curCell[1]] = dirs[selectedDirection]
				self.maze[nx][ny] = inv_dirs[selectedDirection]
				remaining = remaining - 1
			curCell = (nx, ny)
	
	def __str__(self):
		string = ""
		dirs = {"E": 1, "W": 2, "N": 4, "S": 8}
		for i in range(self.size[0]):
			for j in range(self.size[1]):
				if self.maze[i][j] == dirs["E"]:
					string = string + "▌"
				elif self.maze[i][j] == dirs["W"]:
					string = string + "║"
				elif self.maze[i][j] == dirs["N"]:
					string = string + "─"
				elif self.maze[i][j] == dirs["S"]:
					string = string + "_"
				else:
					string = string
			string = string + "\n"
		return string
		