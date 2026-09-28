from os import system

class VirtualMachine:
    def __init__(self):
        self.registers = {'DCS1': 0, 'DCS2': 0, 'DCS3': 0, 'DCS4': 0, 'DCSC': 0, 'DCSCa': 0}
        self.memory = {}
        self.bytes = 6000
        self.pc = 0
        self.running = True
        self.output = ""

    def reset(self):
        self.registers = {'DCS1': 0, 'DCS2': 0, 'DCS3': 0, 'DCS4': 0, 'DCSC': 0, 'DCSCa': 0}
        self.memory = {}
        self.bytes = 6000
        self.pc = 0
        self.running = True
        self.output = ""

    def execute(self, instructions):
        self.reset()
        lines = instructions.strip().split('\n')
        while self.running and self.pc < len(lines):
            instr = lines[self.pc].strip().split()
            if not instr:
                self.pc += 1
                continue
            cmd = instr[0]
            args = instr[1:]

            try:
                match cmd:
                    case "set":
                        self.remove_registers = self.registers
                        reg, val = args
                        self.registers[reg] = val
                    case "add":
                        self.remove_registers = self.registers
                        reg1, reg2 = args
                        self.registers[reg1] += self.registers[reg2]
                    case "msg":
                        char = args[0]
                        self.output += f"{self.memory[char]}\n"
                    case "move":
                        reg1, reg2 = args
                        self.registers[reg1] = self.registers[reg2]
                    case "halt":
                        self.running = False
                    case "paste":
                        char, val = args
                        self.memory[char] = val
                        self.bytes -= len(val)
                    case "corchar":
                        self.bytes += len(char)
                        char, val = args
                        self.memory[char] = val
                        self.bytes -= len(char)
                        if char not in self.memory:
                            self.output += f"Oops, the element not in the memory - {char}:\n\t- Please, check, good writed element name"
                            self.running = False
                    case _:
                        self.output += f"\nOops, running command {cmd} failed - line {self.pc + 1}:\n\t- Please check command on {self.pc + 1} line\n\t\t- The command wrong\n\t\t- The command fictonal\n\t\t- Problem of Dexality emulator"
                        self.running = False
                        
        
            except Exception as e:
                self.output += f"The line error corrupted the emulator, line {self.pc + 1}, error: {e}\n"
                self.running = False

            self.pc += 1
        return self.output, self.registers
