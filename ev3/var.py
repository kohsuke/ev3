# Represents a variable in Program
import struct


class Variable:
    def __init__(self, program, offset:int, size:int):
        self.program = program
        self.offset = offset
        self.size = size

class LocalVariable(Variable):
    def __init__(self, program, offset:int, size:int):
        super().__init__(program, offset, size)

class GlobalVariable(Variable):
    def __init__(self, program, offset:int, size:int):
        super().__init__(program, offset, size)

    __FORMAT = [None, 'b', '<h', None, '<i']

    def __call__(self):
        """
        Access the value of the global variable at the end of the last command
        """

        return struct.unpack_from(self.__FORMAT[self.size], self.program.response, self.offset)[0]
