from flask import *
import os, sqlite3
from database import init_db, insert_user

app = Flask(__name__)
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
shared_data = {}
init_db()
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

    insert_user(data["ip"], data["time"], data["full_name"], data["username"])
    return jsonify({"status": "Data saved"})

@app.route("/get", methods=['GET'])
def get():
    if not check_token():
        return jsonify({"error": "Forbidden"}), 403

    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    cursor.execute("SELECT ip, time, full_name, username FROM users ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()

    result = [
        {"ip": row[0], "time": row[1], "full_name": row[2], "username": row[3]}
        for row in rows
    ]
    if result:
        return jsonify(result)
    else:
        return jsonify({"Answer": "No text provided"})


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)



