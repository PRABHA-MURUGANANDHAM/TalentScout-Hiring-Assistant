import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os
from textblob import TextBlob
import json
import hashlib
from datetime import datetime
import re

# ---------------- ENV ---------------- #
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

st.set_page_config(page_title="TalentScout Hiring Assistant", layout="wide")

# ---------------- UI STYLE ---------------- #
st.markdown("""
<style>
.stTextInput input, .stTextArea textarea { border-radius: 12px; }
.stButton>button {
    background: linear-gradient(to right, #4CAF50, #2E8B57);
    color: white;
    border-radius: 10px;
    height: 3em;
}
</style>
""", unsafe_allow_html=True)

# ---------------- LANGUAGE ---------------- #
language = st.sidebar.selectbox("🌎 Select Language", ["English", "Tamil", "Hindi"])

translations = {
    "English": {
        "title": "💼 TalentScout Hiring Assistant",
        "next": "Next",
        "generate": "Generate Questions",
        "submit": "Submit Answers",
        "complete": "Screening Completed Successfully"
    },
    "Tamil": {
        "title": "💼 TalentScout ஆட்சேர்ப்பு உதவியாளர்",
        "next": "அடுத்தது",
        "generate": "கேள்விகள் உருவாக்கவும்",
        "submit": "சமர்ப்பிக்கவும்",
        "complete": "தேர்வு நிறைவடைந்தது"
    },
    "Hindi": {
        "title": "💼 TalentScout भर्ती सहायक",
        "next": "आगे बढ़ें",
        "generate": "प्रश्न उत्पन्न करें",
        "submit": "जमा करें",
        "complete": "स्क्रीनिंग पूर्ण"
    }
}

T = translations[language]
st.title(T["title"])

# ---------------- SESSION STATE ---------------- #
if "stage" not in st.session_state:
    st.session_state.stage = 1
if "data" not in st.session_state:
    st.session_state.data = {}
if "questions" not in st.session_state:
    st.session_state.questions = []

# ---------------- VALIDATION ---------------- #
def is_valid_gmail(email):
    return email.endswith("@gmail.com")

def is_valid_phone(phone):
    return re.match(r"^\+\d{10,15}$", phone)

# ---------------- PURPOSE CONTROL ---------------- #
def safe_response(user_input):
    unrelated = ["joke","movie","politics","ipl","religion"]
    if any(word in str(user_input).lower() for word in unrelated):
        return "I am here strictly for recruitment screening. Please provide relevant professional information."
    if str(user_input).strip() == "":
        return "This field cannot be empty. Please provide the required information."
    return None

# ---------------- GDPR ANONYMIZED STORAGE ---------------- #
def anonymize_data(data):
    copy = data.copy()
    if "email" in copy:
        copy["email"] = hashlib.sha256(copy["email"].encode()).hexdigest()
    if "phone" in copy:
        copy["phone"] = hashlib.sha256(copy["phone"].encode()).hexdigest()
    copy["timestamp"] = str(datetime.now())
    return copy

def save_candidate_data(data):
    safe = anonymize_data(data)
    with open("simulated_candidate_data.json", "a") as f:
        f.write(json.dumps(safe) + "\n")

# ---------------- QUESTION GENERATION (5 QUESTIONS) ---------------- #
def generate_questions(techstack, experience):
    prompt = f"""
Generate exactly 5 concise professional interview questions.
Tech Stack: {techstack}
Experience: {experience} years
Rules:
- Only questions
- Numbered 1 to 5
- No explanations
- Language: {language}
"""
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "system", "content": prompt}],
        temperature=0.3
    )
    raw = response.choices[0].message.content

    return [line.strip() for line in raw.split("\n")
            if line.strip().startswith(("1.","2.","3.","4.","5."))]

# ---------------- PROGRESS ---------------- #
TOTAL = 9
st.sidebar.write(f"📊 Progress: {st.session_state.stage}/{TOTAL}")
st.sidebar.progress(min(st.session_state.stage / TOTAL, 1.0))

# ---------------- SIDEBAR SUMMARY ---------------- #
if st.session_state.data:
    st.sidebar.markdown("### 👤 Candidate Summary")
    for k,v in st.session_state.data.items():
        if k != "technical_answers":
            st.sidebar.write(f"**{k.capitalize()}**: {v}")

# ---------------- STAGE FLOW ---------------- #

def navigation(prev_stage, next_stage, value, key):
    col1, col2 = st.columns(2)
    with col1:
        if prev_stage != 0:
            if st.button("⬅ Back"):
                st.session_state.stage = prev_stage
                st.rerun()
    with col2:
        if st.button(T["next"]):
            fallback = safe_response(value)
            if fallback:
                st.warning(fallback)
            else:
                st.session_state.data[key] = value
                st.session_state.stage = next_stage
                st.rerun()

# 1️⃣ Name
if st.session_state.stage == 1:
    name = st.text_input("Enter your full name", value=st.session_state.data.get("name",""))
    navigation(0,2,name,"name")

# 2️⃣ Email
elif st.session_state.stage == 2:
    email = st.text_input("Enter Gmail address", value=st.session_state.data.get("email",""))
    col1,col2 = st.columns(2)
    with col1:
        if st.button("⬅ Back"):
            st.session_state.stage = 1
            st.rerun()
    with col2:
        if st.button(T["next"]):
            if not is_valid_gmail(email):
                st.error("Invalid Gmail address")
            else:
                st.session_state.data["email"] = email
                st.session_state.stage = 3
                st.rerun()

# 3️⃣ Phone
elif st.session_state.stage == 3:
    phone = st.text_input("Enter phone (+countrycode)", value=st.session_state.data.get("phone",""))
    col1,col2 = st.columns(2)
    with col1:
        if st.button("⬅ Back"):
            st.session_state.stage = 2
            st.rerun()
    with col2:
        if st.button(T["next"]):
            if not is_valid_phone(phone):
                st.error("Invalid phone format")
            else:
                st.session_state.data["phone"] = phone
                st.session_state.stage = 4
                st.rerun()

# 4️⃣ Experience
elif st.session_state.stage == 4:
    exp = st.text_input("Years of Experience", value=st.session_state.data.get("experience",""))
    navigation(3,5,exp,"experience")

# 5️⃣ Position
elif st.session_state.stage == 5:
    pos = st.text_input("Desired Position", value=st.session_state.data.get("position",""))
    navigation(4,6,pos,"position")

# 6️⃣ Location
elif st.session_state.stage == 6:
    loc = st.text_input("Current Location", value=st.session_state.data.get("location",""))
    navigation(5,7,loc,"location")

# 7️⃣ Tech Stack
elif st.session_state.stage == 7:
    tech = st.text_input("Enter Tech Stack", value=st.session_state.data.get("techstack",""))
    col1,col2 = st.columns(2)
    with col1:
        if st.button("⬅ Back"):
            st.session_state.stage = 6
            st.rerun()
    with col2:
        if st.button(T["generate"]):
            st.session_state.data["techstack"] = tech
            st.session_state.questions = generate_questions(
                tech,
                st.session_state.data.get("experience","1")
            )
            st.session_state.stage = 8
            st.rerun()

# 8️⃣ Technical Questions
elif st.session_state.stage == 8:
    answers = []
    sentiments = []

    for i, q in enumerate(st.session_state.questions):
        st.markdown(f"### {q}")
        ans = st.text_area("Your Answer", key=f"a{i}")
        answers.append(ans)

    col1,col2 = st.columns(2)
    with col1:
        if st.button("⬅ Back"):
            st.session_state.stage = 7
            st.rerun()
    with col2:
        if st.button(T["submit"]):
            for ans in answers:
                if ans.strip():
                    polarity = TextBlob(ans).sentiment.polarity
                    sentiments.append(polarity)

            avg_sentiment = sum(sentiments)/len(sentiments) if sentiments else 0

            st.session_state.data["technical_answers"] = answers
            st.session_state.data["avg_sentiment"] = round(avg_sentiment,2)

            save_candidate_data(st.session_state.data)

            st.session_state.stage = 9
            st.rerun()

# 9️⃣ Final Stage
elif st.session_state.stage == 9:
    st.success(T["complete"])

    avg = st.session_state.data.get("avg_sentiment",0)

    if avg < -0.3:
        st.info("We appreciate your effort. If any question felt challenging, that’s completely okay.")
    elif avg > 0.5:
        st.info("Your enthusiasm and confidence were clearly reflected in your responses.")
    else:
        st.info("Thank you for your professional responses.")

    st.write("Our recruitment team will review your answers carefully.")
