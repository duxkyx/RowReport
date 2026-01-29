# Get the data required for the radar chart on the dashboard
import requests
import api_routes

def get_radar_averages(user_id):
    response = requests.get(f"{api_routes.get_radar_averages}/{user_id}")
    if response.status_code == 200:
        return response.json()
    else:
        return {
            "25_recov": 0,
            "50_recov": 0,
            "75_recov": 0,
            "hang_start": 0,
            "min_angle": 0,
            "catch": 0,
            "effect_start": 0,
            "70_max": 0,
            "max_f": 0,
            "max_70": 0,
            "effect_end": 0,
            "finish": 0,
            "max_angle": 0,
            "release": 0
        }