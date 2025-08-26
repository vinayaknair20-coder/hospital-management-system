from dao.absatractDaoPharma import medecineDaoService
from dao.pharmaDaoImp import medicineDaoImp
from models.medicine import Medicine
from datetime import datetime

class MedicineManagementLib:
    'handles CRUD logic'

    dao_service : medecineDaoService = medicineDaoImp()

    @staticmethod
    def display_medicine():
        medicine = MedicineManagementLib.dao_service.display_all_medicine()
        for medicine in medicine:
            print(medicine)

    @staticmethod
    def insert_medicine():
        medicine=Medicine()
        medicine_id = int(input("Enter the medicine:"))
        medicine.set_medicine_id(medicine_id)
        medicine_name = input("Enter the medicine name:")
        product.set_unitprice(unitprice)
        categoryid = int(input("Enter the ctaegory ID:"))
        product.set_categoryid(categoryid)
        m_date = input("Enter manufacture Date(dd/mm/yyyy):")
        util_date = datetime.strptime(m_date, "%d/%m/%Y")
        conv_m_date = util_date.date()
        product.set_manufacture_date(conv_m_date)
        product.set_is_active(is_active="Y")
        if ProductManagementLib.dao_service.insert_products(product):
            print("inserted successfully.........")
        else:
            print("something went wrong......")

    @staticmethod
    def update_product():
        searchid = int(input("Enter the product ID"))
        #create a method in DAO
        product = ProductManagementLib.dao_service.find_by_product_id(searchid)
        if not product:
            print("Product not found")
            return
        print(product)
        confirm = input("Do you wnat to edit this data?(y/n)")
        if confirm.lower()=="y":
            product.set_product_name(input("Enter new product Name: "))
            product.set_unitprice(float(input("Enter new unit price: ")))
        #pass the object to dao update
            if ProductManagementLib.dao_service.update_product(product,searchid):
                print("Updated successfully......")
            else:
                print("Something went wrong......")
    
    @staticmethod
    def disable_product():
        searchid = int(input("Enter the product ID to disable"))

        product = ProductManagementLib.dao_service.find_by_product_id(searchid)
        if not product:
            print("Product not found")
            return
        print(product)
        confirm = input("Do you wnat to disable this product?(y/n)")
        if confirm.lower()=="y":
            if ProductManagementLib.dao_service.disable_product(searchid):
                print("disable successfull.......")
            else:
                print("Something went wrong......")

    @staticmethod
    def search_by_product_id():
        searchid = int(input("Enter the product ID to search"))

        product = ProductManagementLib.dao_service.find_by_product_id(searchid)
        if not product:
            print("Product not found")
            return
        print(product)
            

    @staticmethod
    def apply_gst_to_product():
        product_id = int(input("Enter the product ID to apply GST:"))
        gst_percent = float(input("Enter GST percentage to apply:"))
        if ProductManagementLib.dao_service.apply_gst(product_id,gst_percent):
            print(f"GST of {gst_percent} applied to product ID {product_id}")
        else:
            print("failed to apply GST")
        
            