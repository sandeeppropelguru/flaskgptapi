from flask import Flask,jsonify
from flask_cors import CORS,cross_origin
import logging

app = Flask(__name__)


@app.route("/api/v1/users")
@cross_origin()
def helloWorld():
    
  return jsonify("Hello, cross-origin-world!")
         


app.run(debug=True)