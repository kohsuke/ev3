from .op import Op

class Sound(Op):
    """
    Sound operations
    """
    def __init__(self,cmds):
        super().__init__(cmds, 0x94)

    def tone(self, volume:int, frequency:int, duration:int):
        """
        Play a monotone

        volume: percent (0-100)
        frequency: Hz (250-10000)
        duration: milliseconds or 0, which is forever
        """
        self.cmd(0x01).c(volume).c(frequency).c(duration)
        return self

    def play(self, volume:int, name:str):
        """
        Play a sound file

        volume: percent (0-100)
        name: sound file name
        """
        self.cmd(0x02).c(volume).s(name)
        return self

    def ready(self):
        """
        block until sound finishes playing
        """
        self.cmd(0x96)