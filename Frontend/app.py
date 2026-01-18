# Main imports
from flask import Flask, render_template, url_for, request, session, flash, redirect
from flask_session import Session
from functools import wraps
import os
import requests

# API Routes
import api_routes

# 
from Telemetry.setup_data import set_session_classes
from Telemetry.api_requests.get_summary import get_summary
from Telemetry.api_requests.get_averages import get_averages

# Dashboard
from Telemetry.graphs.specific.dashboard.avg_syncronisation import get_avg_syncronisation_dashboard
from Telemetry.graphs.specific.dashboard.avg_gateforcex import get_avg_gateforcex_dashboard

# Samples - Sessions
from Telemetry.graphs.specific.sample_plot.sample_syncronisation_plots import get_sample_syncronisation_plots
from Telemetry.graphs.specific.sample_plot.sample_ratio_plots import get_sample_ratio_plots
from Telemetry.graphs.specific.sample_plot.sample_line import get_sample_line_plots

# Average - Sessions
from Telemetry.graphs.specific.average_plot.avg_sync import get_avg_syncronisation_plot
from Telemetry.graphs.specific.average_plot.avg_ratio import get_avg_ratio_plot
from Telemetry.graphs.specific.average_plot.avg_line import get_avg_line_plot

# Overview
from Telemetry.graphs.plot_map import plot_map

# Retrieve data
from Telemetry.api_requests.get_sessions import get_sessions
from Telemetry.api_requests.get_rower_data import get_rower_data

# Setup flask settings
app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = 'e9f8a7d9a8fbd0c44a3ff0e1b7351f3c7b1a64e8f9e3b0e59f46a8cbb3e72c9f'
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Define login required decorator
def login_required(origin):
    @wraps(origin)
    def decorated_function(*args, **kwargs): # Positional arguments and key word arguments, returns the data passed.
        if 'user' in session:
            return origin(*args, **kwargs)
        else:
            return redirect(url_for('login'))
    return decorated_function

# Define role-based access
def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user = session.get('user')
            if not user or user.get(role) != True:
                flash("You do not have permission to access this page.", "danger")
                return redirect(url_for('dashboard'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# Home Page
@app.route('/')
def home():
    response = requests.get(api_routes.get_statistics)
    stats = {}
    if response.status_code == 200:
        stats = response.json()
    else:
        stats = {
            'users': 0,
            'uploads': 0,
            'strokes': 0,
            'distance': 0,
            'wattage': 0
        }   

    return render_template(
        'index.html', 
        statistics=stats
    )

# Register User Page
@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            return render_template(
                "register.html", 
                error='Passwords do not match. Please try again.'
            )

        payload = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "password": password,
        }

        response = requests.post(api_routes.create_user, json=payload)

        if response.status_code == 200:
            return redirect(url_for('login'))
        else:
            return render_template(
                "register.html", 
                error="Email is already in use for another account."
            )

    return render_template('register.html')

# Login Page
@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        payload = {
            "email": email,
            "password": password
        }

        response = requests.get(api_routes.check_user, json=payload)
        if response.status_code == 200:
            user_data = response.json()
            session['user'] = user_data
            return redirect(url_for('dashboard'))
        
        elif response.status_code == 401:
            return render_template(
                "login.html", 
                error="Username or Password incorrect."
            )

    return render_template('login.html')

# Dashboard Page
@app.route('/dashboard', methods=["GET", "POST"])
@login_required
def dashboard():
    user_summary = get_summary(session['user']['id'])
    data_averages = get_averages(session['user']['id'])

    returned_graphs = {
        'radar': get_avg_syncronisation_dashboard(session['user']['id']),
        'gateforcex': get_avg_gateforcex_dashboard(session['user']['id'])
    }

    return render_template(
        "dashboard.html", 
        page='dashboard', 
        user=session['user'], 
        summary=user_summary, 
        averages=data_averages, 
        graphs=returned_graphs
    )

# Flask setup and render upload page
@app.route('/dashboard/upload', methods=['GET', 'POST'])
@login_required
@role_required('is_coach')
def upload():
    if request.method == 'POST':
        button_pressed = request.form.get('action')

        if button_pressed == 'upload':
            file = request.files['file']
            if file:
                try:
                    session_classes = set_session_classes(file)
                except Exception as e:
                    return render_template(
                        "dashboard.html", 
                        page="upload", 
                        user=session['user'],
                        error=f'Error processing file: {str(e)}: File possibly corrupted or invalid format.'
                    )
                
                Rower_Profiles = session_classes[0]
                Boat_Data = session_classes[1]

                # So I can access rower_profiles without having to re calculate all the data.
                session['rower_profiles'] = [rower.to_dict() for rower in Rower_Profiles]
                session['boat_data'] = Boat_Data.to_dict()

                return render_template(
                    "dashboard.html",
                    page="upload",
                    rowers=Rower_Profiles,
                    user=session['user'], 
                    show_upload_modal=True,
                    apiroute_getallusers=api_routes.get_all_users
                )
    
        elif button_pressed == 'confirm_upload':
            # Retrieve session storage from file upload.
            Rower_Profiles = session.get("rower_profiles")
            Boat_Data = session.get("boat_data")

            # Save boat_data to database and store the primary key in the return
            Boat_Data['coach_id'] = session.get('user')['id'] # The user who uploaded the file
            Boat_Data['description'] = request.form.get('description_input')
            Boat_Data['state'] = request.form.get('state_selected')
            Boat_Data['title'] = request.form.get('title_input')

            # API post
            response = requests.post(api_routes.upload_session, json=Boat_Data)
            session_id = response.json()['session_id']

            # Iterate through the rower profiles then upload to database.
            for rower in Rower_Profiles:
                seat = str(rower["seat"])
                user_id = request.form.get(f"user_search_{seat}")

                # Upload user data to DB
                if user_id:
                    rower['user_id'] = int(user_id)
                else:
                    rower['user_id'] = None

                rower['session_id'] = int(session_id)
                response = requests.post(api_routes.upload_user_data, json=rower)

            return redirect(url_for('sessions'))
        
    return render_template(
        "dashboard.html", 
        page="upload", 
        user=session['user'],
    )

# Flask setup and render session selection page
@app.route('/dashboard/sessions', methods=['GET', 'POST'])
@login_required
def sessions():
    all_sessions = get_sessions(session['user']['id'])
    session['cached_rowing_reports'] = all_sessions
    return render_template(
        "dashboard.html", 
        page="sessions", 
        sessions=session['cached_rowing_reports'],
        user=session['user'],
    )

# Session analytics page
@app.route('/dashboard/sessions/session_id=<int:session_id>/page=<page_name>', methods=['GET', 'POST'])
@login_required
def session_page(session_id, page_name):
    # Get session from cache
    session_data = None
    for rowing_session in session.get('cached_rowing_reports', []):
        if rowing_session['id'] == session_id:
            session_data = rowing_session
            break

    # If not session found
    if not session_data:
        return redirect(url_for('sessions'))
    
    # Handle session deletion
    if request.method == 'POST' and request.form.get('action') == 'delete_session':
        # Check if user is a coach
        if not session['user'].get('is_coach', False):
            flash('You are not authorized to delete sessions.', 'error')
            return redirect(url_for('sessions', session_id=session_id, page_name=page_name))

        try:
            # Make API call to delete session
            response = requests.delete(f"{api_routes.delete_session}/{session_id}")
            if response.status_code == 200:
                # Update session cache by removing the deleted session
                session['cached_rowing_reports'] = [s for s in session['cached_rowing_reports'] if s['id'] != session_id]
                return redirect(url_for('sessions'))
            else:
                flash(f'Failed to delete session. Status code: {response.status_code}', 'error')
        except requests.RequestException as e:
            flash(f'Error deleting session: {str(e)}', 'error')
        return redirect(url_for('sessions', session_id=session_id, page_name=page_name))
    
    # Get Rower Data
    rowing_data = get_rower_data(session_id)

    # Checks if user is valid in session
    if not session['user']['is_coach']:
        is_Authenticated = False
        for rower in rowing_data:
            if rower['telemetry']['user_id'] == session['user']['id']:
                is_Authenticated = True

        if not is_Authenticated:
            return redirect(url_for('sessions'))

    name_array = []
    for user_data in rowing_data:
        if user_data['user']['user_id']:
            name_array.append(user_data['user']['last_name'])
        else:
            name_array.append(user_data['telemetry']['name'])

    # Generate graphs
    returned_graphs = {}
    selected_sample = None
    if request.method == 'POST':
        if page_name == 'samples':
            selected_sample = int(request.form.get('sample_id'))
            returned_graphs = {
                "syncronisation": get_sample_syncronisation_plots(rowing_data, names=name_array),
                "ratios": get_sample_ratio_plots(rowing_data, names=name_array),
                "gateforcex": get_sample_line_plots(rowing_data, session_data['normalizedtime'], 'gate_force_x', 'GateForceX', '% Of Cycle', 'Gate Force X (kg)', names=name_array),
                "gateanglevelocity": get_sample_line_plots(rowing_data, session_data['normalizedtime'], 'gate_angle_vel', 'GateAngle Velocity', '% Of Cycle', 'Gate Angle Vel (deg/s)', names=name_array),
                "gateforcepercent": get_sample_line_plots(rowing_data, 'gate_angle', 'gate_force_x', 'Gate Force %', 'Drive Length (%)', 'Gate Force (%)', True, True, names=name_array)
            }

            if session_data['seat_sensors']:
                returned_graphs['legsvelocity'] = get_sample_line_plots(rowing_data, session_data['normalizedtime'], 'seat_posn_vel', 'Legs Velocity','% Of Cycle', 'Legs Vel (deg)', names=name_array)
                returned_graphs['seatposition'] = get_sample_line_plots(rowing_data, 'gate_angle', 'seat_posn', 'Seat Position', 'Gate Angle (deg)', 'Seat Position', names=name_array)
                returned_graphs['legsvelocitygateangle'] = get_sample_line_plots(rowing_data, 'gate_angle', 'seat_posn_vel', 'Legs Velocity', 'Drive Length (%)', 'Legs Velocity (%)', True,True, names=name_array)
                returned_graphs['bodyarmsvelocity'] = get_sample_line_plots(rowing_data, 'gate_angle', 'body_arms_vel', 'Body + Arms Velocity', 'Drive Length (%)', 'Body Arms Vel (%)', True,True, names=name_array)

    if page_name == 'average':
        returned_graphs = {
            "syncronisation": get_avg_syncronisation_plot(rowing_data, names=name_array),
            "ratios": get_avg_ratio_plot(rowing_data, names=name_array),
            "gateforcex": get_avg_line_plot(rowing_data, session_data['normalizedtime'], 'gate_force_x', 'GateForceX', '% Of Cycle', 'Gate Force X (kg)', names=name_array),
            "gateanglevelocity": get_avg_line_plot(rowing_data, session_data['normalizedtime'], 'gate_angle_vel', 'GateAngle Velocity', '% Of Cycle', 'Gate Angle Vel (deg)', names=name_array),
            "gateforcepercent": get_avg_line_plot(rowing_data, 'gate_angle', 'gate_force_x', 'Gate Force %', 'Drive Length (%)', 'Gate Force (%)', True, True, names=name_array)
        }

        if session_data['seat_sensors']:
            returned_graphs['legsvelocity'] = get_avg_line_plot(rowing_data, session_data['normalizedtime'], 'seat_posn_vel', 'Legs Velocity','% Of Cycle', 'Legs Vel (deg)', names=name_array)
            returned_graphs['seatposition'] = get_avg_line_plot(rowing_data, 'gate_angle', 'seat_posn', 'Seat Position', 'Gate Angle (deg)', 'Seat Position', names=name_array)
            returned_graphs['legsvelocitygateangle'] = get_avg_line_plot(rowing_data, 'gate_angle', 'seat_posn_vel', 'Legs Velocity', 'Drive Length (%)', 'Velocity', True,False, names=name_array)
            returned_graphs['bodyarmsvelocity'] = get_avg_line_plot(rowing_data, 'gate_angle', 'body_arms_vel', 'Body + Arms Velocity', 'Drive Length (%)', 'Velocity', True,False, names=name_array)


    elif page_name == 'session':
        rates = []
        for rate in session_data['rating']:
            rates.append(rate)

        returned_graphs = {
            "acceleration": get_sample_line_plots(session_data, 'normalizedtime', 'acceleration', 'Boat Acceleration', 'Normalized Time (%)', 'Acceleration (m/s)', False, False, rates),
            "rowing_speed": get_sample_line_plots(session_data, None, 'meterspersecond', 'Boat Speed', 'Samples | Rate', 'Speed (m/s)', False, False, rates),
            "power_timeline": get_avg_line_plot(rowing_data, None, 'power_timeline', 'Power Timeline', 'Strokes', 'Power (W)', False, False, names=name_array),
        }

    elif page_name == 'overview':
        returned_graphs = {
            "map": plot_map(session_data)
        }

    # Render the page with the correct data
    return render_template(
        "dashboard.html",
        page=page_name,
        rowers=rowing_data,
        boat_data=session_data,
        user=session['user'],
        graphs=returned_graphs,
        sample_selected=selected_sample
    )

# Admin page
@app.route('/dashboard/admin', methods=['GET', 'POST'])
@login_required
@role_required('is_admin')
def admin():
    response = requests.get(api_routes.get_all_users)
    if response.status_code == 200:
        all_users = response.json()
    else:
        all_users = []

    return render_template(
        "dashboard.html", 
        page="admin", 
        all_users=all_users,
        user=session['user']
    )

# Delete user route
@app.route('/dashboard/admin/delete_user/<int:user_id>', methods=['POST'])
@login_required
@role_required('is_admin')
def delete_user(user_id):
    response = requests.delete(f"{api_routes.delete_user}/{user_id}")
    if response.status_code == 200:
        flash('Session deleted successfully.', 'success')
    else:
        flash(f'Failed to delete session. Status code: {response.status_code}', 'error')
    return redirect(url_for('admin'))

# View account details page
@app.route('/dashboard/account')
@login_required
def account():
    return render_template(
        'dashboard.html',
        user=session['user'],
        page='account'
    )

# Logout route
@app.route('/logout')
@login_required
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

# Run the app
if __name__ == '__main__':
    app.run(debug=True)