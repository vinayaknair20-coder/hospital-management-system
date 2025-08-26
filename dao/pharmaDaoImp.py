from typing import List
from dao.absatractDaoPharma import medecineDaoService
from db.db_connection import DBConnection
from models.medicine import Medicine
from pymysql.cursors import DictCursor

class medicineDaoImp(medecineDaoService):
    '''implementation of abstract class methods'''
    #sql queries
    DISPLAY_ALL_MEDICINE ="SELECT*FROM medicine_inventory"
    INSERT_MEDICINE = "INSERT INTO medicine_inventory (medicine_id,medicine_name,generic_name,manufacturer,batch_number,quantity_in_stock,unit_price,expiry_date,minimum_stock_level,is_active) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

    def __init__(self):
        self.conn = DBConnection().get_connection()

    def add_medicine(self,medicine:Medicine)->bool:
        try:
            cursor = self.conn.cursor()#create a cursor object
            cursor.execute(self.INSERT_MEDICINE,
                           (medicine.get_medicine_id(),
                            medicine.get_medicine_name(),
                            medicine.get_gen_medicine_name(),
                            medicine.get_manufacturer(),
                            medicine.get_batch_number(),
                            medicine.get_quantity_in_stock(),
                            medicine.get_unit_price(),
                            medicine.get_expiry_date(),
                            medicine.get_minimum_stock_level(),
                            medicine.get_is_active()
                                ))
            self.conn.commit()
            return cursor.rowcount == 1
        except Exception as e:
            print("Error inserting medicine:",e)
            return False
        finally:
            cursor.close()

    def display_medicine(self)->List[Medicine]:
        medicine = []#To store the records from db
        try:
            cursor = self.conn.cursor(DictCursor)#return data in dictionary format
            cursor.execute(self.DISPLAY_ALL_MEDICINE)#fire the query
            rows = cursor.fetchall()
            for row in rows:
                medicine.append(Medicine(medicine_id=row["medicine_id"],
                                        medicine_name=row["medicine_name"],
                                        generic_name=row["generic_name"],
                                        manufacturer=row["manufacturer"],
                                        batch_number=row["batch_number"],
                                        quantity_in_stock=row["quantity_in_stock"],
                                        unit_price=row["unit_price"],
                                        expiry_date=row["expiry_date"],
                                        minimum_stock_level=row["minimum_stock_level"],
                                        is_active = row["is_active"]
                                        ))
        except Exception as e:
            print("Error fetching medicine:",e)
        finally:
            cursor.close()
        return medicine 