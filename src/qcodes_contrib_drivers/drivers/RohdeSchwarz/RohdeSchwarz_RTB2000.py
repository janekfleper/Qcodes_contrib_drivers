import numpy as np

from qcodes import validators as vals
from qcodes.parameters import Parameter, Function
from qcodes.parameters.val_mapping import create_on_off_val_mapping
from qcodes.instrument import VisaInstrument, InstrumentModule, InstrumentChannel, ChannelList

DATATYPES = {"REAL,32": "f", "UINT,8": "B", "UINT,16": "H", "UINT,32": "I"}

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

class RohdeSchwarzRTB2000Cursor(InstrumentModule):
    def __init__(self, parent: "RohdeSchwarzRTB2000", name: str, **kwargs):
        super().__init__(parent, name, **kwargs)

        self.state = Parameter(
            name="state",
            instrument=self,
            get_cmd=f"cursor:state?",
            set_cmd=f"cursor:state {{}}",
            val_mapping=create_on_off_val_mapping(on_val=1, off_val=0),
            label="Cursor State",
        )

        self.function = Parameter(
            name="function",
            instrument=self,
            get_cmd=f"cursor:function?",
            set_cmd=f"cursor:function {{}}",
            vals=vals.Enum("horizontal", "vertical", "hvertical"),
            label="Cursor Function",
        )

        self.source = Parameter(
            name="source",
            instrument=self,
            get_cmd=f"cursor:source?",
            set_cmd=f"cursor:source {{}}",
            vals=vals.Strings(),
            label="Cursor Source",
        )

        self.tracking = Parameter(
            name="tracking",
            instrument=self,
            get_cmd=f"cursor:tracking?",
            set_cmd=f"cursor:tracking {{}}",
            val_mapping=create_on_off_val_mapping(on_val=1, off_val=0),
            label="Cursor Tracking State",
        )

        self.x1 = Parameter(
            name="x1",
            instrument=self,
            get_cmd=f"cursor:x1position?",
            set_cmd=f"cursor:x1position {{}}",
            vals=vals.Numbers(),
            get_parser=float,
            label="Cursor X1 Position",
        )

        self.x2 = Parameter(
            name="x2",
            instrument=self,
            get_cmd=f"cursor:x2position?",
            set_cmd=f"cursor:x2position {{}}",
            vals=vals.Numbers(),
            get_parser=float,
            label="Cursor X2 Position",
        )

        self.x_delta = Parameter(
            name="x_delta",
            instrument=self,
            get_cmd=f"cursor:xdelta?",
            set_cmd=False,
            get_parser=float,
            label="Cursor X1 - X2",
        )

        self.y1 = Parameter(
            name="y1",
            instrument=self,
            get_cmd=f"cursor:y1position?",
            set_cmd=f"cursor:y1position {{}}",
            vals=vals.Numbers(),
            get_parser=float,
            label="Cursor Y1 Position",
        )

        self.y2 = Parameter(
            name="y2",
            instrument=self,
            get_cmd=f"cursor:y2position?",
            set_cmd=f"cursor:y2position {{}}",
            vals=vals.Numbers(),
            get_parser=float,
            label="Cursor Y2 Position",
        )

        self.y_delta = Parameter(
            name="y_delta",
            instrument=self,
            get_cmd=f"cursor:ydelta?",
            set_cmd=False,
            get_parser=float,
            label="Cursor Y1 - Y2",
        )

        self.x_coupling = Parameter(
            name="x_coupling",
            instrument=self,
            get_cmd=f"cursor:xcoupling?",
            set_cmd=f"cursor:xcoupling {{}}",
            val_mapping=create_on_off_val_mapping(on_val=1, off_val=0),
            label="Cursor X Coupling",
        )

        self.y_coupling = Parameter(
            name="y_coupling",
            instrument=self,
            get_cmd=f"cursor:ycoupling?",
            set_cmd=f"cursor:ycoupling {{}}",
            val_mapping=create_on_off_val_mapping(on_val=1, off_val=0),
            label="Cursor Y Coupling",
        )

        self.autoset = Function(
            name="autoset",
            instrument=self,
            call_cmd="cursor:swave",
        )

        self.autoscale = Parameter(
            name="autoscale",
            instrument=self,
            get_cmd=f"cursor:tracking:scale?",
            set_cmd=f"cursor:tracking:scale {{}}",
            val_mapping=create_on_off_val_mapping(on_val=1, off_val=0),
            label="Cursor Autoscale",
        )

class RohdeSchwarzRTB2000MeasurementStatistics(InstrumentModule):
    def __init__(self, parent: "RohdeSchwarzRTB2000Measurement", name: str, measurement: int, **kwargs):
        super().__init__(parent, name, **kwargs)
        self.measurement = measurement

        self.state = Parameter(
            name="state",
            instrument=self,
            get_cmd=f"measurement{self.measurement}:statistics:enable?",
            set_cmd=f"measurement{self.measurement}:statistics:enable {{}}",
            val_mapping=create_on_off_val_mapping(on_val=1, off_val=0),
            label="Measurement Statistics",
        )

        self.reset = Function(
            name="reset",
            instrument=self,
            call_cmd=f"measurement{self.measurement}:statistics:reset",
        )

    def values(self):
        """Read all values from the statistics buffer

        The buffer size is always 1000. If there are fewer values currently
        stored in the buffer, the empty values will be "9.91E+37". These
        values are not included in the array that is returned.

        Returns:
            numpy.ndarray, dtype = float
        """
        values = self.ask(f"measurement{self.measurement}:statistics:value:all?")
        return np.array([float(value) for value in values.split(",") if value != "9.91E+37"])

    def value(self, n: int) -> float:
        """Read a single value from the statistics buffer

        The value "9.91E+37" is returned as NaN.

        Args:
            n: Buffer index, must be in [1, 1000]

        Returns:
            float
        """
        if n < 1 or n > 1000:
            raise ValueError(f"{n} is invalid: must be between 1 and 1000 inclusive")
        value = self.ask(f"measurement{self.measurement}:statistics:value{n}?")
        return float(value) if value != "9.91E+37" else np.nan

class RohdeSchwarzRTB2000Measurement(InstrumentChannel):
    def __init__(self, parent: "RohdeSchwarzRTB2000", name: str, measurement: int, **kwargs):
        super().__init__(parent, name, **kwargs)
        self.measurement = measurement

        self.state = Parameter(
            name="state",
            instrument=self,
            get_cmd=f"measurement{self.measurement}:enable?",
            set_cmd=f"measurement{self.measurement}:enable {{}}",
            val_mapping=create_on_off_val_mapping(on_val=1, off_val=0),
            label="Measurement State",
        )

        self.type = Parameter(
            name="type",
            instrument=self,
            get_cmd=f"measurement{self.measurement}:main?",
            set_cmd=f"measurement{self.measurement}:main {{}}",
            vals=vals.Strings(),
            label="Measurement Type",
        )

        self.source = Parameter(
            name="source",
            instrument=self,
            get_cmd=f"measurement{self.measurement}:source?",
            set_cmd=f"measurement{self.measurement}:source {{}}",
            vals=vals.Strings(),
            label="Measurement Source",
        )

        self.delay_slope = Parameter(
            name="delay_slope",
            instrument=self,
            get_cmd=f"measurement{self.measurement}:delay:slope?",
            set_cmd=f"measurement{self.measurement}:delay:slope {{}}",
            vals=vals.Strings(),
            label="Measurement Delay Slope",
        )

        self.result = Parameter(
            name="result",
            instrument=self,
            get_cmd=f"measurement{self.measurement}:result:actual?",
            set_cmd=False,
            get_parser=float,
            label="Measurement Result",
        )

        self.average = Parameter(
            name="average",
            instrument=self,
            get_cmd=f"measurement{self.measurement}:result:average?",
            set_cmd=False,
            get_parser=float,
            label="Measurement Average",
        )

        self.std = Parameter(
            name="std",
            instrument=self,
            get_cmd=f"measurement{self.measurement}:result:stddev?",
            set_cmd=False,
            get_parser=float,
            label="Measurement Standard Deviation",
        )

        self.minimum = Parameter(
            name="minimum",
            instrument=self,
            get_cmd=f"measurement{self.measurement}:result:npeak?",
            set_cmd=False,
            get_parser=float,
            label="Measurement Minimum Result",
        )

        self.maximum = Parameter(
            name="maximum",
            instrument=self,
            get_cmd=f"measurement{self.measurement}:result:ppeak?",
            set_cmd=False,
            get_parser=float,
            label="Measurement Maximum Result",
        )

        self.waveform_count = Parameter(
            name="waveform_count",
            instrument=self,
            get_cmd=f"measurement{self.measurement}:result:wfmcount?",
            set_cmd=False,
            get_parser=int,
            label="Measurement Waveform Count",
        )

        self.add_submodule("statistics", RohdeSchwarzRTB2000MeasurementStatistics(self, "statistics", self.measurement))

class RohdeSchwarzRTB2000Timebase(InstrumentModule):
    def __init__(self, parent: "RohdeSchwarzRTB2000", name: str, **kwargs):
        super().__init__(parent, name, **kwargs)

        self.scale = Parameter(
            name="scale",
            instrument=self,
            get_cmd="timebase:scale?",
            set_cmd="timebase:scale {}",
            vals=vals.Numbers(min_value=1e-9, max_value=500),
            get_parser=float,
            label="Horizontal Scale",
        )

        self.position = Parameter(
            name="position",
            instrument=self,
            get_cmd="timebase:position?",
            set_cmd="timebase:position {}",
            vals=vals.Numbers(min_value=-5999.856, max_value=51539607.402),
            get_parser=float,
            label="Horizontal Position",
        )

        self.reference = Parameter(
            name="reference",
            instrument=self,
            get_cmd="timebase:reference?",
            set_cmd="timebase:reference {}",
            val_mapping={"left": 8.33, "middle": 50, "right": 91.7},
            get_parser=float,
            label="Horizontal Reference Point",
        )

        self.range = Parameter(
            name="range",
            instrument=self,
            get_cmd="timebase:range?",
            set_cmd="timebase:range {}",
            vals=vals.Numbers(min_value=1.2e-8, max_value=6000),
            get_parser=float,
            label="Horizontal Range",
        )

        self.real_acquisition_time = Parameter(
            name="real_acquisition_time",
            instrument=self,
            get_cmd="timebase:ratime?",
            get_parser=float,
            label="Real Acquisition Time",
        )

        self.roll_automatic = Parameter(
            name="roll_automatic",
            instrument=self,
            get_cmd="timebase:roll:automatic?",
            set_cmd="timebase:roll:automatic {}",
            val_mapping=create_on_off_val_mapping(on_val=1, off_val=0),
            label="Automatic Roll Mode",
        )

        self.roll_minimum_time = Parameter(
            name="roll_minimum_time",
            instrument=self,
            get_cmd="timebase:roll:mtime?",
            set_cmd="timebase:roll:mtime {}",
            vals=vals.Numbers(min_value=50e-3, max_value=500),
            get_parser=float,
            label="Minimum Roll Time",
        )

    def header(self):
        """Read the timebase header

        The header includes the start time, the stop time, the record length
        and the number of values per interval.

        Returns:
            dict
        """
        header = self.ask("channel:data:header?").split(",")
        start, stop, record_length, values_per_interval = header
        return dict(
            start=float(start),
            stop=float(stop),
            record_length=int(record_length),
            values_per_interval=int(values_per_interval)
        )

    def data(self):
        """Return the timebase data as an array

        Returns:
            numpy.ndarray, dtype = float
        """
        header = self.header()
        return np.linspace(header["start"], header["stop"], num=header["record_length"], endpoint=True)

class RohdeSchwarzRTB2000Acquire(InstrumentModule):
    def __init__(self, parent: "RohdeSchwarzRTB2000", name: str, **kwargs):
        super().__init__(parent, name, **kwargs)

        self.state = Parameter(
            name="state",
            instrument=self,
            get_cmd="acquire:state?",
            set_cmd="acquire:state {}",
            vals=vals.Enum("run", "stop", "break"),
            label="Acquisition State",
        )

        self.type = Parameter(
            name="type",
            instrument=self,
            get_cmd="acquire:type?",
            set_cmd="acquire:type {}",
            vals=vals.Enum("refresh", "average", "envelope"),
            label="Acquisition Type",
        )

        self.interpolate = Parameter(
            name="interpolate",
            instrument=self,
            get_cmd="acquire:interpolate?",
            set_cmd="acquire:interpolate {}",
            vals=vals.Enum("sinx", "linear", "smhd"),
            label="Interpolation Mode",
        )

        self.automatic_points = Parameter(
            name="automatic_points",
            instrument=self,
            get_cmd="acquire:points:automatic?",
            set_cmd="acquire:points:automatic {}",
            val_mapping=create_on_off_val_mapping(on_val=1, off_val=0),
            label="Automatic Record Length",
        )

        self.points = Parameter(
            name="points",
            instrument=self,
            get_cmd="acquire:points?",
            set_cmd="acquire:points {}",
            vals=vals.Ints(min_value=10000, max_value=20000000),
            get_parser=int,
            label="Record Length",
        )

        self.adc_sample_rate = Parameter(
            name="adc_sample_rate",
            instrument=self,
            get_cmd="acquire:points:arate?",
            set_cmd=False,
            get_parser=float,
            label="ADC Sample Rate",
        )

        self.display_sample_rate = Parameter(
            name="display_sample_rate",
            instrument=self,
            get_cmd="acquire:srate?",
            set_cmd=False,
            get_parser=float,
            label="Display Sample Rate",
        )

        self.peak_detect = Parameter(
            name="peak_detect",
            instrument=self,
            get_cmd="acquire:peakdetect?",
            set_cmd="acquire:peakdetect {}",
            val_mapping=create_on_off_val_mapping(on_val="AUTO", off_val="OFF"),
            label="Peak Detection Mode",
        )

        self.high_resolution = Parameter(
            name="high_resolution",
            instrument=self,
            get_cmd="acquire:hresolution?",
            set_cmd="acquire:hresolution {}",
            val_mapping=create_on_off_val_mapping(on_val="AUTO", off_val="OFF"),
            label="High Resolution Mode",
        )

        self.nsingle_count = Parameter(
            name="nsingle_count",
            instrument=self,
            get_cmd="acquire:nsingle:count?",
            set_cmd="acquire:nsingle:count {}",
            vals=vals.Ints(min_value=1, max_value=8),
            get_parser=int,
            label="Number of Single Waveforms",
        )

        self.average_count = Parameter(
            name="average_count",
            instrument=self,
            get_cmd="acquire:average:count?",
            set_cmd="acquire:average:count {}",
            vals=vals.Ints(min_value=2, max_value=100000),
            get_parser=int,
            label="Average Count",
        )

        self.average_reset = Function(
            name="average_reset",
            instrument=self,
            call_cmd="acquire:average:reset"
        )

        self.average_complete = Parameter(
            name="average_complete",
            instrument=self,
            get_cmd="acquire:average:complete?",
            set_cmd=False,
            get_parser=lambda x: bool(int(x)),
            label="Average Completed",
        )

class RohdeSchwarzRTB2000Channel(InstrumentChannel):
    def __init__(self, parent: "RohdeSchwarzRTB2000", name: str, channel: int, **kwargs):
        super().__init__(parent, name, **kwargs)
        self.channel = channel

        self.state = Parameter(
            name="state",
            instrument=self,
            get_cmd=f"channel{self.channel}:state?",
            set_cmd=f"channel{self.channel}:state {{}}",
            val_mapping=create_on_off_val_mapping(on_val=1, off_val=0),
            label="Channel State",
        )

        self.scale = Parameter(
            name="scale",
            instrument=self,
            get_cmd=f"channel{self.channel}:scale?",
            set_cmd=f"channel{self.channel}:scale {{}}",
            vals=vals.Numbers(min_value=1e-3, max_value=5),
            get_parser=float,
            label="Vertical Scale",
        )

        self.range = Parameter(
            name="range",
            instrument=self,
            get_cmd=f"channel{self.channel}:range?",
            set_cmd=f"channel{self.channel}:range {{}}",
            vals=vals.Numbers(min_value=1e-2, max_value=50),
            get_parser=float,
            label="Vertical Range",
        )

        self.position = Parameter(
            name="position",
            instrument=self,
            get_cmd=f"channel{self.channel}:position?",
            set_cmd=f"channel{self.channel}:position {{}}",
            vals=vals.Numbers(min_value=-5, max_value=5),
            get_parser=float,
            label="Vertical Position",
        )

        self.offset = Parameter(
            name="offset",
            instrument=self,
            get_cmd=f"channel{self.channel}:offset?",
            set_cmd=f"channel{self.channel}:offset {{}}",
            vals=vals.Numbers(min_value=-40, max_value=40),
            get_parser=float,
            label="Vertical Offset",
        )

        self.coupling = Parameter(
            name="coupling",
            instrument=self,
            get_cmd=f"channel{self.channel}:coupling?",
            set_cmd=f"channel{self.channel}:coupling {{}}",
            vals=vals.Enum("dclimit", "aclimit", "gnd"),
            label="Channel Coupling",
        )

        self.bandwidth = Parameter(
            name="bandwidth",
            instrument=self,
            get_cmd=f"channel{self.channel}:bandwidth?",
            set_cmd=f"channel{self.channel}:bandwidth {{}}",
            vals=vals.Enum("full", "b20"),
            label="Channel Bandwidth",
        )

        self.polarity = Parameter(
            name="polarity",
            instrument=self,
            get_cmd=f"channel{self.channel}:polarity?",
            set_cmd=f"channel{self.channel}:polarity {{}}",
            vals=vals.Enum("normal", "inverted"),
            label="Channel Polarity",
        )

        self.skew = Parameter(
            name="skew",
            instrument=self,
            get_cmd=f"channel{self.channel}:skew?",
            set_cmd=f"channel{self.channel}:skew {{}}",
            vals=vals.Numbers(min_value=-500e-9, max_value=500e-9),
            get_parser=float,
            label="Channel Skew",
        )

        self.zero_offset = Parameter(
            name="zero_offset",
            instrument=self,
            get_cmd=f"channel{self.channel}:zoffset?",
            set_cmd=f"channel{self.channel}:zoffset {{}}",
            vals=vals.Numbers(min_value=-101e-3, max_value=101e-3),
            get_parser=float,
            label="Channel Zero Offset",
        )

        self.color_scale = Parameter(
            name="color_scale",
            instrument=self,
            get_cmd=f"channel{self.channel}:wcolor?",
            set_cmd=f"channel{self.channel}:wcolor {{}}",
            vals=vals.Enum("temperature", "rainbow", "fire", "default"),
            label="Channel Color Scale",
        )

        self.threshold = Parameter(
            name="threshold",
            instrument=self,
            get_cmd=f"channel{self.channel}:threshold?",
            set_cmd=f"channel{self.channel}:threshold {{}}",
            vals=vals.Numbers(min_value=-100, max_value=100),
            get_parser=float,
            label="Channel Digitization Threshold",
        )

        self.find_threshold = Function(
            name="find_threshold",
            instrument=self,
            call_cmd=f"channel{self.channel}:threshold:findlevel",
        )

        self.threshold_hysteresis = Parameter(
            name="threshold_hysteresis",
            instrument=self,
            get_cmd=f"channel{self.channel}:threshold:hysteresis?",
            set_cmd=f"channel{self.channel}:threshold:hysteresis {{}}",
            vals=vals.Enum("small", "medium", "large"),
            label="Channel Digitization Threshold Hysteresis",
        )

        self.label = Parameter(
            name="label",
            instrument=self,
            get_cmd=f"channel{self.channel}:label?",
            set_cmd=f"channel{self.channel}:label '{{}}'",
            vals=vals.Strings(max_length=8),
            get_parser=lambda x: x.strip('"'),
            label="Channel Label",
        )

        self.label_state = Parameter(
            name="label_state",
            instrument=self,
            get_cmd=f"channel{self.channel}:label:state?",
            set_cmd=f"channel{self.channel}:label:state {{}}",
            val_mapping=create_on_off_val_mapping(on_val=1, off_val=0),
            label="Channel Label State",
        )

        self.y_origin = Parameter(
            name="y_origin",
            instrument=self,
            get_cmd=f"channel{self.channel}:data:yorigin?",
            set_cmd=False,
            get_parser=float,
            label="Voltage Value for the Integer 0",
        )

        self.y_increment = Parameter(
            name="y_increment",
            instrument=self,
            get_cmd=f"channel{self.channel}:data:yincrement?",
            set_cmd=False,
            get_parser=float,
            label="Voltage Value per Integer bit",
        )

        self.y_resolution = Parameter(
            name="y_resolution",
            instrument=self,
            get_cmd=f"channel{self.channel}:data:yresolution?",
            set_cmd=False,
            get_parser=float,
            label="Vertical Bit Resolution",
        )

    def data(self, raw: bool = False):
        """Read the channel data based on the data format

        If the data format is ASCII, the raw data will be a string with the
        values separated by a comma. If the data format is INT, the raw data
        will be an array of dtype int without the scale and origin of the
        y-axis.

        Args:
            raw (bool): Return the raw data if applicable
        """
        data_format = self.parent.data_format()
        if data_format == "ASC,0":
            data = self.ask(f"channel{self.channel}:data?")
            return data if raw else np.array([float(v) for v in data.split(",")])

        datatype = DATATYPES[data_format]
        is_big_endian = (self.parent.byte_order() == "MSBF")
        self.write(f"channel{self.channel}:data?")
        data = np.array(self.parent.visa_handle.read_binary_values(datatype, is_big_endian=is_big_endian))
        if raw or datatype == "REAL,32":
            return data
        return self.y_origin() + (self.y_increment() * data)

class RohdeSchwarzRTB2000(VisaInstrument):
    """
    QCoDeS driver for the Rohde&Schwarz RTB2000 family
    """

    def __init__(self, name: str, address: str, **kwargs):
        super().__init__(name=name, address=address, terminator="\n", **kwargs)

        self.add_submodule("trigger", RohdeSchwarzRTB2000Trigger(self, "trigger"))
        self.add_submodule("cursor", RohdeSchwarzRTB2000Cursor(self, "cursor"))

        measurements = []
        for i in range(1, 7):
            measurement = RohdeSchwarzRTB2000Measurement(self, f"measurement{i}", i)
            self.add_submodule(f"measurement{i}", measurement)
            measurements.append(measurement)
        measurement_list = ChannelList(self, "measurement", RohdeSchwarzRTB2000Measurement, measurements)
        self.add_submodule("measurements", measurement_list)

        self.add_submodule("timebase", RohdeSchwarzRTB2000Timebase(self, "timebase"))
        self.add_submodule("acquire", RohdeSchwarzRTB2000Acquire(self, "acquire"))

        channels = []
        for i in range(1, 5):
            channel = RohdeSchwarzRTB2000Channel(self, f"channel{i}", i)
            self.add_submodule(f"channel{i}", channel)
            channels.append(channel)
        channel_list = ChannelList(self, "channels", RohdeSchwarzRTB2000Channel, channels)
        self.add_submodule("channels", channel_list)

        self.run = Function("run", instrument=self, call_cmd="run")
        self.single = Function("single", instrument=self, call_cmd="single")
        self.stop = Function("stop", instrument=self, call_cmd="stop")

        self.data_format = Parameter(
            name="data_format",
            instrument=self,
            get_cmd="format:data?",
            set_cmd="format:data {}",
            vals=vals.Enum("ascii", "real", "uint,8", "uint,16", "uint,32"),
            label="Data Format",
        )

        self.byte_order = Parameter(
            name="byte_order",
            instrument=self,
            get_cmd="format:border?",
            set_cmd="format:border {}",
            vals=vals.Enum("msbfirst", "lsbfirst"),
            label="Byte Order",
        )
