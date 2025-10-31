from flask import Flask, jsonify, render_template
from flask_cors import CORS
import random, time, threading

app = Flask(__name__)
CORS(app)

traffic_data = {
    "density": 0,
    "light": "green",
    "ambulance": False,
    "game_on": False
}

def update_traffic():
    while True:
        traffic_data["density"] = random.randint(1, 100)
        traffic_data["ambulance"] = random.random() < 0.3

        if traffic_data["ambulance"]:
            traffic_data["game_on"] = False
        else:
            if traffic_data["density"] >= 70:
                traffic_data["light"] = "red"
            elif traffic_data["density"] >= 40:
                traffic_data["light"] = "yellow"
            else:
                traffic_data["light"] = "green"
            traffic_data["game_on"] = traffic_data["light"] == "red"
        time.sleep(10)

threading.Thread(target=update_traffic, daemon=True).start()

@app.route("/status")
def status():
    return jsonify(traffic_data)

# 🔹 NEW: Serve different user views
@app.route("/student")
def student_game():
    return render_template("student_game.html")

@app.route("/teacher")
def teacher_game():
    return render_template("teacher_game.html")

if __name__ == "__main__":
    app.run(debug=True)

