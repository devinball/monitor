from flask import Flask, request
from interface import ServiceInterface

app = Flask(__name__)

service_interface = ServiceInterface()

with open("./authorized_tokens.txt") as f:
    tokens = f.readlines()

def validate_request() -> bool:
    return request.headers.get("auth") in tokens

@app.route("/")
def root() -> str:    
    return ""

@app.route("/info")
def info() -> str:
    if not validate_request():
        return "", 401
    
    return service_interface.get_info()

@app.route("/pause-play")
def pause_play() -> str:
    if not validate_request():
        return "", 401
    
    service_interface.pause_play()
    return ""

@app.route("/previous")
def previous() -> str:
    if not validate_request():
        return "", 401
    
    service_interface.previous()
    return ""

@app.route("/next")
def next() -> str:
    if not validate_request():
        return "", 401
    
    service_interface.next()
    return ""
