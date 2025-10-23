from flask import Flask
from app.models import Driver
app = Flask(__name__)


app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def home():
    return "<h1>Hello World</h1>"


@app.route('/<string:name>', methods=['GET'])
def greet(name: str):
    return f"<h1>Hello {name}</h1>"


@app.route('/api/<path:path>', methods=['GET','POST','PUT','DELETE'])
def api_route(path):
    return f"<h1>API endpoint: {path}</h1>"


app.run()