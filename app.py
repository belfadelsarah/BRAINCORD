from flask import Flask, render_template, request, redirect, url_for
import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv

# =====================
# INIT
# =====================
load_dotenv()  # utile en local, ignoré par Render

app = Flask(__name__)

# =====================
# CONFIG EMAIL
# =====================
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

# =====================
# FONCTION ENVOI EMAIL
# =====================
def send_email(subject, content):
    if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
        raise RuntimeError("Variables EMAIL_ADDRESS ou EMAIL_PASSWORD manquantes")

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = EMAIL_ADDRESS
    msg.set_content(content)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)

# =====================
# ROUTES
# =====================

# -------- HOME --------
@app.route("/")
def home():
    return render_template("index.html")

# -------- SERVICES --------
@app.route("/services")
def services():
    return render_template("services.html")

# -------- CONTACT --------
@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        try:
            name = request.form.get("name")
            email = request.form.get("email")
            message = request.form.get("message")

            email_content = f"""
📩 NOUVEAU MESSAGE - FORMULAIRE CONTACT

Nom : {name}
Email : {email}

Message :
{message}
"""

            send_email(
                "📩 Nouveau message contact - BRAINCORD",
                email_content
            )

            return redirect(url_for("merci"))

        except Exception as e:
            print("ERREUR CONTACT :", e)
            return "Erreur lors de l'envoi du message. Réessayez plus tard.", 500

    return render_template("contact.html")

# -------- DEVIS --------
@app.route("/request-quote", methods=["GET", "POST"])
def request_quote():
    if request.method == "POST":
        try:
            name = request.form.get("name")
            email = request.form.get("email")
            phone = request.form.get("phone")
            project_description = request.form.get("project_description")
            budget = request.form.get("budget")

            email_content = f"""
🧾 NOUVELLE DEMANDE DE DEVIS

Nom : {name}
Email : {email}
Téléphone : {phone}
Budget : {budget}

Description du projet :
{project_description}
"""

            send_email(
                "🧾 Nouvelle demande de devis - BRAINCORD",
                email_content
            )

            return redirect(url_for("merci_devis"))

        except Exception as e:
            print("ERREUR DEVIS :", e)
            return "Erreur lors de l'envoi du devis. Réessayez plus tard.", 500

    return render_template("request_quote.html")

# -------- PAGES MERCI --------
@app.route("/merci")
def merci():
    return render_template("merci.html")

@app.route("/merci-devis")
def merci_devis():
    return render_template("merci_devis.html")

# =====================
# RUN LOCAL UNIQUEMENT
# =====================
if __name__ == "__main__":
    app.run(debug=True)
