from db.db_connection import DBConnection
# from menu.admin_menu import AdminMenu
# from menu.receptionist_menu import receptionist_menu
# from menu.doctor_menu import doctor_menu
# from menu.Pharmacist_menu import Pharmacist_menu
# from menu.lab_technician import lab_technician
import sys
from lib.Pharmacistservices import MedicineManagementLib
from dao.absatractDaoPharma import medecineDaoService
from dao.pharmaDaoImp import medicineDaoImp

def admin_menu():
    print("Welcome to admin Dashboard")


def receptionist_menu():
    print("Welcome to Receptionist Dashboard")

def doctor_menu():
    print(" Welcome to Doctor Dashboard")

def Pharmacist_menu():
    print(" Welcome to Pharmacist Dashboard")
    while True:
        print("\n=========PRODUCT MANAGEMENT MENU==========")
        print("1. ADD PRODUCT")
        print("2. DISPLAY ALL PRODUCTS")

        choice = input("Enter your choice:")
        if choice == "1":
            MedicineManagementLib.insert_medicine()
        elif choice == "2":
            MedicineManagementLib.display_medicine()
        
def lab_technician():
    print("Welcome to Lab_Techniocian Dashboard")

def main():
    while True:
        print("\n======= CLINIC MANAGEMENT ==========")
        print("1. ADMIN")
        print("2. RECEPTIONIST")
        print("3. DOCTOR")
        print("4. PHARMACIST")
        print("5. LAB TECHNICIAN")
        print("6. EXIT")

        choice = input("Enter your choice: ")

        if choice == "1":
            print(" Welcome to Admin Dashboard")
            admin_menu()
        elif choice == "2":
            receptionist_menu()
        elif choice == "3":
            doctor_menu()
        elif choice == "4":
            Pharmacist_menu()
        elif choice == "5":
            lab_technician()
        elif choice == "6":
            print(" Exiting system...")
            break
        else:
            print("⚠ Invalid option! Try again.")


if __name__ =="__main__":
   main()

# if __name__ == "_main_":
#    main()