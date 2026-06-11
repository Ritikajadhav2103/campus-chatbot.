"""
Script to update college database with comprehensive information
"""

import json

# Template for adding comprehensive college information
college_template = {
    "name": "",
    "short_name": "",
    "college_type": "",  # Government / Private / Government Aided
    "established": "",
    "affiliated_university": "",
    "city": "Solapur",
    "address": "",
    "website": "",
    "contact": "",
    "email": "",
    
    "courses_offered": {
        "undergraduate": [],
        "postgraduate": [],
        "diploma": []
    },
    
    "admission_process": {
        "entrance_exam": "",
        "eligibility": "",
        "application_mode": "",
        "selection_criteria": "",
        "important_dates": ""
    },
    
    "fees_structure": {
        "tuition_fee_per_year": "",
        "hostel_fee_per_year": "",
        "other_charges": "",
        "total_approximate": "",
        "scholarship_available": ""
    },
    
    "hostel_availability": {
        "boys_hostel": "",
        "girls_hostel": "",
        "hostel_facilities": []
    },
    
    "facilities": {
        "library": "",
        "laboratories": "",
        "sports": "",
        "wifi": "",
        "cafeteria": "",
        "transport": "",
        "medical": "",
        "auditorium": ""
    },
    
    "placement_information": {
        "placement_rate": "",
        "highest_package": "",
        "average_package": "",
        "top_recruiters": [],
        "training_provided": ""
    },
    
    "history": "",
    "photo_url": "",
    "campus_photos": [],
    "accreditation": "",
    "ranking": "",
    
    "additional_info": {
        "student_clubs": [],
        "events": [],
        "alumni_network": ""
    }
}

def add_college_details():
    """Interactive function to add college details"""
    print("=" * 70)
    print("COLLEGE DATABASE UPDATE TOOL")
    print("=" * 70)
    print()
    print("This tool helps you add comprehensive information for each college.")
    print()
    
    # Load existing database
    try:
        with open('solapur_colleges_database.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
    except:
        print("Error loading database!")
        return
    
    # Show all colleges
    print("COLLEGES IN DATABASE:")
    print("-" * 70)
    
    all_colleges = []
    for category in data['categories'].values():
        for college in category['colleges']:
            all_colleges.append(college)
            print(f"• {college['name']} ({college.get('short_name', 'N/A')})")
    
    print()
    print(f"Total: {len(all_colleges)} colleges")
    print()
    print("=" * 70)
    print()
    print("FIELDS TO ADD FOR EACH COLLEGE:")
    print()
    print("1. College Type (Government/Private/Aided)")
    print("2. Affiliated University")
    print("3. Complete Address")
    print("4. Courses Offered (UG/PG/Diploma)")
    print("5. Admission Process")
    print("   - Entrance Exam")
    print("   - Eligibility")
    print("   - Application Mode")
    print("   - Selection Criteria")
    print("6. Fees Structure")
    print("   - Tuition Fee")
    print("   - Hostel Fee")
    print("   - Other Charges")
    print("   - Scholarships")
    print("7. Hostel Availability")
    print("   - Boys/Girls Hostel")
    print("   - Capacity")
    print("   - Facilities")
    print("8. Facilities")
    print("   - Library")
    print("   - Labs")
    print("   - Sports")
    print("   - WiFi")
    print("   - Cafeteria")
    print("   - Transport")
    print("9. Placement Information")
    print("   - Placement Rate")
    print("   - Packages")
    print("   - Top Recruiters")
    print("10. History (Detailed)")
    print("11. Campus Photos")
    print("12. Accreditation & Ranking")
    print()
    print("=" * 70)
    print()
    print("TEMPLATE FILE CREATED:")
    print("See 'solapur_colleges_enhanced_database.json' for example")
    print()
    print("You can:")
    print("1. Manually edit the JSON file")
    print("2. Or provide information and I'll help structure it")
    print()
    print("=" * 70)

if __name__ == "__main__":
    add_college_details()
