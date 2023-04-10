import random
import matplotlib.pyplot as plt

class GeneticSolver:
	'''
	An implementation of a genetic algorithm,
	as pertains to solving mazes.
	'''
	
	def __init__(self, length, string=""):
		self.length = length
		self.string = string
		self.fitness = 0
		# To prevent ties, we assign a small
		# fitness modifier to each solver
		self.radiation = random.uniform(0.999, 1.001)
	
	def init(self):
		if self.string != "":
			self.string = ""
		for i in range(self.length):
			self.string += str(random.randrange(0, 5))
			
	def mutate(self):
		point = random.randrange(0, len(self.string))
		mutationLength = 1
		while(random.randrange(0, 2) == 1):
			mutationLength += 1
		mutatedSection = ""
		for i in range(mutationLength):
			mutatedSection += str(random.randrange(0, 5))
		mutatedString = list(self.string)
		for i in range(len(mutatedSection)):
			if point + i >= len(self.string):
				break
			else:
				mutatedString[point+i] = mutatedSection[i]
		return GeneticSolver(self.length, "".join(mutatedString))
		
	def crossover(self, parent2):
		mutationLength = 1
		while(random.randrange(0, 3) == 1 and mutationLength < len(self.string)):
			mutationLength += 1
		point1 = random.randrange(0, len(self.string) - mutationLength)
		point2 = random.randrange(0, len(parent2.string) - mutationLength)
		string1 = list(self.string)
		string2 = list(parent2.string)
		string1[point1:point1+mutationLength+1], string2[point2:point2+mutationLength+1] = \
			string2[point2:point2+mutationLength+1], string1[point1:point1+mutationLength+1]
		child1 = GeneticSolver(self.length, "".join(string1))
		child2 = GeneticSolver(self.length, "".join(string2))
		return child1, child2
		
	def lengthen(self, amount):
		for i in range(amount):
			self.string += str(random.randrange(0, 5))
		self.length += amount
		
	def asGeneticObject(self):
		return "".join([str(x) for x in self.string])
		
			
if __name__=="__main__":
	test = GeneticSolver(15)
	test.init()
	test2 = GeneticSolver(15)
	test2.init()
	child1, child2 = test.crossover(test2)