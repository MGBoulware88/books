from flask import Flask, render_template, request, redirect, session
from datetime import datetime
app = Flask(__name__)
secret_key = "CHANGEME"
DB = "books"