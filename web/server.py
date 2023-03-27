from flask import Flask, render_template
from web.log_config import configure_logger

configure_logger()

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("status.min.html")
