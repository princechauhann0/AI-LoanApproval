# 🏦 Loan AI Assistant (Flask + Firebase)

An AI-powered loan assistance system built using **Flask**, **Firebase**, **Google Gemini**, and **LangChain**.  
This project enables:

- 🔹 Smart loan eligibility checking  
- 🔹 Customer data verification (Firebase + Dummy Fallback)  
- 🔹 Automated underwriting  
- 🔹 PDF sanction letter generation  
- 🔹 Admin panel for adding customer records  
- 🔹 Chat interface with guided loan flow  
- 🔹 Realtime chat history saved in Firebase  

---

## 🚀 Features

### 👤 Customer Management (Admin Panel)
- Add new customers using a clean web form.
- Automatically stores customer data in **Firebase Realtime Database**.
- Each customer contains:
  - KYC details  
  - Salary  
  - Credit Score  
  - Current Loan  
  - Pre-approved Loan Limit  

### 🤖 AI Chat Assistant
The assistant follows the loan flow:

1. Welcome → Ask for Customer ID  
2. Verify customer (Firebase → Dummy fallback)  
3. Ask for Loan Amount  
4. Perform Underwriting  
5. Approve or Reject loan  
6. Auto-generate **PDF sanction letter**  

### 📂 Past Chat History
- Every conversation is stored in Firebase  
- Future version includes Chat History UI  

---

## 🧱 Tech Stack

| Component | Technology |
|----------|------------|
| Backend | Flask |
| Database | Firebase Realtime DB |
| AI Model | Google Gemini (via LangChain) |
| PDF Tool | FPDF |
| Frontend | HTML, CSS, JavaScript |
| Deployment | Local / Render / Railway (optional) |

---

## 🔗 Live Demo  
[![Live Demo](https://img.shields.io/badge/Visit-Live%20App-green?style=for-the-badge)](https://ai-loanapproval.onrender.com)


## 🔧 Setup Instructions

# Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/loan-approval-ai
cd loan-approval-a
```

Install the required packages:
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
```bash
pip install -r requirements.txt
```
Configure your environment, including any necessary API keys (Firebase Realtime Database URL, etc.).

Usage

Run the Flask chat application:
```bash
python app.py
```
Run the Admin Panel (Add Customer):

```bash
python form_app.py
```
