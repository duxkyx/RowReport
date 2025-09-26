# Gets the averages from the user telemetry data
import requests
import API_Routes

def get_averages(user_id):
    response = requests.get(f"{API_Routes.get_averages}/{user_id}")
    if response.status_code == 200:
        return response.json()
    else:
        return {
            "UT1": {
                "min_angle": 0,
                "max_angle": 0,
                "arc_length": 0,
                "catch_slip": 0,
                "finish_slip": 0,
                "swivel_power": 0,
                "seat_length": 0
            },
            "UT2": {
                "min_angle": 0,
                "max_angle": 0,
                "arc_length": 0,
                "catch_slip": 0,
                "finish_slip": 0,
                "swivel_power": 0,
                "seat_length": 0
            }
        }