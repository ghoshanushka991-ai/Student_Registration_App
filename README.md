# Smart Education Student Assessment Platform

A Flask-based student assessment dashboard for registering students, recording learning outcomes, and viewing progress and performance.

## Features

- Administrator login
- Student registration
- Student directory
- Module completion tracking
- Quiz score tracking
- Assignment and project status tracking
- Weighted overall progress calculation
- Performance status classification
- Responsive dashboard layout

## Requirements

- Python 3.9 or newer
- Flask

## Setup

Open PowerShell in the project folder:

```powershell
cd "C:\Users\hi\Downloads\Smart_Education_Student_Assessment_Project"

python -m venv .venv
.\.venv\Scripts\Activate.ps1

pip install flask
```

If PowerShell blocks script activation, run the following once in PowerShell as your user:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## Run the application

```powershell
python app.py
```

Open the application at:

[http://127.0.0.1:5000/login](http://127.0.0.1:5000/login)

## Demo login

- Username: `admin`
- Password: `admin123`

## Main workflow

1. Sign in with the demo administrator account.
2. Select **Register student** and enter the student's details.
3. Record modules, quiz results, assignment status, and project status.
4. Review the student's calculated progress and performance.
5. Use the Students page to browse all registered learners.

## Application routes

| Route | Purpose |
| --- | --- |
| `/` | Redirects to the dashboard or login page |
| `/login` | Administrator login |
| `/logout` | Ends the current session |
| `/dashboard` | Overview dashboard |
| `/students` | Student directory |
| `/student/new` | Register a student |
| `/assessment/<student_id>` | Add or update assessment data |
| `/student/<student_id>` | View an individual student's progress |

## Progress calculation

Overall progress is weighted as follows:

- Modules: 25%
- Quiz: 35%
- Assignment: 20%
- Project: 20%

Performance is classified as **Excellent**, **Good**, **Needs Improvement**, or **Incomplete** based on the calculated progress and completion state.

## Project structure

```text
Smart_Education_Student_Assessment_Project/
├── app.py
├── README.md
├── static/
│   └── style.css
└── templates/
    ├── assessment.html
    ├── base.html
    ├── dashboard.html
    ├── login.html
    ├── student.html
    └── students.html
```

## Data storage note

Student data is stored in the `students` dictionary in memory. Records are cleared whenever the application restarts. The login credentials and secret key are also demo values and should be moved to environment variables before production use.
