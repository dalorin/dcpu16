class ValuesDict(dict):
	def __missing__(self, key):
		if key <= 0x3f:
			value = self[key] = key - 0x20
			return value
		else:
			raise KeyError

class DCPU16:
	def __init__(self):
		self.memory = {}
		self.stack = []
		self.pc = 0
		self.sp = 0xffff
		self.clock = 0
	
		self.registers = {
			'A':None,
			'B':None,
			'C':None,
			'X':None,
			'Y':None,
			'Z':None,
			'I':None,
			'J':None
		}
		
		self.ValuesDict = {
			0x00: lambda: self.registers['A'],
			0x01: lambda: self.registers['B'],
			0x02: lambda: self.registers['C'],
			0x03: lambda: self.registers['X'],
			0x04: lambda: self.registers['Y'],
			0x05: lambda: self.registers['Z'],
			0x06: lambda: self.registers['I'],
			0x07: lambda: self.registers['J'],
			0x08: lambda: self.memory[self.registers['A']],
			0x09: lambda: self.memory[self.registers['B']],
			0x0a: lambda: self.memory[self.registers['C']],
			0x0b: lambda: self.memory[self.registers['X']],
			0x0c: lambda: self.memory[self.registers['Y']],
			0x0d: lambda: self.memory[self.registers['Z']],
			0x0e: lambda: self.memory[self.registers['I']],
			0x0f: lambda: self.memory[self.registers['J']],
			0x10: lambda: self.memory[self.nextWord() + self.registers['A']],
			0x11: lambda: self.memory[self.nextWord() + self.registers['B']],
			0x12: lambda: self.memory[self.nextWord() + self.registers['C']],
			0x13: lambda: self.memory[self.nextWord() + self.registers['X']],
			0x14: lambda: self.memory[self.nextWord() + self.registers['Y']],
			0x15: lambda: self.memory[self.nextWord() + self.registers['Z']],
			0x16: lambda: self.memory[self.nextWord() + self.registers['I']],
			0x17: lambda: self.memory[self.nextWord() + self.registers['J']],
			0x18: lambda: self.POP(),
			0x19: lambda: self.PEEK(),
			0x1a: lambda: self.PUSH(),
			0x1b: lambda: self.sp,
			0x1c: lambda: self.pc,
			0x1d: lambda: self.o,	
			0x1e: lambda: self.memory[self.nextWord()],
			0x1f: lambda: self.nextWord(),
		}
		
	def nextWord(self):		
		word = self.memory[self.pc]
		self.pc += 1
		return word
	
	def POP(self):
		word = self.memory[self.sp]
		self.sp +=1
		return word
		
	def PEEK(self):
		return self.memory[self.sp]
		
	def PUSH(self):		
		word = self.memory[self.sp]
		self.sp = self.sp - 1
		return word
	
	def SET(self, a, b):
		a = b
		self.clock += 1

	def ADD(self, a, b):
		a = a + b
		self.clock += 2
	
	def SUB(self, a, b):
		a = a - b
		self.clock += 2
	
	def MUL(self, a, b):
		a = a * b
		self.clock += 2
	
	def DIV(self, a, b):
		a = a / b
		self.clock += 3
	
	def MOD(self, a, b):
		a = a % b
		self.clock += 3
	
	def SHL(self, a, b):
		a = a << b
		self.clock += 2
	
	def SHR(self, a, b):
		a = a >> b
		self.clock += 2
	
	def AND(self, a, b):
		a = a & b
		self.clock += 1
	
	def BOR(self, a, b):
		a = a | b
		self.clock += 1
	
	def XOR(self, a, b):
		a = a ^ b #?
		self.clock += 1
	
	def IFE(self, a, b):
		if a == b:
			self.clock += 2
		else:
			self.pc += 1
			self.clock += 3			
	
	def IFN(self, a, b):
		if a != b:			
			self.clock += 2
		else:
			self.pc += 1
			self.clock += 3
	
	def IFG(self, a, b):
		if a > b:
			self.clock += 2
		else:
			self.pc += 1
			self.clock += 3
	
	def IFB(self, a, b):
		if (a & b) == 0:
			self.clock += 2
		else:
			self.pc += 1
			self.clock += 3
	
	def handleInstruction(self, word):
		print "Executing instruction: 0x%x" % word
		opcode = word & 0b1111
		a = (word >> 4) & 0b111111
		b = (word >> 10) & 0b111111
		print "opcode: 0x%x\ta: 0x%x\tb: 0x%x" % (opcode, a, b)
		
		if opcode == 0x0:
			if a == 0x0:
				pass
			elif a == 0x01:
				pass
			elif 0x02 > opcode > 0x3f:
				pass
		elif opcode == 0x1:
			self.SET(a, b)
		elif opcode == 0x2:
			self.ADD(a, b)
		elif opcode == 0x3:
			self.SUB(a, b)
		elif opcode == 0x4:
			self.MUL(a, b)
		elif opcode == 0x5:
			self.DIV(a, b)
		elif opcode == 0x6:
			self.MOD(a, b)
		elif opcode == 0x7:
			self.SHL(a, b)
		elif opcode == 0x8:
			self.SHR(a, b)
		elif opcode == 0x9:
			self.AND(a, b)
		elif opcode == 0xa:
			self.BOR(a, b)
		elif opcode == 0xb:
			self.XOR(a, b)
		elif opcode == 0xc:
			self.IFE(a, b)
		elif opcode == 0xd:
			self.IFN(a, b)
		elif opcode == 0xe:
			self.IFG(a, b)
		elif opcode == 0xf:
			self.IFB(a, b)
			
		self.printState()
	
	def printState(self):
		print "Clock: %d\tPC: %d\tSP:%d" % (self.clock, self.pc, self.sp)
	
	def run(self):
		pass		
		