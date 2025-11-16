"""
Web app entrypoint.
"""

from flask import Flask

app = Flask(__name__)


@app.route("/")
def index():
    """Return homepage."""
    return "Hello from web-app"
