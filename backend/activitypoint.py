points={
  "National Initiatives": {
    ("NCC","NSS"):60,
  },
  "Sports & Games": {
    ("Sports","Games"):{
        "College Events":8,
        "Zonal Events":15,
        "State/ University Events":25,
        "National Events":40,
        "International Events":60,
    }, 
  },
  "Cultural Activities": {
    ("Music", "Performing arts", "Literary arts"):{
        "College Events":8,
        "Zonal Events":12,
        "State/ University Events":20,
        "National Events":40,
        "International Events":60,
    },
  },
  ("Professional Self Initiatives"): {
    "Tech Fest, Tech Quiz":{
        "College Events":10,
        "Zonal Events":20,
        "State/ University Events":30,
        "National Events":40,
        "International Events":50,
    },
    ("MOOC with final assessment certificate","Foreign Language Skill (TOFEL/IELTS/BEC exams etc.)"):50,
    ("Competitions conducted by Professional Societies"):{
        "College Events":10,
        "Zonal Events":15,
        "State/ University Events":20,
        "National Events":30,
        "International Events":40,
    },
    (
        "Attending Full time Conference / Seminars / Exhibitions / Workshop / STTP conducted at IITs/NITs",
        "Poster Presentation at IITs/NITs",
        "Industrial Training/Internship (at least for 5 full days)"
    ):20,
    ("Paper presentation/publication at IITs/NITs"):30,
    ("Industrial/Exhibition visits"):5,
  },
  "Entrepreneurship and Innovation": {
    (
        "Start-up Company – Registered legally",
        "Prototype developed and tested",
        "Awards for Products developed",
        "Innovative technologies developed and used by industries/users"
    ):60,
    ("Patent-Filed"):30,
    ("Patent - Published"):35,
    ("Patent- Approved","Societal innovations"):50,
    (
        "Patent- Licensed",
        "Got venture capital funding for innovative ideas/products.",
        "Startup Employment (Offering jobs to two persons less than Rs. 15000/- per month)"
    ):80,
  },
  "Leadership & Management": {
    (
        "Student Professional Societies (IEEE, IET, ASME, SAE, NASA etc.)",
        "College Association Chapters (Mechanical, Civil, Electrical etc.)",
        "Festival & Technical Events (College approved)",
        "Hobby Clubs",
        "Special Initiatives (Approval from College and University is mandatory)"
    ):{
        "Core coordinator":15,
        "Sub coordinator":10,
        "Volunteer":5,
    },
    ("Elected student representatives"):{
        "Chairman":30,
        "Secretary":25,
        "Other Council Members":15,
    },
  },
}

achievment={
  ("National Initiatives"): {
    (" C certificate / outstanding performance supported by certification"):20, 
    (
        "Best NSS Volunteer Awardee (University level), supported by certification",
        "Participation in National Integration Camp, supported by certification",
        "Pre Republic Day Parade Camp (South India), supported by certification"
    ):10,
    (
        "Best NSS Volunteer Awardee (State / National level), supported by certification",
        "Participation in Republic Day Parade Camp, supported by certification",
        "International Youth Exchange Programme, supported by certification",
    ):20,
  },
  ("Sports & Games","Cultural Activities"): {
    "First Prize":{
        "College Events":10,
        "Zonal Events":10,
        "State/ University Events":10,
        "National Events":20,
        "International Events":20,
    }, 
    "Second Prize":{
        "College Events":8,
        "Zonal Events":8,
        "State/ University Events":8,
        "National Events":16,
        "International Events":16,
    }, 
    "Third Prize":{
        "College Events":5,
        "Zonal Events":5,
        "State/ University Events":5,
        "National Events":12,
        "International Events":12,
    },
  },
  ("Professional Self Initiatives"): {"Certificate of recognition":10}
}

def CalculateActivityPoint(certificate):
    criteria = certificate["criteria"]
    sub_criteria = certificate["subCriteria"]
    level = certificate.get("level", "")
    achievement = certificate.get("achievement", "")

    points_earned = 0

    # Helper function to find the key in a dictionary where the key is a tuple
    def find_key_in_tuple_dict(d, key):
        for k in d:
            if isinstance(k, tuple) and key in k:
                return d[k]
        return None

    # Check if the criteria is in the points dictionary
    if criteria in points:
        criteria_data = points[criteria]
        # Check if sub_criteria is in the criteria_data dictionary
        if isinstance(criteria_data, dict):
            sub_criteria_data = find_key_in_tuple_dict(criteria_data, sub_criteria)
            if sub_criteria_data:
                if isinstance(sub_criteria_data, dict) and level:
                    points_earned += sub_criteria_data.get(level, 0)
                else:
                    points_earned += sub_criteria_data
        elif isinstance(criteria_data, int):
            points_earned += criteria_data

    # Check if the criteria is in the achievement dictionary
    if criteria in achievment:
        achievement_data = achievment[criteria]
        if achievement:
            if achievement in achievement_data:
                achievement_points = achievement_data[achievement]
                if isinstance(achievement_points, dict) and level:
                    points_earned += achievement_points.get(level, 0)
                else:
                    points_earned += achievement_points
        elif sub_criteria in achievement_data:
            sub_achievement_points = achievement_data[sub_criteria]
            if isinstance(sub_achievement_points, dict) and level:
                points_earned += sub_achievement_points.get(level, 0)
            else:
                points_earned += sub_achievement_points
    else:
        # Check if the criteria is in the tuple keys in the achievement dictionary
        achievement_data = find_key_in_tuple_dict(achievment, criteria)
        if achievement_data:
            if achievement:
                if achievement in achievement_data:
                    achievement_points = achievement_data[achievement]
                    if isinstance(achievement_points, dict) and level:
                        points_earned += achievement_points.get(level, 0)
                    else:
                        points_earned += achievement_points
            elif sub_criteria in achievement_data:
                sub_achievement_points = achievement_data[sub_criteria]
                if isinstance(sub_achievement_points, dict) and level:
                    points_earned += sub_achievement_points.get(level, 0)
                else:
                    points_earned += sub_achievement_points

    return points_earned

# print(CalculateActivityPoint(
#         {
#     "criteria": "Sports & Games",
#     "subCriteria": "Sports",
#     "level": "College Events",
#     "achievement": "First Prize"
# }
#     )
# )