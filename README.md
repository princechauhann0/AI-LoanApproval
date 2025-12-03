## 🏦 Loan AI Assistant (Multi-Agent • Flask + Firebase + Gemini)

An intelligent multi-agent loan assistance system built using Flask, Firebase, Google Gemini, and LangChain.

This project simulates 4 internal AI agents:

🟦 KYC Agent – verifies customers

🟩 Underwriting Agent – EMI & approval

🟪 Documentation Agent – creates sanction letters

🟧 Supervisor Agent – talks to user & routes tasks

## 🚀 Features
👥 Multi-Agent AI System

Supervisor Agent handles the conversation

KYC Agent validates customer ID

Underwriter Agent decides loan approval

Documentation Agent generates & emails sanction letters

Smooth, guided chat loan flow

Smart detection of custXXXX IDs

Smart detection of loan amount numbers

Uses backend Flask calls via tokens:

[[FLASK_CALL:VERIFY_KYC]]

[[FLASK_CALL:UNDERWRITE]]

## 👤 Customer Management (Admin Panel)

Add customers using the customer form panel

Stores customer data in Firebase Realtime Database

Automatically saves:

Name

Email

Phone

PAN

Salary

Credit score

Pre-approved limit

Current loan status

Dummy customers available as fallback

## 📂 Chat History (Firebase)

Every chat is stored under:

/sessions/<session_id>/messages


Session metadata stored under:

/sessions/<session_id>/meta

## 📄 Auto PDF Sanction Letters

Fully automated:

PDF generation with XHTML2PDF

Customer details

Loan amount, EMI, Tenure

Validity period

Processing fees & conditions

Auto email using Gmail SMTP

## 🧱 Tech Stack
Component	Technology
Backend	Flask
Multi-Agent System	Simulated Supervisor + 3 Worker Agents
AI Model	Google Gemini (LangChain)
Database	Firebase Realtime DB
PDF Engine	XHTML2PDF / ReportLab
Email	Gmail SMTP
Frontend	HTML, CSS, JS
Deployment	Render


## 🔗 Live Demo  
[![Live Demo](https://img.shields.io/badge/Visit-Live%20App-green?style=for-the-badge)](https://ai-loanapproval.onrender.com) 

## 🔧 Setup Instructions
📥 Installation
1️⃣ Clone the repository
```bash
git clone https://github.com/yourusername/Loan-Approval-AI-1
cd Loan-Approval-AI-1
```
2️⃣ Install dependencies
```bash
pip install -r requirements.txt
```
3️⃣ Create your config.json
```bash
Create a file named config.json in the project folder:

{
  "firebase_database_url": "",
  "firebase_api_key": "",
  "gemini_api_key": "",
  "llm_model": "gemini-2.5-flash",
  "llm_temperature": 0.7,
  "gmail_user": "",
  "gmail_app_password": "",
  "gmail_from": ""
}
```
▶️ Usage
🧠 Start the Multi-Agent Chat System
```bash
python app.py
```

Runs on:
```bash
http://localhost:5000
```
📝 Open the Admin Customer Panel
```bash
python form_app.py
```
