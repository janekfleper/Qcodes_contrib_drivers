from qcodes.instrument import VisaInstrument

class RohdeSchwarzRTB2000(VisaInstrument):
    """
    QCoDeS driver for the Rohde&Schwarz RTB2000 family
    """

    def __init__(self, name: str, address: str, **kwargs):
        super().__init__(name=name, address=address, terminator="\n", **kwargs)
