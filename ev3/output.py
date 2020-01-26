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
        return self.cmds.op(op).c(self.__layer(layer)).c(self.__ports(ports))


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
        self.__head(0xA3, ports, layer).c(1 if brake else 0)
        return self

    def power(self, power: int, ports: int = None, layer: int = None):
        """
        Set the power level

        power: [-100,100]
        """
        self.__head(0xA4, ports, layer).c(power)
        return self

    def speed(self, speed: int, ports: int = None, layer: int = None):
        """
        Set the speed level. The device will adjust the power to achieve the right speed.

        power: [-100,100]
        """
        self.__head(0xA5, ports, layer).c(speed)
        return self

    def start(self, ports: int = None, layer: int = None):
        """
        Start the motors
        """
        self.__head(0xA6, ports, layer)
        return self
