from db.db_connection import DBConnection
from pymysql.cursors import DictCursor

class PharmacyDispenseDao:
    def __init__(self):
        self.conn = DBConnection().get_connection()

    def get_pending_prescriptions(self):
        try:
            cursor = self.conn.cursor(DictCursor)
            query = """
            SELECT mp.med_prescription_id, mp.prescription_id, mp.medicine_name, 
                   mp.medicine_quantity, mp.dosage, mi.medicine_id, mi.quantity_in_stock,
                   a.patient_name, a.appointment_id
            FROM med_prescription mp
            JOIN prescriptions p ON mp.prescription_id = p.prescription_id
            JOIN appointments a ON p.appointment_id = a.appointment_id
            LEFT JOIN medicine_inventory mi ON LOWER(mp.medicine_name) = LOWER(mi.medicine_name) 
            LEFT JOIN medicine_billing mb ON mp.med_prescription_id = mb.med_prescription_id
            WHERE mb.med_prescription_id IS NULL AND mi.is_active = 1
            ORDER BY mp.prescription_id
            """
            cursor.execute(query)
            return cursor.fetchall()
        except Exception as e:
            print("Error fetching prescriptions:", e)
            return []
        finally:
            cursor.close()

    def dispense_medicine(self, med_prescription_id, medicine_id, dispense_qty, appointment_id):
        try:
            cursor = self.conn.cursor(DictCursor)
            
            # Get current stock and price
            cursor.execute("SELECT quantity_in_stock, unit_price, medicine_name FROM medicine_inventory WHERE medicine_id=%s", (medicine_id,))
            stock = cursor.fetchone()
            
            if not stock:
                return False, "Medicine not found in inventory"
            
            if stock['quantity_in_stock'] < dispense_qty:
                return False, f"Insufficient stock. Available: {stock['quantity_in_stock']}, Required: {dispense_qty}"
            
            # Update inventory - decrease stock
            cursor.execute(
                "UPDATE medicine_inventory SET quantity_in_stock = quantity_in_stock - %s WHERE medicine_id = %s",
                (dispense_qty, medicine_id)
            )
            
            # Add billing record
            total = dispense_qty * stock['unit_price']
            cursor.execute(
                "INSERT INTO medicine_billing (med_prescription_id, quantity_dispensed, unit_price, total_amount, appointment_id) VALUES (%s,%s,%s,%s,%s)",
                (med_prescription_id, dispense_qty, stock['unit_price'], total, appointment_id)
            )
            
            # Get new stock level
            cursor.execute("SELECT quantity_in_stock FROM medicine_inventory WHERE medicine_id = %s", (medicine_id,))
            new_stock = cursor.fetchone()['quantity_in_stock']
            
            self.conn.commit()
            
            return True, f"Dispensed {dispense_qty} units of {stock['medicine_name']}. Stock updated. Remaining: {new_stock} units"
            
        except Exception as e:
            self.conn.rollback()
            return False, f"Error dispensing: {e}"
        finally:
            cursor.close()

    def get_bill_for_appointment(self, appointment_id):
        try:
            cursor = self.conn.cursor(DictCursor)
            query = """
            SELECT mb.billing_id, mp.medicine_name, mb.quantity_dispensed, 
                   mb.unit_price, mb.total_amount, a.patient_name
            FROM medicine_billing mb
            JOIN med_prescription mp ON mb.med_prescription_id = mp.med_prescription_id
            JOIN prescriptions p ON mp.prescription_id = p.prescription_id
            JOIN appointments a ON p.appointment_id = a.appointment_id
            WHERE mb.appointment_id = %s
            """
            cursor.execute(query, (appointment_id,))
            items = cursor.fetchall()
            total = sum(item['total_amount'] for item in items)
            return items, total
        except Exception as e:
            print("Error fetching bill:", e)
            return [], 0
        finally:
            cursor.close()
