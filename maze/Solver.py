from collections import deque
import matplotlib.pyplot as plt


class Solver:
	'''
	DFS, BFS and Genetic algorithms for solving mazes.
	'''

	def __init__(self, maze, width, height, start, end):
		self.width = width
		self.height = height
		if type(maze) == str:
			self.maze = self.convertMaze(maze)
		else:
			self.maze = maze
		self.visited = []
		self.finalPath = []
		self.path = []
		self.start = start
		self.end = end
		self.moves = {
			"north": (-1, 0),
			"south": (1, 0),
			"east": (0, 1),
			"west": (0, -1)
		}

	def convertMaze(self, maze):
		# convert a binary maze to a 2D array of ints
		convertedMaze = [[0]*self.width for _ in range(self.height)]
		for i in range(self.height):
			for j in range(self.width):
				convertedMaze[i][j] = int(maze[i*self.width + j])
		return convertedMaze

	def DFS(self):
		stack = [self.start]
		prev = {}
		visited = []
		while stack:
			node = stack.pop()
			visited.append(node)
			self.path.append(node)
			if node == self.end:
				# backtrack from end to start
				while node != self.start:
					node = prev[node]
					self.finalPath.append(node)
					self.path.remove(node)
				self.finalPath.reverse()
				return True
			neighbours = self.getNeighbours(node)
			for neighbour in neighbours:
				if neighbour not in visited:
					stack.append(neighbour)
					visited.append(neighbour)
					prev[neighbour] = node
		return False

	def BFS(self):
		queue = [self.start]
		prev = {}
		visited = []
		while queue:
			node = queue.pop(0)
			visited.append(node)
			self.path.append(node)
			if node == self.end:
				while node != self.start:
					node = prev[node]
					self.finalPath.append(node)
					self.path.remove(node)
				self.finalPath.reverse()
				return True
			neighbours = self.getNeighbours(node)
			for neighbour in neighbours:
				if neighbour not in visited:
					queue.append(neighbour)
					visited.append(neighbour)
					prev[neighbour] = node
		return False

	def getNeighbours(self, node):
		neighbours = []
		for move in self.moves:
			neighbour = (node[0] + self.moves[move][0],
						 node[1] + self.moves[move][1])
			if self.validMove(neighbour):
				neighbours.append(neighbour)
		return neighbours

	def validMove(self, node):
		if node[0] < 0 or node[0] >= len(self.maze):
			return False
		if node[1] < 0 or node[1] >= len(self.maze[0]):
			return False
		if self.maze[node[0]][node[1]] == 1:
			return False
		return True

	def displayPath(self):
		plt.imshow(self.maze, cmap=plt.cm.binary)

		# hide the axes
		plt.xticks([])
		plt.yticks([])

		for node in self.finalPath:
			plt.plot(node[1], node[0], 'bo', markersize=10)

		for node in self.path:
			plt.plot(node[1], node[0], 'bo', markersize=10, alpha=0.3)

		plt.plot(self.start[1], self.start[0], 'go', markersize=10)
		plt.plot(self.end[1], self.end[0], 'ro', markersize=10)
		plt.title('Maze', size=12)
		plt.show()


if __name__ == "__main__":

	maze = [
		[1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
		[1, 0, 1, 0, 1, 0, 0, 0, 0, 1],
		[1, 0, 1, 0, 1, 0, 0, 0, 0, 1],
		[1, 0, 1, 0, 1, 1, 1, 1, 0, 1],
		[1, 0, 1, 0, 0, 0, 0, 1, 0, 1],
		[1, 0, 1, 0, 0, 0, 0, 1, 0, 1],
		[1, 0, 0, 0, 0, 0, 0, 1, 0, 1],
		[1, 0, 1, 0, 0, 0, 0, 0, 0, 1],
		[1, 0, 1, 0, 0, 0, 0, 0, 0, 1],
		[1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
	]

	maze1 = [
		[1, 1, 1, 1],
		[1, 0, 0, 1],
		[1, 0, 0, 1],
		[1, 0, 0, 1],
		[1, 1, 1, 1]
	]

	maze1B = "11111001100110011111"
	start = (1, 1)
	end = (3, 2)
	solver = Solver(maze1B, 4, 5, start, end)

	path = solver.BFS()
	if path:
		solver.displayPath()
	else:
		print("No path found")
