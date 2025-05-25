import sqlite3
import os

DB_NAME = 'hospital_chatbot.db'

# Delete existing corrupted database if it exists
if os.path.exists(DB_NAME):
    os.remove(DB_NAME)
    

# Connect to SQLite database (creates new file)
conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

# Drop and recreate all tables
cursor.executescript('''
    DROP TABLE IF EXISTS Reviews;
    DROP TABLE IF EXISTS FAQs;
    DROP TABLE IF EXISTS Services;
    DROP TABLE IF EXISTS Doctors;
    DROP TABLE IF EXISTS Hospitals;

    CREATE TABLE Hospitals (
        hospital_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        address TEXT,
        specialties TEXT,
        phone TEXT,
        emergency BOOLEAN
    );

    CREATE TABLE Doctors (
        doctor_id INTEGER PRIMARY KEY AUTOINCREMENT,
        hospital_id INTEGER,
        name TEXT,
        department TEXT,
        availability TEXT,
        FOREIGN KEY(hospital_id) REFERENCES Hospitals(hospital_id)
    );

    CREATE TABLE Services (
        service_id INTEGER PRIMARY KEY AUTOINCREMENT,
        hospital_id INTEGER,
        service_name TEXT,
        FOREIGN KEY(hospital_id) REFERENCES Hospitals(hospital_id)
    );

    CREATE TABLE FAQs (
        faq_id INTEGER PRIMARY KEY AUTOINCREMENT,
        hospital_id INTEGER,
        question TEXT,
        answer TEXT,
        FOREIGN KEY(hospital_id) REFERENCES Hospitals(hospital_id)
    );

    CREATE TABLE Reviews (
        review_id INTEGER PRIMARY KEY AUTOINCREMENT,
        hospital_id INTEGER,
        patient_name TEXT,
        rating INTEGER,
        comment TEXT,
        FOREIGN KEY(hospital_id) REFERENCES Hospitals(hospital_id)
    );
''')

# Original 5 Hospitals
hospitals = [
    ("Aster Ramesh Hospitals", "Collector Office Rd, Beside Hindu College Grounds, Nagarampalem, Guntur, Andhra Pradesh 522004", "Cardiology, Oncology, Neurology", "+91 8632377777", 1),
    ("Lalitha Super Specialities Hospital", "12-21-13, Kothapet Main Road, Kothapeta, Guntur, Andhra Pradesh 522001", "Cardiology, Neurology, Surgery, Gastroenterology, Orthopedics, Nephrology, Pulmonology, Radiology, Physical Medicine, Gynecology & Obstetrics", "+91 8632222866", 1),
    ("Sreshta Hospitals", "JKC College Road, Gujjanagundla, Guntur, Andhra Pradesh 522007", "Cardiology, Neurology, Pulmonology, Nephrology, Gastroenterology, Endocrinology, Orthopedics, Obstetrics & Gynecology, Urology, Surgery, Pediatrics, Radiology, Anesthesiology, Critical Care, ENT, Plastic Surgery", "+91 7799988108", 1),
    ("Vikaas Hospitals", "D.No. 26, 2-6/1, Collector Office Road, Nagarampalem, Guntur, Andhra Pradesh 522004", "Cardiology, Neurology, Nephrology, Gastroenterology, Orthopedics, Obstetrics & Gynecology, Surgery, Urology, Pulmonology, Endocrinology, Oncology, Dentistry, Pediatrics, Rheumatology, Physiotherapy", "+91 7731960108", 1),
    ("Amrutha Hospitals", "Old Club Road, Kothapet, Guntur, Andhra Pradesh 522001", "Cardiology, Orthopedics, Neurosurgery, General Medicine & Surgery, Pediatrics, Maxillofacial Surgery, Emergency & Critical Care", "+91 8632210123", 1)
]

# New 5 Hospitals in Guntur district
new_hospitals = [
    ("Guntur General Hospital", "Near Bus Stand, Guntur, Andhra Pradesh 522002", "General Medicine, Surgery, Pediatrics, Orthopedics", "+91 8632244555", 1),
    ("Sai Krishna Hospital", "10-5-22, Arundalpet, Guntur, Andhra Pradesh 522002", "Cardiology, Neurology, Nephrology, Emergency Care", "+91 8632244666", 1),
    ("Rainbow Care Hospital", "11-3-45, Brodipet, Guntur, Andhra Pradesh 522002", "Maternity, Pediatrics, General Surgery", "+91 8632244777", 0),
    ("Sri Venkateswara Hospital", "Beside RTC Complex, Guntur, Andhra Pradesh 522002", "Orthopedics, Neurology, Emergency Care", "+91 8632244888", 1),
    ("Curewell Hospital", "Opposite Amaravathi Stadium, Guntur, Andhra Pradesh 522002", "General Medicine, Dermatology, ENT, Surgery", "+91 8632244999", 0)
]

# Insert hospitals (original + new)
cursor.executemany('''
    INSERT INTO Hospitals (name, address, specialties, phone, emergency)
    VALUES (?, ?, ?, ?, ?)
''', hospitals + new_hospitals)

# Fetch hospital ids after insert to link doctors, services, etc.
cursor.execute("SELECT hospital_id, name FROM Hospitals")
hospital_id_map = {name: hid for hid, name in cursor.fetchall()}

# Original doctors (adjusted hospital_id from map)
doctors = [
    (hospital_id_map["Aster Ramesh Hospitals"], "Dr. Yadlapalli Lakshmana Swamy", "Orthopaedics", "24/7"),
    (hospital_id_map["Lalitha Super Specialities Hospital"], "Dr. Lakshmikantham", "Gynecology", "24/7"),
    (hospital_id_map["Sreshta Hospitals"], "Dr. Nagarjuna Gottipati", "General Medicine", "24/7"),
    (hospital_id_map["Vikaas Hospitals"], "Dr. Sushmitha Yadlapalli", "Radiology", "24/7"),
    (hospital_id_map["Amrutha Hospitals"], "Dr. Hemasundar Korrapati", "Cardiology", "24/7"),
    (hospital_id_map["Aster Ramesh Hospitals"], "Dr. Priyanka Poda", "Pulmonology", "24/7"),
    (hospital_id_map["Aster Ramesh Hospitals"], "Dr. Hima Bindu Bolla", "Neurology", "24/7"),
    (hospital_id_map["Lalitha Super Specialities Hospital"], "Dr. K. Vara Prasada Rao", "Nephrology", "24/7"),
    (hospital_id_map["Lalitha Super Specialities Hospital"], "Dr. Tharaka Mourya", "Urology", "24/7"),
    (hospital_id_map["Sreshta Hospitals"], "Dr. Videha Divi", "Gastroenterology", "24/7"),
    (hospital_id_map["Sreshta Hospitals"], "Dr. B. Nagaraju", "Interventional Cardiology", "24/7"),
    (hospital_id_map["Vikaas Hospitals"], "Dr. Suresh Babu Vallepu", "Neurology", "24/7"),
    (hospital_id_map["Vikaas Hospitals"], "Dr. Siva Ramakrishna D", "Gastroenterology & Hepatology", "24/7"),
    (hospital_id_map["Amrutha Hospitals"], "Dr. Pavan Kommineni", "Orthopedics", "24/7"),
    (hospital_id_map["Amrutha Hospitals"], "Dr. Bhagya Rekha", "Obstetrics & Gynecology", "24/7"),
    (hospital_id_map["Amrutha Hospitals"], "Dr. Shalini Ankem", "Dentistry", "24/7"),
]

# New doctors for new hospitals
new_doctors = [
    (hospital_id_map["Guntur General Hospital"], "Dr. Ramesh Kumar", "General Medicine", "9AM-5PM"),
    (hospital_id_map["Guntur General Hospital"], "Dr. Anjali Verma", "Pediatrics", "10AM-4PM"),
    (hospital_id_map["Sai Krishna Hospital"], "Dr. Naveen Reddy", "Cardiology", "24/7"),
    (hospital_id_map["Sai Krishna Hospital"], "Dr. Sunitha Rao", "Nephrology", "9AM-6PM"),
    (hospital_id_map["Rainbow Care Hospital"], "Dr. Priya Singh", "Maternity", "8AM-2PM"),
    (hospital_id_map["Sri Venkateswara Hospital"], "Dr. Kiran Kumar", "Orthopedics", "24/7"),
    (hospital_id_map["Sri Venkateswara Hospital"], "Dr. Divya Patel", "Neurology", "10AM-5PM"),
    (hospital_id_map["Curewell Hospital"], "Dr. Sameer Ahmed", "Dermatology", "9AM-4PM"),
    (hospital_id_map["Curewell Hospital"], "Dr. Rajesh Sharma", "ENT", "9AM-3PM"),
]

cursor.executemany('''
    INSERT INTO Doctors (hospital_id, name, department, availability)
    VALUES (?, ?, ?, ?)
''', doctors + new_doctors)

# Original services
services = [
    (hospital_id_map["Aster Ramesh Hospitals"], "Appointment Booking"),
    (hospital_id_map["Aster Ramesh Hospitals"], "Pharmacy"),
    (hospital_id_map["Lalitha Super Specialities Hospital"], "Appointment Booking"),
]

# New services for new hospitals
new_services = [
    (hospital_id_map["Guntur General Hospital"], "Emergency Services"),
    (hospital_id_map["Sai Krishna Hospital"], "24/7 Emergency"),
    (hospital_id_map["Rainbow Care Hospital"], "Maternity Care"),
    (hospital_id_map["Sri Venkateswara Hospital"], "Orthopedic Surgery"),
    (hospital_id_map["Curewell Hospital"], "Dermatology Consultation"),
]

cursor.executemany('''
    INSERT INTO Services (hospital_id, service_name)
    VALUES (?, ?)
''', services + new_services)

# Original FAQs
faqs = [
    (hospital_id_map["Aster Ramesh Hospitals"], "What are the visiting hours?", "Visiting hours are from 9AM to 7PM daily."),
    (hospital_id_map["Aster Ramesh Hospitals"], "Do you have a pharmacy?", "Yes, an in-house pharmacy is available 24/7."),
    (hospital_id_map["Lalitha Super Specialities Hospital"], "Do you accept insurance?", "Yes, we accept most major insurance providers."),
    (hospital_id_map["Lalitha Super Specialities Hospital"], "Is emergency service available?", "Yes, emergency care is provided 24/7."),
    (hospital_id_map["Sreshta Hospitals"], "Do you offer specialist consultations?", "Yes, consultations are available for over 15 specialties."),
    (hospital_id_map["Sreshta Hospitals"], "What are the OPD timings?", "Outpatient services are open from 8AM to 8PM."),
    (hospital_id_map["Vikaas Hospitals"], "Can I book appointments online?", "Yes, online appointment booking is available."),
    (hospital_id_map["Vikaas Hospitals"], "Do you offer cashless treatment?", "Yes, cashless treatment is available for insurance patients."),
    (hospital_id_map["Amrutha Hospitals"], "What surgeries do you perform?", "We offer general, orthopedic, neuro, and maxillofacial surgeries."),
    (hospital_id_map["Amrutha Hospitals"], "How can I reach in an emergency?", "You can call our helpline +91 8632210123 any time.")
]

# New FAQs for new hospitals
new_faqs = [
    (hospital_id_map["Guntur General Hospital"], "Is emergency service available?", "Yes, 24/7 emergency services."),
    (hospital_id_map["Sai Krishna Hospital"], "Do you have ICU?", "Yes, equipped ICU available."),
    (hospital_id_map["Rainbow Care Hospital"], "Do you provide prenatal care?", "Yes, specialized maternity care is offered."),
    (hospital_id_map["Sri Venkateswara Hospital"], "Can I book an appointment online?", "Online appointment booking is available."),
    (hospital_id_map["Curewell Hospital"], "What are your OPD timings?", "OPD is open from 9AM to 5PM.")
]

cursor.executemany('''
    INSERT INTO FAQs (hospital_id, question, answer)
    VALUES (?, ?, ?)
''', faqs + new_faqs)

# Original reviews
reviews = [
    (hospital_id_map["Aster Ramesh Hospitals"], "Sanjay", 5, "Excellent service and friendly staff."),
    (hospital_id_map["Lalitha Super Specialities Hospital"], "Anjali", 4, "Good facilities but parking is an issue."),
    (hospital_id_map["Sreshta Hospitals"], "Ravi", 5, "Doctors are very knowledgeable and caring."),
    (hospital_id_map["Vikaas Hospitals"], "Meena", 4, "Clean and well maintained."),
    (hospital_id_map["Amrutha Hospitals"], "Kiran", 5, "Highly recommended for orthopedic treatments."),
]

# New reviews for new hospitals
new_reviews = [
    (hospital_id_map["Guntur General Hospital"], "Ramesh", 4, "Good general hospital with friendly staff."),
    (hospital_id_map["Sai Krishna Hospital"], "Divya", 5, "Excellent cardiology department."),
    (hospital_id_map["Rainbow Care Hospital"], "Anita", 3, "Good maternity care but needs better facilities."),
    (hospital_id_map["Sri Venkateswara Hospital"], "Hari", 4, "Effective orthopedic treatments."),
    (hospital_id_map["Curewell Hospital"], "Sita", 4, "Good general medicine and dermatology services."),
]

cursor.executemany('''
    INSERT INTO Reviews (hospital_id, patient_name, rating, comment)
    VALUES (?, ?, ?, ?)
''', reviews + new_reviews)

conn.commit()
conn.close()

print("Database setup complete with 10 hospitalsin Guntur district.")
