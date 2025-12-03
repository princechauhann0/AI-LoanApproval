from flask import Flask, request, render_template
import json
import requests

app = Flask(__name__)

# Load config.json (contains realtime_url)
with open("config.json") as f:
    config = json.load(f)

@app.route("/")
def form():
    return render_template("form.html")

@app.route("/add-customer", methods=["POST"])
def add_customer():

    # MATCH FORM FIELD NAMES EXACTLY
    name = request.form["customerName"]
    phone = request.form["phoneNumber"]
    age = request.form["age"]
    city = request.form["city"]
    pan = request.form["panNumber"]
    email = request.form["emailAddress"]
    salary = request.form["salary"]
    currentloan = request.form["currentLoan"]
    credit = request.form["creditScore"]

    customer_id = f"cust{phone}"

    data = {
        "kyc": {
            "name": name,
            "phone": phone,
            "email":email,
            "age": int(age),
            "city": city,
            "pannumber": pan,
            "currentloan": int(currentloan)
        },
        "salary": int(salary),
        "credit_score": int(credit),
    }

    # URL to push to Realtime DB
    url = config["firebase_database_url"].rstrip("/") + f"/customers/{customer_id}.json"

    # SAVE DATA
    requests.put(url, json=data)

    return render_template("form.html", success=True)

if __name__ == "__main__":
    app.run(debug=True, port=5001)
