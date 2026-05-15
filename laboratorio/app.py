from flask import Flask, render_template, request, redirect
from flask import session, url_for, jsonify

app = Flask(__name__)
app.secret_key = "lab_secret_key"

USERNAME = "admin"
PASSWORD = "admin123"


@app.route("/")
def home():

    if "logged_in" in session:
        return redirect(url_for("dashboard"))

    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():

    error = None

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        if username == USERNAME and password == PASSWORD:

            session["logged_in"] = True
            session["role"] = "administrator"

            return redirect(url_for("dashboard"))

        else:
            error = "Invalid username or password"

    return render_template("login.html", error=error)


@app.route("/dashboard")
def dashboard():

    if "logged_in" not in session:
        return redirect(url_for("login"))

    return render_template(
        "dashboard.html",
        role=session.get("role")
    )


# ==========================================
# VULNERABLE ENDPOINT (LAB ONLY)
# ==========================================

@app.route("/maintenance/access")
def maintenance_access():

    auth = request.headers.get("X-Maintenance-Token")

    if auth == "VISION-2026":

        session["logged_in"] = True
        session["role"] = "administrator"

        return jsonify({
            "status": "success",
            "message": "maintenance access granted",
            "role": "administrator"
        })

    return jsonify({
        "status": "denied"
    }), 403


@app.route("/logout")
def logout():

    session.clear()
    return redirect(url_for("login"))

@app.route("/maintenance")
def maintenance():

    return """
    <!DOCTYPE html>

    <html>

    <head>
        <title>Maintenance Interface</title>
        <script src="/static/js/maintenance.js"></script>
    </head>

    </html>
    """, 403

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)