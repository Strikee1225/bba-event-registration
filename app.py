from flask import Flask, render_template, jsonify, request, redirect, url_for
from bson.objectid import ObjectId
from database import events_collection, registrations_collection, messages_collection

app = Flask(__name__)


# =========================
# HOME PAGE
# =========================

@app.route("/")
def home():
    return render_template("index.html")


# =========================
# EVENTS PAGE
# =========================

@app.route("/events")
def events():

    try:
        event_list = list(events_collection.find())

    except Exception:
        event_list = [
            {
                "_id": "1",
                "title": "BBA Business Seminar",
                "category": "Seminar",
                "date": "25 September 2026",
                "time": "10:00 AM",
                "location": "BBA Building",
                "description": "A business seminar for BBA students."
            },
            {
                "_id": "2",
                "title": "BBA Sports Day",
                "category": "Activity",
                "date": "30 September 2026",
                "time": "9:00 AM",
                "location": "University Sports Center",
                "description": "A fun sports activity for BBA students."
            },
            {
                "_id": "3",
                "title": "Marketing Workshop",
                "category": "Workshop",
                "date": "5 October 2026",
                "time": "1:00 PM",
                "location": "BBA Building",
                "description": "A practical workshop about marketing and business."
            }
        ]

    return render_template("events.html", events=event_list)


# =========================
# EVENT DETAIL
# =========================

@app.route("/event/<event_id>")
def event_detail(event_id):

    events = [
        {
            "_id": "1",
            "title": "BBA Business Seminar",
            "category": "Seminar",
            "date": "25 September 2026",
            "time": "10:00 AM",
            "location": "BBA Building",
            "description": "A business seminar for BBA students."
        },
        {
            "_id": "2",
            "title": "BBA Sports Day",
            "category": "Activity",
            "date": "30 September 2026",
            "time": "9:00 AM",
            "location": "University Sports Center",
            "description": "A fun sports activity for BBA students."
        },
        {
            "_id": "3",
            "title": "Marketing Workshop",
            "category": "Workshop",
            "date": "5 October 2026",
            "time": "1:00 PM",
            "location": "BBA Building",
            "description": "A practical workshop about marketing and business."
        }
    ]

    event = next(
        (e for e in events if e["_id"] == event_id),
        None
    )

    if event is None:
        return "Event not found", 404

    return render_template("event.html", event=event)


# =========================
# REGISTER
# =========================

@app.route("/register/<event_id>", methods=["GET", "POST"])
def register(event_id):

    events = [
        {
            "_id": "1",
            "title": "BBA Business Seminar",
            "category": "Seminar",
            "date": "25 September 2026",
            "time": "10:00 AM",
            "location": "BBA Building"
        },
        {
            "_id": "2",
            "title": "BBA Sports Day",
            "category": "Activity",
            "date": "30 September 2026",
            "time": "9:00 AM",
            "location": "University Sports Center"
        },
        {
            "_id": "3",
            "title": "Marketing Workshop",
            "category": "Workshop",
            "date": "5 October 2026",
            "time": "1:00 PM",
            "location": "BBA Building"
        }
    ]

    event = next(
        (e for e in events if e["_id"] == event_id),
        None
    )

    if event is None:
        return "Event not found", 404

    if request.method == "POST":

        registration = {
            "event_id": event_id,
            "event_title": event["title"],
            "name": request.form["name"],
            "student_id": request.form["student_id"],
            "email": request.form["email"],
            "phone": request.form["phone"]
        }

        # Try to save registration to MongoDB
        try:
            registrations_collection.insert_one(registration)
        except Exception as e:
            print("MongoDB registration error:", e)

        return render_template(
            "registration_success.html",
            event=event
        )

    return render_template(
        "register.html",
        event=event
    )


# =========================
# REGISTRATION SUCCESS
# =========================

@app.route("/registration-success")
def registration_success():

    return render_template(
        "registration_success.html"
    )


# =========================
# MY REGISTRATIONS
# =========================

@app.route("/my-registrations", methods=["GET", "POST"])
def my_registrations():

    registrations = []

    if request.method == "POST":

        student_id = request.form["student_id"]

        try:
            registrations = list(
                registrations_collection.find({
                    "student_id": student_id
                })
            )
        except Exception as e:
            print("MongoDB error:", e)

    return render_template(
        "my_registrations.html",
        registrations=registrations
    )


# =========================
# CANCEL REGISTRATION
# =========================

@app.route("/cancel-registration/<registration_id>", methods=["POST"])
def cancel_registration(registration_id):

    try:

        registrations_collection.delete_one({
            "_id": ObjectId(registration_id)
        })

        return redirect(url_for("my_registrations"))

    except Exception as e:

        return f"Error: {e}", 500


# =========================
# ABOUT
# =========================

@app.route("/about")
def about():

    return render_template("about.html")


# =========================
# CONTACT
# =========================

@app.route("/contact", methods=["GET", "POST"])
def contact():

    if request.method == "POST":

        message = {
            "name": request.form["name"],
            "email": request.form["email"],
            "message": request.form["message"]
        }

        try:
            messages_collection.insert_one(message)
        except Exception as e:
            print("MongoDB message error:", e)

        return """
        <script>
            alert("Message sent successfully!");
            window.location.href = "/contact";
        </script>
        """

    return render_template("contact.html")


# =========================
# API - GET EVENTS
# =========================

@app.route("/api/events")
def get_events():

    try:

        events = list(
            events_collection.find(
                {},
                {"_id": 0}
            )
        )

        return jsonify(events)

    except Exception:

        return jsonify([])


# =========================
# RUN FLASK
# =========================

if __name__ == "__main__":
    app.run(debug=True)
