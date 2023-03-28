class Instruction:
	def __init__(self, terms, output):
		self.terms = terms
		if "Register" not in str(type(output)) or output.registerType != "output":
			raise ValueError("Output must be an output register")
		self.output = output
		
	def addTerm(self, term):
		self.terms.append(term)
		
	def op(self):
		return NotImplementedError("Cannot execute base Instruction")

class AddInstruction(Instruction):
	def op(self):
		result = None
		if len(self.terms) == 0:
			self.output.assign(self.output.value())
			return
		else:
			result = 0
			for term in self.terms:
				if "Register" in str(type(term)):
					result = result + term.value
				else:
					result = result + term
			self.output.assign(result)
			return
			
class SubtractInstruction(Instruction):
	def op(self):
		result = None
		if len(self.terms) == 0:
			self.output.assign(self.output.value())
			return
		else:
			result = 0
			for term in self.terms:
				if "Register" in str(type(term)):
					result = result - term.value
				else:
					result = result - term
			self.output.assign(result)
			return
			
class MultiplyInstruction(Instruction):
	def op(self):
		result = None
		if len(self.terms) == 0:
			self.output.assign(self.output.value())
			return
		else:
			result = 0
			for term in self.terms:
				if "Register" in str(type(term)):
					result = result * term.value
				else:
					result = result * term
			self.output.assign(result)
			return
			
class DivideInstruction(Instruction):
	def op(self):
		result = None
		if len(self.terms) == 0:
			self.output.assign(self.output.value())
			return
		else:
			result = 0
			for term in self.terms:
				if "Register" in str(type(term)):
					result = result / term.value
				else:
					result = result / term
			self.output.assign(result)
			return	