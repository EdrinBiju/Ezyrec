from flask import Flask, jsonify, request

app = Flask(__name__)

# Maximum points for NSS and NCC
MAX_POINTS_NATIONAL = 60

# Additional marks for outstanding performance
ADDITIONAL_MARKS_NATIONAL = {
    "University level": 10,
    "State / National level": 20,
    "National Integration Camp / Pre Republic Day Parade Camp (South India)": 10,
    "Republic Day Parade Camp / International Youth Exchange Programme": 20
}

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
        "MOOC with final assessment certificate": {
            "points": 50, "max_points": 50, "verification": "certificate"
        },
        "Competitions conducted by Professional Societies": {
            "Level I": {"points": 10, "max_points": 40, "verification": "certificate"},
            "Level II": {"points": 15, "max_points": 40, "verification": "certificate"},
            "Level III": {"points": 20, "max_points": 40, "verification": "certificate"},
            "Level IV": {"points": 30, "max_points": 40, "verification": "certificate"},
            "Level V": {"points": 40, "max_points": 40, "verification": "certificate"}
        },
        "Attending Full time Conference/ Seminars /Exhibitions/ Workshop/ STTP at IITs/NITs": {
            "points": 15, "max_points": 30, "verification": "certificate"
        },
        "Attending Full time Conference/ Seminars /Exhibitions/ Workshop/ STTP at KTU or its affiliated institutes": {
            "points": 6, "max_points": 12, "verification": "certificate", "max_participation": 2
        },
        "Paper presentation/ publication at IITs/NITs": {
            "points": 20, "max_points": 40, "verification": "certificate", "recognition_points": 10
        },
        "Paper presentation/ publication at KTU or its affiliated institutes": {
            "points": 10, "max_points": 20, "verification": "certificate", "recognition_points": 10
        },
        "Poster Presentation at IITs/NITs": {
            "points": 8, "max_points": 16, "verification": "certificate", "recognition_points": 2
        },
        "Poster Presentation at KTU or its affiliated institutes": {
            "points": 4, "max_points": 8, "verification": "certificate", "recognition_points": 2
        },
        "Industrial Training/ Internship": {
            "points": 20, "max_points": 20, "verification": "certificate or Letter from Authorities"
        },
        "Industrial/ Exhibition visits": {
            "points": 5, "max_points": 10, "verification": "certificate or Letter from Authorities or Documentary evidence"
        },
        "Foreign Language Skill - TOEFL/IELTS/BEC": {
            "points": 50, "max_points": 50, "verification": "certificate"
        }
    },
    "Entrepreneurship and Innovation": {
        "Start-up Company – Registered legally": {
            "points": 60, "max_points": 60, "verification": "documentary evidence"
        },
        "Patent-Filed": {
            "points": 30, "max_points": 60, "verification": "documentary evidence"
        },
        "Patent - Published": {
            "points": 35, "max_points": 60, "verification": "documentary evidence"
        },
        "Patent  - Approved": {
            "points": 50, "max_points": 60, "verification": "documentary evidence"
        },
        "Patent- Licensed": {
            "points": 80, "max_points": 80, "verification": "documentary evidence"
        },
        "Prototype developed and tested": {
            "points": 60, "max_points": 60, "verification": "documentary evidence"
        },
        "Awards for Products developed": {
            "points": 60, "max_points": 60, "verification": "documentary evidence"
        },
        "Innovative technologies developed and used by industries/users": {
            "points": 60, "max_points": 60, "verification": "documentary evidence"
        },
        "Got venture capital funding for innovative ideas/products": {
            "points": 80, "max_points": 80, "verification": "documentary evidence"
        },
        "Startup Employment (Offering jobs to two persons not less than Rs. 15000/- per month)": {
            "points": 80, "max_points": 80, "verification": "documentary evidence"
        },
        "Societal innovations": {
            "points": 50, "max_points": 50, "verification": "documentary evidence"
        }
    },
    "Leadership & Management": {
        "Student Professional Societies - IEEE, IET, ASME, SAE, NASA, others": {
            "Core coordinator": {"points": 15},
            "Sub coordinator": {"points": 10},
            "Volunteer": {"points": 5},
            "max_points": 40,
            "verification": "documentary evidence"
        },
        "College Association Chapters (Mechanical, Civil, Electrical etc.)": {
            "Core coordinator": {"points": 15},
            "Sub coordinator": {"points": 10},
            "Volunteer": {"points": 5},
            "max_points": 40,
            "verification": "documentary evidence"
        },
        "Festival & Technical Events": {
            "Core coordinator": {"points": 15},
            "Sub coordinator": {"points": 10},
            "Volunteer": {"points": 5},
            "max_points": 40,
            "verification": "documentary evidence"
        },
        "Hobby Clubs": {
            "Core coordinator": {"points": 15},
            "Sub coordinator": {"points": 10},
            "Volunteer": {"points": 5},
            "max_points": 40,
            "verification": "documentary evidence"
        },
        "Elected student representatives": {
            "Chairman": {"points": 30},
            "Secretary": {"points": 25},
            "Other Council members": {"points": 15},
            "max_points": 60,
            "verification": "documentary evidence"
        }
    }
}


@app.route('/calculate_national_points', methods=['POST'])
def calculate_national_points():
    data = request.get_json()

    activity = data.get('activity')
    duration = data.get('duration')
    certificate = data.get('certificate')

    if activity in ["NSS", "NCC"]:
        points = 0

        # Check if duration is at least 2 years
        if duration >= 2:
            points += MAX_POINTS_NATIONAL

            # Check if certificate provided and it is either a certificate or letter from authorities
            if certificate and (certificate.lower() == "certificate" or certificate.lower() == "letter from authorities"):
                # Additional marks for outstanding performance
                if "Best NSS Volunteer Awardee (University level)" in certificate:
                    points += min(ADDITIONAL_MARKS_NATIONAL["University level"], 70 - points)
                elif "Best NSS Volunteer Awardee (State / National level)" in certificate:
                    points += min(ADDITIONAL_MARKS_NATIONAL["State / National level"], 80 - points)
                elif "Participation in National Integration Camp/Pre Republic Day Parade Camp (South India)" in certificate:
                    points += min(ADDITIONAL_MARKS_NATIONAL["National Integration Camp / Pre Republic Day Parade Camp (South India)"], 70 - points)
                elif "Participation in Republic Day Parade Camp / International Youth Exchange Programme" in certificate:
                    points += min(ADDITIONAL_MARKS_NATIONAL["Republic Day Parade Camp / International Youth Exchange Programme"], 80 - points)

        return jsonify({'points': min(points, 80)})
    else:
        return jsonify({'error': 'Invalid activity.'}), 400


@app.route('/calculate_sports_points', methods=['POST'])
def calculate_sports_points():
    data = request.get_json()

    activity = data.get('activity')
    level = data.get('level')
    participation = data.get('participation')
    first_prize = data.get('first_prize')
    second_prize = data.get('second_prize')
    third_prize = data.get('third_prize')
    certificate = data.get('certificate')

    if activity in activities["Sports & Games"] and level in activities["Sports & Games"][activity]:
        activity_details = activities["Sports & Games"][activity][level]

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
        return jsonify({'error': 'Invalid segment, activity, or level.'}), 400


@app.route('/calculate_cultural_points', methods=['POST'])
def calculate_cultural_points():
    data = request.get_json()

    activity = data.get('activity')
    level = data.get('level')
    participation = data.get('participation')
    first_prize = data.get('first_prize')
    second_prize = data.get('second_prize')
    third_prize = data.get('third_prize')
    certificate = data.get('certificate')

    if activity in activities["Cultural Activities"] and level in activities["Cultural Activities"][activity]:
        activity_details = activities["Cultural Activities"][activity][level]

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
        return jsonify({'error': 'Invalid segment, activity, or level.'}), 400


@app.route('/calculate_professional_points', methods=['POST'])
def calculate_professional_points():
    data = request.get_json()

    activity = data.get('activity')
    level = data.get('level')
    participation = data.get('participation')
    documents = data.get('documents')

    if activity in activities["Professional Self Initiatives"]:
        activity_details = activities["Professional Self Initiatives"][activity]

        # Check if the activity has levels
        if isinstance(activity_details, dict):
            if level in activity_details:
                activity_level_details = activity_details[level]
                total_points = activity_level_details['points']

                # Add recognition points if available
                if 'recognition_points' in activity_level_details:
                    total_points += activity_level_details['recognition_points']

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


@app.route('/calculate_entrepreneurship_points', methods=['POST'])
def calculate_entrepreneurship_points():
    data = request.get_json()

    activity = data.get('activity')

    if activity in activities["Entrepreneurship and Innovation"]:
        activity_details = activities["Entrepreneurship and Innovation"][activity]

        total_points = activity_details['points']

        # Limit total points to maximum points allowed
        total_points = min(total_points, activity_details['max_points'])

        return jsonify({'points': total_points})
    else:
        return jsonify({'error': 'Invalid activity.'}), 400


@app.route('/calculate_leadership_points', methods=['POST'])
def calculate_leadership_points():
    data = request.get_json()

    activity = data.get('activity')
    role = data.get('role')

    if activity in activities["Leadership & Management"] and role in activities["Leadership & Management"][activity]:
        role_details = activities["Leadership & Management"][activity][role]

        total_points = role_details['points']

        # Limit total points to maximum points allowed
        total_points = min(total_points, role_details['max_points'])

        return jsonify({'points': total_points})
    else:
        return jsonify({'error': 'Invalid activity or role.'}), 400


if __name__ == '__main__':
    app.run(debug=True)
