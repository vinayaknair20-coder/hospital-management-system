from db.db_connection import DBConnection
# from menu.admin_menu import AdminMenu
# from menu.receptionist_menu import receptionist_menu
#from menu.doctor_menu import doctor_menu
#from menu.Pharmacist_menu import Pharmacist_menu
from lib.labtechmanagementlib import LabtechManagementLib
import sys


class Lab:
    def __init__(self):
        self.labtechmanagementlib= LabtechManagementLib()

    def showmenu(self):
        while True:
            print("1.Add test")

            choice = input("Enter your choice: ")

            if choice == "1":
                self.labtechmanagementlib.create_test()

            elif choice == "2":
                self.labtechmanagementlib.display_all()


