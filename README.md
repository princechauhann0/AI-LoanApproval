# 🏦 Loan AI Assistant
### Multi-Agent • Flask • Firebase • Gemini

An intelligent **multi-agent loan assistance system** built using **Flask**, **Firebase**, **Google Gemini**, and **LangChain**.

Your system simulates **4 internal AI agents**:

- 🟧 **orchestrator Agent** – Talks to users & routes tasks  
- 🟦 **Verification Agent** – Verifies customer identity  
- 🟩 **Underwriting Agent** – EMI calculation & approval  
- 🟪 **Documentation Agent** – Generates sanction letters  

---

# 🚀 Features

## 🤖 Multi-Agent AI System
- Supervisor controls the flow  
- Detects customer IDs (`custXXXX`) automatically  
- Detects loan amounts automatically 
- Friendly conversational responses for general questions

---

## 👤 Customer Management (Admin Panel)
- Add & manage customers easily  
- Stores records in **Firebase Realtime Database**  
- Automatically saves:
- Name  
- Email  
- Phone  
- PAN  
- Salary  
- Credit Score  
- Pre-approved Limit  
- Current Loan Status  
- Dummy fallback customers included

---

## 💬 Chat History (Firebase)

Messages stored at:
```bash
/sessions/<session_id>/messages
```
Session metadata stored at:
```bash
/sessions/<session_id>/meta
```

---

## 📄 Automated Sanction Letters

The system auto-generates PDF sanction letters:

- Customer details  
- Loan amount, EMI, Tenure  
- Interest rate  
- Validity period  
- Conditions  
- Processing fee  
- Sends email via **Gmail SMTP**  

Powered by **XHTML2PDF** & **ReportLab**.

---

# 🧱 Tech Stack

| Component | Technology |
|----------|------------|
| Backend | Flask |
| Multi-Agent Logic | Simulated Supervisor + 3 Worker Agents |
| AI Model | Google Gemini (LangChain) |
| Database | Firebase Realtime DB |
| PDF Engine | XHTML2PDF / ReportLab |
| Email Sender | Gmail SMTP |
| Frontend | HTML, CSS, JS |
| Deployment | Render |

---

# 🔗 Live Demo
[![Live Demo](https://img.shields.io/badge/Visit-Live%20App-green?style=for-the-badge)](https://ai-loanapproval.onrender.com)

---

# 🔧 Setup Instructions

## 📥 Installation

### 1️⃣ Clone the repository
```bash
git clone https://github.com/yourusername/Loan-Approval-AI-1
cd Loan-Approval-AI-1
```
### 2️⃣ Install dependencies
```bash
pip install -r requirements.txt
```
### 3️⃣ Create config.json

Create a file in the project root named config.json with the following structure:
```bash
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
### ▶️ Usage
🧠 Run the Multi-Agent Chat System
```bash
python app.py
```
Runs at:
```bash
http://localhost:5000
```
### 📝 Run Customer Admin Panel (optional)
```bash
python form_app.py
```
