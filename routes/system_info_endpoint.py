"""
Endpoint Processing: System Info
"""
# Built-in

# Special
from flask import jsonify, make_response
from flask_restful import Resource

# App
from lib.system import SystemInfoResponse
from api.event import post_event


class SystemInfoEndpoint(Resource):
    """
    Manage System Information Requests

    Methods
    ----------
    get -> Get the current system information.

    """

    def get(self):
        """
        Get the current system information

        Parameters
        ----------
        none

        Returns
        -------
        json :
            {
                "serverName": "host name",
                "serverTime": "current time on server GMT",
                "success": true
            }
        """

        func = f"{__name__}.{__class__.__name__}.get"
        post_event(
            "log_debug", f"{func}", f"Managing request to retrieve System Information."
        )

        # Do the work
        info = SystemInfoResponse()
        info.success = True

        response = make_response(
            jsonify(info.__dict__),
            200,
        )
        response.headers["Content-Type"] = "application/json"

        post_event("log_debug", f"{func}", f"Returning requested System Information.")

        return response
