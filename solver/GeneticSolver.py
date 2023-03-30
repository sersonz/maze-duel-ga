import random
import numpy as np

class GeneticSolver:
	'''
	An implementation of a genetic algorithm,
	as pertains to solving mazes.
	'''
	
	def __init__(self, length):
		self.length = length
		self.string = ""
	
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
		self.string = mutatedString
		
	def lengthen(self, newLength):
		for i in range(newLength - self.length):
			self.string += str(random.randrange(0, 5))
		self.length = newLength
		
			
if __name__=="__main__":
	test = GeneticSolver(15)