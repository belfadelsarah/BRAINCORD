from flask import Flask, render_template, request, redirect, url_for
import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv

# =====================
# INIT
# =====================
load_dotenv()

app = Flask(__name__)

# =====================
# CONFIG EMAIL
# =====================
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

# ⚠️ NE PAS CRASHER L'APP EN PROD
EMAIL_ENABLED = True
if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
    EMAIL_ENABLED = False
    print("⚠️ Email désactivé : variables manquantes")

# =====================
# ENVOI EMAIL (SAFE)
# =====================
def send_email(subject, content):
    if not EMAIL_ENABLED:
        print("📩 Email non envoyé (email désactivé)")
        return

    try:
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = EMAIL_ADDRESS
        msg.set_content(content)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=10) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)

        print("✅ Email envoyé avec succès")

    except Exception as e:
        # 🔥 ON LOG MAIS ON NE PLANTE PAS
        print("❌ Erreur envoi email :", e)

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
# RUN LOCAL
# =====================
if __name__ == "__main__":
    app.run(debug=True)
