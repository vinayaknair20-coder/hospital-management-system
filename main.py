from db.db_connection import DBConnection
from lib.Pharmacistservices import MedicineManagementLib
from dao.staff_dao import StaffDao
from lib.admin_library import AdminLibrary
from lib.stafflibrary import StaffLibrary
from lib.labtechmanagementlib import LabtechManagementLib
from lib.PatientManagementLib import ReceptionistServices
from lib.doc_managementlib import DoctorServices
from lib.Doctorlibrary import DoctorLibrary
from dao.doctorDao import DoctorDao
# Uncomment these when ready:
# from lib.PatientManagementLib import ReceptionistServices
# from lib.menudriven import DoctorServices

import sys

def safe_input(prompt: str = "") -> str:
    """Flush potential buffered keypresses on Windows, then read input."""
    if sys.platform == "win32":
        try:
            import msvcrt
            while msvcrt.kbhit():
                msvcrt.getch()
        except Exception:
            pass
    return input(prompt)

class AdminMenu:
    def __init__(self):
        self.stafflib = StaffLibrary()
        self.admin_lib = AdminLibrary()
        self.doctorlib = DoctorLibrary()  # Uncomment when implemented

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
            print("5. Search doctor by id")
            print("6. Back")

            choice = input("Enter your choice: ")

            if choice == "1":
                self.doctorlib.add_doctor()
            elif choice == "2":
                self.doctorlib.update_doctor()
            elif choice == "3":
                self.doctorlib.deactivate_doctor()
            elif choice == "4":
                self.doctorlib.list_doctors()
            elif choice == "5":
                self.doctorlib.search_doctor_by_id()       
            elif choice == "6":
                break
            else:
                print("Invalid choice!")

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
    try:
        conn = DBConnection().get_connection()
        print(" Database connected successfully!")
        return True
    except Exception as e:
        print(f" Database connection failed: {e}")
        return False

def receptionist_menu():
    print("========== Welcome to Receptionist Dashboard ==========")
    while True:
        print('============== SERVICES ================\n1. PATIENT\n2. APPOINTMENTS\n3. BILLING\n4. EXIT')
        choice=input('enter your choice: ')
        if choice=='1':
            while True:
                print('============== SERVICES ==============\n1.ADD PATIENT\n2.DISPLAY PATIENT\n3.SEARCH PATIENT\n4.UPDATE PATIENT\n5.EXIT')
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
            while True:
                print('=============== SERVICES ==============\n1.BOOK APPOINTMENT\n2.VIEW ALL APPOINTMENTS\n3.SEARCH APPOINTMENT USING PATIENT ID\n4.RESCHEDULE APPOINTMENT\n5.CANCEL APPOINTMENT\n6.EXIT')
                choice=input('enter your choice: ')
                if choice=='1':
                    ReceptionistServices.book_appointment()
                elif choice=='2':  
                    ReceptionistServices.display_all_appointments()
                elif choice=='3':
                    ReceptionistServices.search_appointment()
                elif choice=='4':
                    ReceptionistServices.reschedule_appointment()
                elif choice=='5':
                    ReceptionistServices.cancel_appointment()
                elif choice=='6':
                    break
                else:
                    print("Invalid Choice, Try Again !!!")  
        elif choice=='3':
            while True:
                print('=============== SERVICES ==============\n1.GENERATE BILL\n2.VIEW BILL\n3.EXIT')
                choice=input('enter your choice: ')
                if choice=='1':
                    ReceptionistServices.add_bill() 
                elif choice=='2':
                    ReceptionistServices.show_bill()
                elif choice=='3':
                    break
                else:
                    print("Invalid Choice, Try Again !!!")
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
            print(" Patient management not implemented yet.")
        elif choice == "5":
            break
        else:
            print(" Invalid choice! Please enter 1-5.")


def doctor_menu():
    while True:
        # clear_screen()
        print("\n Welcome to Doctor Dashboard")
        print("\n---SERVICES---")
        print("1. Appointments")
        print("2. Consultations")
        print("3. Prescriptions")
        print("4. Go to main menu")

        choice = safe_input("Enter your choice: ").strip()

        if choice == '1':
            DoctorServices.display_appointments()
            safe_input("\n✔ Press Enter to continue...")
        elif choice == '2':
            while True:
                # clear_screen()
                print("\n--- CONSULTATIONS ---")
                print("1. Create consultation")
                print("2. Display consultation by patient id")
                print("3. Display consultations of doctor")
                print("4. Go back")
                opt = safe_input("\nEnter your choice: ").strip()
                if opt == '1':
                    DoctorServices.create_new_consultation()
                    safe_input("\n✔ Press Enter to continue...")
                elif opt == '2':
                    DoctorServices.view_patient_consultation()
                    safe_input("\n✔ Press Enter to continue...")
                elif opt == '3':
                    DoctorServices.view_doctors_consultation()
                    safe_input("\n✔ Press Enter to continue...")
                elif opt == '4':
                    break
                else:
                    print("⚠ Invalid option")
                    safe_input("\nPress Enter...")
        elif choice == '3':
            while True:
                print("\n--- PRESCRIPTIONS ---")
                print("1. Add prescription")
                print("2. List prescriptions by patient id")
                print("3. Go back")
                ch = safe_input("Enter choice: ").strip()

                if ch == '1':
                    # Prescription creation menu now handles medicines/tests internally
                    DoctorServices.create_prescription_menu()
                    safe_input("\n✔ Press Enter to continue...")

                elif ch == '2':
                    # Display prescriptions by patient id
                    DoctorServices.view_prescription_by_patient_id()
                    safe_input("\n✔ Press Enter to continue...")

                elif ch == '3':
                    break

                else:
                    print("⚠ Invalid choice!!")
                    safe_input("\nPress Enter...")
        elif choice=='4':
            break
        else:
            print('invalid choice!!')




def pharmacist_menu():
    print("\nPHARMACY MANAGEMENT MENU")
    while True:
        print("\n" + "="*60)
        print("PHARMACY MANAGEMENT OPTIONS")
        print("="*60)
        print("1. Add Medicine")
        print("2. Display All Medicines")
        print("3. Update Medicine")
        print("4. Disable Medicine")
        print("5. Search Medicine By ID")
        print("6. Search Medicines By Type")
        print("7. Stock Alerts")
        print("8. Medicine Statistics")
        print("9. View Pending Prescriptions")
        print("10. Dispense Medicines")
        print("11. View Bills")
        print("12. Go To Main Menu")
        
        choice = input("Enter your choice (1-12): ").strip()
        
        try:
            if choice == "1":
                MedicineManagementLib.insert_medicine()
            elif choice == "2":
                MedicineManagementLib.display_medicine()
            elif choice == "3":
                MedicineManagementLib.update_medicine()
            elif choice == "4":
                MedicineManagementLib.disable_medicine()
            elif choice == "5":
                MedicineManagementLib.search_by_medicine_id()
            elif choice == "6":
                MedicineManagementLib.search_by_medicine_type()
            elif choice == "7":
                MedicineManagementLib.show_stock_alerts()
            elif choice == "8":
                MedicineManagementLib.show_medicine_statistics()
            elif choice == "9":
                from lib.pharmacydispenselib import PharmacyDispenseService
                PharmacyDispenseService.view_pending_prescriptions()
            elif choice == "10":
                from lib.pharmacydispenselib import PharmacyDispenseService
                PharmacyDispenseService.dispense_and_bill()
            elif choice == "11":
                from lib.pharmacydispenselib import PharmacyDispenseService
                PharmacyDispenseService.print_bill()
            elif choice == "12":
                break
            else:
                print("Invalid choice. Please enter a number between 1-12.")
        except Exception as e:
            print(f"Error in pharmacy services: {e}")




def lab_technician():
    print("Welcome to Lab_Technician Dashboard")
    while True:
        print('services\n1.ADD TEST\n2.LIST TEST\n3.SEARCH TEST\n4.UPDATE TEST\n5.DELETE TEST\n6.PRESCRIPTION VIEW\n7.ADD TEST RESULT\n8.LIST TEST RESULTS\n9.BACK')
        choice=safe_input('enter choice: ').strip()
        if choice=='1':
            LabtechManagementLib.create_test()
            safe_input("\n✔ Press Enter to continue...")
        elif choice=='2':
            LabtechManagementLib.display_all()
            safe_input("\n✔ Press Enter to continue...")
        elif choice=='3':
            LabtechManagementLib.search_by_id()
            safe_input("\n✔ Press Enter to continue...")
        elif choice=='4':
            LabtechManagementLib.update_test()
            safe_input("\n✔ Press Enter to continue...")
        elif choice=='5':
            LabtechManagementLib.disable_product()
            safe_input("\n✔ Press Enter to continue...")
        elif choice=='6':
            LabtechManagementLib.view_prescription_results()
            safe_input("\n✔ Press Enter to continue...")
        elif choice=='7':
            LabtechManagementLib.add_test_result()
            safe_input("\n✔ Press Enter to continue...")
        elif choice=='8':
            LabtechManagementLib.list_all_results()
            safe_input("\n✔ Press Enter to continue...")
        elif choice=='9':
            break
        else:
            print("Invalid choice")
     

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
            print(" Invalid Username(email) or Password")
            return None
        if not user.get("is_active", True):
            print(" Account is deactivated. Contact Admin.")
            return None
        print(f" Login successful! Welcome {user['staff_name']} ({user['role_name']})")
        return user
    except Exception as e:
        print(f" Login error: {e}")
        return None

def main():
    display_welcome_banner()
    if not test_database_connection():
        print(" Cannot start application without database connection")
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
                    ReceptionistServices.receptionist_main_menu()
                elif role == "doctor":
                    doctor_menu()
                elif role == "pharmacist":
                    pharmacist_menu()
                elif role == "lab tech":
                    lab_technician()
                else:
                    print(f" Role '{role}' not recognized.")
        elif choice == "2":
            print(" Exiting... Goodbye!")
            break
        else:
            print(" Invalid choice. Try again.")

if __name__ == "__main__":
    main()
