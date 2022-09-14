from typing import Any, Optional, Sequence, Tuple

import numpy as np

from qcodes import validators as vals
from qcodes.instrument import VisaInstrument
from qcodes.instrument.channel import ChannelList, InstrumentChannel, InstrumentModule
from qcodes.instrument.parameter import Parameter
from qcodes.utils.helpers import create_on_off_val_mapping


class Output(InstrumentModule):
    def __init__(self, parent: 'WW1070', name: str, **kwargs: Any):
        super().__init__(parent, name, **kwargs)

        self.state = Parameter(
            name="state",
            instrument=self,
            set_cmd=f":output:state {{}}",
            get_cmd=":output:state?",
            val_mapping=create_on_off_val_mapping(),
            docstring="Turn the output on and off",
        )

        self.filter = Parameter(
            name="filter",
            instrument=self,
            set_cmd=f":output:filter {{}}",
            get_cmd=":output:filter?",
            vals=vals.Enum("none", "25M", "50M", "all"),
            docstring="Select the filter that is connected to the output",
        )

class Function(InstrumentModule):
    def __init__(self, parent: 'WW1070', name: str, **kwargs: Any):
        super().__init__(parent, name, **kwargs)

        self.mode = Parameter(
            name="mode",
            instrument=self,
            set_cmd=f"function:mode {{}}",
            get_cmd="function:mode?",
            vals=vals.Enum("fixed", "user", "sequence"),
            docstring="Type of waveform at the output connector",
        )

        self.shape = Parameter(
            name="shape",
            instrument=self,
            set_cmd=f"function:shape {{}}",
            get_cmd="function:shape?",
            docstring="Shape of the waveform at the output connector",
        )

class Voltage(InstrumentModule):
    def __init__(self, parent: 'WW1070', name: str, **kwargs: Any):
        super().__init__(parent, name, **kwargs)

        self.amplitude = Parameter(
            name="amplitude",
            instrument=self,
            set_cmd=f":voltage {{}}",
            get_cmd=":voltage?",
            get_parser=float,
            vals=vals.MultiType(vals.Numbers(10e-3, 10),
                                vals.Enum("minimum", "maximum")),
            docstring="Peak to peak amplitude of the output waveform",
        )

        self.offset = Parameter(
            name="offset",
            instrument=self,
            set_cmd=f":voltage:offset {{}}",
            get_cmd=":voltage:offset?",
            get_parser=float,
            vals=vals.Numbers(-4.5, 4.5),
            docstring="Amplitude offset of the output waveform",
        )

class WW1070(VisaInstrument):
    """
    This is the QCoDeS driver for the Keysight InfiniiVision oscilloscopes
    """

    def __init__(
        self,
        name: str,
        address: str,
        timeout: float = 20,
        silence_pyvisapy_warning: bool = False,
        **kwargs: Any,
    ):
        """
        Initialises the arbitrary waveform generator.
        Args:
            name: Name of the instrument used by QCoDeS
            address: Instrument address as used by VISA
            timeout: Visa timeout, in secs.
            channels: The number of channels on the scope.
            silence_pyvisapy_warning: Don't warn about pyvisa-py at startup
        """
        super().__init__(name, address, timeout=timeout, terminator="\n", **kwargs)
        self.connect_message()

        self.model = self.IDN()['model']

        self.add_submodule("output", Output(self, "output"))
        self.add_submodule("function", Function(self, "function"))
        self.add_submodule("voltage", Voltage(self, "voltage"))
