from typing import List
from dao.absatractDaoPharma import MedecineDaoService
from db.db_connection import DBConnection
from models.medicine import Medicine
from pymysql.cursors import DictCursor

class MedicineDaoImp(MedecineDaoService):
    DISPLAY_ALL_MEDICINE = (
        "SELECT * FROM medicine_inventory WHERE is_active = '1' ORDER BY medicine_type, medicine_name"
    )
    INSERT_MEDICINE = (
        "INSERT INTO medicine_inventory (medicine_id, medicine_name, generic_name, medicine_type, manufacturer,"
        "batch_number, quantity_in_stock, unit_price, expiry_date, minimum_stock_level) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    )
    UPDATE_MEDICINE = (
    "UPDATE medicine_inventory SET medicine_name = %s, medicine_type = %s, unit_price = %s, quantity_in_stock = %s WHERE medicine_id = %s")


    DISABLE_MEDICINE = (
        "UPDATE medicine_inventory SET is_active = '0' WHERE medicine_id = %s"
    )
    FIND_BY_ID = "SELECT * FROM medicine_inventory WHERE medicine_id = %s"
    FIND_BY_TYPE = ("SELECT * FROM medicine_inventory "
        "WHERE medicine_type = %s AND is_active = '1' ORDER BY medicine_name")
    GET_MEDICINE_TYPES = "SELECT DISTINCT medicine_type FROM medicine_inventory WHERE is_active = '1' ORDER BY medicine_type"
    FIND_CRITICAL_STOCK = (
        "SELECT * FROM medicine_inventory WHERE quantity_in_stock <= 10 AND is_active = '1' ORDER BY quantity_in_stock ASC, medicine_name"
    )

    def __init__(self):
        self.conn = DBConnection().get_connection()

    def add_medicine(self, medicine: Medicine) -> bool:
        cursor = None
        try:
            self.conn.ping(reconnect=True)
            cursor = self.conn.cursor()
            cursor.execute(self.INSERT_MEDICINE, (
                medicine.get_medicine_id(),
                medicine.get_medicine_name(),
                medicine.get_gen_medicine_name(),
                medicine.get_medicine_type(),
                medicine.get_manufacturer(),
                medicine.get_batch_number(),
                medicine.get_quantity_in_stock(),
                medicine.get_unit_price(),
                medicine.get_expiry_date(),
                medicine.get_minimum_stock_level()))
            self.conn.commit()
            return cursor.rowcount == 1
        except Exception as e:
            print(f"Error inserting medicine: {e}")
            if self.conn:
                self.conn.rollback()
            return False
        finally:
            if cursor:
                cursor.close()

    def display_all_medicine(self) -> List[Medicine]:
        medicines = []
        cursor = None
        try:
            self.conn.ping(reconnect=True)
            cursor = self.conn.cursor(DictCursor)
            cursor.execute(self.DISPLAY_ALL_MEDICINE)
            rows = cursor.fetchall()
            for row in rows:
                medicines.append(self._create_medicine_from_row(row))
            return medicines
        except Exception as e:
            print(f"Error fetching medicines: {e}")
            return []
        finally:
            if cursor:
                cursor.close()

    def update_medicine(self, medicine: Medicine, medicine_id: int) -> bool:
        cursor = None
        try:
            self.conn.ping(reconnect=True)
            cursor = self.conn.cursor(DictCursor)
            cursor.execute(self.UPDATE_MEDICINE, (
                medicine.get_medicine_name(),
                medicine.get_medicine_type(),
                medicine.get_unit_price(),
                medicine.get_quantity_in_stock(),  # ADD THIS LINE
                medicine_id))
            self.conn.commit()
            return cursor.rowcount == 1

        except Exception as e:
            print(f"Error updating medicine: {e}")
            if self.conn:
                self.conn.rollback()
            return False
        finally:
            if cursor:
                cursor.close()



    def disable_medicine(self, medicine_id: int) -> bool:
        cursor = None
        try:
            self.conn.ping(reconnect=True)
            cursor = self.conn.cursor(DictCursor)
            cursor.execute(self.DISABLE_MEDICINE, (medicine_id,))
            self.conn.commit()
            return cursor.rowcount == 1
        except Exception as e:
            print(f"Error disabling medicine: {e}")
            if self.conn:
                self.conn.rollback()
            return False
        finally:
            if cursor:
                cursor.close()

    def find_by_medicine_id(self, medicine_id: int) -> Medicine:
        cursor = None
        try:
            self.conn.ping(reconnect=True)
            cursor = self.conn.cursor(DictCursor)
            cursor.execute(self.FIND_BY_ID, (medicine_id,))
            row = cursor.fetchone()
            if row:
                return self._create_medicine_from_row(row)
            return None
        except Exception as e:
            print(f"Error finding medicine: {e}")
            return None
        finally:
            if cursor:
                cursor.close()

    def find_by_medicine_type(self, medicine_type: str) -> List[Medicine]:
        medicines = []
        cursor = None
        try:
            self.conn.ping(reconnect=True)
            cursor = self.conn.cursor(DictCursor)
            cursor.execute(self.FIND_BY_TYPE, (medicine_type,))
            rows = cursor.fetchall()
            for row in rows:
                medicines.append(self._create_medicine_from_row(row))
            return medicines
        except Exception as e:
            print(f"Error finding medicines by type: {e}")
            return []
        finally:
            if cursor:
                cursor.close()

    def get_medicine_types(self) -> List[str]:
        cursor = None
        try:
            self.conn.ping(reconnect=True)
            # FIXED: Use DictCursor here too
            cursor = self.conn.cursor(DictCursor)
            cursor.execute(self.GET_MEDICINE_TYPES)
            rows = cursor.fetchall()
            # FIXED: Access by column name instead of index
            return [row["medicine_type"] for row in rows]
        except Exception as e:
            print(f"Error fetching medicine types: {e}")
            return []
        finally:
            if cursor:
                cursor.close()

    def get_critical_stock_medicines(self) -> List[Medicine]:
        medicines = []
        cursor = None
        try:
            self.conn.ping(reconnect=True)
            cursor = self.conn.cursor(DictCursor)
            cursor.execute(self.FIND_CRITICAL_STOCK)
            rows = cursor.fetchall()
            for row in rows:
                medicines.append(self._create_medicine_from_row(row))
            return medicines
        except Exception as e:
            print(f"Error fetching critical stock medicines: {e}")
            return []
        finally:
            if cursor:
                cursor.close()

    def _create_medicine_from_row(self, row: dict) -> Medicine:
        return Medicine(
            medicine_id=row["medicine_id"],
            medicine_name=row["medicine_name"],
            generic_name=row["generic_name"],
            medicine_type=row["medicine_type"],
            manufacturer=row["manufacturer"],
            batch_number=row["batch_number"],
            quantity_in_stock=row["quantity_in_stock"],
            unitprice=row["unit_price"],
            expiry_date=row["expiry_date"],
            minimum_stock_level=row["minimum_stock_level"],
            is_active=row["is_active"]
        )
