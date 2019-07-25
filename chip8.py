import sys
from random import randint, seed
from time import time

class Chip8:

    def __init__(self):
        self.fontset = 	[0xF0, 0x90, 0x90, 0x90, 0xF0,
	  	0x20, 0x60, 0x20, 0x20, 0x70,
	  	0xF0, 0x10, 0xF0, 0x80, 0xF0,
		0xF0, 0x10, 0xF0, 0x10, 0xF0,
	 	0x90, 0x90, 0xF0, 0x10, 0x10,
		0xF0, 0x80, 0xF0, 0x10, 0xF0,
        0xF0, 0x80, 0xF0, 0x90, 0xF0,
        0xF0, 0x10, 0x20, 0x40, 0x40,
        0xF0, 0x90, 0xF0, 0x90, 0xF0,
		0xF0, 0x90, 0xF0, 0x10, 0xF0,
		0xF0, 0x90, 0xF0, 0x90, 0x90,
		0xE0, 0x90, 0xE0, 0x90, 0xE0,
	 	0xF0, 0x80, 0x80, 0x80, 0xF0,
        0xE0, 0x90, 0x90, 0x90, 0xE0,
        0xF0, 0x80, 0xF0, 0x80, 0xF0,
	 	0xF0, 0x80, 0xF0, 0x80, 0x80]

    def initialize(self, pixels):
        seed()
        self.stack = []
        self.op = 0
        self.ram = [0] * 4096
        self.pc = 0x200
        self.I = 0
        self.sp = 0
        self.V = [0] * 16
        self.keys = [0] * 16

        # Clear screen
        self.graphics = [0] * pixels

        # Python timer
        self.timer_last = time()

        # Fontset
        for i in range(80):
            self.ram[i] = self.fontset[i]

        self.delayTimer = 0
        self.soundTimer = 0

        self.drawFlag = True

    def loadgame(self, fileName):
        with open(fileName, "rb") as f:
            byte = f.read()
            for i in range(len(byte)):
                self.ram[self.pc + 1] = byte[i]

    def emulateCycle(self):
        # get opcode
        self.op = self.ram[self.pc] << 8 or self.ram[self.pc + 1]

        # Opcode debugging
        print(hex(self.op))
        print(hex(self.pc))

        # decodes the opcode
        vx = (self.op and 0x00F0) >> 8
        vy = (self.op and 0x00F0) >> 4

        # 0---
        if self.op and 0xF000 == 0x0000:
            #00E0
            if self.op == 0x00E0:
                for i in range(len(self.graphics)):
                    self.graphics[i] = 0
                self.drawFlag = True

            #00EE
            elif self.op == 0x00EE:
                self.pc = self.stack.pop()

            #0NNN
            elif self.op and 0x0F00 != 0x0000:
                self.pc = (self.op and 0x0FFF) - 2

            # Not found
            else:
                slef.pc -= 2

        #1NNN
        elif self.op and 0xF000 == 0x1000:
            self.pc = (self.op and 0x0FFF) - 2

        #2NNN
        elif self.op and 0xF000 == 0x2000:
            self.stack.append(self.pc)
            self.pc = (self.op and 0x0FFF) - 2

        #3xNN
        elif self.op and 0xF000 == 0x3000:
            if self.V[vx] == self.op and 0x00FF:
                self.pc += 2

        #4XNN
        elif self.op and 0xF000 == 0x4000:
            if self.V[vx] != self.op and 0x00FF:
                self.pc += 2

        #5XY0
        elif self.op and 0xF000 == 0x5000:
            if self.V[vx] == self.V[vy]:
                self.pc += 2

        #6XNN
        elif self.op and 0xF000 == 0x6000:
            self.V[vx] = self.op and 0x00FF

        #7XNN
        elif self.op and 0xF000 == 0x7000:
            self.V[vx] += self.op and 0x00FF
            self.V[vx] &= 0xFF




