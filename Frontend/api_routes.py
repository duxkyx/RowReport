import os

API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")

def api_route(path: str) -> str:
    return str(API_BASE_URL + path)

create_user = api_route("/register")
check_user = api_route("/login")
get_all_users = api_route("/get_all_users")

upload_session = api_route('/upload/session')
upload_user_data = api_route('/upload/user_data')
delete_session = api_route('/delete/session')
delete_user = api_route('/delete/user')

get_averages = api_route('/user_data/get_averages')
get_summary = api_route('/user_data/get_summary')
get_radar_averages = api_route('/user_data/get_radar_averages')
get_telemetry_data_training_zones = api_route('/user_data/get_telemetry_data')
get_sessions = api_route('/user_data/get_sessions')
get_rower_data = api_route('/user_data/get_rower_data')
