from flask import Flask
from flask import Flask, jsonify
from config import config
import json
import mariadb

app = Flask(__name__)
conn = mariadb.connect(**config)
cur = conn.cursor()

from app.views import hello, auth, dashboard
from app.models import models
