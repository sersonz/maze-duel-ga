class Register:
	'''
	A register for a linear GP tree.
	'''
	
	def __init__(self, name, registerType, initValue=None, valid=lambda x: True):
		if(registerType not in ["input", "constant", "variable", "output"]):
			raise ValueError("Unacceptable register type " + str(registerType))
		elif(initValue == None and registerType in ["variable", "output"]):
			raise ValueError("Variable and output registers must be initialized")
		else:
			self.name = name
			self.registerType = registerType
			self.value = initValue
			self.valid = valid
			
	def assign(self, value, inputOp=False):
		if not self.valid(value):
			raise ValueError("Value " + str(value) + " is not valid for register " + str(self.name))
		elif self.registerType in ["constant", "input"] and not inputOp:
			raise ValueError("Cannot write to register " + str(self.name) + " of type " + str(self.registerType))
		else:
			self.value = value