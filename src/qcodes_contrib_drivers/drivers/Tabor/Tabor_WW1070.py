from typing import Any, Optional, Sequence, Tuple

import numpy as np

from qcodes import validators as vals
from qcodes.instrument import VisaInstrument
from qcodes.instrument.channel import ChannelList, InstrumentChannel, InstrumentModule
from qcodes.instrument.function import Function
from qcodes.instrument.parameter import Parameter
from qcodes.utils.helpers import create_on_off_val_mapping


class TaborWW1070Output(InstrumentModule):
    def __init__(self, parent: "TaborWW1070", name: str, **kwargs: Any):
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
            vals=vals.Enum("NONE", "25M", "50M", "ALL"),
            docstring="Select the filter that is connected to the output",
        )


class TaborWW1070Function(InstrumentModule):
    def __init__(self, parent: "TaborWW1070", name: str, **kwargs: Any):
        super().__init__(parent, name, **kwargs)

        self.mode = Parameter(
            name="mode",
            instrument=self,
            set_cmd="function:mode {}",
            get_cmd="function:mode?",
            vals=vals.Enum("FIX", "USER", "SEQ"),
            docstring="Type of waveform at the output connector",
        )

        self.shape = Parameter(
            name="shape",
            instrument=self,
            set_cmd="function:shape {}",
            get_cmd="function:shape?",
            vals=vals.Enum(
                "SIN", "TRI", "SQU", "PULS", "RAMP", "SINC", "EXP", "GAUS", "NOIS", "DC"
            ),
            docstring="Shape of the waveform at the output connector",
        )


class TaborWW1070Voltage(InstrumentModule):
    def __init__(self, parent: "TaborWW1070", name: str, **kwargs: Any):
        super().__init__(parent, name, **kwargs)

        self.amplitude = Parameter(
            name="amplitude",
            instrument=self,
            set_cmd="voltage {}",
            get_cmd="voltage?",
            get_parser=float,
            vals=vals.MultiType(vals.Numbers(10e-3, 10), vals.Enum("MIN", "MAX")),
            docstring="Peak to peak amplitude of the output waveform",
        )

        self.offset = Parameter(
            name="offset",
            instrument=self,
            set_cmd="voltage:offset {}",
            get_cmd="voltage:offset?",
            get_parser=float,
            vals=vals.Numbers(-4.5, 4.5),
            docstring="Amplitude offset of the output waveform",
        )


class TaborWW1070Trigger(InstrumentModule):
    def __init__(self, parent: "TaborWW1070", name: str, **kwargs: Any):
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
            vals=vals.Enum("POS", "NEG"),
            docstring="Set the edge sensitivity for the trigger input",
        )

        self.source = Parameter(
            name="source",
            instrument=self,
            set_cmd="trigger:source:advance {}",
            get_cmd="trigger:source:advance?",
            vals=vals.Enum("EXT", "INT"),
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


class TaborWW1070(VisaInstrument):
    """
    This is the QCoDeS driver for the Tabor WW1070 series AWG
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
        super().__init__(name, address, timeout=timeout, terminator="\r\n", **kwargs)
        self.connect_message()

        self.model = self.IDN()["model"]

        self.opt = Parameter(
            name="opt",
            instrument=self,
            set_cmd=False,
            get_cmd="*opt?",
            docstring="Query the device options",
        )

        self.error = Parameter(
            name="error",
            instrument=self,
            set_cmd=False,
            get_cmd=":system:error?",
            docstring="Query for error codes",
        )

        self.add_submodule("output", TaborWW1070Output(self, "output"))
        self.add_submodule("function", TaborWW1070Function(self, "function"))
        self.add_submodule("voltage", TaborWW1070Voltage(self, "voltage"))
        self.add_submodule("trigger", TaborWW1070Trigger(self, "trigger"))
