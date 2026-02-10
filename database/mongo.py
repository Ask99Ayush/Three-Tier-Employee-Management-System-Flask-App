from pymongo import MongoClient
from bson.objectid import ObjectId
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Read environment variables
MONGO_URI = os.getenv("MONGO_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME")

if not MONGO_URI or not DATABASE_NAME:
    raise RuntimeError("MONGO_URI and DATABASE_NAME must be set in the .env file")

# Create MongoDB client
client = MongoClient(MONGO_URI)

# Select database
db = client[DATABASE_NAME]

# Reusable collection object
employees_collection = db["employees"]


# ========================
# CRUD Helper Functions
# ========================

def get_all_employees():
    """Fetch all employees from the database"""
    return list(employees_collection.find())


def get_employee_by_id(employee_id):
    """Fetch a single employee by ObjectId"""
    return employees_collection.find_one({"_id": ObjectId(employee_id)})


def create_employee(employee_data):
    """Insert a new employee record"""
    return employees_collection.insert_one(employee_data)


def update_employee(employee_id, updated_data):
    """Update an existing employee record"""
    return employees_collection.update_one(
        {"_id": ObjectId(employee_id)},
        {"$set": updated_data}
    )


def delete_employee(employee_id):
    """Delete an employee record"""
    return employees_collection.delete_one(
        {"_id": ObjectId(employee_id)}
    )