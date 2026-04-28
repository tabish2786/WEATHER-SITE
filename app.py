from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)
API = os.getenv("0994648b3e1187d9108c93795cf9bb07") or "0994648b3e1187d9108c93795cf9bb07"
@app.route("/")

def home():
    return render_template("index.html")
@app.route("/weather", methods=["POST"])

def get_weather():
    data = request.get_json()
    city = data.get("city")
    if not city:
        return jsonify({"ok": False, "error": "Enter a city name"})
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric"
        response = requests.get(url, timeout=5)
        data = response.json()
        if response.ok:
            weather = {
                "city": city.title(),
                "temperature": round(data["main"]["temp"]),
                "description": data["weather"][0]["description"].title(),
                "humidity": data["main"]["humidity"],
                "wind": round(data["wind"]["speed"] * 3.6, 1),  # m/s → km/h
                "feels": round(data["main"]["feels_like"]),
                "icon": data["weather"][0]["icon"]
            }
            return jsonify({"ok": True, "weather": weather})
        else:
            return jsonify({
                "ok": False,
                "error": data.get("message", "City not found")
            })
    except requests.exceptions.RequestException:
        return jsonify({
            "ok": False,
            "error": "Network error, try again"
        })
        
if __name__ == "__main__":
    app.run(debug=True)
