# Gets user sessions for session page
import requests
import api_routes

def get_rower_data(session_id):
    response = requests.get(f"{api_routes.get_rower_data}/{session_id}")
    if response.status_code == 200:
        return response.json()
    else:
        return []
    