from flask import Flask, jsonify, request
from google.cloud import firestore
from google.cloud.exceptions import NotFound
from datetime import datetime
import pytz

app = Flask(__name__)

# Assuming the JSON key file is in the same directory as your Flask app
json_credentials_path = "sshv1-fff-firebase-adminsdk-z3zxs-7d83d52c07.json"

# Initialize Firestore using the service account key
firestore_client = firestore.Client.from_service_account_json(json_credentials_path)

# Maximum number of entries to keep
MAX_ENTRIES = 100

# Set the desired time zone
desired_time_zone = pytz.timezone('Asia/Manila')

@app.route('/')
def home():
    return "Welcome to the Firestore-Flask Integration po!"

@app.route('/get_data')
def get_data():
    try:
        # Example: Retrieve data from Firestore
        data_ref = firestore_client.collection('SSHv1').document('SensorData')
        data = data_ref.get().to_dict()

        return jsonify(data)
    except NotFound:
        return jsonify({'error': 'Document not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/write_data', methods=['POST'])
def write_data():
    try:
        # Extract parameters from the request
        temperature = request.json.get('temperature')
        mq135_gas_level = request.json.get('mq135_gas_level')
        mq2_gas_level = request.json.get('mq2_gas_level')
        acceleration = request.json.get('acceleration')
        gyroscope = request.json.get('gyroscope')

        # Get current date and time in UTC
        current_datetime_utc = datetime.utcnow()

        # Convert UTC time to desired time zone
        current_datetime = current_datetime_utc.replace(tzinfo=pytz.utc).astimezone(desired_time_zone)

        # Example: Write data to Firestore
        data_ref = firestore_client.collection('SSHv1').document('SensorData')

        # Get current data
        current_data = data_ref.get().to_dict()

        # Check the number of entries
        if current_data and len(current_data) >= MAX_ENTRIES:
            # Sort entries by timestamp and get the oldest one
            oldest_entry_key = min(current_data.keys())

            # Delete the oldest entry
            data_ref.update({
                oldest_entry_key: firestore.DELETE_FIELD
            })

        # Add new data using set with merge=True
        data_ref.set({
            f'{current_datetime}': {
                'temperature': temperature,
                'mq135_gas_level': mq135_gas_level,
                'mq2_gas_level': mq2_gas_level,
                'acceleration': acceleration,
                'gyroscope': gyroscope,
            }
        }, merge=True)

        return jsonify({'success': True}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
