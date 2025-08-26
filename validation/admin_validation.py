import re
from datetime import datetime

def validate_name(name: str):
    if not re.match(r"^[A-Za-z ]{2,50}$", name):
        raise ValueError("Staff name must only contain alphabets and spaces (2-50 chars).")
    return name

def validate_age(age: str):
    if not age.isdigit() or not (18 <= int(age) <= 65):
        raise ValueError("Age must be a number between 18 and 65.")
    return int(age)

def validate_phone(phone: str):
    if not re.match(r"^[0-9]{10}$", phone):
        raise ValueError("Phone number must be exactly 10 digits.")
    return phone

def validate_email(email: str):
    if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email):
        raise ValueError("Invalid email format.")
    return email

def validate_date(doj: str):
    try:
        doj_date = datetime.strptime(doj, "%Y-%m-%d")
        if doj_date > datetime.today():
            raise ValueError("Date of Joining cannot be in the future.")
        return doj
    except ValueError:
        raise ValueError("Date of Joining must be in YYYY-MM-DD format.")
