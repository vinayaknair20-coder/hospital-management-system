import re
from datetime import date


def validate_name(name: str) -> bool:
    # Name: no leading space, only alphabets/spaces, at least 3 characters
    if not isinstance(name, str) or not re.fullmatch(r"^(?! )[A-Za-z ]{3,}$", name.strip()):
      raise ValueError("Invalid Name. Try Again !!!")
    return True

from datetime import datetime

def validate_blood_group(blood_group: str) -> bool:
    """Validate blood group with case sensitivity (only exact match allowed)."""
    valid_blood_groups = ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"]
    if blood_group not in valid_blood_groups:   # Case-sensitive check
        raise ValueError(f"Blood group must be one of {valid_blood_groups} !!!.")
    return True

from datetime import datetime

def validate_DOB(dob: str) -> str:
    try:
        # Expect input in YYYY/MM/DD format
        dob_date = datetime.strptime(dob, "%Y/%m/%d").date()
        if dob_date > datetime.today().date():
            raise ValueError("DOB cannot be in the future.")
        return dob_date.strftime("%Y-%m-%d")  # MySQL format
    except:
        raise ValueError("Invalid DOB. Use YYYY/MM/DD.")



def validate_age(age: int) -> bool:
    # Age: must be integer between 1 and 120
    if not (isinstance(age, int) and 1 <= age <= 120):
        raise ValueError("Invalid Age . Try Again!!!")
    return True

def validate_gender(gender: str) -> bool:
    if gender not in ["M", "F", "O"]:
        raise ValueError("Gender must be 'M', 'F', or 'O'!!!.")
    return True

def validate_blood_group(blood_group: str) -> bool:
    valid_blood_groups = ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-" ]
    if blood_group not in valid_blood_groups:
        raise ValueError(f"Blood group must be one of {valid_blood_groups} !!!.")
    return True

def validate_phone_number(phone: str) -> bool:
    # Phone number: 10 digits, starts with 6/7/8/9
    if not (isinstance(phone, str) and phone.isdigit() and len(phone) == 10 and phone[0] in "6789"):
        raise ValueError("Phone number must be 10 digits and start with 6, 7, 8, or 9.!!!")
    return True

def validate_email(email: str) -> bool:
    # Only Gmail addresses allowed
    if not re.fullmatch(r"[a-zA-Z0-9._%+-]+@gmail\.com", email):
        raise ValueError("Email must be a valid Gmail address (example@gmail.com).!!!!")
    return True

def validate_address(address: str) -> bool:
    if not (isinstance(address, str) and len(address.strip()) >= 3):
        raise ValueError("Address must be at least 3 characters long.!!!!")
    return True

def validate_emergency_contact(contact: str) -> bool:
    if not (isinstance(contact, str) and contact.isdigit() and len(contact) == 10 and contact[0] in "6789"):
        raise ValueError("Emergency contact must be 10 digits and start with 6, 7, 8, or 9.!!!!")
    return True


