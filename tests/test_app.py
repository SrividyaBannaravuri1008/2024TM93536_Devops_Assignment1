"""
ACEest Fitness & Gym - Pytest Test Suite
Tests all Flask endpoints and core business logic.
"""
import pytest
import json
from app import app, PROGRAMS, clients_db


@pytest.fixture
def client():
    """Create a Flask test client."""
    app.config["TESTING"] = True
    with app.test_client() as c:
        clients_db.clear()  # reset in-memory DB before each test
        yield c


# ---------- INDEX & HEALTH ----------

def test_index_returns_200(client):
    response = client.get("/")
    assert response.status_code == 200


def test_index_returns_app_info(client):
    response = client.get("/")
    data = json.loads(response.data)
    assert data["app"] == "ACEest Fitness & Gym"
    assert data["status"] == "running"


def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["status"] == "healthy"


# ---------- PROGRAMS ----------

def test_get_programs_returns_list(client):
    response = client.get("/programs")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "programs" in data
    assert isinstance(data["programs"], list)
    assert len(data["programs"]) == 3


def test_get_programs_contains_expected(client):
    response = client.get("/programs")
    data = json.loads(response.data)
    assert "Fat Loss (FL) - 3 day" in data["programs"]
    assert "Muscle Gain (MG) - PPL" in data["programs"]
    assert "Beginner (BG)" in data["programs"]


def test_get_specific_program(client):
    response = client.get("/programs/Beginner (BG)")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "details" in data
    assert "desc" in data["details"]
    assert "factor" in data["details"]


def test_get_invalid_program_returns_404(client):
    response = client.get("/programs/Unknown Program")
    assert response.status_code == 404
    data = json.loads(response.data)
    assert "error" in data


# ---------- CALORIE CALCULATION ----------

def test_calculate_calories_valid(client):
    payload = {"weight": 70, "program": "Fat Loss (FL) - 3 day"}
    response = client.post("/calories",
                           data=json.dumps(payload),
                           content_type="application/json")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["estimated_calories"] == 70 * 22  # factor = 22


def test_calculate_calories_muscle_gain(client):
    payload = {"weight": 80, "program": "Muscle Gain (MG) - PPL"}
    response = client.post("/calories",
                           data=json.dumps(payload),
                           content_type="application/json")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["estimated_calories"] == 80 * 35


def test_calculate_calories_missing_weight(client):
    payload = {"program": "Beginner (BG)"}
    response = client.post("/calories",
                           data=json.dumps(payload),
                           content_type="application/json")
    assert response.status_code == 400


def test_calculate_calories_missing_program(client):
    payload = {"weight": 65}
    response = client.post("/calories",
                           data=json.dumps(payload),
                           content_type="application/json")
    assert response.status_code == 400


def test_calculate_calories_invalid_weight(client):
    payload = {"weight": -10, "program": "Beginner (BG)"}
    response = client.post("/calories",
                           data=json.dumps(payload),
                           content_type="application/json")
    assert response.status_code == 400


def test_calculate_calories_invalid_program(client):
    payload = {"weight": 70, "program": "NonExistentProgram"}
    response = client.post("/calories",
                           data=json.dumps(payload),
                           content_type="application/json")
    assert response.status_code == 404


def test_calculate_calories_no_body(client):
    response = client.post("/calories", content_type="application/json")
    assert response.status_code == 400


# ---------- CLIENT MANAGEMENT ----------

def test_save_client_valid(client):
    payload = {"name": "Ravi Kumar", "age": 28, "weight": 75, "program": "Beginner (BG)"}
    response = client.post("/clients",
                           data=json.dumps(payload),
                           content_type="application/json")
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data["client"]["name"] == "Ravi Kumar"


def test_save_client_calculates_calories(client):
    payload = {"name": "Priya", "age": 25, "weight": 60, "program": "Fat Loss (FL) - 3 day"}
    response = client.post("/clients",
                           data=json.dumps(payload),
                           content_type="application/json")
    data = json.loads(response.data)
    assert data["client"]["calories"] == 60 * 22


def test_save_client_missing_name(client):
    payload = {"age": 30, "weight": 70, "program": "Beginner (BG)"}
    response = client.post("/clients",
                           data=json.dumps(payload),
                           content_type="application/json")
    assert response.status_code == 400


def test_save_client_missing_program(client):
    payload = {"name": "John", "weight": 70}
    response = client.post("/clients",
                           data=json.dumps(payload),
                           content_type="application/json")
    assert response.status_code == 400


def test_save_client_invalid_program(client):
    payload = {"name": "John", "weight": 70, "program": "Fake Program"}
    response = client.post("/clients",
                           data=json.dumps(payload),
                           content_type="application/json")
    assert response.status_code == 400


def test_get_all_clients_empty(client):
    response = client.get("/clients")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["clients"] == []


def test_get_all_clients_after_save(client):
    payload = {"name": "Arun", "weight": 80, "program": "Muscle Gain (MG) - PPL"}
    client.post("/clients", data=json.dumps(payload), content_type="application/json")
    response = client.get("/clients")
    data = json.loads(response.data)
    assert len(data["clients"]) == 1
    assert data["clients"][0]["name"] == "Arun"


# ---------- BMI CALCULATION ----------

def test_bmi_normal_weight(client):
    payload = {"weight": 70, "height": 175}
    response = client.post("/bmi",
                           data=json.dumps(payload),
                           content_type="application/json")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["category"] == "Normal"
    assert data["bmi"] == round(70 / (1.75 ** 2), 1)


def test_bmi_overweight(client):
    payload = {"weight": 80, "height": 170}
    response = client.post("/bmi",
                           data=json.dumps(payload),
                           content_type="application/json")
    data = json.loads(response.data)
    assert data["category"] == "Overweight"


def test_bmi_underweight(client):
    payload = {"weight": 45, "height": 170}
    response = client.post("/bmi",
                           data=json.dumps(payload),
                           content_type="application/json")
    data = json.loads(response.data)
    assert data["category"] == "Underweight"


def test_bmi_obese(client):
    payload = {"weight": 120, "height": 170}
    response = client.post("/bmi",
                           data=json.dumps(payload),
                           content_type="application/json")
    data = json.loads(response.data)
    assert data["category"] == "Obese"


def test_bmi_missing_height(client):
    payload = {"weight": 70}
    response = client.post("/bmi",
                           data=json.dumps(payload),
                           content_type="application/json")
    assert response.status_code == 400


def test_bmi_missing_weight(client):
    payload = {"height": 175}
    response = client.post("/bmi",
                           data=json.dumps(payload),
                           content_type="application/json")
    assert response.status_code == 400


def test_bmi_invalid_values(client):
    payload = {"weight": -5, "height": 175}
    response = client.post("/bmi",
                           data=json.dumps(payload),
                           content_type="application/json")
    assert response.status_code == 400


# ---------- PROGRAMS DATA VALIDATION ----------

def test_all_programs_have_required_keys():
    for name, details in PROGRAMS.items():
        assert "factor" in details, f"{name} missing 'factor'"
        assert "desc" in details, f"{name} missing 'desc'"
        assert details["factor"] > 0, f"{name} factor must be positive"


def test_program_factors_are_reasonable():
    for name, details in PROGRAMS.items():
        factor = details["factor"]
        assert 15 <= factor <= 50, f"{name} factor {factor} out of realistic range"
