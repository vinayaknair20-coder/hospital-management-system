from dao.staff_dao import StaffDao
from menu.admin_menu import AdminMenu
from lib.admin_library import AdminLibrary
from menu.Receptionistmenu import receptionist_menu  # to be created
# from menu.doctor_menu import DoctorMenu
# from menu.pharmacist_menu import PharmacistMenu
# from menu.lab_menu import LabMenu

def login():
    staff_dao = StaffDao()
    email = input("Enter email: ")
    password = input("Enter Password: ")

    user = AdminLibrary.authenticate_user(email, password)

    if not user:
        print("❌ Username(email) or Password")
        return None
    if not user.get("is_active", True):
        print("❌ Account is deactivated. Contact Admin.")
        return None

    print(f"✅ Login successful! Welcome {user['staff_name']} ({user['role_name']})")
    return user


def main():
    while True:
        print("\n======= CLINIC MANAGEMENT ==========")
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
                    # ReceptionistMenu().show_menu()
                elif role == "doctor":
                    print("👉 Doctor menu coming soon...")
                    # DoctorMenu().show_menu()
                elif role == "pharmacist":
                    print("👉 Pharmacist menu coming soon...")
                    # PharmacistMenu().show_menu()
                elif role == "lab technician":
                    print("👉 Lab Technician menu coming soon...")
                    # LabMenu().show_menu()
                else:
                    print("❌ Role not recognized.")
        elif choice == "2":
            print("👋 Exiting... Goodbye!")
            break
        else:
            print("❌ Invalid choice. Try again.")

if __name__ == "__main__":
    main()
