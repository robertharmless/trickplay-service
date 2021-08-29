"""
Simple app to create Trick Play - Mode from/for HLS m3u8.
"""
# Built-in

# Special
from flask import Flask, jsonify, make_response
from flask_restful import reqparse, abort, Api, Resource

# App
from api.event import post_event
from api.log_listener import setup_log_event_handlers
from lib.system import SystemInfoResponse
from lib.trick_play import TrickPlay

setup_log_event_handlers()

app = Flask(__name__)
api = Api(app)


class SystemInfoEndpoint(Resource):
    """
    Manage System Information Requests
    """

    def get(self):

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


class TrickPlayEndpoint(Resource):
    """
    Manage Trick Play Requests
    """

    def post(self):

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


## API Routes
api.add_resource(SystemInfoEndpoint, "/api/systemInfo")
api.add_resource(TrickPlayEndpoint, "/api/trickPlay/hls")


## Error handling
@app.errorhandler(404)
def resource_not_found(e):

    message = {"success": False, "message": f"{e}"}
    response = make_response(
        jsonify(message),
        404,
    )
    response.headers["Content-Type"] = "application/json"

    return response


## Setting up the app
if __name__ == "__main__":
    app.run()
