from dao.abstractLabDao import AbstractLabDao
from dao.LabDaoImp import LabDaoimplementation
from models.labtech import LabTech

class LabtechManagementLib:
    dao_service: AbstractLabDao = LabDaoimplementation()

    @staticmethod
    def display_all():
        products = LabtechManagementLib.dao_service.display_test()
        for product in products:
            print(product)   # ✅ print each product

    @staticmethod
    def create_test():
        labtech = LabTech()

        labtech.test_id = input("Enter ID: ")
        labtech.test_name = input("Enter Test Name: ")
        labtech.test_category = input("Enter the Category: ")
        labtech.normal_range_min = int(input("Enter minimum range: "))
        labtech.normal_range_max = int(input("Enter maximum range: "))
        labtech.unit_of_measurement = input("Enter measurement: ")
        labtech.test_price = int(input("Enter price: "))

        if LabtechManagementLib.dao_service.create_test(labtech):
            print("Inserted successfully...")
        else:
            print("Something went wrong!!!")
