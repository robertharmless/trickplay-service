"""
FFMPEG fundtions
"""
# Built-in
from os import environ
import subprocess
from dataclasses import dataclass, field
from typing import List
import pathlib

# Special

# App
from api.event import post_event


@dataclass
class RunResult:
    """
    Result for when running an ffmpeg command.
    """

    data: str = None
    errors: List[str] = field(default_factory=list)
    success: bool = False


class FFMPEG:
    ffmpeg_binary = "/usr/local/ffmpeg"
    version = "0"

    def __init__(self) -> None:
        self.name = pathlib.Path(__file__).name.replace(".py", "")

        func = f"{__package__}.{self.name}.{__class__.__name__}.__init__"

        FFMPEG_PATH_key = "FFMPEG_PATH"
        if FFMPEG_PATH_key in environ:
            post_event(
                "log_debug", f"{func}", f"Using the {FFMPEG_PATH_key} from environment."
            )
            self.ffmpeg_binary = environ[FFMPEG_PATH_key]
        else:
            post_event("log_debug", f"{func}", f"Using the default {FFMPEG_PATH_key}.")

        self.verify_ffmpeg_path()

    def verify_ffmpeg_path(self) -> bool:
        """
        Find if ffmpeg exists.
        """
        success = False
        func = f"{__package__}.{self.name}.{__class__.__name__}.verify_ffmpeg_path"

        arguments = ["-version"]
        post_event("log_debug", f"{func}", f"Checking ffmpeg exists.")

        exists = self.run(arguments)

        if exists.success is True:
            post_event(
                "log_debug",
                f"{func}",
                f"It appears that ffmpeg exists at {self.ffmpeg_binary}.",
            )
            success = True

        return success

    def run(self, arguments: list):
        """
        Run an ffmpeg command
        """
        result = RunResult()

        func = f"{__package__}.{self.name}.{__class__.__name__}.run"

        cmd = arguments
        cmd.insert(0, self.ffmpeg_binary)
        post_event("log_debug", f"{func}", f"runing the command:{cmd}")

        try:
            result.data = subprocess.run(cmd)
            post_event("log_debug", f"{func}", f"results -> {result.data}")

            if result.data.returncode == 0:
                post_event("log_info", f"{func}", f"ffmpeg command successful.")
                result.success = True

        except OSError as oer:
            result.errors.append(oer)

        except ValueError as ver:
            result.errors.append(ver)

        if result.success is not True:
            post_event("log_error", f"{func}", f"ffmpeg command failed.")
            post_event("log_error", f"{func}", f"{result.errors}")

        return result


if __name__ == "__main__":
    from api.log_listener import setup_log_event_handlers

    setup_log_event_handlers()

    ffmpeg = FFMPEG()
