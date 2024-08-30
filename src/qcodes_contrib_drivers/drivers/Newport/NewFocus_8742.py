import time
import logging
from typing import List, Optional, Dict

from qcodes import validators as vals
from qcodes.instrument import VisaInstrument
from qcodes.instrument.channel import ChannelList, InstrumentChannel
from qcodes.instrument.parameter import Parameter

log = logging.getLogger(__name__)


class NewportNewFocus8742Exception(Exception):
    pass


class NewportNewFocus8742ErrorCode(NewportNewFocus8742Exception):
    def __init__(self, cmd: str, err: int, msg: str) -> None:
        self.failed_command = cmd
        self.error_code = err
        self.error_message = msg
        super().__init__(f"Command {cmd} failed with error code {err} ({msg})")


class NewportNewFocus8742Axis(InstrumentChannel):
    """Represents one of the axes of a NewFocus 8742 controller."""

    def __init__(self, parent: "NewportNewFocus8742", axis: int) -> None:
        assert axis in (1, 2, 3, 4)
        super().__init__(parent, f"axis_{axis}")
        self.axis = axis

        self.motor_type = Parameter(
            name="motor_type",
            instrument=self,
            set_cmd=f"{self.axis}QM{{}}",
            get_cmd=f"{self.axis}QM?",
            get_parser=int,
            vals=vals.Ints(min_value=0, max_value=3),
        )

        self.acceleration = Parameter(
            name="acceleration",
            instrument=self,
            set_cmd=f"{self.axis}AC{{}}",
            get_cmd=f"{self.axis}AC?",
            get_parser=int,
            vals=vals.Ints(min_value=1, max_value=200000),
        )

        self.velocity = Parameter(
            name="velocity",
            instrument=self,
            set_cmd=f"{self.axis}VA{{}}",
            get_cmd=f"{self.axis}VA?",
            get_parser=int,
            vals=vals.Ints(min_value=1, max_value=2000),
        )

        self.home_position = Parameter(
            name="home_position",
            instrument=self,
            set_cmd=f"{self.axis}DH{{}}",
            get_cmd=f"{self.axis}DH?",
            get_parser=int,
            vals=vals.Ints(min_value=-int(2**31), max_value=int(2**31) - 1),
        )

        self.actual_position = Parameter(
            name="actual_position",
            instrument=self,
            set_cmd=False,
            get_cmd=f"{self.axis}TP?",
            get_parser=int,
        )

        self.move_absolute = Parameter(
            name="move_absolute",
            instrument=self,
            set_cmd=f"{self.axis}PA{{}}",
            get_cmd=f"{self.axis}PA?",
            get_parser=int,
            vals=vals.Ints(min_value=-int(2**31), max_value=int(2**31) - 1),
        )

        self.move_relative = Parameter(
            name="move_relative",
            instrument=self,
            set_cmd=f"{self.axis}PR{{}}",
            get_cmd=f"{self.axis}PR?",
            get_parser=int,
            vals=vals.Ints(min_value=-int(2**31), max_value=int(2**31) - 1),
        )

    def move(self, direction: str) -> None:
        """Indefinite move command."""
        assert direction in ["+", "-"]
        self.write(f"{self.axis}MV{direction}")

    def stop(self) -> None:
        """Stop motion command."""
        self.write(f"{self.axis}ST")


class NewportNewFocus8742(VisaInstrument):
    """
    QCoDeS driver for the Newport NewFocus 8742 Picomotor Motion Controller.
    Args:
        name (str): name of the instrument.
        address (str): VISA string describing the TCP connection,
            for example "TCPIP::192.168.0.74::23::SOCKET".
    """

    # After a command which does not generate a response, a short
    # delay is needed before we can send the following command.
    command_delay = 0.002

    def __init__(self, name: str, address: str, timeout: float = 1.0) -> None:
        super().__init__(name, address, timeout=timeout, terminator="\r\n")

        self.log.debug(f"Opening NewportNewFocus8742 at {address}")
        axes = [NewportNewFocus8742Axis(self, axis + 1) for axis in range(4)]
        axis_list = ChannelList(self, "axes", NewportNewFocus8742Axis, axes)
        self.add_submodule("axes", axis_list)

        self.add_function("reset", call_cmd="RS", args=())

    def get_last_error(self) -> List[str]:
        """Send a TB command (get error of previous command) and return
        a numerical error code and the error message.
        Returns:
            int: Error code for previous command.
            str: Error message for previous command.
        This function is called automatically after each command sent
        to the device. When a command results in error, exception
        NewportNewFocus8742ErrorCode is raised.
        """
        err, msg = self.ask("TB?").split(",")
        return int(err), msg

    def get_idn(self) -> Dict[str, Optional[str]]:
        resp = self.ask("VE")
        words = resp.strip().split()
        if len(words) == 4:
            model = words[0]
            version = words[2]
            info = words[3]
        else:
            msg = f"Unexpected response to VE command: {resp!r}"
            self.log.warning(msg)
            raise NewportNewFocus8742Exception(msg)
        return {"vendor": "Newport", "model": model, "firmware": version, "info": info}

    def write(self, cmd: str) -> None:
        super().write(cmd)
        time.sleep(self.command_delay)
        err, msg = self.get_last_error()
        if err != 0:
            self.log.warning(f"Command {cmd} failed with error {err} ({msg})")
            raise NewportNewFocus8742ErrorCode(cmd, err, msg)
