from db.db_connection import DBConnection
from lib.Pharmacistservices import MedicineManagementLib

def test_database_connection():
    try:
        conn = DBConnection().get_connection()
        print("Database connected successfully!")
        conn.close()
        return True
    except Exception as e:
        print(f"Database connection failed: {e}")
        return False

def admin_menu():
    print("Welcome to Admin Dashboard")
    while True:
        print("\n========== ADMIN MENU ==========")
        print("1. USER MANAGEMENT")
        print("2. SYSTEM REPORTS")
        print("3. DATABASE BACKUP")
        print("4. SYSTEM SETTINGS")
        print("5. GO TO MAIN MENU")
        choice = input("Enter your choice: ").strip()
        if choice == "5":
            break
        print("Coming Soon...")

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
        # print("6. Search Medicines By Type")
        print("6. Stock Alerts")
        print("7. Medicine Statistics")
        print("8. Go To Main Menu")
        choice = input("Enter your choice (1-9): ").strip()
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
            # elif choice == "6":
            #     MedicineManagementLib.search_by_medicine_type()
            elif choice == "6":
                MedicineManagementLib.show_stock_alerts()
            elif choice == "7":
                MedicineManagementLib.show_medicine_statistics()
            elif choice == "8":
                break
            else:
                print("Invalid choice. Please enter a number between 1-9.")
        except Exception as e:
            print("Error in pharmacy services:", e)

def display_welcome_banner():
    print("=" * 45)
    print("CLINIC MANAGEMENT SYSTEM")
    print("Unified Healthcare Solution")
    print("=" * 45)

def main():
    display_welcome_banner()
    if not test_database_connection():
        print("Cannot start application without database connection.")
        return
    while True:
        print("\n======= MAIN MENU ==========")
        print("1. Admin")
        print("2. Pharmacist")
        print("3. Exit")
        print("=" * 30)
        choice = input("Enter your choice (1-3): ").strip()
        try:
            if choice == "1":
                admin_menu()
            elif choice == "2":
                pharmacist_menu()
            elif choice == "3":
                print("Thank you for using Clinic Management System!")
                break
            else:
                print("Invalid option! Please enter 1-3.")
        except KeyboardInterrupt:
            print("\nSystem interrupted by user.\nGoodbye!")
            break

if __name__ == "__main__":
    main()
