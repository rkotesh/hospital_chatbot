import streamlit as st
import sqlite3
import pandas as pd

DB_NAME = "hospital_chatbot.db"

st.set_page_config(page_title="🏥 Hospital Chatbot Dashboard", layout="wide")

st.sidebar.title("🏥 Hospital Chatbot")

def get_connection():
    return sqlite3.connect(DB_NAME)

def fetch_hospitals():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT hospital_id, name FROM Hospitals")
        return cursor.fetchall()

def fetch_hospital_info(hospital_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT name, address, specialties, phone, emergency 
            FROM Hospitals WHERE hospital_id=?
        """, (hospital_id,))
        return cursor.fetchone()

def fetch_doctors(hospital_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT name, department, availability FROM Doctors WHERE hospital_id=?
        """, (hospital_id,))
        return cursor.fetchall()

def fetch_services(hospital_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT service_name FROM Services WHERE hospital_id=?", (hospital_id,))
        return cursor.fetchall()

def fetch_faqs(hospital_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT question, answer FROM FAQs WHERE hospital_id=?", (hospital_id,))
        return cursor.fetchall()

def fetch_reviews(hospital_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT patient_name, rating, comment FROM Reviews WHERE hospital_id=?", (hospital_id,))
        return cursor.fetchall()

# Fetch hospital list and build dictionary {name: id}
hospitals = fetch_hospitals()
hospital_dict = {name: hid for hid, name in hospitals}

search_term = st.sidebar.text_input("🔍 Search Hospitals", "").lower()
if search_term:
    filtered_hospitals = [name for name in hospital_dict.keys() if search_term in name.lower()]
else:
    filtered_hospitals = list(hospital_dict.keys())

if not filtered_hospitals:
    st.sidebar.warning("No hospitals match your search.")
    st.stop()

selected_hospital = st.sidebar.selectbox("🏥 Select Hospital", filtered_hospitals)
selected_hospital_id = hospital_dict[selected_hospital]

st.title("🏥 Hospital Information")

info = fetch_hospital_info(selected_hospital_id)
if info:
    name, address, specialties, phone, emergency = info
    st.header(f"🏥 {name}")
    st.write(f"**Address:** {address}")
    st.write(f"**Specialties:** {specialties}")
    st.write(f"**Phone:** {phone}")
    st.write(f"**Emergency Services:** {'Yes' if emergency else 'No'}")

    doctors = fetch_doctors(selected_hospital_id)
    if doctors:
        st.subheader("👨‍⚕️ Doctors")
        df_doctors = pd.DataFrame(doctors, columns=["Name", "Department", "Availability"])
        st.table(df_doctors)
    else:
        st.info("No doctors found for this hospital.")

    services = fetch_services(selected_hospital_id)
    if services:
        st.subheader("🧪 Services")
        for service_name, in services:
            st.write(f"- {service_name}")
    else:
        st.info("No services listed for this hospital.")

    faqs = fetch_faqs(selected_hospital_id)
    if faqs:
        st.subheader("❓ FAQs")
        for q, a in faqs:
            st.markdown(f"**Q:** {q}")
            st.markdown(f"**A:** {a}")
            st.markdown("---")
    else:
        st.info("No FAQs found.")

    reviews = fetch_reviews(selected_hospital_id)
    if reviews:
        st.subheader("🌟 Reviews")
        for patient, rating, comment in reviews:
            st.markdown(f"**{patient}** rated: {rating} ⭐")
            st.write(comment)
            st.markdown("---")
    else:
        st.info("No reviews found.")
else:
    st.warning("No data found for this hospital.")
