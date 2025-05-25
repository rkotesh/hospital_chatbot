import sqlite3

DB_NAME = 'hospital_chatbot.db'

# --- Database helper functions ---

def fetch_all_hospitals():
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM Hospitals")
        rows = cursor.fetchall()
        conn.close()
        return [row[0] for row in rows]
    except sqlite3.Error as e:
        return [f"Database error: {e}"]

def fetch_hospital_info(hospital_name):
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT address, specialties, phone, emergency FROM Hospitals WHERE LOWER(name) = ?",
            (hospital_name.lower(),)
        )
        row = cursor.fetchone()
        conn.close()
        if row:
            address, specialties, phone, emergency = row
            emergency_text = "Yes" if emergency else "No"
            return (
                f"🏥 Address: {address}\n"
                f"🩺 Specialties: {specialties}\n"
                f"📞 Phone: {phone}\n"
                f"🚑 Emergency Services: {emergency_text}"
            )
        else:
            return "Hospital not found."
    except sqlite3.Error as e:
        return f"Database error: {e}"

def fetch_doctors(hospital_name):
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute(
            '''
            SELECT Doctors.name, Doctors.department, Doctors.availability 
            FROM Doctors JOIN Hospitals ON Doctors.hospital_id = Hospitals.hospital_id
            WHERE LOWER(Hospitals.name) = ?
            ''',
            (hospital_name.lower(),)
        )
        rows = cursor.fetchall()
        conn.close()
        if rows:
            response = "👨‍⚕️ Doctors:\n"
            for name, department, availability in rows:
                response += f"- {name}, Dept: {department}, Availability: {availability}\n"
            return response.strip()
        else:
            return "No doctors found."
    except sqlite3.Error as e:
        return f"Database error: {e}"

def fetch_services(hospital_name):
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute(
            '''
            SELECT Services.service_name 
            FROM Services JOIN Hospitals ON Services.hospital_id = Hospitals.hospital_id
            WHERE LOWER(Hospitals.name) = ?
            ''',
            (hospital_name.lower(),)
        )
        rows = cursor.fetchall()
        conn.close()
        if rows:
            services = [row[0] for row in rows]
            return "🛠️ Services:\n- " + "\n- ".join(services)
        else:
            return "No services found."
    except sqlite3.Error as e:
        return f"Database error: {e}"

def fetch_faqs(hospital_name):
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute(
            '''
            SELECT question, answer 
            FROM FAQs JOIN Hospitals ON FAQs.hospital_id = Hospitals.hospital_id
            WHERE LOWER(Hospitals.name) = ?
            ''',
            (hospital_name.lower(),)
        )
        rows = cursor.fetchall()
        conn.close()
        if rows:
            faqs = ""
            for question, answer in rows:
                faqs += f"❓ Q: {question}\n💬 A: {answer}\n\n"
            return faqs.strip()
        else:
            return "No FAQs found."
    except sqlite3.Error as e:
        return f"Database error: {e}"

def fetch_reviews(hospital_name):
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute(
            '''
            SELECT patient_name, rating, comment 
            FROM Reviews JOIN Hospitals ON Reviews.hospital_id = Hospitals.hospital_id
            WHERE LOWER(Hospitals.name) = ?
            ''',
            (hospital_name.lower(),)
        )
        rows = cursor.fetchall()
        conn.close()
        if rows:
            reviews = ""
            for patient_name, rating, comment in rows:
                reviews += f"⭐ {patient_name} rated {rating}/5:\n{comment}\n\n"
            return reviews.strip()
        else:
            return "No reviews found."
    except sqlite3.Error as e:
        return f"Database error: {e}"

# --- Combined information command ---

def fetch_hospital_details(hospital_name):
    info = fetch_hospital_info(hospital_name)
    doctors = fetch_doctors(hospital_name)
    services = fetch_services(hospital_name)
    faqs = fetch_faqs(hospital_name)
    reviews = fetch_reviews(hospital_name)

    return (
        f"{info}\n\n"
        f"{doctors}\n\n"
        f"{services}\n\n"
        f"📚 FAQs:\n{faqs}\n\n"
        f"📝 Reviews:\n{reviews}"
    )

# --- Chatbot logic ---

def chatbot():
    print("\n🤖 Welcome to the Hospital Chatbot!")
    print(
        "Type a command like:\n"
        "- list of hospitals\n"
        "- hospital info [hospital name]\n"
        "- doctors [hospital name]\n"
        "- services [hospital name]\n"
        "- faq [hospital name]\n"
        "- reviews [hospital name]\n"
        "- details [hospital name] (for all info)\n"
        "Type 'exit' to quit.\n"
    )

    while True:
        user_input = input("You: ").strip()

        if not user_input:
            print("Please enter a valid command.")
            continue

        if user_input.lower() == "exit":
            print("👋 Thank you for using the chatbot. Goodbye!")
            break

        lower_input = user_input.lower()

        if lower_input == "list of hospitals":
            hospitals = fetch_all_hospitals()
            print("🏥 Hospitals in the database:")
            for hospital in hospitals:
                print("-", hospital)

        elif lower_input.startswith("hospital info "):
            name = user_input[14:].strip()
            print(fetch_hospital_info(name))

        elif lower_input.startswith("doctors "):
            name = user_input[8:].strip()
            print(fetch_doctors(name))

        elif lower_input.startswith("services "):
            name = user_input[9:].strip()
            print(fetch_services(name))

        elif lower_input.startswith("faq "):
            name = user_input[4:].strip()
            print(fetch_faqs(name))

        elif lower_input.startswith("reviews "):
            name = user_input[8:].strip()
            print(fetch_reviews(name))

        elif lower_input.startswith("details "):
            name = user_input[8:].strip()
            print(fetch_hospital_details(name))

        else:
            print("❗ Unknown command. Please try again with a valid format.")

# --- Main execution ---

if __name__ == "__main__":
    chatbot()
