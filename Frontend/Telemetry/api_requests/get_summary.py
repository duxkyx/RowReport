# Get the summary i.e. number of sessions, total strokes, total distance, user type
import requests
import API_Routes

def get_summary(user_id):
    response = requests.get(f"{API_Routes.get_summary}/{user_id}")
    if response.status_code == 200:
        return response.json()
    else:
        return {
            "num_sessions": 0,
            "total_strokes": 0,
            "total_distance": 0,
            "user_type": "N/A"
        }