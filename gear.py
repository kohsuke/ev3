class Gear:
    TURRET = 56
    BIG = 40
    MEDIUM = 24


    """
    Represents a specific gear ratio.
    Used as a callable object to map the degree to tach count
    """
    def __init__(self, src:int, dst:int):
        self.src = src
        self.dst = dst

    def __call__(self, degree:int):
        return int(degree * self.dst / self.src)