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

from flask import Flask, jsonify, request

app = Flask(__name__)

# Sample data for activities and their points
activities = {
    "National Initiatives": {
        "NSS": {"max_points": 60, "min_duration": 2},
        "NCC": {"max_points": 60, "min_duration": 2},
        # Add more activities and their details here
    },
    "Sports & Games": {
        "Sports": {"max_points": 100, "min_duration": 1},
        "Games": {"max_points": 80, "min_duration": 1},
        # Add more activities and their details here
    },
    # Add more segments and activities as needed
}


@app.route('/calculate_points', methods=['POST'])
def calculate_points():
    data = request.get_json()

    segment = data.get('segment')
    activity = data.get('activity')
    duration = data.get('duration')
    certification = data.get('certification')
    points = 0

    if segment in activities and activity in activities[segment]:
        activity_details = activities[segment][activity]
        if duration >= activity_details['min_duration']:
            points = activity_details['max_points']
            # Additional points for certification
            if certification:
                # Adjust points based on certification type
                if "Best NSS Volunteer Awardee" in certification:
                    points += min(20, 70 - points)
                elif "Participation in National Integration Camp" in certification or "Pre Republic Day Parade Camp" in certification:
                    points += min(10, 70 - points)
                elif "Best NSS Volunteer Awardee" in certification or "Participation in Republic Day Parade Camp" in certification or "International Youth Exchange Programme" in certification:
                    points += min(20, 80 - points)
        else:
            return jsonify({'error': 'Minimum duration requirement not met for the activity.'}), 400
    else:
        return jsonify({'error': 'Invalid segment or activity.'}), 400

    return jsonify({'points': points})


if __name__ == '__main__':
    app.run(debug=True)


#//sports and games//


from flask import Flask, jsonify, request

app = Flask(__name__)

# Sample data for activities and their points
activities = {
    "Sports & Games": {
        "sports": {
            "Level I": {"participation_points": 8, "first_prize_points": 10, "second_prize_points": 8, "third_prize_points": 5},
            "Level II": {"participation_points": 15, "first_prize_points": 10, "second_prize_points": 8, "third_prize_points": 5},
            "Level III": {"participation_points": 25, "first_prize_points": 10, "second_prize_points": 8, "third_prize_points": 5},
            "Level IV": {"participation_points": 60, "first_prize_points": 20, "second_prize_points": 16, "third_prize_points": 12},
            "Level V": {"participation_points": 80, "first_prize_points": 20, "second_prize_points": 16, "third_prize_points": 12},
        },
        "games": {
            "Level I": {"participation_points": 8, "first_prize_points": 10, "second_prize_points": 8, "third_prize_points": 5},
            "Level II": {"participation_points": 15, "first_prize_points": 10, "second_prize_points": 8, "third_prize_points": 5},
            "Level III": {"participation_points": 25, "first_prize_points": 10, "second_prize_points": 8, "third_prize_points": 5},
            "Level IV": {"participation_points": 60, "first_prize_points": 20, "second_prize_points": 16, "third_prize_points": 12},
            "Level V": {"participation_points": 80, "first_prize_points": 20, "second_prize_points": 16, "third_prize_points": 12},
        }
    }
}


@app.route('/calculate_points', methods=['POST'])
def calculate_points():
    data = request.get_json()

    segment = data.get('segment')
    activity = data.get('activity')
    level = data.get('level')
    participation = data.get('participation')
    first_prize = data.get('first_prize')
    second_prize = data.get('second_prize')
    third_prize = data.get('third_prize')

    if segment in activities and activity in activities[segment] and level in activities[segment][activity]:
        activity_details = activities[segment][activity][level]

        total_points = activity_details['participation_points']

        # Add points for prizes won
        total_points += first_prize * activity_details['first_prize_points']
        total_points += second_prize * activity_details['second_prize_points']
        total_points += third_prize * activity_details['third_prize_points']

        return jsonify({'points': min(total_points, 80)})  # Limit points to 80 for Level IV and V
    else:
        return jsonify({'error': 'Invalid segment, activity, or level.'}), 400


if __name__ == '__main__':
    app.run(debug=True)

#//cultural//
from flask import Flask, jsonify, request

app = Flask(__name__)

# Sample data for activities and their points
activities = {
    "Cultural Activities": {
        "Music": {
            "Level I": {"participation_points": 8, "first_prize_points": 10, "second_prize_points": 8, "third_prize_points": 5},
            "Level II": {"participation_points": 12, "first_prize_points": 10, "second_prize_points": 8, "third_prize_points": 5},
            "Level III": {"participation_points": 20, "first_prize_points": 10, "second_prize_points": 8, "third_prize_points": 5},
            "Level IV": {"participation_points": 40, "first_prize_points": 20, "second_prize_points": 16, "third_prize_points": 12},
            "Level V": {"participation_points": 60, "first_prize_points": 20, "second_prize_points": 16, "third_prize_points": 12},
        },
        "Performing arts": {
            "Level I": {"participation_points": 8, "first_prize_points": 10, "second_prize_points": 8, "third_prize_points": 5},
            "Level II": {"participation_points": 12, "first_prize_points": 10, "second_prize_points": 8, "third_prize_points": 5},
            "Level III": {"participation_points": 20, "first_prize_points": 10, "second_prize_points": 8, "third_prize_points": 5},
            "Level IV": {"participation_points": 40, "first_prize_points": 20, "second_prize_points": 16, "third_prize_points": 12},
            "Level V": {"participation_points": 60, "first_prize_points": 20, "second_prize_points": 16, "third_prize_points": 12},
        },
        "Literary arts": {
            "Level I": {"participation_points": 8, "first_prize_points": 10, "second_prize_points": 8, "third_prize_points": 5},
            "Level II": {"participation_points": 12, "first_prize_points": 10, "second_prize_points": 8, "third_prize_points": 5},
            "Level III": {"participation_points": 20, "first_prize_points": 10, "second_prize_points": 8, "third_prize_points": 5},
            "Level IV": {"participation_points": 40, "first_prize_points": 20, "second_prize_points": 16, "third_prize_points": 12},
            "Level V": {"participation_points": 60, "first_prize_points": 20, "second_prize_points": 16, "third_prize_points": 12},
        }
    }
}


@app.route('/calculate_points', methods=['POST'])
def calculate_points():
    data = request.get_json()

    segment = data.get('segment')
    activity = data.get('activity')
    level = data.get('level')
    participation = data.get('participation')
    first_prize = data.get('first_prize')
    second_prize = data.get('second_prize')
    third_prize = data.get('third_prize')

    if segment in activities and activity in activities[segment] and level in activities[segment][activity]:
        activity_details = activities[segment][activity][level]

        total_points = activity_details['participation_points']

        # Add points for prizes won
        total_points += first_prize * activity_details['first_prize_points']
        total_points += second_prize * activity_details['second_prize_points']
        total_points += third_prize * activity_details['third_prize_points']

        return jsonify({'points': min(total_points, 80)})  # Limit points to 80 for Level IV and V
    else:
        return jsonify({'error': 'Invalid segment, activity, or level.'}), 400


if __name__ == '__main__':
    app.run(debug=True)




