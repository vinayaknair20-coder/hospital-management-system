"""
Unified Clinic Management System
Main entry point for all clinic operations
Team: Hospital Management System Development Team
"""

from db.db_connection import DBConnection
from lib.Pharmacistservices import MedicineManagementLib
from dao.staff_dao import StaffDao
from lib.admin_library import AdminLibrary
from lib.stafflibrary import StaffLibrary
from lib.labtechmanagementlib import LabtechManagementLib
from lib.PatientManagementLib import ReceptionistServices
# Uncomment these when ready:
# from lib.PatientManagementLib import ReceptionistServices
# from lib.menudriven import DoctorServices

class AdminMenu:
    def __init__(self):
        self.stafflib = StaffLibrary()
        self.admin_lib = AdminLibrary()
        # self.doctorlib = DoctorLibrary()  # Uncomment when implemented

    def show_menu(self):
        while True:
            print("\n====== ADMIN MENU ======")
            print("1. Staff Management")
            print("2. Doctor Management")
            print("3. Role Management")
            print("4. Specialization Management")
            print("5. Logout")
            choice = input("Enter your choice: ")
            if choice == "1":
                self.staff_management_menu()
            elif choice == "2":
                self.doctor_management_menu()
            elif choice == "3":
                self.role_management_menu()
            elif choice == "4":
                self.specialization_management_menu()
            elif choice == "5":
                print("Logging out...")
                break
            else:
                print("Invalid choice! Please try again.")

    def staff_management_menu(self):
        while True:
            print("\n--- Staff Management ---")
            print("1. Add Staff")
            print("2. Update Staff")
            print("3. Deactivate Staff")
            print("4. List Staff")
            print("5. Back")
            choice = input("Enter your choice: ")
            if choice == "1":
                self.stafflib.create_staff()
            elif choice == "2":
                self.stafflib.update_staff()
            elif choice == "3":
                self.stafflib.deactivate_staff()
            elif choice == "4":
                self.stafflib.list_staff()
            elif choice == "5":
                break
            else:
                print("Invalid choice!")

    def doctor_management_menu(self):
        while True:
            print("\n--- Doctor Management ---")
            print("1. Add Doctor Profile")
            print("2. Update Doctor Profile")
            print("3. Deactivate Doctor")
            print("4. List Doctors")
            print("5. Back")
            choice = input("Enter your choice: ")
            if choice in ["1", "2", "3", "4"]:
                print("🚧 Doctor management not implemented yet.")
            elif choice == "5":
                break
            else:
                print("Invalid choice!")

    def role_management_menu(self):
        while True:
            print("\n--- Role Management ---")
            print("1. Create Role")
            print("2. List Roles")
            print("3. Back")
            choice = input("Enter your choice: ")
            if choice == "1":
                self.admin_lib.create_role()
            elif choice == "2":
                self.admin_lib.list_roles()
            elif choice == "3":
                break
            else:
                print("Invalid choice!")

    def specialization_management_menu(self):
        while True:
            print("\n--- Specialization Management ---")
            print("1. Create Specialization")
            print("2. List Specializations")
            print("3. Back")
            choice = input("Enter your choice: ")
            if choice == "1":
                self.admin_lib.create_specialization()
            elif choice == "2":
                self.admin_lib.list_specialization()
            elif choice == "3":
                break
            else:
                print("Invalid choice!")

def test_database_connection():
    """Test database connection at startup"""
    try:
        conn = DBConnection().get_connection()
        print("✅ Database connected successfully!")
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def receptionist_menu():
    print("Welcome to Receptionist Dashboard")
    while True:
        print('SERVICES\n1. PATIENT\n2. APPOINTMENTS\n3. BILLING\n4. EXIT')
        choice=input('enter your choice: ')
        if choice=='1':
            while True:
                print('SERVICES\n1.ADD PATIENT\n2.DISPLAY PATIENT\n3.SEARCH PATIENT\n4.UPDATE PATIENT\n5.EXIT')
                choice=input('enter your choice: ')
                if choice=='1':
                    ReceptionistServices.add_patients()
                elif choice=='2':
                    ReceptionistServices.display_all()
                elif choice=='3':
                    ReceptionistServices.search_patient()
                elif choice =='4':
                    ReceptionistServices.update_patient()
                elif choice =='5':
                    break
                else:
                    print("Invalid Choice, Try Again !!!")
        elif choice=='2':
            ReceptionistServices.book_appointment()
        elif choice=='4':
            break
        else:
            print("Invalid Choice, try again !!!")

def patient_management_menu():
    print("\n========== PATIENT MANAGEMENT ==========")
    while True:
        print("1. ADD PATIENT")
        print("2. SEARCH PATIENT")
        print("3. DISPLAY ALL PATIENTS")
        print("4. UPDATE PATIENT")
        print("5. BACK TO RECEPTIONIST MENU")
        choice = input("Enter your choice: ").strip()
        if choice in ["1", "2", "3", "4"]:
            print("🚧 Patient management not implemented yet.")
        elif choice == "5":
            break
        else:
            print("❌ Invalid choice! Please enter 1-5.")

def doctor_menu():
    print("\n👩‍⚕️ Welcome to Doctor Dashboard")
    while True:
        print("\n========== DOCTOR SERVICES ==========")
        print("1. APPOINTMENTS")
        print("2. CONSULTATIONS")
        print("3. PRESCRIPTIONS")
        print("4. PATIENT RECORDS")
        print("5. GO TO MAIN MENU")
        choice = input("Enter your choice: ").strip()
        if choice in ["1", "2", "3", "4"]:
            print("🚧 Doctor services not implemented yet.")
        elif choice == "5":
            break
        else:
            print("❌ Invalid choice! Please enter 1-5.")

def pharmacist_menu():
    print("\n💊 Welcome to Pharmacist Dashboard")
    while True:
        print("\n========== MEDICINE MANAGEMENT MENU ==========")
        print("1. ADD MEDICINE")
        print("2. DISPLAY ALL MEDICINES")
        print("3. BACK TO MAIN MENU")
        choice = input("Enter your choice: ").strip()
        if choice == "1":
            MedicineManagementLib.insert_medicine()
        elif choice == "2":
            MedicineManagementLib.display_medicine()
        elif choice == "3":
            break
        else:
            print("❌ Invalid choice! Please enter 1-3.")


def lab_technician():
    print("Welcome to Lab_Technician Dashboard")
    while True:
        print('services\n1.ADD TEST\n2.LIST TEST\n3.EXIT')
        choice=input('enter choice: ')
        if choice=='1':
            LabtechManagementLib.create_test()
        elif choice=='2':
            LabtechManagementLib.display_all()
        elif choice=='3':
            break
        else:
            print("Try again")
     

def display_welcome_banner():
    print("=" * 50)
    print("         CLINIC MANAGEMENT SYSTEM")
    print("       Unified Healthcare Solution")
    print("   Team: Hospital Management Developers")
    print("=" * 50)

def login():
    try:
        email = input("Enter email: ")
        password = input("Enter Password: ")
        user = AdminLibrary.authenticate_user(email, password)
        if not user:
            print("❌ Invalid Username(email) or Password")
            return None
        if not user.get("is_active", True):
            print("❌ Account is deactivated. Contact Admin.")
            return None
        print(f"✅ Login successful! Welcome {user['staff_name']} ({user['role_name']})")
        return user
    except Exception as e:
        print(f"❌ Login error: {e}")
        return None

def main():
    display_welcome_banner()
    if not test_database_connection():
        print("❌ Cannot start application without database connection")
        return
    while True:
        print("\n======= CLINIC MANAGEMENT SYSTEM ==========")
        print("1. Login")
        print("2. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            user = login()
            if user:
                role = user["role_name"].lower()
                if role == "admin":
                    AdminMenu().show_menu()
                elif role == "receptionist":
                    receptionist_menu()
                elif role == "doctor":
                    doctor_menu()
                elif role == "pharmacist":
                    pharmacist_menu()
                elif role == "lab tech":
                    lab_technician()
                else:
                    print(f"❌ Role '{role}' not recognized.")
        elif choice == "2":
            print("👋 Exiting... Goodbye!")
            break
        else:
            print("❌ Invalid choice. Try again.")

if __name__ == "__main__":
    main()
