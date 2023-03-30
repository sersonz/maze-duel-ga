import random
import numpy as np
from Register import Register
from Instruction import *

class GeneticSolver:
	'''
	An implementation of a linear GP tree,
	as pertains to solving mazes.
	'''
	
	def __init__(self):
		self.registers = {}
		self.nextConstantRegister = 0
		self.nextInputRegister = 0
		self.nextVariableRegister = 0
		self.nextOutputRegister = 0
		self.instructions = []
		self.shouldMove = False
		self.stackPointer = 0
		
	def init(self, minInstructions, maxInstructions):
		self.addConstantRegister(1)
		self.addConstantRegister(-1)
		self.addInputRegister(valid=lambda x: x >= 0 and x <= 1)
		self.addInputRegister(valid=lambda x: x >= 0 and x <= 1)
		self.addInputRegister(valid=lambda x: x >= 0 and x <= 1)
		self.addInputRegister(valid=lambda x: x >= 0 and x <= 1)
		self.addOutputRegister(0)
		instructionCount = random.randrange(minInstructions, maxInstructions)
		registerPool = []
		for register in list(self.registers.keys()):
			if self.registers[register].registerType in ["input", "constant"]:
				registerPool.append(self.registers[register])
		instructionCount = random.randrange(minInstructions, maxInstructions)
		for i in range(1, instructionCount):
			chosenInstruction = random.choice(instructionList)
			term1 = random.choice(registerPool)
			term2 = random.choice(registerPool)
			self.instructions.append(chosenInstruction([term1, term2], self.registers["o0"]))
		
	def addConstantRegister(self, value):
		self.registers["c" + str(self.nextConstantRegister)] = Register("c" + str(self.nextConstantRegister), "constant", initValue=value)
		self.nextConstantRegister += 1
		
	def addInputRegister(self, valid=lambda x: True):
		self.registers["i" + str(self.nextInputRegister)] = Register("i" + str(self.nextInputRegister), "input", valid=valid)
		self.nextInputRegister += 1

	def addOutputRegister(self, value):
		self.registers["o" + str(self.nextOutputRegister)] = Register("o" + str(self.nextOutputRegister), "output", initValue=value)
		self.nextOutputRegister += 1
		
	def addVariableRegister(self, value):
		self.registers["v" + str(self.nextVariableRegister)] = Register("v" + str(self.nextVariableRegister), "variable", initValue=value)
		self.nextVariableRegister += 1
		
	def assign(self, register, value):
		if register not in list(self.registers.keys()):
			raise ValueError("No register named " + str(register) + " exists in this genetic object")
		else:
			self.registers[register].assign(value)
			
	def addInstruction(self, insType, terms, output):
		inp = []
		for term in terms:
			if term not in list(self.registers.keys()):
				inp.append(term)
			else:
				inp.append(self.registers[term])
		self.instructions.append(insType(inp, self.registers[output]))
	
	def step(self, inputs={}):
		for inp in list(inputs.keys()):
			self.registers[inp].assign(inputs[inp], inputOp=True)
		try:
		   result = self.instructions[self.stackPointer].op()
		   self.stackPointer += 1
		   if result == False:
			   while type(self.instructions[stackPointer]) != EndIfInstruction:
				   self.stackPointer += 1
				   if self.stackPointer > len(self.instructions):
					   break
		except Exception as e:
			print(e)

		
			
	def __str__(self):
		result = "GeneticSolver("
		for register in list(self.registers.keys()):
			result = result + str(register) + ":" + str(self.registers[register].value) + ","
		result += ")"
		return result
			
if __name__=="__main__":
	test = GeneticSolver()
	test.init(10, 25)