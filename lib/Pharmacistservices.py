from dao.absatractDaoPharma import MedecineDaoService
from dao.pharmaDaoImp import MedicineDaoImp
from models.medicine import Medicine
from datetime import datetime

class MedicineManagementLib:
    'handles CRUD logic'

    dao_service : MedecineDaoService = MedicineDaoImp()

    @staticmethod
    def display_medicine():
        medicine = MedicineManagementLib.dao_service.display_all_medicine()
        for medicine in medicine:
            print(medicine)

    @staticmethod
    def insert_medicine():
        medicine=Medicine()
        medicine_id = int(input("Enter the medicine ID:"))
        medicine.set_medicine_id(medicine_id)
        medicine_name = input("Enter the medicine name:") 
        medicine.set_medicine_name(medicine_name)
        generic_name= input("Enter the generic name:")
        medicine.set_gen_medicine_name(generic_name)
        manufacturer= input("Enter the manufacturer:")
        medicine.set_manufacturer(manufacturer)
        batch_number= int(input("Enter the batch number:"))
        medicine.set_batch_number(batch_number)
        quantity_in_stock= int(input("Enter quantity in stock:"))
        medicine.set_quantity_in_stock(quantity_in_stock)
        unit_price= int(input("Enter the unit price:"))
        medicine.set_unit_price(unit_price)
        expiry_date = input("Enter expiry Date(dd/mm/yyyy):")
        util_date = datetime.strptime(expiry_date, "%d/%m/%Y")
        conv_m_date = util_date.date()
        medicine.set_expiry_date(conv_m_date)
        minimum_stock_level= int(input("Enter the minimum_stock_level:"))
        medicine.set_minimum_stock_level(minimum_stock_level)
        
       
        if MedicineManagementLib.dao_service.add_medicine(medicine):
            print("inserted successfully.........")
        else:
            print("something went wrong......")

    @staticmethod
    def update_medicine():
        searchid = int(input("Enter the medicine ID"))
        #create a method in DAO
        medicine = MedicineManagementLib.dao_service.find_by_medicine_id(searchid)
        if not medicine:
            print("medicine not found")
            return
        print(medicine)
        confirm = input("Do you wnat to edit this data?(y/n)")
        if confirm.lower()=="y":
            medicine.set_medicine_name(input("Enter new product Name: "))
            medicine.set_unit_price(float(input("Enter new unit price: "))
                            )
        #pass the object to dao update
            if MedicineManagementLib.dao_service.update_medicine(medicine,searchid):
                print("Updated successfully......")
            else:
                print("Something went wrong......")
    
    @staticmethod
    def disable_medicine():
        searchid = int(input("Enter the medicine ID to disable"))

        medicine = MedicineManagementLib.dao_service.find_by_medicine_id(searchid)
        if not medicine:
            print("medicine not found")
            return
        print(medicine)
        confirm = input("Do you wnat to disable this medicine?(y/n)")
        if confirm.lower()=="y":
            if MedicineManagementLib.dao_service.disable_medicine(searchid):
                print("disable successfull.......")
            else:
                print("Something went wrong......")

    @staticmethod
    def search_by_medicine_id():
        searchid = int(input("Enter the medicine ID to search"))

        medicine = MedicineManagementLib.dao_service.find_by_medicine_id(searchid)
        if not medicine:
            print("medicine not found")
            return
        print(medicine)

    