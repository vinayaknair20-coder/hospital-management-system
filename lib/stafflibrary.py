import hashlib
from dao.staff_dao import StaffDao
from validation.admin_validation import validate_name, validate_age, validate_phone, validate_email, validate_date


class StaffLibrary:
    def __init__(self):
        self.dao = StaffDao()

    def create_staff(self):
        try:
            staff_id = self.dao.get_next_staff_id()  # Auto staff ID
            staff_name = validate_name(input("Enter Staff Name: "))
            role_id = input("Enter Role ID: ")
            age = validate_age(input("Enter Age: "))
            phone_number = validate_phone(input("Enter Phone Number: "))
            email = validate_email(input("Enter Email: "))
            doj = validate_date(input("Enter Date of Joining (YYYY-MM-DD): "))

            # Auto-generate password
            default_password = (staff_name[:5].lower() + phone_number[-4:]) if phone_number else "password@123"
            password_hash = hashlib.sha256(default_password.encode()).hexdigest()

            print(f"Generated Staff ID: {staff_id}")
            print(f"Default Password : {default_password}")

            # Save staff to DB
            self.dao.add_staff(
                staff_id, staff_name, role_id, age,
                phone_number, email, doj, password_hash
            )
        except ValueError as ve:
            print(f"❌ Validation Error: {ve}")
        except Exception as e:
            print(f"❌ Unexpected Error: {e}")

    def update_staff(self):
        staff_id = input("Enter Staff ID to update: ")
        phone_number = validate_phone(input("Enter new Phone Number: "))
        email = validate_email(input("Enter new Email: "))
        self.dao.update_staff(staff_id, phone_number, email)

    def deactivate_staff(self):
        staff_id = input("Enter Staff ID to deactivate: ")
        self.dao.deactivate_staff(staff_id)

    def list_staff(self):
        staff_list = self.dao.list_staff()
        if not staff_list:
            print("⚠ No staff found.")
        else:
            print("\n--- Staff ---")
            for s in staff_list:
                print(f"ID: {s['staff_id']}, Name: {s['staff_name']}, Age: {s['age']}, "
                      f"Phone: {s['phone_number']}, Role: {s['role_id']}, Active: {s['is_active']}")
