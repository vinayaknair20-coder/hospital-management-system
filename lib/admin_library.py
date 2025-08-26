import hashlib
from dao.admin_dao import AdminDao
from db.db_connection import DBConnection


class AdminLibrary:
    def __init__(self):
        self.dao = AdminDao()

    # ---------------- ROLE LIBRARY ----------------

    @staticmethod
    def authenticate_user(email, password):
        db = DBConnection()
        conn = db.get_connection()
        cursor = None
        try:
            cursor = conn.cursor()
            sql = """SELECT s.staff_id, s.staff_name, s.email, s.password_hash, 
                            s.is_active, r.role_name
                     FROM staff s
                     JOIN roles r ON s.role_id = r.role_id
                     WHERE s.email=%s"""
            cursor.execute(sql, (email,))
            user = cursor.fetchone()
            if not user:
                return None

            staff_id, staff_name, email, password_hash, is_active, role_name = user

            # Hash the entered password
            entered_hash = hashlib.sha256(password.encode()).hexdigest()

            if password_hash == entered_hash:
                return {
                    "staff_id": staff_id,
                    "staff_name": staff_name,
                    "email": email,
                    "is_active": is_active,
                    "role_name": role_name
                }
            else:
                return None
        except Exception as e:
            print("❌ Error in authentication:", e)
            return None
        finally:
            if cursor:
                cursor.close()



    def create_role(self):
        role_id = input("Enter Role ID: ")
        role_name = input("Enter Role Name: ")
        description = input("Enter Role Description: ")
        

        if not role_name.strip():
            print("❌ Role Name cannot be empty.")
            return

        self.dao.create_role(role_id, role_name, description)

    def list_roles(self):
        roles = self.dao.list_roles()
        if not roles:
            print("⚠ No roles found.")
        else:
            print("\n--- Roles ---")
            for r in roles:
                print(f"ID: {r['role_id']}, Name: {r['role_name']}, Active: {r['is_active']}")

    # ---------------- SPECIALIZATION LIBRARY ----------------
    def create_specialization(self):
        specialization_id = input("Enter Specialization ID (e.g., SPEC001): ")
        specialization_name = input("Enter Specialization Name: ")
        description = input("Enter Description: ")

        if not specialization_name.strip():
            print("❌ Specialization Name cannot be empty.")
            return

        self.dao.create_specialization(specialization_id, specialization_name, description)

    def list_specialization(self):
        specs = self.dao.list_specialization()
        if not specs:
            print("⚠ No specializations found.")
        else:
            print("\n--- Specializations ---")
            for s in specs:
                print(f"ID: {s['specialization_id']}, Name: {s['specialization_name']}, Description: {s['description']}")
