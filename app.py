import csv

from flask import Flask, render_template, jsonify, request
import pandas as pd
from datetime import datetime
from functools import lru_cache
app = Flask(__name__)

# Load and process CSV data


@lru_cache(maxsize=1)
def load_reliability_data():
    try:
        df = pd.read_csv('data/reliability_data.csv')
        df['date'] = pd.to_datetime(df['date'], format='mixed')
        return df
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return pd.DataFrame()

def calculate_metrics(df):
    if df.empty:
        return {}

    failures = df[df['event_type'] == 'failure']

    total_equipment = df['equipment_id'].nunique()
    total_failures = len(failures)
    total_downtime = failures['downtime_hours'].sum()

    total_uptime = (total_equipment * 24 * 30) - total_downtime

    mtbf = (total_uptime / total_failures) if total_failures > 0 else 0
    mttr = failures['downtime_hours'].mean() if total_failures > 0 else 0

    availability = (
        (total_uptime / (total_uptime + total_downtime)) * 100
        if (total_uptime + total_downtime) > 0
        else 100
    )

    return {
        'mtbf': round(mtbf, 2),
        'mttr': round(mttr, 2),
        'availability': round(availability, 2),
        'total_equipment': total_equipment,
        'active_alerts': len(df[df['status'] == 'critical']),
        'failure_count': total_failures
    }

def get_equipment_status(df):
    if df is None:
        return []
    
    equipment = df.groupby('equipment_id').agg({
        'equipment_name': 'first',
        'status': 'last',
        'failure_type': lambda x: x[x != 'none'].iloc[-1] if any(x != 'none') else 'None',
        'date': 'max',
        'downtime_hours': 'sum'
    }).reset_index()
    
    equipment_list = []
    for _, row in equipment.iterrows():
        fail_count = len(df[(df['equipment_id'] == row['equipment_id']) & (df['event_type'] == 'failure')])
        equipment_list.append({
            'id': row['equipment_id'],
            'name': row['equipment_name'],
            'status': row['status'],
            'last_failure': row['failure_type'] if row['failure_type'] != 'none' else 'None',
            'last_updated': row['date'].strftime('%Y-%m-%d %H:%M'),
            'total_downtime': round(row['downtime_hours'], 1),
            'failure_count': fail_count
        })
    return equipment_list

def get_failure_trends(df):
    if df is None:
        return {'dates': [], 'failures': []}
    
    failures = df[df['event_type'] == 'failure']
    daily_failures = failures.groupby(failures['date'].dt.date).size().reset_index(name='count')
    dates = daily_failures['date'].astype(str).tolist()
    counts = daily_failures['count'].tolist()
    return {'dates': dates, 'failures': counts}

def get_pareto_data(df):
    if df is None:
        return {'categories': [], 'counts': []}
    
    failure_counts = df[df['event_type'] == 'failure']['failure_type'].value_counts()
    return {
        'categories': failure_counts.index.tolist(),
        'counts': failure_counts.values.tolist()
    }

def get_equipment_details(df, equipment_id):
    if df is None:
        return None
    
    equip_data = df[df['equipment_id'] == equipment_id]
    if equip_data.empty:
        return None
    
    failures = equip_data[equip_data['event_type'] == 'failure']
    history = []
    
    for _, row in equip_data.iterrows():
        history.append({
            'date': row['date'].strftime('%Y-%m-%d %H:%M'),
            'event': row['event_type'],
            'failure_type': row['failure_type'] if row['failure_type'] != 'none' else '-',
            'downtime': row['downtime_hours'],
            'status': row['status']
        })
    
    return {
        'id': equipment_id,
        'name': equip_data['equipment_name'].iloc[0],
        'status': equip_data['status'].iloc[-1],
        'total_failures': len(failures),
        'total_downtime': round(failures['downtime_hours'].sum(), 2) if not failures.empty else 0,
        'history': history
    }

def get_maintenance_data(df):
    if df is None:
        return []
    
    # Filter for all repair/maintenance events in the CSV
    maintenance = df[df['event_type'] == 'repair'].copy()
    maint_list = []
    
    for _, row in maintenance.iterrows():
        # Display the specific type you selected (Inspection, etc.)
        display_type = row['failure_type'] if row['failure_type'] != 'none' else 'Repair'
        
        maint_list.append({
            'equipment': row['equipment_name'],
            'equipment_id': row['equipment_id'],
            'date': row['date'].strftime('%Y-%m-%d %H:%M'),
            'type': display_type,
            'status': 'Scheduled' if row['status'] == 'maintenance' else 'Completed',
            'duration': row['downtime_hours']
        })
    
    # Sort by date (newest first)
    return sorted(maint_list, key=lambda x: x['date'], reverse=True)



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_sidebar')
def get_sidebar():
    return render_template('sidebar.html')

@app.route('/equipment')
def equipment():
    return render_template('equipment.html')

@app.route('/analysis')
def analysis():
    return render_template('analysis.html')

@app.route('/maintenance')
def maintenance():
    return render_template('maintenance.html')

@app.route('/api/metrics')
def api_metrics():
    df = load_reliability_data()
    metrics = calculate_metrics(df)
    return jsonify(metrics)

@app.route('/api/equipment')
def api_equipment():
    df = load_reliability_data()
    equipment = get_equipment_status(df)
    return jsonify(equipment)

@app.route('/api/equipment/<equipment_id>')
def api_equipment_detail(equipment_id):
    df = load_reliability_data()
    details = get_equipment_details(df, equipment_id)
    return jsonify(details) if details else jsonify({'error': 'Not found'}), 404

@app.route('/api/trends')
def api_trends():
    df = load_reliability_data()
    trends = get_failure_trends(df)
    return jsonify(trends)

@app.route('/api/alerts')
def api_alerts():
    df = load_reliability_data()
    if df is None:
        return jsonify([])
    
    critical = df[df['status'] == 'critical'].tail(5)
    alerts = []
    for _, row in critical.iterrows():
        alerts.append({
            'equipment': row['equipment_name'],
            'message': f"Critical failure: {row['failure_type']}",
            'time': row['date'].strftime('%Y-%m-%d %H:%M'),
            'severity': 'critical'
        })
    return jsonify(alerts)

@app.route('/api/maintenance')
def api_maintenance():
    df = load_reliability_data()
    maint = get_maintenance_data(df)
    return jsonify(maint)

@app.route('/api/failure_analysis')
def api_failure_analysis():
    df = load_reliability_data()
    if df is None:
        return jsonify([])
    
    analysis = []
    failures = df[df['event_type'] == 'failure']
    
    for failure_type in failures['failure_type'].unique():
        count = len(failures[failures['failure_type'] == failure_type])
        total_time = failures[failures['failure_type'] == failure_type]['downtime_hours'].sum()
        analysis.append({
            'type': failure_type,
            'count': count,
            'total_downtime': round(total_time, 2),
            'avg_repair_time': round(total_time / count, 2) if count > 0 else 0
        })
    
    return jsonify(sorted(analysis, key=lambda x: x['count'], reverse=True))

@app.route('/api/schedule', methods=['POST'])
def schedule_maintenance():
    try:
        data = request.json
        equipment_id = str(data.get('equipment_id')).strip()
        date_val = data.get('date') 
        maint_type = data.get('type')
        
        # Capture current HH:MM to make the entry dynamic
        current_time = datetime.now().strftime("%H:%M")
        if len(date_val) == 10: 
            date_val = f"{date_val} {current_time}"

        # Improved Lookup Logic
        df = load_reliability_data()
        equip_name = "Unknown Equipment"
        if df is not None:
            # Match ID and extract the name string
            name_match = df[df['equipment_id'] == equipment_id]['equipment_name'].unique()
            if len(name_match) > 0:
                equip_name = str(name_match[0])

        new_row = [
            date_val,
            equipment_id,
            equip_name,
            'repair',
            str(maint_type).strip(),
            0,
            'maintenance'
        ]

        with open('data/reliability_data.csv', 'a', newline='') as f:
            writer = csv.writer(f, lineterminator='\n')
            writer.writerow(new_row)
        load_reliability_data.cache_clear()

        return jsonify({"status": "success", "message": f"Scheduled: {equip_name}"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
    