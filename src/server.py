
"""PLIK SŁUŻĄCY DO URUCHOMIENIA LOKALNEGO SERWERA"""
from flask import Flask, jsonify, request

app = Flask(__name__)

global_data = {}


@app.route("/")
def homepage():
    return "<html><body>Homepage</body></html>"


@app.route("/api/getdata", methods=['GET'])
def getdata():
    global global_data
    return jsonify(global_data), 200


@app.route("/api/setdata", methods=['POST'])
def setdata():
    global global_data
    data = request.get_json()
    if data is not None and 'data' in data:
        global_data.setdefault(data['id'], data['data'])
    return {}, 201


@app.route("/api/updatedata",methods=['PUT'])
def updatedata():
    global global_data
    data = request.get_json()
    if data is not None and 'data' in data:
            global_data[data['id']] = data['data']
    return {}, 201


@app.route("/api/deletedata", methods=['DELETE'])
def deletedata():
    global global_data
    global_data.clear()
    return {}, 201


if __name__ == "__main__":
    app.run()
