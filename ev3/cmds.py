import struct
from .sound import Sound

class EV3Cmds():
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

    def op(self,op):
        """
        Start a builder that packs arguments for a given operation
        """
        return self.Builder(self.cmds).b(op)

    _DIRECT_COMMAND_REPLY       = 0x00
    _DIRECT_COMMAND_NO_REPLY    = 0x80

    class Builder():
        def __init__(self,cmds):
            self.cmds = cmds

        def bytes(self, bytes):
            """
            Appends bytes to cmds
            """
            self.cmds += bytes
            return self

        def p(self,*args):
            """
            Pack arguments to cmds
            """
            return self.bytes(struct.pack(*args))

        def b(self,v):
            """
            Pack one byte as-is
            """
            return self.p('<B', v&0xFF)

        def c(self,v):
            """
            Encode a constant into a variable length byte sequence
            """
            if -32<=v and v<32:
                return self.p('<b', v&0x1F)       # 6 bits
            if -128<=v and v<128:
                return self.p('<Bb', 0x81, v)     # 8 bits
            if -32768<=v and v<32768:
                return self.p('<Bh', 0x82, v)     # 16 bits
            else:
                return self.p('<Bi', 0x83, v)     # 32 bits

        def s(self,s):
            """
            Encode a string
            """
            return self.bytes(b'\x84' + s.encode() + b'\x00')
