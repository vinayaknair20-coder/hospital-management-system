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

    