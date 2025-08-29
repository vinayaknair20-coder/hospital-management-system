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

    @staticmethod
    def search_by_id():
        searchid = int(input("Enter the test id"))
        #create amethod in DAO
        product = LabtechManagementLib.dao_service.find_by_test_id(searchid)
        if not product:
            print("test not found")
            return 
        print(product)

    @staticmethod
    def update_test():
        searchid = input("Enter the test id: ")   # don’t cast to int, test_id is VARCHAR

        product = LabtechManagementLib.dao_service.find_by_test_id(searchid)
        if not product:
            print("Test not found")
            return

        print("Current Data:", product)

        confirm = input("Do you want to edit this data? (y/n): ")
        if confirm.lower() == 'y':
            # Assign values properly (not function call)
            product.test_name = input("Enter new Test Name: ")
            product.unit_of_measurement = input("Enter new Unit of Measurement: ")
            product.test_price = float(input("Enter New Unit Price: "))

            # Call DAO update
            if LabtechManagementLib.dao_service.update_test(product, searchid):
                print("Updated successfully ✅")
            else:
                print("Something went wrong ❌")
    @staticmethod
    def disable_product():
        search_id = input("Enter the test id: ")

        product = LabtechManagementLib.dao_service.find_by_test_id(search_id)
        if not product:
            print("Test not found")
            return

        print(product)
        confirm = input("Do you want to disable this test? (y/n): ")
        if confirm.lower() == 'y':
            if LabtechManagementLib.dao_service.delete_test(search_id):
                print("Test disabled successfully.")
            else:
                print("Something went wrong.")

    @staticmethod
    def init(conn):
        """Initialize DAO service with DB connection"""
        LabtechManagementLib.dao_service = LabDaoimplementation(conn)

    @staticmethod
    def view_prescription_results():
        results = LabtechManagementLib.dao_service.view_prescription_results()
        if not results:
            print("No prescriptions or results found.")
            return

        for row in results:
            print(f"PrescriptionID: {row['prescription_id']}, "
                  f"Test: {row['test_name']}, "
                  f"Value: {row['test_value']}, "
                  f"Status: {row['result_status']}, "
                  f"Date: {row['tested_date']}, "
                  f"Lab Note: {row['lab_resultcol']}")
            
    @staticmethod
    def add_test_result():
        try:
            test_prescription_id = input("Enter Test Prescription ID: ")
            test_value = input("Enter Test Value: ")
            result_status = input("Enter Result Status (Normal/Abnormal/etc): ")
            tested_date = input("Enter Tested Date (YYYY-MM-DD): ")
            lab_resultcol = input("Enter Lab Notes/Comments: ")

            if LabtechManagementLib.dao_service.add_test_result(
                test_prescription_id, test_value, result_status, tested_date, lab_resultcol
            ):
                print("✅ Test result added successfully.")
            else:
                print("❌ Failed to add test result.")
        except Exception as e:
            print("Error in lib layer:", e)
            