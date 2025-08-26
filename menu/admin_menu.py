from lib.stafflibrary import StaffLibrary
from lib.admin_library import AdminLibrary



class AdminMenu:
    def __init__(self):
        self.stafflib = StaffLibrary()
        #self.doctorlib = DoctorLibrary()
        self.admin_lib = AdminLibrary()

    def show_menu(self):
        while True:
            print("\n====== ADMIN MENU ======")
            print("1. Staff Management")
            print("2. Doctor Management")
            print("3. Role Management")
            print("4.Specialization Management")
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

    # ---------------- Staff Management ----------------
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

    # ---------------- Doctor Management ----------------
    def doctor_management_menu(self):
        while True:
            print("\n--- Doctor Management ---")
            print("1. Add Doctor Profile")
            print("2. Update Doctor Profile")
            print("3. Deactivate Doctor")
            print("4. List Doctors")
            print("5. Back")

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
                break
            else:
                print("Invalid choice!")

    # ---------------- Role Management ----------------
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
            print("1. Create specialization")
            print("2. List specialization")
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