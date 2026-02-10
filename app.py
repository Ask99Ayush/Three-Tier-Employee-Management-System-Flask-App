from flask import Flask, render_template, request, redirect, url_for, flash
from dotenv import load_dotenv
import os

from database.mongo import (
    get_all_employees,
    get_employee_by_id,
    create_employee,
    update_employee,
    delete_employee
)

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

if not app.secret_key:
    raise RuntimeError("SECRET_KEY must be set in the .env file")



# Routes (Application Layer)
@app.route("/")
def index():
    employees = get_all_employees()
    return render_template("index.html", employees=employees)


@app.route("/add", methods=["GET", "POST"])
def add_employee():
    if request.method == "POST":
        employee_data = {
            "full_name": request.form.get("full_name"),
            "email": request.form.get("email"),
            "department": request.form.get("department"),
            "role": request.form.get("role"),
            "salary": request.form.get("salary"),
            "date_of_joining": request.form.get("date_of_joining"),
            "status": request.form.get("status"),
        }

        create_employee(employee_data)
        flash("Employee added successfully!", "success")
        return redirect(url_for("index"))

    return render_template("add.html")


@app.route("/edit/<employee_id>", methods=["GET", "POST"])
def edit_employee(employee_id):
    employee = get_employee_by_id(employee_id)

    if not employee:
        flash("Employee not found", "error")
        return redirect(url_for("index"))

    if request.method == "POST":
        updated_data = {
            "full_name": request.form.get("full_name"),
            "email": request.form.get("email"),
            "department": request.form.get("department"),
            "role": request.form.get("role"),
            "salary": request.form.get("salary"),
            "date_of_joining": request.form.get("date_of_joining"),
            "status": request.form.get("status"),
        }

        update_employee(employee_id, updated_data)
        flash("Employee updated successfully!", "success")
        return redirect(url_for("index"))

    return render_template("edit.html", employee=employee)


@app.route("/delete/<employee_id>")
def delete_employee_route(employee_id):
    delete_employee(employee_id)
    flash("Employee deleted successfully!", "success")
    return redirect(url_for("index"))


# Application Entry Point
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=os.getenv("FLASK_DEBUG") == "True"
    )