from flask import Flask, render_template, request, redirect, url_for
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

app = Flask(__name__)

# =====================
# SENDGRID EMAIL
# =====================
def send_email(subject, content):
    message = Mail(
        from_email="belfadelsarah5@gmail.com",  # ⚠️ vérifié sur SendGrid
        to_emails="belfadelsarah5@gmail.com",   # où tu reçois les mails
        subject=subject,
        plain_text_content=content
    )

    try:
        sg = SendGridAPIClient(os.environ.get("SENDGRID_API_KEY"))
        response = sg.send(message)
        print("✅ Email envoyé via SendGrid")
        print("Status Code:", response.status_code)
        print("Headers:", response.headers)
    except Exception as e:
        print("❌ Erreur SendGrid :", e)

# =====================
# ROUTES
# =====================

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/services")
def services():
    return render_template("services.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")

        email_content = f"""
NOUVEAU MESSAGE - CONTACT

Nom : {name}
Email : {email}

Message :
{message}
"""
        send_email("Nouveau message contact - BRAINCORD", email_content)
        return redirect(url_for("merci"))

    return render_template("contact.html")

@app.route("/request-quote", methods=["GET", "POST"])
def request_quote():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        project_description = request.form.get("project_description")
        budget = request.form.get("budget")

        email_content = f"""
DEMANDE DE DEVIS

Nom : {name}
Email : {email}
Téléphone : {phone}
Budget : {budget}

Projet :
{project_description}
"""
        send_email("Nouvelle demande de devis - BRAINCORD", email_content)
        return redirect(url_for("merci_devis"))

    return render_template("request_quote.html")

@app.route("/merci")
def merci():
    return render_template("merci.html")

@app.route("/merci-devis")
def merci_devis():
    return render_template("merci_devis.html")

# =====================
# TEST EMAIL (optionnel)
# =====================
@app.route("/test-email")
def test_email():
    send_email("Test Render", "Email OK depuis Render")
    return "EMAIL OK"

# =====================
# RUN
# =====================
if __name__ == "__main__":
    app.run(debug=True)
