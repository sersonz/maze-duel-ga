import random
import numpy as np

class GeneticSolver:
	'''
	An implementation of a genetic algorithm,
	as pertains to solving mazes.
	'''
	
	def __init__(self, length, string=""):
		self.length = length
		self.string = string
		self.fitness = 0
	
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
		mutatedString.insert(point, mutatedSection)
		del mutatedString[point]
		return GeneticSolver(self.length, mutatedString)
		
	def crossover(self, parent2):
		point1 = random.randrange(0, len(self.string))
		point2 = random.randrange(0, len(self.string))
		mutationLength = 1
		while(random.randrange(0, 2) == 1):
			mutationLength += 1
		string1 = list(self.string)
		string2 = list(parent2.string)
		print(string1[point1:point1+mutationLength])
		print(string2[point2:point2+mutationLength])
		string1[point1:point1+mutationLength], string2[point2:point2+mutationLength] = \
			string2[point2:point2+mutationLength], string1[point1:point1+mutationLength]
		return GeneticSolver(self.length, "".join(string1)), GeneticSolver(self.length, "".join(string2))
		
	def lengthen(self, newLength):
		for i in range(newLength - self.length):
			self.string += str(random.randrange(0, 5))
		self.length = newLength
		
			
if __name__=="__main__":
	test = GeneticSolver(15)
	test.init()
	test2 = GeneticSolver(15)
	test2.init()
	child1, child2 = test.crossover(test2)