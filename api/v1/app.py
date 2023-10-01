#!/usr/bin/python3
"""
This module runs my API
"""
from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv

host = getenv('HBNB_API_HOST', '0.0.0.0')
port = getenv('HBNB_API_PORT', '5000')

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_storage(self):
    """This closes the database session"""
    storage.close()


if __name__ == '__main__':
    app.run(host=host, port=port, threaded=True)
