"""
Configuration Settings.
"""
# Built-in
from os import environ
from os.path import join, expanduser, exists
import socket

# App
from api.event import post_event


class App:
    """
    App configs
    """

    hostname = None
    appname = "trick play service"

    # teams related variables
    video_alert_url = None

    # folders
    capture_folder_name = None
    destination_folder_name = None

    def __init__(self):

        self.hostname = socket.gethostname()

        self.video_alert_url = environ["VIDEO_ALERT_URL"]

        self.capture_folder_name = environ["CAPTURE_FOLDER_NAME"]
        self.destination_folder_name = environ["DESTINATION_FOLDER_NAME"]


class Logs(object):
    """
    Logging configs
    """

    loglevel = 10

    log_folder = None
    log_filename = None
    log_file_path = None

    def __init__(self):
        app = App()
        func = f"{__name__}"

        # NOTSET=0, DEBUG=10, INFO=20, WARN=30, ERROR=40, and CRITICAL=50
        self.loglevel = int(environ["LOGLEVEL"] if environ["LOGLEVEL"] != None else 10)

        self.log_filename = f"{app.appname}.log"
        self.log_folder = f"{expanduser('~')}/Library/Logs/"

        # Verify log file exists
        self.log_file_path = join(self.log_folder, self.log_filename)

        if exists(self.log_file_path):
            # do something
            print("log exists")

        else:
            # create one
            with open(self.log_file_path, "w") as fp:
                post_event(
                    "log_debug", f"{func}", f"Created the log file:{self.log_filename}."
                )
                pass
