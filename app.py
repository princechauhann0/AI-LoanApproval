import os
import re
import json
import time
import smtplib
import requests
import io
from datetime import datetime, timedelta
from email.message import EmailMessage
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from fpdf import FPDF
from xhtml2pdf import pisa

try:
    from langchain_google_genai import ChatGoogleGenerativeAI
except:
    ChatGoogleGenerativeAI = None

try:
    from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
except:
    class SystemMessage:
        def __init__(self, content): self.content = content
    class HumanMessage:
        def __init__(self, content): self.content = content
    class AIMessage:
        def __init__(self, content): self.content = content

CONFIG_PATH = "config.json"
config = json.load(open(CONFIG_PATH))



FIREBASE_DB_URL = config.get("firebase_database_url", "").rstrip("/")
FIREBASE_API_KEY = config.get("firebase_api_key", "")
API_KEY = config.get("gemini_api_key", "")
MODEL_NAME = config.get("llm_model", "gemini-2.5-flash")
MODEL_TEMP = float(config.get("llm_temperature", 0.7))

GMAIL_USER = config.get("gmail_user", "")
GMAIL_APP_PASSWORD = config.get("gmail_app_password", "")
GMAIL_FROM = config.get("gmail_from", GMAIL_USER)

if API_KEY:
    os.environ["GOOGLE_API_KEY"] = API_KEY
    os.environ["GENAI_API_KEY"] = API_KEY
    os.environ["GOOGLE_GENAI_API_KEY"] = API_KEY
    os.environ["GOOGLE_API_USE_CLIENT_CERTIFICATE"] = "false"



app = Flask(__name__, static_folder="static", static_url_path="/static", template_folder="templates")
CORS(app)

session_histories = {}
session_data = {}

DUMMY_CUSTOMERS = {
    "cust01": {"customer_id": "cust01", "name": "Ramesh S.", "email": "ramesh@example.com", "phone": "9876543210", "credit_score": 810, "salary": 80000},
    "cust10": {"customer_id": "cust10", "name": "Neha C.", "email": "neha@example.com", "phone": "8080808080", "credit_score": 740, "salary": 50000}
}

llm = None
if ChatGoogleGenerativeAI and API_KEY:
    try:
        llm = ChatGoogleGenerativeAI(model=MODEL_NAME, google_api_key=API_KEY, temperature=MODEL_TEMP, safety_settings=None)
    except:
        llm = None

LLM_SYSTEM_PROMPT = """
You are the Master Agent for Loan Sales.

Primary tasks:
1. If user provides a customer ID (custXXXXX format) → respond only [[FLASK_CALL:VERIFY_KYC]].
2. After KYC is successful, if user provides a loan amount → respond only [[FLASK_CALL:UNDERWRITE]].
3. After underwriting and sanction email sent, if user asks about sanction letter → reply normally: "Your sanction letter has already been emailed."

Fallback Behavior:
If the user asks *anything else* (general queries, doubts, FAQs, off-topic questions, banking information, loan info, etc.),
respond normally in a helpful and friendly tone WITHOUT triggering FLASK_CALL.

Examples:
- "What is EMI?" → explain EMI.
- "What documents are needed?" → answer normally.
- "Tell me about personal loans" → answer normally.
- "Who are you?" → answer normally.
- "I want to calculate monthly EMI" → explain formula.

Important:
NEVER trigger FLASK_CALL unless:
- User provides a valid customer ID → VERIFY_KYC
- User provides a loan amount AFTER KYC → UNDERWRITE

NEVER mix text with FLASK_CALL commands.
"""

def get_session_history(session_id):
    if session_id not in session_histories:
        session_histories[session_id] = [SystemMessage(content=LLM_SYSTEM_PROMPT)]
    return session_histories[session_id]

def save_message_to_firebase(session_id, sender, message):
    if not FIREBASE_DB_URL or FIREBASE_DB_URL == "h":
        return
    try:
        url = f"{FIREBASE_DB_URL}/sessions/{session_id}/messages.json?auth={FIREBASE_API_KEY}"
        data = {"timestamp": datetime.utcnow().isoformat(), "sender": sender, "message": message}
        requests.post(url, json=data, timeout=3)
    except:
        pass

def save_session_meta(session_id, meta):
    if not FIREBASE_DB_URL or FIREBASE_DB_URL == "h":
        return
    try:
        requests.patch(f"{FIREBASE_DB_URL}/sessions/{session_id}/meta.json?auth={FIREBASE_API_KEY}", json=meta, timeout=3)
    except:
        pass

def get_customer_from_firebase(customer_id):
    if not FIREBASE_DB_URL or FIREBASE_DB_URL == "h":
        return None
    try:
        resp = requests.get(f"{FIREBASE_DB_URL}/customers/{customer_id}.json?auth={FIREBASE_API_KEY}", timeout=3)
        if resp.status_code != 200:
            return None
        data = resp.json()
        if not data:
            return None
        kyc = data.get("kyc", {})
        return {
            "customer_id": customer_id,
            "name": kyc.get("name") or data.get("name"),
            "email": kyc.get("email") or data.get("email"),
            "phone": kyc.get("phone", ""),
            "pannumber": kyc.get("pannumber", ""),
            "city": kyc.get("city", ""),
            "age": kyc.get("age", ""),
            "credit_score": data.get("credit_score", 0),
            "pre_approved_limit": data.get("pre_approved_limit", 0),
            "salary": data.get("salary", 0),
            "current_loan_status": kyc.get("currentloan", "NA")
        }
    except:
        return None

def verify_kyc(customer_id):
    c = get_customer_from_firebase(customer_id)
    if c:
        c["status"] = "Verification Successful"
        return c
    dummy = DUMMY_CUSTOMERS.get(customer_id.lower())
    if dummy:
        dummy["status"] = "Verification Successful"
        return dummy
    return {"status": "Verification Failed", "message": "Customer ID not found"}

def calculate_preapproved_limit_from_salary(salary):
    try:
        return float(salary) * 15
    except:
        return 0

def determine_tenure_months(salary):
    try:
        s = float(salary)
    except:
        s = 0
    if s < 40000:
        return 48
    if s <= 80000:
        return 60
    return 72

def calculate_emi(principal, rate, months):
    r = (rate / 100) / 12
    if months <= 0:
        return None
    if r == 0:
        return principal / months
    return (principal * r * (1+r)**months) / ((1+r)**months - 1)

def underwrite(customer, loan_amount):
    try:
        loan_amount = float(loan_amount)
    except:
        return {"status": "Rejection", "message": "Loan amount must be numeric"}
    name = customer.get("name")
    credit = int(customer.get("credit_score", 0))
    salary = float(customer.get("salary", 0))
    limit = customer.get("pre_approved_limit") or 0
    if limit <= 0:
        limit = calculate_preapproved_limit_from_salary(salary)
        customer["pre_approved_limit"] = limit
    tenure = determine_tenure_months(salary)
    emi = calculate_emi(loan_amount, 12, tenure)
    if credit < 700:
        return {"status": "Rejection", "message": f"Dear {name}, your credit score is too low"}
    if loan_amount <= limit:
        return {"status": "Pre-Approved", "message": f"Loan ₹{int(loan_amount):,} pre-approved. EMI ₹{int(emi):,}/month for {tenure} months.", "emi": emi, "tenure_months": tenure, "pre_approved_limit": limit}
    if loan_amount <= 2 * limit:
        if emi <= salary * 0.5:
            return {"status": "Approval", "message": f"Approved. EMI ₹{int(emi):,}/month for {tenure} months.", "emi": emi, "tenure_months": tenure, "pre_approved_limit": limit}
        return {"status": "Rejection", "message": "EMI exceeds 50% of salary"}
    return {"status": "Rejection", "message": "Requested amount exceeds eligibility"}

SANCTIONS_DIR = "sanctions"
os.makedirs(SANCTIONS_DIR, exist_ok=True)

def generate_sanction_letter_pdf(customer_input, loan_amount, tenure):
    if isinstance(customer_input, dict):
        customer_name = customer_input.get("name")
        customer_city = customer_input.get("city", "")
        customer_id = customer_input.get("customer_id", "")
    else:
        customer_name = customer_input
        customer_city = ""
        customer_id = ""
    app_no = f"APP-{int(time.time())}"
    sanctioned_on = datetime.utcnow().strftime("%d-%b-%Y")
    validity_days = 60
    valid_until = (datetime.utcnow() + timedelta(days=validity_days)).strftime("%d-%b-%Y")
    interest_rate = 12
    emi = calculate_emi(loan_amount, interest_rate, tenure)
    processing_fee = 999
    other_charges = "NIL"
    security = "No collateral required"
    conditions = ["PAN verification", "Salary slip last 3 months"]
    safe_name = customer_name.replace(" ", "_")
    filename = f"Sanction_Letter_{safe_name}_{app_no}.pdf"
    path = os.path.join(SANCTIONS_DIR, filename)
    html = render_template("letter.html",
                           date=sanctioned_on,
                           customer_name=customer_name,
                           customer_city=customer_city,
                           application_no=app_no,
                           loan_amount=f"{int(loan_amount):,}",
                           tenure=tenure,
                           emi=f"{int(emi) if emi else 'N/A'}")
    with open(path, "wb") as f:
        pisa_status = pisa.CreatePDF(io.BytesIO(html.encode('utf-8')), dest=f)
    return path

def generate_sanction_pdf(customer, amount):
    safe = re.sub(r"[^\w\d]+", "_", customer["name"])
    file_name = f"Sanction_{safe}_{customer['customer_id']}_{int(amount)}.pdf"
    path = os.path.join(SANCTIONS_DIR, file_name)
    c = canvas.Canvas(path, pagesize=letter)
    c.setFont("Helvetica-Bold", 18)
    c.drawString(50, 750, "Tata Capital – Loan Sanction Letter")
    c.setFont("Helvetica", 12)
    c.drawString(50, 720, f"Customer: {customer['name']}")
    c.drawString(50, 700, f"ID: {customer['customer_id']}")
    c.drawString(50, 680, f"Loan Amount: ₹{int(amount):,}")
    c.drawString(50, 660, "This is a system-generated sanction letter.")
    c.showPage()
    c.save()
    return {"file_name": file_name, "local_path": path}

def send_email_with_attachment(to_email, subject, body, pdf_path):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = GMAIL_FROM
    msg["To"] = to_email
    msg.set_content(body)
    with open(pdf_path, "rb") as f:
        msg.add_attachment(f.read(), maintype="application", subtype="pdf", filename=os.path.basename(pdf_path))
    smtp = smtplib.SMTP("smtp.gmail.com", 587)
    smtp.starttls()
    smtp.login(GMAIL_USER, GMAIL_APP_PASSWORD)
    smtp.send_message(msg)
    smtp.quit()

def local_master_agent(session_id, text):
    t = text.lower()
    m = re.search(r"\b(cust[\w\d]+)\b", t)
    if m:
        return "[[FLASK_CALL:VERIFY_KYC]]"
    if session_data.get(session_id) and session_data[session_id].get("sanction"):
        if "sanction" in t or "letter" in t:
            s = session_data[session_id]["sanction"]
            return f"The sanction letter has been emailed to {s.get('email')}."
    if session_id in session_data:
        if re.search(r"\d{3,}", t):
            return "[[FLASK_CALL:UNDERWRITE]]"
        return "Please provide the loan amount."
    return "Please provide your customer ID in format custXXXX."

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    session_id = data.get("session_id")
    user_input = data.get("user_input")
    save_message_to_firebase(session_id, "user", user_input)
    hist = get_session_history(session_id)
    hist.append(HumanMessage(content=user_input))
    if llm:
        try:
            res = llm.invoke(hist)
            text = getattr(res, "content", "")
        except:
            text = local_master_agent(session_id, user_input)
    else:
        text = local_master_agent(session_id, user_input)
    hist.append(AIMessage(content=text))
    save_message_to_firebase(session_id, "bot", text)
    m = re.search(r"\[\[FLASK_CALL:([A-Z_]+)\]\]", text)
    cmd = f"[[FLASK_CALL:{m.group(1)}]]" if m else None
    return jsonify({"response_text": "Processing request..." if cmd else text, "orchestration_command": cmd})

@app.route("/orchestrate", methods=["POST"])
def orchestrate():
    data = request.json
    step = data.get("step")
    session_id = data.get("session_id")
    info = data.get("customer_info")

    if step == "VERIFY_KYC":
        cid = info.get("customer_id")
        c = verify_kyc(cid)
        if c.get("status") == "Verification Successful":
            session_data[session_id] = c.copy()
            save_session_meta(session_id, {"customer_name": c["name"], "email": c.get("email")})
            return jsonify({"status": "success", "customer_data": c, "next_step": "ASK_LOAN_AMOUNT"})
        return jsonify({"status": "error", "message": c["message"], "next_step": "AWAITING_KYC"})

    if step == "UNDERWRITE":
        c = session_data.get(session_id)
        amt = info.get("loan_amount")
        result = underwrite(c, amt)

        if result["status"] in ["Pre-Approved", "Approval"]:

            tenure = result.get("tenure_months")
            fpdf_path = generate_sanction_letter_pdf(c, int(amt), int(tenure))

            email = c.get("email")
            send_email_with_attachment(email, "Your Sanction Letter", "Please find attached your sanction letter.", fpdf_path)

            session_data[session_id]["sanction"] = {
                "pdf": os.path.basename(fpdf_path),
                "email": email
            }

            save_session_meta(session_id, {"sanction_pdf_path": fpdf_path})

            return jsonify({
                "status": "complete",
                "worker_message": result["message"],
                "email_message": f"Sanction letter sent to {email}",
                "emi": result.get("emi"),
                "tenure_months": result.get("tenure_months")
            })

        return jsonify({"status": "complete", "worker_message": result["message"]})
    
@app.route("/new_chat")
def new_chat():
    session_id = f"sess_{int(time.time())}"
    session_histories[session_id] = [SystemMessage(content=LLM_SYSTEM_PROMPT)]
    session_data[session_id] = {}
    return jsonify({"session_id": session_id})

@app.route("/")
def index():
    return render_template("chat.html")

if __name__ == "__main__":
    app.run(port=5000, debug=True)

