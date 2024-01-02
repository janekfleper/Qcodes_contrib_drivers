from qcodes import validators as vals
from qcodes.parameters import Parameter, Function
from qcodes.instrument import VisaInstrument, InstrumentModule
from qcodes.utils.helpers import create_on_off_val_mapping

class RohdeSchwarzRTB2000EdgeTrigger(InstrumentModule):
    def __init__(self, parent: "RohdeSchwarzRTB2000Trigger", name: str, **kwargs):
        super().__init__(parent, name, **kwargs)

        self.slope = Parameter(
            name="slope",
            instrument=self,
            get_cmd="trigger:a:edge:slope?",
            set_cmd="trigger:a:edge:slope {}",
            vals=vals.Enum("positive", "negative", "either"),
            label="Slope for the Edge Trigger",
        )

        self.coupling = Parameter(
            name="coupling",
            instrument=self,
            get_cmd="trigger:a:edge:coupling?",
            set_cmd="trigger:a:edge:coupling {}",
            vals=vals.Enum("dc", "ac", "lfreject"),
            label="Coupling for the Trigger Source",
        )

        self.hf_reject = Parameter(
            name="hf_reject",
            instrument=self,
            get_cmd="trigger:a:edge:filter:hfreject?",
            set_cmd="trigger:a:edge:filter:hfreject {}",
            val_mapping=create_on_off_val_mapping(on_val=1, off_val=0),
            label="HF Reject for the Trigger Source",
        )

        self.noise_reject = Parameter(
            name="noise_reject",
            instrument=self,
            get_cmd="trigger:a:edge:filter:nreject?",
            set_cmd="trigger:a:edge:filter:nreject {}",
            val_mapping=create_on_off_val_mapping(on_val=1, off_val=0),
            label="Noise Reject for the Trigger Source",
        )


class RohdeSchwarzRTB2000WidthTrigger(InstrumentModule):
    def __init__(self, parent: "RohdeSchwarzRTB2000Trigger", name: str, **kwargs):
        super().__init__(parent, name, **kwargs)

        self.polarity = Parameter(
            name="polarity",
            instrument=self,
            get_cmd="trigger:a:width:polarity?",
            set_cmd="trigger:a:width:polarity {}",
            vals=vals.Enum("positive", "negative"),
            label="Pulse Polarity",
        )

        self.range = Parameter(
            name="range",
            instrument=self,
            get_cmd="trigger:a:width:range?",
            set_cmd="trigger:a:width:range {}",
            vals=vals.Enum("within", "outside", "shorter", "longer"),
            label="Pulse Width Measurement",
        )

        self.width = Parameter(
            name="width",
            instrument=self,
            get_cmd="trigger:a:width:width?",
            set_cmd="trigger:a:width:width {}",
            vals=vals.Numbers(min_value=20e-9, max_value=6.87194685440),
            get_parser=float,
            label="Pulse Width",
        )

        self.delta = Parameter(
            name="delta",
            instrument=self,
            get_cmd="trigger:a:width:delta?",
            set_cmd="trigger:a:width:delta {}",
            vals=vals.Numbers(min_value=6.4e-9, max_value=0.053687088),
            get_parser=float,
            label="Pulse Width Variation",
        )

class RohdeSchwarzRTB2000Trigger(InstrumentModule):
    def __init__(self, parent: "RohdeSchwarzRTB2000", name: str, **kwargs):
        super().__init__(parent, name, **kwargs)

        self.mode = Parameter(
            name="mode",
            instrument=self,
            get_cmd="trigger:a:mode?",
            set_cmd="trigger:a:mode {}",
            vals=vals.Enum("auto", "normal"),
            label="Trigger Mode",
        )

        self.source = Parameter(
            name="source",
            instrument=self,
            get_cmd="trigger:a:source?",
            set_cmd="trigger:a:source {}",
            vals=vals.Enum("ch1", "ch2", "ch3", "ch4", "ext", "line"),
            label="Trigger Source",
        )

        self.type = Parameter(
            name="type",
            instrument=self,
            get_cmd="trigger:a:type?",
            set_cmd="trigger:a:type {}",
            vals=vals.Enum("edge", "width", "tv", "bus", "logic", "line"),
            label="Trigger Type",
        )

        self.holdoff_mode = Parameter(
            name="holdoff_mode",
            instrument=self,
            get_cmd="trigger:a:holdoff:mode?",
            set_cmd="trigger:a:holdoff:mode {}",
            vals=vals.Enum("time", "off", "tv", "bus", "logic", "line"),
            label="Trigger Holdoff",
        )

        self.holdoff_time = Parameter(
            name="holdoff_time",
            instrument=self,
            get_cmd="trigger:a:holdoff:time?",
            set_cmd="trigger:a:holdoff:time {}",
            vals=vals.Numbers(min_value=51.2e-9, max_value=13.7),
            get_parser=float,
            label="Trigger Holdoff Time",
        )

        self.level = Parameter(
            name="level",
            instrument=self,
            get_cmd="trigger:a:level?",
            set_cmd="trigger:a:level {}",
            vals=vals.Numbers(min_value=-25, max_value=25),
            get_parser=float,
            label="Trigger Level",
        )

        self.find_level = Function(
            name="find_level",
            instrument=self,
            call_cmd="trigger:a:findlevel",
        )

        self.add_submodule("edge", RohdeSchwarzRTB2000EdgeTrigger(self, "edge"))
        self.add_submodule("width", RohdeSchwarzRTB2000WidthTrigger(self, "width"))

class RohdeSchwarzRTB2000(VisaInstrument):
    """
    QCoDeS driver for the Rohde&Schwarz RTB2000 family
    """

    def __init__(self, name: str, address: str, **kwargs):
        super().__init__(name=name, address=address, terminator="\n", **kwargs)

        self.add_submodule("trigger", RohdeSchwarzRTB2000Trigger(self, "trigger"))
