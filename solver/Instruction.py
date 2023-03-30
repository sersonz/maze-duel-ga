class Instruction:
	def __init__(self, terms, output):
		self.terms = terms
		if "Register" not in str(type(output)) or output.registerType != "output":
			raise ValueError("Output must be an output register")
		self.output = output
		
	def op(self):
		return NotImplementedError("Cannot execute base Instruction")
	
class TurnRightInstruction(Instruction):
	def op(self):
		self.output.assign((self.output.value + 1) % 4)
		return None
		
class TurnLeftInstruction(Instruction):
	def op(self):
		self.output.assign((self.output.value - 1) % 4)
		return None
	
class BranchGEInstruction(Instruction):
	def op(self):
		return (self.terms[0].value >= self.terms[1].value)
	
class BranchLEInstruction(Instruction):
	def op(self):
		return (self.terms[0].value <= self.terms[1].value)
	
class BranchEQInstruction(Instruction):
	def op(self):
		return (self.terms[0].value == self.terms[1].value)
	
class EndIfInstruction(Instruction):
	def op(self):
		return None
	
instructionList = [TurnRightInstruction, TurnLeftInstruction] * 25 + [BranchGEInstruction, \
				   BranchLEInstruction, BranchEQInstruction] * 2 + [EndIfInstruction] * 5