"""
Endpoint Processing: Trick Play
"""
# Built-in

# Special
from flask import jsonify, make_response
from flask_restful import Resource, reqparse

# App
from lib.trick_play import TrickPlay
from api.event import post_event


class TrickPlayEndpoint(Resource):
    """
    Manage Trick Play Requests
    
    Methods
    ----------
    post -> Create trick play assets for an HLS master.m3u8 file.

    """

    def post(self):
        """
        Create trick play assets for an HLS master.m3u8 file

        Parameters
        ----------
        master
            url or local path of the master.m3u8 file.
            ex. http://server.cc/path/master.m3u8

        Returns
        -------
        json :
            {
                "data": "string that references the trick play index.",
                "message": "Instructions or a successful message.",
                "success": false
            }
        """

        func = f"{__name__}.{__class__.__name__}.post"
        post_event(
            "log_debug",
            f"{func}",
            f"Managing request to create trick play assets for manifest.",
        )

        # Do the work
        parser = reqparse.RequestParser()
        parser.add_argument(
            "master", type=str, help="HLS master.m3u8 manifest location.", required=True
        )
        args = parser.parse_args()

        post_event("log_debug", f"{func}", f"Parsed args:{args}")

        trickplay = TrickPlay(master=args.master)
        trick_play_result = trickplay.generate_trickplay_assets()

        response = make_response(
            jsonify(trick_play_result.__dict__),
            200,
        )
        response.headers["Content-Type"] = "application/json"

        post_event(
            "log_debug", f"{func}", f"Returning results to create trick play assets."
        )

        return response
