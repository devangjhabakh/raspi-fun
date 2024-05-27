from flask import Flask, json, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)