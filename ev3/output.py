from .var import Variable

class Output:
    """
    Output operations
    """

    def __init__(self, cmds):
        self.cmds = cmds
        self.layer(0)  # use layer 0 by default
        self.__ports = lambda x: x  # require ports to be specified explicitly

    def layer(self, n):
        """
        Control the default layer, which only matters for daisy chaining
        """
        self.__layer = lambda o: o if o else n
        return self

    def ports(self, n):
        """
        Specify the default ports to control

        n: bit fields of size 4
        """
        self.__ports = lambda o: o if o else n
        return self

    def __head(self,op: int, ports, layer):
        return self.cmds.op(op).p1(self.__layer(layer)).p1(self.__ports(ports))


    def reset(self, ports: int = None, layer: int = None):
        """
        Reset the tacho count of motors
        """
        self.__head(0xA2, ports, layer)
        return self

    def stop(self, brake: bool = False, ports: int = None, layer: int = None):
        """
        Stop the motor

        brake: if true, the motor actively tries to hold the stop. Otherwise it's free
        """
        self.__head(0xA3, ports, layer).p1(1 if brake else 0)
        return self

    def power(self, power: int, ports: int = None, layer: int = None):
        """
        Set the power level

        power: [-100,100]
        """
        self.__head(0xA4, ports, layer).p1(power)
        return self

    def speed(self, speed: int, ports: int = None, layer: int = None):
        """
        Set the speed level. The device will adjust the power to achieve the right speed.

        power: [-100,100]
        """
        self.__head(0xA5, ports, layer).p1(speed)
        return self

    def start(self, ports: int = None, layer: int = None):
        """
        Start the motors
        """
        self.__head(0xA6, ports, layer)
        return self

    def polarity(self, polarity: int, ports: int = None, layer: int = None):
        """
        Start the motors
        """
        self.__head(0xA7, ports, layer).p1(polarity)
        return self

    def read(self, speed: Variable, tacho: Variable, ports: int = None, layer: int = None):
        """
        Read the current motor speed and tacho count
        """
        self.__head(0xA8, ports, layer).p1(speed).p4(tacho)
        return self

    def ready(self, ports: int = None, layer: int = None):
        """
        Wait until motors get idle
        """
        self.__head(0xAA, ports, layer)
        return self

    def move_by_step(self, step1:int, step2:int, step3:int, power: int = None, speed: int = None, brake: bool = False, ports: int = None, layer: int = None):
        """
        ramp up, sustain, and ramp down, counted in tacho counts, and given in power or speed

        power/speed [-100,100]
        """
        self.__move(0xAC, 0xAE, step1, step2, step3, power, speed, brake, ports, layer)

    def move_by_time(self, step1:int, step2:int, step3:int, power: int = None, speed: int = None, brake: bool = False, ports: int = None, layer: int = None):
        """
        ramp up, sustain, and ramp down, counted in milliseconds, and given in power or speed

        power/speed [-100,100]
        """
        self.__move(0xAD, 0xAF, step1, step2, step3, power, speed, brake, ports, layer)

    def __move(self, powerOpCode:int, speedOpCode:int, step1:int, step2:int, step3:int, power: int = None, speed: int = None, brake: bool = False, ports: int = None, layer: int = None):
        if speed != None and power != None:
            raise Exception("speed and power are mutually exclusive")
        level = speed if speed else power
        if level == None:
            raise Exception("speed or power must be specified")

        self.__head(powerOpCode if power else speedOpCode, ports, layer).p1(level).p4(step1).p4(step2).p4(step3).p1(1 if brake else 0)