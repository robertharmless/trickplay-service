"""
Simple app to create Trick Play - Mode from/for HLS m3u8.
"""
# Built-in


# Special
from flask import Flask

# App
from api.event import post_event
from api.log_listener import setup_log_event_handlers

setup_log_event_handlers()

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

#TODO: Add catching errors
#TODO: Convert to restful focus
#TODO: Proper validation could be helpful. Parsing paramters?

#TODO: Point to trick play-mode

#TODO: Able to work with multiple storage methods. Though ffmpeg may require being local.

#TODO: Mesasure progress for insights?
#TODO: Add Postman Collection
#TODO: Add Open API documentation

