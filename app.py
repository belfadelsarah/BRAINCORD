from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route("/", endpoint="home")
def home():
    return render_template("index.html")

@app.route("/services", endpoint="services")
def services():
    return render_template("services.html")

@app.route("/contact", methods=["GET", "POST"], endpoint="contact")
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")

        print("CONTACT:", name, email, message)

        return redirect(url_for("merci"))

    return render_template("contact.html")

@app.route("/merci", endpoint="merci")
def merci():
    return render_template("merci.html")

@app.route("/request_quote", methods=["GET", "POST"], endpoint="request_quote")
def request_quote():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        project_description = request.form.get("project_description")
        budget = request.form.get("budget")

        print("DEVIS:", name, email, phone, budget, project_description)

        return redirect(url_for("merci_devis"))

    return render_template("request_quote.html")

@app.route("/merci-devis", endpoint="merci_devis")
def merci_devis():
    return render_template("merci_devis.html")

if __name__ == "__main__":
    app.run(debug=True)
