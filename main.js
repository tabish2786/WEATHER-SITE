const form = document.getElementById("searchForm");
const input = document.getElementById("cityInput");
const result = document.getElementById("result");
const error = document.getElementById("error");
const empty = document.getElementById("empty");

// 🔍 SEARCH EVENT
form.addEventListener("submit", async (e) => {
    e.preventDefault();   // 🚨 page reload rokta hai

    const city = input.value.trim();

    if (!city) {
        showError("Enter a city name");
        return;
    }

    // UI reset
    error.innerText = "";
    empty.style.display = "none";
    result.innerHTML = "Loading... ⏳";

    try {
        const res = await fetch("/weather", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ city })
        });

        const data = await res.json();

        if (data.ok) {
            showWeather(data.weather);
        } else {
            showError(data.error);
        }

    } catch (err) {
        showError("Network error");
    }
});


// 🌦 SHOW WEATHER
function showWeather(w) {
    result.innerHTML = `
    <h2>${w.city}</h2>

    <!-- WEATHER ICON -->
    <img src="https://openweathermap.org/img/wn/${w.icon}@2x.png" class="icon">

    <h1>${w.temperature}°C</h1>

    <p>${w.description}</p>

    <div class="extra">

        <div>
            <p>Humidity</p>
            <strong>💧${w.humidity}%</strong>
        </div>

        <div>
            <p>Wind</p>
            <strong>🌬${w.wind} km/h</strong>
        </div>

        <div>
            <p>Feels Like</p>
            <strong>🌡${w.feels}°C</strong>
        </div>

    </div>
`;
}
// ❌ SHOW ERROR
function showError(msg) {
    result.innerHTML = "";
    error.innerText = msg;
}


// 🎯 AUTO FOCUS
input.focus();