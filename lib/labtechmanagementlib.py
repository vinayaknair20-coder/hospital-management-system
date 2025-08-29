from dao.abstractLabDao import AbstractLabDao
from dao.LabDaoImp import LabDaoimplementation
from models.labtech import LabTech

class LabtechManagementLib:
    dao_service: AbstractLabDao = LabDaoimplementation()

    @staticmethod
    def display_all():
        products = LabtechManagementLib.dao_service.display_test()
        for product in products:
            print(product)   # print each product

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
            try:
                product.test_name = input("Enter new Test Name: ")
                product.unit_of_measurement = input("Enter new Unit of Measurement: ")
                product.test_price = float(input("Enter New Unit Price: "))
                print("\nUpdating record...")

                ok = LabtechManagementLib.dao_service.update_test(product, searchid)
                if ok:
                    print("Updated successfully ✅")
                else:
                    print("Update did not modify any row (check test_id / is_active). ❌")
            except Exception as e:
                print("Error during update:", e)
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
            print(
                f"PrescriptionID: {row.get('prescription_id', 'N/A')}, "
                f"Test: {row.get('test_name', 'N/A')}, "
                f"Value: {row.get('test_value', 'N/A')}, "
                f"Status: {row.get('result_status', 'N/A')}, "
                f"Date: {row.get('tested_date', 'N/A')}"
            )

    @staticmethod
    def list_all_results():
        rows = LabtechManagementLib.dao_service.list_all_test_results()
        if not rows:
            print("No test results found.")
            return
        # Render as a table
        headers = [
            ("ResultID", 9),
            ("TestPrescID", 12),
            ("PrescriptionID", 15),
            ("Test", 22),
            ("Value", 10),
            ("Status", 10),
            ("Date", 19),
        ]
        def fmt(text, width):
            t = "" if text is None else str(text)
            return (t[:width-1] + "…") if len(t) > width else t.ljust(width)

        line = " ".join(h.ljust(w) for h, w in headers)
        sep = "-" * len(line)
        print("\nTEST RESULTS")
        print(sep)
        print(line)
        print(sep)
        for r in rows:
            cols = [
                fmt(r.get('result_id'), 9),
                fmt(r.get('test_prescription_id'), 12),
                fmt(r.get('prescription_id'), 15),
                fmt(r.get('test_name'), 22),
                fmt(r.get('test_value'), 10),
                fmt(r.get('result_status'), 10),
                fmt(r.get('tested_date'), 19),
            ]
            print(" ".join(cols))
        print(sep)
            
    @staticmethod
    def add_test_result():
        try:
            # Validate inputs
            test_prescription_id_str = input("Enter Test Prescription ID: ").strip()
            if not test_prescription_id_str.isdigit():
                print("Invalid Test Prescription ID. It must be a number.")
                return
            test_prescription_id = int(test_prescription_id_str)

            test_value = input("Enter Test Value: ").strip()
            if not test_value:
                print("Test Value cannot be empty.")
                return

            result_status = input("Enter Result Status (Normal/Abnormal/etc): ").strip()
            allowed_status = {"normal", "abnormal", "borderline"}
            if result_status.lower() not in allowed_status:
                print("Invalid status. Use one of: Normal, Abnormal, Borderline")
                return

            tested_date = input("Enter Tested Date (YYYY-MM-DD): ").strip()
            import re
            if not re.match(r"^\d{4}-\d{2}-\d{2}$", tested_date):
                print("Invalid date format. Use YYYY-MM-DD.")
                return

            lab_resultcol = input("Enter Lab Notes/Comments (optional): ").strip()

            if LabtechManagementLib.dao_service.add_test_result(
                test_prescription_id, test_value, result_status.capitalize(), tested_date, lab_resultcol or None
            ):
                print("✅ Test result added successfully.")
            else:
                print("❌ Failed to add test result.")
        except Exception as e:
            print("Error in lib layer:", e)
            