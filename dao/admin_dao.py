import pymysql
from db.db_connection import DBConnection


class AdminDao:
    def create_role(self, role_id, role_name,description):
        db = DBConnection()
        conn = db.get_connection()
        cursor = None
        try:
            cursor = conn.cursor()
            sql = "INSERT INTO roles (role_id, role_name,description) VALUES (%s, %s,%s)"
            cursor.execute(sql, (role_id, role_name,description))
            conn.commit()
            print("✅ Role created successfully!")
        except Exception as e:
            print(f"❌ Error creating role: {e}")
        finally:
            if cursor:
                cursor.close()

    def list_roles(self):
        db = DBConnection()
        conn = db.get_connection()
        cursor = None
        try:
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            sql = "SELECT * FROM roles"
            cursor.execute(sql)
            return cursor.fetchall()
        except Exception as e:
            print("❌ Error listing roles:", e)
            return []
        finally:
            if cursor:
                cursor.close()

    def create_specialization(self, specialization_id, specialization_name,description):
        db = DBConnection()
        conn = db.get_connection()
        cursor = None
        try:
            cursor = conn.cursor()
            sql = "INSERT INTO specializations (specialization_id, specialization_name,description) VALUES (%s, %s, %s)"
            cursor.execute(sql, (specialization_id, specialization_name,description))
            conn.commit()
            print("✅ Specialization created successfully!")
        except Exception as e:
            print(f"❌ Error creating specialization: {e}")
        finally:
            if cursor:
                cursor.close()

    def list_specialization(self):
        db = DBConnection()
        conn = db.get_connection()
        cursor = None
        try:
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            sql = "SELECT * FROM specializations"
            cursor.execute(sql)
            return cursor.fetchall()
        except Exception as e:
            print("❌ Error listing specialization:", e)
            return []
        finally:
            if cursor:
                cursor.close()
