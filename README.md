💼 TalentScout Hiring Assistant

TalentScout Hiring Assistant is an AI-powered recruitment screening chatbot built using Python and Streamlit.

The application collects essential candidate details through a structured multi-step workflow, dynamically generates technical questions based on the candidate’s tech stack, and performs sentiment analysis to evaluate response tone and communication confidence.

This project demonstrates conversational UI design, workflow management, sentiment analysis integration, and simulated backend data handling following privacy-aware principles.

🚀 Features

✅ Multi-step candidate information collection

✅ Back and Next navigation for editing inputs

✅ Dynamic generation of 5 technical questions

✅ Tech stack-based customization

✅ Sentiment analysis using TextBlob

✅ Professional fallback responses for unexpected inputs

✅ Simulated anonymized backend storage

✅ Duplicate submission prevention

✅ Clean and structured Streamlit UI

🧠 Technologies Used

Python

Streamlit

TextBlob (Sentiment Analysis)

UUID (Unique Application ID Generation)

🔄 Application Workflow

Collect candidate details:

Full Name

Email Address

Phone Number

Years of Experience

Desired Position

Current Location

Tech Stack

Generate 5 technical questions based on tech stack.

Collect candidate responses.

Perform sentiment analysis on answers.

Store anonymized data in simulated backend.

Display professional submission confirmation.

🔐 Data Handling & Privacy

Candidate data is processed in anonymized format.

No real database storage is used (simulated backend only).

Designed following GDPR-aware data handling principles.

No sensitive information is exposed.

TalentScout-Hiring-Assistant
│
├── app.py              → Main Streamlit application
├── utils.py            → Helper functions (validation, questions, sentiment)
├── requirements.txt    → Project dependencies
├── README.md           → Documentation
└── .gitignore          → Ignored system & environment files



▶️ How to Run Locally
1️⃣ Clone the repository
git clone https://github.com/your-username/TalentScout-Hiring-Assistant.git
cd TalentScout-Hiring-Assistant

2️⃣ Install dependencies
pip install -r requirements.txt

3️⃣ Run the application
streamlit run app.py

📌 Project Purpose

This project demonstrates:

Conversational AI interface design

Structured multi-step form implementation

Sentiment analysis integration

Recruitment automation workflow

Privacy-aware data processing

Clean project structuring for GitHub

📈 Future Enhancements

Recruiter dashboard

Database integration (SQLite / PostgreSQL)

AI-based answer scoring

Resume upload feature

Deployment on Streamlit Cloud
