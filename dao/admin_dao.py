import pymysql
from db.db_connection import DBConnection


class AdminDao:
    def create_role(self, role_id, role_name,description):
        db = DBConnection()
        self.conn = db.get_connection()
        cursor = None
        try:
            self.conn.ping(reconnect=True)
            cursor = self.conn.cursor()
            sql = "INSERT INTO roles (role_id, role_name,decsription) VALUES (%s, %s,%s)"
            cursor.execute(sql, (role_id, role_name,description))
            self.conn.commit()
            print("✅ Role created successfully!")
        except Exception as e:
            print(f"❌ Error creating role: {e}")
        finally:
            if cursor:
                cursor.close()

    def list_roles(self):
        db = DBConnection()
        self.conn = db.get_connection()
        self.cursor = None
        try:
            self.conn.ping(reconnect=True)
            cursor = self.conn.cursor(pymysql.cursors.DictCursor)
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
        self.conn = db.get_connection()
        cursor = None
        try:
            self.conn.ping(reconnect=True)
            cursor = self.conn.cursor()
            sql = "INSERT INTO specializations (specialization_id, specialization_name,description) VALUES (%s, %s, %s)"
            cursor.execute(sql, (specialization_id, specialization_name,description))
            self.conn.commit()
            print("✅ Specialization created successfully!")
        except Exception as e:
            print(f"❌ Error creating specialization: {e}")
        finally:
            if cursor:
                cursor.close()

    def list_specialization(self):
        db = DBConnection()
        self.conn = db.get_connection()
        cursor = None
        try:
            self.conn.ping(reconnect=True)
            cursor = self.conn.cursor(pymysql.cursors.DictCursor)
            sql = "SELECT * FROM specializations"
            cursor.execute(sql)
            return cursor.fetchall()
        except Exception as e:
            print("❌ Error listing specialization:", e)
            return []
        finally:
            if cursor:
                cursor.close()
