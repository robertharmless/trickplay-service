"""
Simple app to create Trick Play - Mode from/for HLS m3u8.
"""
# Built-in

# Special
from flask import Flask, jsonify, make_response
from flask_restful import Api

# App
from api.event import post_event
from api.log_listener import setup_log_event_handlers

from routes.system_info_endpoint import SystemInfoEndpoint
from routes.trick_play_endpoint import TrickPlayEndpoint

setup_log_event_handlers()

app = Flask(__name__)
api = Api(app)


## API Routes
api.add_resource(SystemInfoEndpoint, "/api/systemInfo")
api.add_resource(TrickPlayEndpoint, "/api/trickPlay/hls")


## Error handling
@app.errorhandler(404)
def resource_not_found(e):

    func = f"{__name__}.resource_not_found"
    post_event(
        "log_exception",
        f"{func}",
        f"{e}",
    )
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
