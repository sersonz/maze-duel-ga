import matplotlib.pyplot as plt


class Solver:
    '''
    DFS, BFS and Genetic algorithms for solving mazes.
    '''

    def __init__(self, maze):
        self.maze = maze
        self.visited = []
        self.path = []
        self.moves = {
            "north": (-1, 0),
            "south": (1, 0),
            "east": (0, 1),
            "west": (0, -1)
        }

    def DFS(self, start, end):
        self.visited.append(start)
        if start == end:
            self.path.append(start)
            return True
        else:
            neighbours = self.getNeighbours(start)
            for neighbour in neighbours:
                if neighbour not in self.visited:
                    if self.DFS(neighbour, end):
                        self.path.append(start)
                        return True
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
        if self.maze[node[0]][node[1]] == 1:
            return False
        return True

    def displayPath(self, start, end):
        plt.imshow(self.maze, cmap=plt.cm.binary)

        # hide the axes
        plt.xticks([])
        plt.yticks([])

        # hide the frame
        ax = plt.gca()
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)

        # draw borders around each cell
        for x in range(len(self.maze)):
            for y in range(len(self.maze[0])):
                # top border 
                plt.plot([y + 0.5, y + 1 + 0.5],
                         [x + 0.5, x + 0.5], color='black')
                # bottom border
                plt.plot([y + 0.5, y + 1 + 0.5],
                         [x + 1 + 0.5, x + 1 + 0.5], color='black')
                # left border
                plt.plot([y + 0.5, y + 0.5],
                         [x + 0.5, x + 1 + 0.5], color='black')
                # right border
                plt.plot([y + 0.5 + 1, y + 1 + 0.5],
                         [x + 0.5, x + 1 + 0.5], color='black')

        for node in self.path:
            plt.plot(node[1], node[0], 'bo', markersize=10)

        plt.plot(start[0], start[1], 'go')
        plt.plot(end[1], end[0], 'ro')
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

solver = Solver(maze)
start = (1, 1)
end = (1, 7)
path = solver.DFS(start, end)
if path:

    solver.displayPath(start, end)
else:
    print("No path found")
