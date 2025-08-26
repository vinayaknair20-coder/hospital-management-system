from datetime import datetime
import pymysql
from db.db_connection import DBConnection
import re
import hashlib


class StaffDao:
    
    def add_staff(self, staff_id, staff_name, role_id, age, phone_number, email, doj, password):
        db = DBConnection()
        conn = db.get_connection()
        cursor = None
        try:
            cursor = conn.cursor()
            sql = """INSERT INTO staff 
                     (staff_id, staff_name, role_id, age, phone_number, email, date_of_joining, password_hash) 
                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            cursor.execute(sql, (staff_id, staff_name, role_id, age, phone_number, email, doj, password_hash))
            conn.commit()
            print("✅ Staff added successfully!")
        except Exception as e:
            print(f"❌ Error while adding staff: {e}")
        finally:
            if cursor:
                cursor.close()

    def update_staff(self, staff_id, phone_number, email):
        db = DBConnection()
        conn = db.get_connection()
        cursor = None
        try:
            cursor = conn.cursor()
            sql = "UPDATE staff SET phone_number=%s, email=%s WHERE staff_id=%s"
            cursor.execute(sql, (phone_number, email, staff_id))
            conn.commit()
            print("✅ Staff updated successfully.")
        except Exception as e:
            print("❌ Error updating staff:", e)
        finally:
            if cursor:
                cursor.close()

    def deactivate_staff(self, staff_id):
        db = DBConnection()
        conn = db.get_connection()
        cursor = None
        try:
            cursor = conn.cursor()
            sql = "UPDATE staff SET is_active=FALSE WHERE staff_id=%s"
            cursor.execute(sql, (staff_id,))
            conn.commit()
            print("✅ Staff deactivated successfully.")
        except Exception as e:
            print("❌ Error deactivating staff:", e)
        finally:
            if cursor:
                cursor.close()

    def list_staff(self):
        db = DBConnection()
        conn = db.get_connection()
        cursor = None
        try:
            cursor = conn.cursor(pymysql.cursors.DictCursor)  
            sql = "SELECT * FROM staff"
            cursor.execute(sql)
            result = cursor.fetchall()
            return result
        except Exception as e:
            print("❌ Error listing staff:", e)
            return []
        finally:
            if cursor:
                cursor.close()

    def get_next_staff_id(self):
        conn = DBConnection().get_connection()
        cursor = None
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT staff_id FROM staff ORDER BY staff_id DESC LIMIT 1")
            result = cursor.fetchone()
            if result:
                last_id = result[0]  # e.g. "S005"
                num = int(last_id[1:]) + 1
                return f"S{num:03d}"
            else:
                return "S001"
        except Exception as e:
            print("❌ Error generating staff_id:", e)
            return "S001"
        finally:
            if cursor:
                cursor.close()            
