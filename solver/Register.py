class Register:
	'''
	A register for a linear GP tree.
	'''
	
	def __init__(self, name, registerType, initValue=None, valid=lambda x: True):
		if(registerType not in ["input", "variable", "constant", "calculation", "output"]):
			raise ValueError("Unacceptable register type " + str(registerType))
		elif(initValue == None and registerType in ["calculation", "output"]):
			raise ValueError("Calculation and output variables must be initialized")
		else:
			self.name = name
			self.registerType = registerType
			self.value = initValue
			self.valid = valid
			
	def assign(self, value):
		if not self.valid(value):
			raise ValueError("Value " + str(value) + " is not valid for register " + str(self.name))
		elif self.registerType in ["constant", "variable"]:
			raise ValueError("Cannot write to register " + str(self.name) + " of type " + str(self.registerType))
		else:
			self.value = value