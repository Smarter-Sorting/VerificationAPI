from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route("/")
def status():
    data = {
        'message': 'Hello World!'
    }
    return jsonify(data), 200


@app.route("/verification", methods=['POST'])
def verify():
    if request.is_json:
        data = request.json
        # parse data
        # send to database
        return jsonify({"message": "data received"}), 200
    else:
        return jsonify({"error": "Request body is invalid"}), 400
