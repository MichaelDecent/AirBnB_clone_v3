#!/usr/bin/python3
""" this Module handles all route endpoints """
from api.v1.views import app_views
from flask import jsonify

@app_views.route('/status')
def status():
    """returns the status of a request"""
    return jsonify({"status": "OK"})