import os
import sys
from datetime import datetime
from math import sin

vendor_path = os.path.join(os.path.dirname(__file__), "vendor")
if os.path.isdir(vendor_path):
    sys.path.insert(0, vendor_path)

from flask import Flask, jsonify, render_template, request


app = Flask(__name__)


def get_energy_prices():
    now = datetime.now()
    wave = sin(now.timestamp() / 45)
    slow_wave = sin(now.timestamp() / 90)

    return {
        "diesel": round(7.62 + wave * 0.08, 2),
        "industrial_power": round(0.82 + slow_wave * 0.03, 2),
        "shore_power": round(1.05 + wave * 0.04, 2),
        "updated_at": now.strftime("%Y-%m-%d %H:%M:%S"),
    }


def to_float(value, default):
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def calculate_results(form):
    prices = get_energy_prices()

    distance = to_float(form.get("distance"), 50)
    speed = max(to_float(form.get("speed"), 10), 0.1)
    power = to_float(form.get("power"), 200)
    battery_capacity = to_float(form.get("battery_capacity"), 1200)
    diesel_consumption = to_float(form.get("diesel_consumption"), 8)
    hybrid_diesel_ratio = min(max(to_float(form.get("hybrid_diesel_ratio"), 40), 0), 100)

    voyage_hours = distance / speed
    electric_energy = power * voyage_hours
    diesel_volume = distance * diesel_consumption

    diesel = {
        "name": "柴油方案",
        "energy": f"{diesel_volume:.1f} L",
        "cost": diesel_volume * prices["diesel"],
        "carbon": diesel_volume * 2.68,
        "score": 58,
    }

    electric = {
        "name": "纯电方案",
        "energy": f"{electric_energy:.1f} kWh",
        "cost": electric_energy * prices["industrial_power"],
        "carbon": electric_energy * 0.5703,
        "score": 88 if electric_energy <= battery_capacity else 72,
    }

    electric_ratio = 100 - hybrid_diesel_ratio
    hybrid_diesel_volume = diesel_volume * hybrid_diesel_ratio / 100
    hybrid_electric_energy = electric_energy * electric_ratio / 100
    hybrid = {
        "name": "混合动力方案",
        "energy": f"{hybrid_diesel_volume:.1f} L + {hybrid_electric_energy:.1f} kWh",
        "cost": (
            hybrid_diesel_volume * prices["diesel"]
            + hybrid_electric_energy * prices["shore_power"]
        ),
        "carbon": hybrid_diesel_volume * 2.68 + hybrid_electric_energy * 0.5703,
        "score": 76,
    }

    options = [diesel, electric, hybrid]
    best = min(options, key=lambda item: (item["carbon"], item["cost"]))
    baseline_cost = max(diesel["cost"], 1)
    baseline_carbon = max(diesel["carbon"], 1)

    return {
        "prices": prices,
        "inputs": {
            "ship_type": form.get("ship_type", "内河货船"),
            "distance": distance,
            "speed": speed,
            "power": power,
            "battery_capacity": battery_capacity,
            "diesel_consumption": diesel_consumption,
            "hybrid_diesel_ratio": hybrid_diesel_ratio,
            "voyage_hours": voyage_hours,
        },
        "options": options,
        "best": best,
        "cost_saving": max((baseline_cost - best["cost"]) / baseline_cost * 100, 0),
        "carbon_saving": max((baseline_carbon - best["carbon"]) / baseline_carbon * 100, 0),
    }


@app.route("/", methods=["GET", "POST"])
def index():
    form = request.form if request.method == "POST" else {}
    result = calculate_results(form)
    return render_template("index.html", result=result)


@app.route("/api/prices")
def prices():
    return jsonify(get_energy_prices())


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5055))
    app.run(host="0.0.0.0", port=port, debug=False)
