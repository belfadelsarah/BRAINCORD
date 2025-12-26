from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route("/", endpoint="home")
def home():
    return render_template("index.html")

@app.route("/services", endpoint="services")
def services():
    return render_template("services.html")

@app.route("/contact", endpoint="contact")
def contact():
    return render_template("contact.html")

@app.route("/request_quote", endpoint="request_quote")
def request_quote():
    return render_template("request_quote.html")

if __name__ == "__main__":
    app.run(debug=True)