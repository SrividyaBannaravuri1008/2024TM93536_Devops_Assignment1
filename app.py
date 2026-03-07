"""
ACEest Fitness & Gym - Flask Web Application
Version: 3.2.4 (Flask adaptation)
"""
from flask import Flask, jsonify, request

app = Flask(__name__)

# ---------- DATA ----------
PROGRAMS = {
    "Fat Loss (FL) - 3 day": {
        "factor": 22,
        "desc": "3-day full-body fat loss program",
        "workout": "Mon: Back Squat 5x5 + Core | Wed: Bench Press + 21-15-9 | Fri: Zone 2 Cardio 30min",
        "diet": "Breakfast: Egg Whites + Oats | Lunch: Grilled Chicken + Brown Rice | Dinner: Fish Curry + Millet Roti | Target: ~2000 kcal"
    },
    "Muscle Gain (MG) - PPL": {
        "factor": 35,
        "desc": "Push/Pull/Legs hypertrophy program",
        "workout": "Mon: Squat 5x5 | Tue: Bench 5x5 | Wed: Deadlift 4x6 | Thu: Front Squat 4x8 | Fri: Incline Press | Sat: Barbell Rows",
        "diet": "Breakfast: 4 Eggs + PB Oats | Lunch: Chicken Biryani | Dinner: Mutton Curry + Jeera Rice | Target: ~3200 kcal"
    },
    "Beginner (BG)": {
        "factor": 26,
        "desc": "3-day simple beginner full-body program",
        "workout": "Circuit: Air Squats, Ring Rows, Push-ups | Focus: Technique & Form",
        "diet": "Balanced Tamil Meals: Idli-Sambar, Rice-Dal, Chapati | Protein: 120g/day"
    }
}

# In-memory client store (used for unit testing; production would use a DB)
clients_db = {}


# ---------- ROUTES ----------
@app.route("/")
def index():
    return jsonify({
        "app": "ACEest Fitness & Gym",
        "version": "3.2.4",
        "status": "running"
    })


@app.route("/health")
def health():
    return jsonify({"status": "healthy"}), 200


@app.route("/programs", methods=["GET"])
def get_programs():
    """Return all available fitness programs."""
    return jsonify({"programs": list(PROGRAMS.keys())}), 200


@app.route("/programs/<program_name>", methods=["GET"])
def get_program(program_name):
    """Return details for a specific program."""
    program = PROGRAMS.get(program_name)
    if not program:
        return jsonify({"error": "Program not found"}), 404
    return jsonify({"program": program_name, "details": program}), 200


@app.route("/calories", methods=["POST"])
def calculate_calories():
    """Calculate estimated daily calories based on weight and program."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body required"}), 400

    weight = data.get("weight")
    program_name = data.get("program")

    if weight is None or program_name is None:
        return jsonify({"error": "Both 'weight' and 'program' are required"}), 400

    if not isinstance(weight, (int, float)) or weight <= 0:
        return jsonify({"error": "Weight must be a positive number"}), 400

    program = PROGRAMS.get(program_name)
    if not program:
        return jsonify({"error": "Program not found"}), 404

    calories = int(weight * program["factor"])
    return jsonify({
        "weight_kg": weight,
        "program": program_name,
        "estimated_calories": calories
    }), 200


@app.route("/clients", methods=["GET"])
def get_clients():
    """Return all saved clients."""
    return jsonify({"clients": list(clients_db.values())}), 200


@app.route("/clients", methods=["POST"])
def save_client():
    """Save or update a client record."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body required"}), 400

    name = data.get("name", "").strip()
    program_name = data.get("program", "")

    if not name:
        return jsonify({"error": "Client name is required"}), 400
    if not program_name:
        return jsonify({"error": "Program is required"}), 400
    if program_name not in PROGRAMS:
        return jsonify({"error": "Invalid program"}), 400

    weight = data.get("weight", 0)
    factor = PROGRAMS[program_name]["factor"]
    calories = int(weight * factor) if weight > 0 else None

    client = {
        "name": name,
        "age": data.get("age"),
        "weight": weight,
        "program": program_name,
        "calories": calories
    }
    clients_db[name] = client

    return jsonify({"message": "Client saved", "client": client}), 201


@app.route("/clients/<name>", methods=["GET"])
def get_client(name):
    """Return a specific client by name."""
    client = clients_db.get(name)
    if not client:
        return jsonify({"error": "Client not found"}), 404
    return jsonify({"client": client}), 200


@app.route("/bmi", methods=["POST"])
def calculate_bmi():
    """Calculate BMI and return category."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body required"}), 400

    weight = data.get("weight")
    height = data.get("height")

    if weight is None or height is None:
        return jsonify({"error": "Both 'weight' (kg) and 'height' (cm) are required"}), 400

    if not isinstance(weight, (int, float)) or weight <= 0:
        return jsonify({"error": "Weight must be a positive number"}), 400
    if not isinstance(height, (int, float)) or height <= 0:
        return jsonify({"error": "Height must be a positive number"}), 400

    h_m = height / 100.0
    bmi = round(weight / (h_m ** 2), 1)

    if bmi < 18.5:
        category = "Underweight"
        risk = "Potential nutrient deficiency, low energy."
    elif bmi < 25:
        category = "Normal"
        risk = "Low risk if active and strong."
    elif bmi < 30:
        category = "Overweight"
        risk = "Moderate risk; focus on adherence and progressive activity."
    else:
        category = "Obese"
        risk = "Higher risk; prioritize fat loss, consistency, and supervision."

    return jsonify({
        "weight_kg": weight,
        "height_cm": height,
        "bmi": bmi,
        "category": category,
        "risk": risk
    }), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
