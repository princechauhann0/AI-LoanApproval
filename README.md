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
