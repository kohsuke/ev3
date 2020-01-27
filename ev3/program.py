import struct
import io
from .sound import Sound
from .ui import UI
from .output import Output
from .var import *


class Program:
    """
    Represents a sequence of commands that expose
    low-level EV3 capability building blocks.

    Otherwise known as "EV3 direct commands"
    """

    def __init__(self):
        self.cmds = bytearray()     # packed bytes representing commands
        self.seqNum = 42            # command sequence number
        self.localMem = 0           # local variables used
        self.globalMem = 0          # global variables used
        self.sound = Sound(self)
        self.ui = UI(self)
        self.output = Output(self)

        self.response = []          # response from the last command sent. used by global variables

    def __align(self, i:int, sz:int):
        """
            Pad the length to the multiple of 'sz'
        """
        return (i+sz)//sz * sz;

    def localVar(self, size:int):
        """
        Allocates a local variable, which can then be used as parameters to commands later
        """
        self.localMem = self.__align(self.localMem, size)
        v = LocalVariable(self, self.localMem, size)
        self.localMem += size
        return v

    def globalVar(self, size:int):
        """
        Allocates a global variable, which can then be used as parameters to commands later.
        """
        self.globalMem = self.__align(self.globalMem, size)
        v = GlobalVariable(self, self.globalMem, size)
        self.globalMem += size
        return v

    def encode(self) -> bytes:
        """
        Packs the commands given thus far to a  packet byte array
        """
        return struct.pack('<hhBh',
                    len(self.cmds)+5,
                    self.seqNum,
                    self._DIRECT_COMMAND_REPLY,
                    self.localMem * 1024 + self.globalMem) + self.cmds

    def send(self, writable):
        """
        Write this command sequence to a given file handle
        """
        writable.write(self.encode())

        # read response
        rsp = writable.read(2048)
        # rspLen = struct.unpack('<H',rsp[:2])[0]
        seqNum,code=struct.unpack('<Hb',rsp[2:5])
        if code != self._DIRECT_REPLY:
            raise Exception("Command execution failed %d"%code)
        # TODO: verify that seqNum checks out
        self.response = rsp[5:]

    def op(self, op):
        """
        Start a builder that packs arguments for a given operation
        """
        return self.Builder(self.cmds).b(op)

    _DIRECT_COMMAND_REPLY       = 0x00
    _DIRECT_COMMAND_NO_REPLY    = 0x80

    _DIRECT_REPLY               = 0x02
    _DIRECT_REPLY_ERROR         = 0x04

    class Builder:
        def __init__(self, cmds):
            self.cmds = cmds

        def bytes(self, bytes):
            """
            Appends bytes to cmds
            """
            self.cmds += bytes
            return self

        def f(self, *args):
            """
            Format & pack arguments to cmds
            """
            return self.bytes(struct.pack(*args))

        def b(self, v):
            """
            Pack one byte as-is
            """
            return self.f('<B', v & 0xFF)

        def p1(self, v):
            return self.p(v,1)

        def p2(self, v):
            return self.p(v,2)

        def p4(self, v):
            return self.p(v,4)

        def c(self):
            pass

        def p(self, v, size: int):
            """
            Encode a parameter into a variable length byte sequence

            size: size of the parameter in bytes, to verify that the variables given is consistent in size
            """
            flag = 0    # literal
            if isinstance(v,Variable):
                if isinstance(v,LocalVariable):
                    flag = 0x40
                elif isinstance(v,GlobalVariable):
                    flag = 0x60
                if size != v.size:
                    raise Exception("Expecting variable of size %d but got %d instead"%(size,v.size))
                v = v.offset

            if -32 <= v < 32:
                return self.f('<b', flag | v & 0x3F)       # 6 bits
            if -128 <= v < 128:
                return self.f('<Bb', flag | 0x81, v)        # 8 bits
            if -32768 <= v < 32768:
                return self.f('<Bh', flag | 0x82, v)        # 16 bits
            else:
                return self.f('<Bi', flag | 0x83, v)        # 32 bits

        def s(self, s):
            """
            Encode a string
            """
            return self.bytes(b'\x84' + s.encode() + b'\x00')
