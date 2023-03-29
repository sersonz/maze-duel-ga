import random
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
		self.stackPointer = 0
		
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
		self.instructions[self.stackPointer].op()
		self.stackPointer += 1
			
	def __str__(self):
		result = "GeneticSolver("
		for register in list(self.registers.keys()):
			result = result + str(register) + ":" + str(self.registers[register].value) + ","
		result += ")"
		return result
			
if __name__=="__main__":
	test = GeneticSolver()
	test.addConstantRegister(1)
	test.addInputRegister(valid=lambda x: x < 5)
	test.addOutputRegister(0)
	test.addVariableRegister(1)
	test.addInstruction(AddInstruction, ["v0", 1], "o0")
	print(test)
	test.step({"i0": 1})
	print(test)