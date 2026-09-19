from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = "smart-education-demo-key"

# In-memory storage (no database required)
students = {}

USERNAME = "admin"
PASSWORD = "admin123"


def calculate_progress(student):
    """
    Overall progress:
    Modules = 25%
    Quiz = 35%
    Assignment = 20%
    Project = 20%
    """

    module_pct = (
        (student["modules_completed"] / student["total_modules"]) * 100
        if student["total_modules"]
        else 0
    )

    quiz_pct = (
        (student["quiz_score"] / student["quiz_total"]) * 100
        if student["quiz_total"]
        else 0
    )

    assignment_pct = (
        100 if student["assignment_status"] == "Completed" else 0
    )

    project_pct = (
        100 if student["project_status"] == "Completed" else 0
    )

    overall = (
        (module_pct * 0.25)
        + (quiz_pct * 0.35)
        + (assignment_pct * 0.20)
        + (project_pct * 0.20)
    )

    return round(overall, 2)


def performance_status(progress, complete=False):

    if complete:
        if progress >= 85:
            return "Excellent"
        elif progress >= 70:
            return "Good"
        else:
            return "Needs Improvement"

    if progress >= 85:
        return "Excellent"
    elif progress >= 70:
        return "Good"
    elif progress > 0:
        return "Needs Improvement"
    else:
        return "Incomplete"


def enrich(student):

    student = dict(student)

    # Module percentage
    if student["total_modules"]:
        student["module_percentage"] = round(
            student["modules_completed"]
            / student["total_modules"]
            * 100,
            2
        )
    else:
        student["module_percentage"] = 0

    # Quiz percentage
    if student["quiz_total"]:
        student["quiz_percentage"] = round(
            student["quiz_score"]
            / student["quiz_total"]
            * 100,
            2
        )
    else:
        student["quiz_percentage"] = 0

    # Overall progress
    student["overall_progress"] = calculate_progress(student)

    # Performance status
    complete = (
        student["modules_completed"] == student["total_modules"]
        and student["assignment_status"] == "Completed"
        and student["project_status"] == "Completed"
    )

    student["performance"] = performance_status(
        student["overall_progress"],
        complete
    )

    return student


# ---------------- HOME ----------------

@app.route("/")
def index():

    if "user" in session:
        return redirect(url_for("dashboard"))

    return redirect(url_for("login"))


# ---------------- LOGIN ----------------

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if username == USERNAME and password == PASSWORD:

            session["user"] = username

            return redirect(url_for("dashboard"))

        flash(
            "Invalid username or password. Please try again.",
            "error"
        )

    return render_template("login.html")


# ---------------- LOGOUT ----------------

@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login"))


# ---------------- DASHBOARD ----------------

@app.route("/dashboard")
def dashboard():

    if "user" not in session:
        return redirect(url_for("login"))

    data = [
        enrich(student)
        for student in students.values()
    ]

    return render_template(
        "dashboard.html",
        students=data
    )


# ---------------- STUDENT LIST ----------------

@app.route("/students")
def student_list():

    if "user" not in session:
        return redirect(url_for("login"))

    data = [
        enrich(student)
        for student in students.values()
    ]

    return render_template(
        "students.html",
        students=data
    )


# ---------------- STUDENT REGISTRATION ----------------

@app.route("/student/new", methods=["GET", "POST"])
def student():

    if "user" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":

        name = request.form.get("name", "").strip()
        student_id = request.form.get("student_id", "").strip()
        email = request.form.get("email", "").strip()
        phone = request.form.get("phone", "").strip()
        course = request.form.get("course", "").strip()

        # Required field validation
        if not all([
            name,
            student_id,
            email,
            phone,
            course
        ]):

            flash(
                "All registration fields are required.",
                "error"
            )

            return render_template("student.html")

        # Duplicate student ID
        if student_id in students:

            flash(
                "Student ID already exists. Please use a unique ID.",
                "error"
            )

            return render_template("student.html")

        # Email validation
        if (
            "@" not in email
            or "." not in email.split("@")[-1]
        ):

            flash(
                "Please enter a valid email address.",
                "error"
            )

            return render_template("student.html")

        # Phone validation
        if not phone.isdigit() or not (7 <= len(phone) <= 15):

            flash(
                "Phone number must contain 7–15 digits.",
                "error"
            )

            return render_template("student.html")

        # Store student
        students[student_id] = {

            "name": name,
            "student_id": student_id,
            "email": email,
            "phone": phone,
            "course": course,

            "total_modules": 10,
            "modules_completed": 0,

            "quiz_score": 0,
            "quiz_total": 100,

            "assignment_status": "Pending",
            "project_status": "Pending",
        }

        flash(
            "Student registered successfully. "
            "Now record the assessment.",
            "success"
        )

        return redirect(
            url_for(
                "assessment",
                student_id=student_id
            )
        )

    return render_template("student.html")


# ---------------- ASSESSMENT ----------------

@app.route(
    "/assessment/<student_id>",
    methods=["GET", "POST"]
)
def assessment(student_id):

    if "user" not in session:
        return redirect(url_for("login"))

    # Check student
    if student_id not in students:

        flash(
            "Student not found.",
            "error"
        )

        return redirect(url_for("student_list"))

    student_data = students[student_id]

    if request.method == "POST":

        try:

            modules_completed = int(
                request.form.get(
                    "modules_completed",
                    ""
                )
            )

            quiz_score = float(
                request.form.get(
                    "quiz_score",
                    ""
                )
            )

            quiz_total = float(
                request.form.get(
                    "quiz_total",
                    ""
                )
            )

        except ValueError:

            flash(
                "Modules and quiz values must be numeric.",
                "error"
            )

            return render_template(
                "assessment.html",
                student=enrich(student_data)
            )

        # Module validation
        if not (
            0
            <= modules_completed
            <= student_data["total_modules"]
        ):

            flash(
                f"Modules completed must be between 0 "
                f"and {student_data['total_modules']}.",
                "error"
            )

            return render_template(
                "assessment.html",
                student=enrich(student_data)
            )

        # Quiz validation
        if (
            quiz_total <= 0
            or quiz_score < 0
            or quiz_score > quiz_total
        ):

            flash(
                "Quiz score must be non-negative "
                "and cannot exceed the quiz total.",
                "error"
            )

            return render_template(
                "assessment.html",
                student=enrich(student_data)
            )

        # Assignment and project status
        assignment = request.form.get(
            "assignment_status"
        )

        project = request.form.get(
            "project_status"
        )

        if (
            assignment not in {
                "Pending",
                "Completed"
            }
            or project not in {
                "Pending",
                "Completed"
            }
        ):

            flash(
                "Please select valid assignment "
                "and project statuses.",
                "error"
            )

            return render_template(
                "assessment.html",
                student=enrich(student_data)
            )

        # Update student assessment
        student_data.update({

            "modules_completed": modules_completed,

            "quiz_score": quiz_score,

            "quiz_total": quiz_total,

            "assignment_status": assignment,

            "project_status": project,
        })

        flash(
            "Assessment updated successfully.",
            "success"
        )

        return redirect(
            url_for(
                "student_progress",
                student_id=student_id
            )
        )

    return render_template(
        "assessment.html",
        student=enrich(student_data)
    )


# ---------------- INDIVIDUAL STUDENT PROGRESS ----------------

@app.route("/student/<student_id>")
def student_progress(student_id):

    if "user" not in session:
        return redirect(url_for("login"))

    if student_id not in students:

        flash(
            "Student not found.",
            "error"
        )

        return redirect(url_for("student_list"))

    return render_template(
        "dashboard.html",
        student=enrich(students[student_id]),
        students=[]
    )


# ---------------- RUN APPLICATION ----------------
if __name__ == "__main__":
    print("APP STARTING...")
    app.run(debug=False)