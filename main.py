"""
Unified Clinic Management System
Main entry point for all clinic operations
Team: Hospital Management System Development Team
"""

from db.db_connection import DBConnection
from lib.Pharmacistservices import MedicineManagementLib

# from lib.PatientManagementLib import ReceptionistServices  
# from lib.menudriven import DoctorServices
# from lib.labtechmanagementlib import LabtechManagementLib
# import sys
# import getpass


def test_database_connection():
    """Test database connection at startup"""
    try:
        conn = DBConnection().get_connection()
        print("✅ Database connected successfully!")
        conn.close()
        return True
    except Exception as e:
        print(f" Database connection failed: {e}")
        return False


def admin_menu():
    """Admin Dashboard - System Administration"""
    print("\n Welcome to Admin Dashboard")
    while True:
        print("\n========== ADMIN MENU ==========")
        print("1. USER MANAGEMENT")
        print("2. SYSTEM REPORTS")
        print("3. DATABASE BACKUP")
        print("4. SYSTEM SETTINGS")
        print("5. GO TO MAIN MENU")
        
        choice = input("Enter your choice: ").strip()
        
        if choice == "1":
            print(" User Management - Coming Soon...")
        elif choice == "2":
            print(" System Reports - Coming Soon...")
        elif choice == "3":
            print(" Database Backup - Coming Soon...")
        elif choice == "4":
            print(" System Settings - Coming Soon...")
        elif choice == "5":
            break
        else:
            print(" Invalid choice! Please enter 1-5.")


def receptionist_menu():
    """Receptionist Dashboard - Patient & Appointment Management"""
    print("\n👩 Welcome to Receptionist Dashboard")
    while True:
        print("\n========== RECEPTIONIST SERVICES ==========")
        print("1. PATIENT MANAGEMENT")
        print("2. APPOINTMENTS")
        print("3. BILLING")
        print("4. GO TO MAIN MENU")
        
        choice = input("Enter your choice: ").strip()
        
        if choice == "1":
            patient_management_menu()
        elif choice == "2":
            try:
                ReceptionistServices.book_appointment()
            except Exception as e:
                print(f" Error with appointments: {e}")
        elif choice == "3":
            print(" Billing System - Coming Soon...")
        elif choice == "4":
            break
        else:
            print("❌ Invalid choice! Please enter 1-4.")


def patient_management_menu():
    """Patient Management Sub-menu"""
    while True:
        print("\n========== PATIENT MANAGEMENT ==========")
        print("1. ADD PATIENT")
        print("2. SEARCH PATIENT")
        print("3. DISPLAY ALL PATIENTS")
        print("4. UPDATE PATIENT")
        print("5. BACK TO RECEPTIONIST MENU")
        
        choice = input("Enter your choice: ").strip()
        
        try:
            if choice == "1":
                ReceptionistServices.add_patients()
            elif choice == "2":
                ReceptionistServices.search_patient()
            elif choice == "3":
                ReceptionistServices.display_all()
            elif choice == "4":
                ReceptionistServices.update_patient()
            elif choice == "5":
                break
            else:
                print(" Invalid choice! Please enter 1-5.")
        except Exception as e:
            print(f" Error in patient management: {e}")


def doctor_menu():
    """Doctor Dashboard - Medical Services"""
    print("\n Welcome to Doctor Dashboard")
    while True:
        print("\n========== DOCTOR SERVICES ==========")
        print("1. APPOINTMENTS")
        print("2. CONSULTATIONS")
        print("3. PRESCRIPTIONS")
        print("4. PATIENT RECORDS")
        print("5. GO TO MAIN MENU")
        
        choice = input("Enter your choice: ").strip()
        
        try:
            if choice == "1":
                DoctorServices.display_appointments()
            elif choice == "2":
                print(" Consultations - Coming Soon...")
            elif choice == "3":
                print(" Prescriptions - Coming Soon...")
            elif choice == "4":
                print(" Patient Records - Coming Soon...")
            elif choice == "5":
                break
            else:
                print(" Invalid choice! Please enter 1-5.")
        except Exception as e:
            print(f" Error in doctor services: {e}")


def pharmacist_menu():
    """Pharmacist Dashboard - Medicine & Inventory Management"""
    print("\n Welcome to Pharmacist Dashboard")
    while True:
        print("\n========== PRODUCT MANAGEMENT MENU ==========")
        print("1. ADD MEDICINE")
        print("2. DISPLAY ALL MEDICINES")
        print("3. UPDATE MEDICINE")
        print("4. DELETE MEDICINE")
        print("5. SEARCH MEDICINE")
        # print("6. LOW STOCK ALERTS")
        # print("7. EXPIRY ALERTS")
        # print("8. GO TO MAIN MENU")

        choice = input("Enter your choice: ").strip()
        
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
                print(" Low Stock Alerts - Coming Soon...")
            elif choice == "7":
                print(" Expiry Alerts - Coming Soon...")
            elif choice == "8":
                break
            else:
                print(" Invalid choice! Please enter 1-2.")
        except Exception as e:
            print(f" Error in pharmacy services: {e}")


def lab_technician_menu():
    """Lab Technician Dashboard - Test Management"""
    print("\n Welcome to Lab Technician Dashboard")
    while True:
        print("\n========== LAB SERVICES ==========")
        print("1. ADD TEST")
        print("2. DISPLAY ALL TESTS")
        print("3. UPDATE TEST RESULTS")
        print("4. SEARCH TESTS")
        print("5. GENERATE REPORTS")
        print("6. GO TO MAIN MENU")
        
        choice = input("Enter your choice: ").strip()
        
        try:
            if choice == "1":
                LabtechManagementLib.create_test()
            elif choice == "2":
                LabtechManagementLib.display_all()
            elif choice == "3":
                print(" Update Test Results - Coming Soon...")
            elif choice == "4":
                print(" Search Tests - Coming Soon...")
            elif choice == "5":
                print(" Generate Reports - Coming Soon...")
            elif choice == "6":
                break
            else:
                print(" Invalid choice! Please enter 1-6.")
        except Exception as e:
            print(f" Error in lab services: {e}")


def display_welcome_banner():
    """Display welcome banner"""
    print("=" * 50)
    print(" CLINIC MANAGEMENT SYSTEM")
    print("   Unified Healthcare Solution")
    print("   Team: Hospital Management Developers")
    print("=" * 50)


def main():
    """Main application entry point"""
    display_welcome_banner()
    
    # Test database connection
    if not test_database_connection():
        print(" Cannot start application without database connection.")
        return
    
    while True:
        try:
            print("\n======= CLINIC MANAGEMENT SYSTEM ==========")
            print("1.  ADMIN")
            print("2.  RECEPTIONIST") 
            print("3.  DOCTOR")
            print("4.  PHARMACIST")
            print("5.  LAB TECHNICIAN")
            print("6.  EXIT")
            print("=" * 45)

            choice = input("Enter your choice (1-6): ").strip()

            if choice == "1":
                admin_menu()
            elif choice == "2":
                receptionist_menu()
            elif choice == "3":
                doctor_menu()
            elif choice == "4":
                pharmacist_menu()
            elif choice == "5":
                lab_technician_menu()
            elif choice == "6":
                print(" Thank you for using Clinic Management System!")
                print(" Saving data and closing connections...")
                break
            else:
                print(" Invalid option! Please enter a number between 1-6.")
                
        except KeyboardInterrupt:
            print("\n System interrupted by user.")
            print(" Goodbye!")
            break
        except Exception as e:
            print(f" System error: {e}")
            print(" Restarting main menu...")


if __name__ == "__main__":
    main()
