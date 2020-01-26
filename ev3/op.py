class Op():
    """
    Base class for operation group
    """

    def __init__(self,cmds:'EV3Cmds', op:int):
        self.cmds = cmds
        self.op = op

    def cmd(self,c):
        return self.cmds.cmd(self.op,c)
