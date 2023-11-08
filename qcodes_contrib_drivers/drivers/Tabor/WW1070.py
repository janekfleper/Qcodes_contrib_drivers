from typing import Any, Optional, Sequence, Tuple

import numpy as np

from qcodes import validators as vals
from qcodes.instrument import VisaInstrument
from qcodes.instrument.channel import ChannelList, InstrumentChannel, InstrumentModule
from qcodes.instrument.parameter import Parameter
from qcodes.utils.helpers import create_on_off_val_mapping


class Output(InstrumentModule):
    def __init__(self, parent: "WW1070", name: str, **kwargs: Any):
        super().__init__(parent, name, **kwargs)

        self.state = Parameter(
            name="state",
            instrument=self,
            set_cmd=f"output:state {{}}",
            get_cmd="output:state?",
            val_mapping=create_on_off_val_mapping(on_val=1, off_val=0),
            docstring="Turn the output on and off",
        )

        self.filter = Parameter(
            name="filter",
            instrument=self,
            set_cmd=f"output:filter {{}}",
            get_cmd="output:filter?",
            vals=vals.Enum("none", "25M", "50M", "all"),
            docstring="Select the filter that is connected to the output",
        )


class Function(InstrumentModule):
    def __init__(self, parent: "WW1070", name: str, **kwargs: Any):
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
    def __init__(self, parent: "WW1070", name: str, **kwargs: Any):
        super().__init__(parent, name, **kwargs)

        self.level = Parameter(
            name="level",
            instrument=self,
            set_cmd=f"voltage:level {{}}",
            get_cmd="voltage:level?",
            get_parser=float,
            vals=vals.MultiType(
                vals.Numbers(10e-3, 10), vals.Enum("minimum", "maximum")
            ),
            docstring="Peak to peak amplitude of the output waveform",
        )

        self.offset = Parameter(
            name="offset",
            instrument=self,
            set_cmd=f"voltage:offset {{}}",
            get_cmd="voltage:offset?",
            get_parser=float,
            vals=vals.Numbers(-4.5, 4.5),
            docstring="Amplitude offset of the output waveform",
        )


class Trigger(InstrumentModule):
    def __init__(self, parent: "WW1070", name: str, **kwargs: Any):
        super().__init__(parent, name, **kwargs)

        self.burst = Parameter(
            name="burst",
            instrument=self,
            set_cmd="trigger:burst {}",
            get_cmd="trigger:burst?",
            val_mapping=create_on_off_val_mapping(on_val=1, off_val=0),
            docstring="Turn the burst mode on and off",
        )

        self.count = Parameter(
            name="count",
            instrument=self,
            set_cmd="trigger:count {}",
            get_cmd="trigger:count?",
            get_parser=int,
            vals=vals.Ints(1, 1000000),
            docstring="Trigger burst counter",
        )

        self.gate = Parameter(
            name="gate",
            instrument=self,
            set_cmd="trigger:gate {}",
            get_cmd="trigger:gate?",
            val_mapping=create_on_off_val_mapping(on_val=1, off_val=0),
            docstring="Turn the gate mode on and off",
        )

        self.phase = Parameter(
            name="phase",
            instrument=self,
            set_cmd="trigger:phase {}",
            get_cmd="trigger:phase?",
            get_parser=int,
            vals=vals.Ints(0, 2000000),
            docstring="Trigger start phase",
        )

        self.slope = Parameter(
            name="slope",
            instrument=self,
            set_cmd="trigger:slope {}",
            get_cmd="trigger:slope?",
            vals=vals.Enum("positive", "negative"),
            docstring="Set the edge sensitivity for the trigger input",
        )

        self.source = Parameter(
            name="source",
            instrument=self,
            set_cmd="trigger:source:advance {}",
            get_cmd="trigger:source:advance?",
            vals=vals.Enum("external", "internal"),
            docstring="Set trigger input source",
        )

        self.timer = Parameter(
            name="timer",
            instrument=self,
            set_cmd="trigger:timer {}",
            get_cmd="trigger:timer?",
            get_parser=float,
            vals=vals.Numbers(100e-3, 2e6),
            docstring="Set the timer for the internal trigger generator",
        )

        self.immediate = Function(
            name="immediate",
            instrument=self,
            call_cmd="trigger:immediate",
            docstring="Simulate a trigger event",
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
        **kwargs: Any,
    ):
        """
        Initialises the arbitrary waveform generator.
        Args:
            name: Name of the instrument used by QCoDeS
            address: Instrument address as used by VISA
            timeout: Visa timeout, in secs.
            channels: The number of channels on the scope.
        """
        super().__init__(name, address, timeout=timeout, terminator="\n", **kwargs)
        self.connect_message()

        self.model = self.IDN()["model"]

        self.add_submodule("output", Output(self, "output"))
        self.add_submodule("function", Function(self, "function"))
        self.add_submodule("voltage", Voltage(self, "voltage"))
        self.add_submodule("trigger", Trigger(self, "trigger"))
