from flask import Flask, request, jsonify
from pymongo import MongoClient
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017/')
db = client['student_management']

# Routes

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    user = db.users.find_one({'username': username, 'password': password})
    if user:
        return jsonify({'message': 'Login successful', 'user': user}), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/results', methods=['GET'])
def get_results():
    results = list(db.results.find())
    return jsonify(results), 200

@app.route('/results', methods=['POST'])
def add_result():
    data = request.get_json()
    db.results.insert_one(data)
    return jsonify({'message': 'Result added successfully'}), 201

@app.route('/notifications', methods=['GET'])
def get_notifications():
    notifications = list(db.notifications.find())
    return jsonify(notifications), 200

@app.route('/notifications', methods=['POST'])
def add_notification():
    data = request.get_json()
    db.notifications.insert_one(data)
    return jsonify({'message': 'Notification added successfully'}), 201

@app.route('/fetch_results', methods=['GET'])
def fetch_results():
    url = "https://api.ktu.edu.in/ktu-web-service/anon/individualresult";
    response = requests.get(url)
    if response.status_code == 200:
        html_content = response.text
        # Parse HTML content using BeautifulSoup or any other library
        # Extract necessary information such as student results
        # Insert the results into MongoDB
        return jsonify({'message': 'Results fetched successfully'}), 200
    else:
        return jsonify({'message': 'Failed to fetch results'}), 500

if __name__ == '__main__':
    app.run(debug=True)