

class UI():
    OPUI_WRITE = 0x82

    """
    UI operations
    """
    def __init__(self,cmds):
        self.cmds = cmds

    def led(self, color:str, mode:str):
        """
        Change LED mode

        color:  'red', 'green', 'orange'
        mode:   'on', 'off', 'pulse', 'flash'
        """
        c = ['green','red','orange'].index(color)
        m = ['off','on','flash','pulse'].index(mode)
        if m==0:
            v = 0
        else:
            v = (m-1)*3 + c + 1

        self.cmds.op(self.OPUI_WRITE).b(0x1b).p1(v)
        return self

