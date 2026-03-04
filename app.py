from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API = "f3d10ee88570b97b54cd0f71d2e0568a"

@app.route("/", methods=["GET", "POST"])
def home():
    weather = None
    error = None

    if request.method == "POST":
        city = request.form["city"]
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric"

        response = requests.get(url)
        data = response.json()

        if response.status_code == 200:
            weather = {
                "city": city,
                "temperature": data["main"]["temp"],
                "description": data["weather"][0]["description"]
            }
        else:
            error = data.get("message", "Something went wrong")

    return render_template("index.html", weather=weather, error=error)

if __name__ == "__main__":
    app.run(debug=True)