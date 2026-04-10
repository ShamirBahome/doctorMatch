from models import db, Doctor, User, Review, WalkinClinic
from datetime import datetime


def seed_database():
    print("Seeding database...")

    if Doctor.query.count() > 0:
        print("Database already has data. Skipping.")
        return

    doctors = [
        Doctor(
            first_name="Sarah", last_name="Johnson", gender="Female",
            phone="519-555-0101", clinic_name="Guelph Family Health Team",
            address="21 Yarmouth St, Guelph", postal_code="N1H 4G1",
            latitude=43.5448, longitude=-80.2482,
            accepting_new_patients=True, wait_time_weeks=4,
            languages="English,French",
            specializations="Family Medicine,Preventive Care",
            education="University of Toronto, MD",
            years_of_experience=15, cpso_number="CPSO-001", verified=True,
        ),
        Doctor(
            first_name="Michael", last_name="Chen", gender="Male",
            phone="519-555-0102", clinic_name="Stone Road Medical Centre",
            address="435 Stone Rd W, Guelph", postal_code="N1G 2X6",
            latitude=43.5289, longitude=-80.2673,
            accepting_new_patients=True, wait_time_weeks=2,
            languages="English,Mandarin,Cantonese",
            specializations="Family Medicine,Geriatrics",
            education="McMaster University, MD",
            years_of_experience=10, cpso_number="CPSO-002", verified=True,
        ),
        Doctor(
            first_name="Priya", last_name="Patel", gender="Female",
            phone="519-555-0103", clinic_name="Westwood Family Medicine",
            address="55 Delhi St, Guelph", postal_code="N1E 4J1",
            latitude=43.5501, longitude=-80.2350,
            accepting_new_patients=False,
            languages="English,Hindi,Gujarati,Punjabi",
            specializations="Family Medicine,Pediatrics,Women's Health",
            education="Western University, MD",
            years_of_experience=20, cpso_number="CPSO-003", verified=True,
        ),
        Doctor(
            first_name="James", last_name="Wilson", gender="Male",
            phone="519-555-0104", clinic_name="Gordon Street Medical Centre",
            address="170 Gordon St, Guelph", postal_code="N1H 4G5",
            latitude=43.5399, longitude=-80.2509,
            accepting_new_patients=True, wait_time_weeks=6,
            languages="English",
            specializations="Family Medicine,Sports Medicine",
            education="Queen's University, MD",
            years_of_experience=8, cpso_number="CPSO-004", verified=True,
        ),
        Doctor(
            first_name="Fatima", last_name="Hassan", gender="Female",
            phone="519-555-0105", clinic_name="Riverside Medical Clinic",
            address="75 Wyndham St S, Guelph", postal_code="N1H 4E9",
            latitude=43.5460, longitude=-80.2498,
            accepting_new_patients=False,
            languages="English,Arabic,Urdu,French",
            specializations="Family Medicine,Women's Health,Mental Health",
            education="University of Ottawa, MD",
            years_of_experience=12, cpso_number="CPSO-005", verified=True,
        ),
        Doctor(
            first_name="David", last_name="Thompson", gender="Male",
            phone="519-555-0106", clinic_name="Downtown Guelph Health Centre",
            address="176 Wyndham St N, Guelph", postal_code="N1H 8N9",
            latitude=43.5475, longitude=-80.2488,
            accepting_new_patients=True, wait_time_weeks=3,
            languages="English,French",
            specializations="Family Medicine,Chronic Disease",
            education="McGill University, MD",
            years_of_experience=18, cpso_number="CPSO-006", verified=True,
        ),
        Doctor(
            first_name="Lisa", last_name="Wang", gender="Female",
            phone="519-555-0107", clinic_name="South End Medical Clinic",
            address="500 Edinburgh Rd S, Guelph", postal_code="N1G 4T7",
            latitude=43.5225, longitude=-80.2600,
            accepting_new_patients=True, wait_time_weeks=1,
            languages="English,Mandarin,Korean",
            specializations="Family Medicine,Pediatrics",
            education="UBC, MD",
            years_of_experience=7, cpso_number="CPSO-007", verified=True,
        ),
        Doctor(
            first_name="Ahmed", last_name="Mohamed", gender="Male",
            phone="519-555-0108", clinic_name="Guelph Medical Place",
            address="85 Norfolk St, Guelph", postal_code="N1H 4J4",
            latitude=43.5440, longitude=-80.2510,
            accepting_new_patients=False,
            languages="English,Arabic,Somali",
            specializations="Family Medicine,Internal Medicine",
            education="University of Toronto, MD",
            years_of_experience=14, cpso_number="CPSO-008", verified=True,
        ),
        Doctor(
            first_name="Emily", last_name="Brown", gender="Female",
            phone="519-555-0109", clinic_name="Willow Creek Family Practice",
            address="200 Speedvale Ave W, Guelph", postal_code="N1H 1C4",
            latitude=43.5580, longitude=-80.2600,
            accepting_new_patients=True, wait_time_weeks=8,
            languages="English,Spanish,Portuguese",
            specializations="Family Medicine,Maternity Care",
            education="Dalhousie University, MD",
            years_of_experience=11, cpso_number="CPSO-009", verified=True,
        ),
        Doctor(
            first_name="Robert", last_name="Kim", gender="Male",
            phone="519-555-0110", clinic_name="University Medical Clinic",
            address="160 Chancellors Way, Guelph", postal_code="N1G 0E1",
            latitude=43.5300, longitude=-80.2270,
            accepting_new_patients=False,
            languages="English,Korean,Japanese",
            specializations="Family Medicine,Student Health",
            education="McMaster University, MD",
            years_of_experience=5, cpso_number="CPSO-010", verified=True,
        ),
    ]

    for doctor in doctors:
        db.session.add(doctor)

    # Create sample users
    user1 = User(email="john@example.com", first_name="John", last_name="Smith", postal_code="N1G 2W1")
    user1.set_password("password123")
    db.session.add(user1)

    user2 = User(email="maria@example.com", first_name="Maria", last_name="Garcia", postal_code="N1H 3A5")
    user2.set_password("password123")
    db.session.add(user2)

    db.session.flush()

    # Create sample reviews
    reviews = [
        Review(doctor_id=1, user_id=1, rating=5, title="Amazing doctor!", comment="Dr. Johnson is incredibly thorough and caring."),
        Review(doctor_id=1, user_id=2, rating=4, title="Great experience", comment="Very professional clinic. Highly recommend."),
        Review(doctor_id=2, user_id=1, rating=5, title="Speaks Mandarin!", comment="So grateful to find a doctor who speaks Mandarin."),
        Review(doctor_id=2, user_id=2, rating=5, title="Best in Guelph", comment="Dr. Chen goes above and beyond."),
        Review(doctor_id=3, user_id=1, rating=4, title="Great with kids", comment="Dr. Patel is wonderful with children."),
        Review(doctor_id=4, user_id=2, rating=3, title="Good but long waits", comment="Knowledgeable but long wait times."),
        Review(doctor_id=6, user_id=1, rating=5, title="Excellent care", comment="Very experienced and thorough."),
        Review(doctor_id=7, user_id=2, rating=4, title="Friendly doctor", comment="Clean clinic, efficient service."),
        Review(doctor_id=9, user_id=1, rating=5, title="Wonderful care", comment="Amazing throughout my pregnancy."),
    ]

    for review in reviews:
        db.session.add(review)

    # Create walk-in clinics
    clinics = [
        WalkinClinic(name="Guelph Walk-In Clinic", address="160 Kortright Rd W, Guelph", phone="519-836-2971",
                     latitude=43.5247, longitude=-80.2540, current_wait_minutes=45, is_open=True,
                     hours="Mon-Fri: 9AM-8PM, Sat-Sun: 10AM-4PM"),
        WalkinClinic(name="Stone Road Walk-In Clinic", address="435 Stone Rd W, Guelph", phone="519-763-5544",
                     latitude=43.5289, longitude=-80.2673, current_wait_minutes=30, is_open=True,
                     hours="Mon-Fri: 8AM-7PM, Sat: 9AM-3PM"),
        WalkinClinic(name="Westmount Medical Walk-In", address="20 Westmount Rd, Guelph", phone="519-822-4455",
                     latitude=43.5400, longitude=-80.2700, current_wait_minutes=60, is_open=True,
                     hours="Mon-Fri: 9AM-5PM"),
        WalkinClinic(name="Victoria Road Walk-In", address="525 Victoria Rd N, Guelph", phone="519-824-6770",
                     latitude=43.5520, longitude=-80.2300, current_wait_minutes=20, is_open=True,
                     hours="Mon-Fri: 8AM-8PM, Sat-Sun: 9AM-5PM"),
    ]

    for clinic in clinics:
        db.session.add(clinic)

    db.session.commit()
    print("✅ Database seeded!")
    print(f"   {len(doctors)} doctors")
    print("   2 users")
    print(f"   {len(reviews)} reviews")
    print(f"   {len(clinics)} walk-in clinics")
