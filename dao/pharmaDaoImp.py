from typing import List
from dao.absatractDaoPharma import MedecineDaoService
from db.db_connection import DBConnection
from models.medicine import Medicine
from pymysql.cursors import DictCursor

class MedicineDaoImp(MedecineDaoService):
    '''implementation of abstract class methods'''
    #sql queries
    DISPLAY_ALL_MEDICINE ="SELECT * FROM medicine_inventory WHERE is_active ='1'"
    INSERT_MEDICINE = "INSERT INTO medicine_inventory (medicine_id,medicine_name,generic_name,manufacturer,batch_number,quantity_in_stock,unit_price,expiry_date,minimum_stock_level) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    UPDATE_MEDICINE =  "UPDATE medicine_inventory set medicine_name = %s,unit_price = %s WHERE medicine_id = %s "
    DISABLE_MEDICINE = "UPDATE medicine_inventory set is_active = '0' WHERE medicine_id = %s "
    FIND_BY_ID = "SELECT * FROM medicine_inventory where medicine_id = %s"

    def __init__(self):
        self.conn = DBConnection().get_connection()

    def add_medicine(self,medicine:Medicine)->bool:
        try:
            self.conn.ping(reconnect=True)
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
                            # medicine.get_is_active()
                                ))
            self.conn.commit()
            return cursor.rowcount == 1
        except Exception as e:
            print("Error inserting medicine:",e)
            return False
        finally:
            cursor.close()

    def display_all_medicine(self)->List[Medicine]:
        medicine = []#To store the records from db
        try:
            self.conn.ping(reconnect=True)
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
                                        unitprice=row["unit_price"],
                                        expiry_date=row["expiry_date"],
                                        minimum_stock_level=row["minimum_stock_level"],
                                        is_active = row["is_active"]
                                        ))
        except Exception as e:
            print("Error fetching medicine:",e)
        finally:
            cursor.close()
        return medicine 
    
    def update_medicine(self,medicine:Medicine,medicine_id:int)->bool:
        try:
            self.conn.ping(reconnect=True)
            cursor = self.conn.cursor(DictCursor)#return data in dictionary format
            cursor.execute(self.UPDATE_MEDICINE,(medicine.get_medicine_name(),medicine.get_unit_price(),medicine_id))
            self.conn.commit()
            return cursor.rowcount == 1
        except Exception as e:
            print("Error updating medicine",e)
            return False
        finally:
            cursor.close()
        
    def disable_medicine(self,medicine_id:int)->bool:
        try:
            self.conn.ping(reconnect=True)
            cursor=self.conn.cursor(DictCursor)
            cursor.execute(self.DISABLE_MEDICINE,
                           (medicine_id,))
            self.conn.commit()
            return cursor.rowcount == 1
        except Exception as e:
            print("Error disabling medicine:",e)
            return False
        finally:
            cursor.close()

    def find_by_medicine_id(self, medicine_id:int):
        medicine = None
        try:
            self.conn.ping(reconnect=True)
            cursor = self.conn.cursor(DictCursor)#return data in dictionary format
            cursor.execute(self.FIND_BY_ID,(medicine_id,))
            row = cursor.fetchone()
            if row:
                medicine = (Medicine(medicine_id=row["medicine_id"],
                                        medicine_name=row["medicine_name"],
                                        generic_name=row["generic_name"],
                                        manufacturer=row["manufacturer"],
                                        batch_number=row["batch_number"],
                                        quantity_in_stock=row["quantity_in_stock"],
                                        unitprice=row["unit_price"],
                                        expiry_date=row["expiry_date"],
                                        minimum_stock_level=row["minimum_stock_level"],
                                        is_active = row["is_active"]
                                        ))
        except Exception as e:
            print("Error finding medicine",e)
        finally:
            cursor.close()
        return medicine