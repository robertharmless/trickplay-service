"""
System Information
"""
from datetime import datetime
import socket


class SystemInfo:
    """
    System Info Response Model
    """

    serverName = None
    serverTime = None
    success = False

    def __init__(self, serverName=socket.gethostname(), serverTime=datetime.now()):
        self.serverName = serverName
        self.serverTime = serverTime
