class Sound():
    """
    Sound operations
    """
    def __init__(self,cmds):
        self.cmds = cmds

    def tone(self, volume:int, frequency:int, duration:int):
        """
        Play a monotone

        volume: percent (0-100)
        frequency: Hz (250-10000)
        duration: milliseconds or 0, which is forever
        """
        self.cmds.op(0x94).b(0x01).p1(volume).p2(frequency).p2(duration)
        return self

    def play(self, volume:int, name:str):
        """
        Play a sound file

        volume: percent (0-100)
        name: sound file name
        """
        self.cmds.op(0x94).b(0x02).p1(volume).s(name)
        return self

    def ready(self):
        """
        block until sound finishes playing
        """
        self.cmds.op(0x96)