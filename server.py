from flask import *
import os

app = Flask(__name__)
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
shared_data = {}

def check_token():
    token = request.headers.get("Authorization")
    return token == f"Bearer {ACCESS_TOKEN}"

@app.route('/post', methods=['POST'])
def post():
    if not check_token():
        return jsonify({"error": "Forbidden"}), 403

    data = request.get_json()
    ip = data.get("ip")
    time = data.get("time")
    full_name = data.get("full_name")
    username = data.get("username")

    shared_data["ip"] = ip
    shared_data["time"] = time
    shared_data["full_name"] = full_name
    shared_data["username"] = username

    return jsonify({"status": "Data saved"})

@app.route("/get", methods=['GET'])
def get():
    if not check_token():
        return jsonify({"error": "Forbidden"}), 403

    if not shared_data:
        return jsonify({"error": "No data available"}), 404

    return jsonify(shared_data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

