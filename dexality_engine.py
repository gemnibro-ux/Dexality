class VirtualMachine:
    def __init__(self):
        self.memory = {}
        self.bytes = 6000
        self.pc = 0
        self.running = True
        self.output = ""
        self.registers = {'DUN1': 0, 'DUN2': 0, 'DUN3': 0, 'DUN4': 0, 'DCN': 0, 'DSN': self.pc}

    def reset(self):
        self.memory = {}
        self.bytes = 6000
        self.pc = 0
        self.running = True
        self.output = ""
        self.registers = {'DUN1': 0, 'DUN2': 0, 'DUN3': 0, 'DUN4': 0, 'DCN': 0, 'DSN': self.pc}

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
                    case "add":
                        reg1, reg2 = args
                        self.registers[reg1] += self.registers[reg2]
                    case "sub":
                        reg1, reg2 = args
                        self.registers[reg1] -= self.registers[reg2]
                    case "mul":
                        reg1, reg2 = args
                        self.registers[reg1] *= self.registers[reg2]
                    case "div":
                        reg1, reg2 = args
                        self.registers[reg1] /= self.registers[reg2]
                    case "msg":
                        code, obj = args
                        if code == "cell":
                            self.output += f"{self.memory[obj]}\n"
                        elif code == "reg":
                            self.output += str(self.registers[obj]) + "\n"
                    case "move":
                        reg, val = args
                        self.registers[reg] = int(val)
                    case "halt":
                        self.running = False

                    case "cell":
                        cell, val = args
                        self.memory[cell] = val
                        self.bytes -= len(val)
                    case "corcell":
                        self.bytes += len(val)
                        cell, val = args
                        self.memory[cell] = val
                        self.bytes -= len(cell)

                        if cell not in self.memory:
                            self.output += f"Oops, the element not in the memory - {cell}:\n\t- Please, check, good writed element name"
                            self.running = False
                    case "cleancell":
                        cell = args[0]
                        self.memory[cell] = ""
        
            except Exception as e:
                self.output += f"The line error corrupted the emulator, line {self.pc + 1}, error: {e}\n"
                self.running = False

            self.pc += 1

        return self.output, self.registers
