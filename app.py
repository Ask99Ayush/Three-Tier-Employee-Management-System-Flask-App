from flask import Flask, render_template, request, redirect, url_for, flash
from dotenv import load_dotenv
import os
import json
import redis


from database.mongo import (
    get_all_employees,
    get_employee_by_id,
    create_employee,
    update_employee,
    delete_employee
)


load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")


if not app.secret_key:

    raise RuntimeError("SECRET_KEY must be set in the .env file")


redis_client = redis.Redis(
    host="redis",
    port=6379,
    decode_responses=True 
)


@app.route("/")
def index():
    """
    Home Page
    - Shows list of employees
    - Uses Redis cache (employees:all)
    """

    cache_key = "employees:all"

    #Check Redis first (CACHE HIT)
    cached_data = redis_client.get(cache_key)
    if cached_data:
        print("Redis Cache HIT: employees list")
        employees = json.loads(cached_data)

    #Cache MISS → Query MongoDB → Store in Redis
    else:
        print("Redis Cache MISS: employees list")
        employees = get_all_employees()

        redis_client.setex(
            cache_key,
            60,  # TTL = 60 seconds
            json.dumps(employees)
        )

    return render_template("index.html", employees=employees)


@app.route("/add", methods=["GET", "POST"])
def add_employee():
    """
    Add New Employee
    - NO caching for POST
    - Invalidate employee list cache after insert
    """

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

        # Write to database
        create_employee(employee_data)

        # Cache Invalidation
        # Employee list has changed
        redis_client.delete("employees:all")

        flash("Employee added successfully!", "success")
        return redirect(url_for("index"))

    return render_template("add.html")


@app.route("/edit/<employee_id>", methods=["GET", "POST"])
def edit_employee(employee_id):
    """
    Edit Employee
    - GET: Cache employee by ID
    - POST: Update DB + invalidate related cache
    """

    cache_key = f"employee:{employee_id}"

    #Try Redis for employee details
    cached_data = redis_client.get(cache_key)
    if cached_data:
        print(f"Redis Cache HIT: employee {employee_id}")
        employee = json.loads(cached_data)
    else:
        print(f"Redis Cache MISS: employee {employee_id}")
        employee = get_employee_by_id(employee_id)

        if employee:
            redis_client.setex(
                cache_key,
                120,  # TTL = 120 seconds
                json.dumps(employee)
            )

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

        # Update database
        update_employee(employee_id, updated_data)

        #Cache Invalidation
        redis_client.delete("employees:all")              # list cache
        redis_client.delete(f"employee:{employee_id}")    # single employee cache

        flash("Employee updated successfully!", "success")
        return redirect(url_for("index"))

    return render_template("edit.html", employee=employee)


@app.route("/delete/<employee_id>")
def delete_employee_route(employee_id):
    """
    Delete Employee
    - Remove from DB
    - Invalidate list + individual cache
    """

    delete_employee(employee_id)

    #Cache Invalidation
    redis_client.delete("employees:all")
    redis_client.delete(f"employee:{employee_id}")

    flash("Employee deleted successfully!", "success")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",   # Required for Docker
        port=5000,
        debug=os.getenv("FLASK_DEBUG") == "True"
    )