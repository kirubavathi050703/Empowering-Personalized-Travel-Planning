from flask import Flask, request, render_template, redirect, url_for
import sqlite3

app = Flask(__name__)

# ---------- DATABASE ----------
def init_db():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    # Trips table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS trips (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        start_date TEXT,
        end_date TEXT
    )
    """)

    # Activities table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS activities (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        trip_id INTEGER,
        city TEXT,
        activity TEXT,
        cost INTEGER
    )
    """)

    conn.commit()
    conn.close()

init_db()

# ---------- ROUTES ----------

# 🔹 HOME
@app.route("/")
def home():
    return redirect("/login")


# 🔹 LOGIN PAGE (FAKE LOGIN FOR HACKATHON)
@app.route("/login")
def login():
    return render_template("login.html")


# 🔹 DASHBOARD
@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


# 🔹 SHOW CREATE TRIP PAGE
@app.route("/create-trip-page")
def create_trip_page():
    return render_template("create_trip.html")


# 🔹 CREATE TRIP
@app.route("/create-trip", methods=["POST"])
def create_trip():
    name = request.form["name"]
    start = request.form["start"]
    end = request.form["end"]

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO trips (name, start_date, end_date) VALUES (?,?,?)",
        (name, start, end)
    )
    conn.commit()
    conn.close()

    return redirect("/view-trips")


# 🔹 SHOW ADD ACTIVITY PAGE
@app.route("/add-activity-page")
def add_activity_page():
    return render_template("add_activity.html")


# 🔹 ADD ACTIVITY
@app.route("/add-activity", methods=["POST"])
def add_activity():
    trip_id = request.form["trip_id"]
    city = request.form["city"]
    activity = request.form["activity"]
    cost = request.form["cost"]

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO activities (trip_id, city, activity, cost) VALUES (?,?,?,?)",
        (trip_id, city, activity, cost)
    )
    conn.commit()
    conn.close()

    return redirect("/view-trips")


# 🔹 VIEW ALL TRIPS
@app.route("/view-trips")
def view_trips():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM trips")
    trips = cur.fetchall()

    trips_with_budget = []
    for trip in trips:
        trip_id, name, start_date, end_date = trip
        cur.execute("SELECT SUM(cost) FROM activities WHERE trip_id=?", (trip_id,))
        total_budget = cur.fetchone()[0] or 0

        trips_with_budget.append({
            "id": trip_id,
            "name": name,
            "start_date": start_date,
            "end_date": end_date,
            "budget": total_budget
        })

    conn.close()
    return render_template("view_trips.html", trips=trips_with_budget)


# 🔹 ITINERARY PAGE
@app.route("/itinerary/<int:trip_id>")
def itinerary(trip_id):
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("SELECT city, activity, cost FROM activities WHERE trip_id=?", (trip_id,))
    activities = cur.fetchall()
    conn.close()

    return render_template("itinerary.html", activities=activities)


# ---------- RUN ----------
if __name__ == "__main__":
    app.run(debug=True)
