from flask import Flask, jsonify, request

app = Flask(__name__)

# Sample data for activities and their points
activities = {
    "National Initiatives": {
        "NSS": {
            "points": 60,
            "max_points": 60,
            "additional_marks": {
                "Best NSS Volunteer Awardee (University level)": 10,
                "Best NSS Volunteer Awardee (State / National level)": 20
            },
            "verification": "documentary evidence"
        },
        "NCC": {
            "points": 60,
            "max_points": 60,
            "additional_marks": {
                # Similar additional marks can be added for NCC activities
            },
            "verification": "documentary evidence"
        }
    },
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
    },
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
    },
    "Professional Self Initiatives": {
        "Tech fest, tech quiz": {
            "Level I": {"points": 10, "max_points": 50, "verification": "certificate"},
            "Level II": {"points": 20, "max_points": 50, "verification": "certificate"},
            "Level III": {"points": 30, "max_points": 50, "verification": "certificate"},
            "Level IV": {"points": 40, "max_points": 50, "verification": "certificate"},
            "Level V": {"points": 50, "max_points": 50, "verification": "certificate"}
        },
        # Add other professional self initiatives here
    },
    "Entrepreneurship and Innovation": {
        "Start-up Company – Registered legally": {
            "points": 60, "max_points": 60, "verification": "documentary evidence"
        },
        # Add other entrepreneurship and innovation activities here
    },
    "Leadership & Management": {
        "Student Professional Societies - IEEE, IET, ASME, SAE, NASA, others": {
            "Core coordinator": {"points": 15},
            "Sub coordinator": {"points": 10},
            "Volunteer": {"points": 5},
            "max_points": 40,
            "verification": "documentary evidence"
        },
        # Add other leadership and management activities here
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
    certificate = data.get('certificate')

    if segment in activities and activity in activities[segment]:
        if segment == "Sports & Games":
            if level in activities[segment][activity]:
                activity_details = activities[segment][activity][level]

                total_points = activity_details['participation_points']

                # Add points for prizes won
                total_points += first_prize * activity_details['first_prize_points']
                total_points += second_prize * activity_details['second_prize_points']
                total_points += third_prize * activity_details['third_prize_points']

                # Add additional points for winning
                if certificate and (first_prize > 0 or second_prize > 0 or third_prize > 0):
                    total_points += min(20, 80 - total_points)  # Additional points capped at 20

                return jsonify({'points': min(total_points, 80)})  # Limit points to 80 for Level IV and V
            else:
                return jsonify({'error': 'Invalid level for the activity.'}), 400
        elif segment == "National Initiatives":
            if activity in activities[segment]:
                activity_details = activities[segment][activity]

                points = activity_details['points']

                # Check if duration is at least 2 years
                duration = data.get('duration')
                if duration >= 2:
                    points += activity_details['max_points'] - activity_details['points']  # Max points for duration

                    # Check if certification provided
                    if certificate:
                        # Additional marks for outstanding performance
                        for mark in activity_details['additional_marks'].values():
                            points += min(mark, activity_details['max_points'] - points)

                return jsonify({'points': min(points, 80)})  # Limit points to 80
            else:
                return jsonify({'error': 'Invalid activity.'}), 400
        elif segment == "Cultural Activities":
            if level in activities[segment][activity]:
                activity_details = activities[segment][activity][level]

                total_points = activity_details['participation_points']

                # Add points for prizes won
                total_points += first_prize * activity_details['first_prize_points']
                total_points += second_prize * activity_details['second_prize_points']
                total_points += third_prize * activity_details['third_prize_points']

                # Add additional points for winning
                if certificate and (first_prize > 0 or second_prize > 0 or third_prize > 0):
                    total_points += min(20, 80 - total_points)  # Additional points capped at 20

                return jsonify({'points': min(total_points, 80)})  # Limit points to 80 for Level IV and V
            else:
                return jsonify({'error': 'Invalid level for the activity.'}), 400
        elif segment == "Professional Self Initiatives":
            if activity in activities[segment]:
                activity_details = activities[segment][activity]

                # Check if the activity has levels
                if isinstance(activity_details, dict):
                    if level in activity_details:
                        activity_level_details = activity_details[level]
                        total_points = activity_level_details['points']

                        # Limit total points to maximum points allowed
                        total_points = min(total_points, activity_level_details['max_points'])

                        return jsonify({'points': total_points})
                    else:
                        return jsonify({'error': 'Invalid level for the activity.'}), 400
                else:
                    total_points = activity_details['points']
                    return jsonify({'points': total_points})
            else:
                return jsonify({'error': 'Invalid activity.'}), 400
        elif segment == "Entrepreneurship and Innovation":
            if activity in activities[segment]:
                activity_details = activities[segment][activity]

                total_points = activity_details['points']

                # Limit total points to maximum points allowed
                total_points = min(total_points, activity_details['max_points'])

                return jsonify({'points': total_points})
            else:
                return jsonify({'error': 'Invalid activity.'}), 400
        elif segment == "Leadership & Management":
            role = data.get('role')
            if activity in activities[segment] and role in activities[segment][activity]:
                role_details = activities[segment][activity][role]

                total_points = role_details['points']

                # Limit total points to maximum points allowed
                total_points = min(total_points, role_details['max_points'])

                return jsonify({'points': total_points})
            else:
                return jsonify({'error': 'Invalid activity or role.'}), 400
    else:
        return jsonify({'error': 'Invalid segment or activity.'}), 400


if __name__ == '__main__':
    app.run(debug=True)
