import hashlib
import secrets
from dao.admin_dao import AdminDao
from db.db_connection import DBConnection
import pymysql

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
                     WHERE s.email=%s AND s.is_active=1"""
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
            return None
        except Exception as e:
            print(f"❌ Error in authentication: {e}")
            return None
        finally:
            if cursor:
                cursor.close()

    def create_role(self):
        try:
            role_id = input("Enter Role ID: ").strip()
            role_name = input("Enter Role Name: ").strip()
            description = input("Enter Role Description: ").strip()

            # Input validation
            if not role_id:
                print("❌ Role ID cannot be empty.")
                return

            if not role_name:
                print("❌ Role Name cannot be empty.")
                return

            # Check if role already exists
            existing_roles = self.dao.list_roles()
            for role in existing_roles:
                if role['role_id'] == role_id:
                    print(f"❌ Role with ID '{role_id}' already exists.")
                    return
                if role['role_name'].upper() == role_name.upper():
                    print(f"❌ Role with name '{role_name}' already exists.")
                    return

            self.dao.create_role(role_id, role_name, description)
            print(f"✅ Role '{role_name}' created successfully!")

        except Exception as e:
            print(f"❌ Error creating role: {e}")

    def list_roles(self):
        try:
            roles = self.dao.list_roles()
            if not roles:
                print("⚠ No roles found.")
            else:
                print("\n" + "="*50)
                print("               ROLES LIST")
                print("="*50)
                print(f"{'ID':<10} {'Name':<20} {'Active':<8}")
                print("-"*50)
                for r in roles:
                    active_status = "Yes" if r['is_active'] else "No"
                    print(f"{r['role_id']:<10} {r['role_name']:<20} {active_status:<8}")
                print("="*50)
        except Exception as e:
            print(f"❌ Error listing roles: {e}")

    # ---------------- SPECIALIZATION LIBRARY ----------------

    def create_specialization(self):
        try:
            specialization_id = input("Enter Specialization ID (e.g., SPEC001): ").strip().upper()
            specialization_name = input("Enter Specialization Name: ").strip()
            description = input("Enter Description: ").strip()

            # Input validation
            if not specialization_id:
                print("❌ Specialization ID cannot be empty.")
                return

            if not specialization_name:
                print("❌ Specialization Name cannot be empty.")
                return

            # Validate ID format
            if not specialization_id.startswith('SPEC') or len(specialization_id) != 7:
                print("❌ Specialization ID must be in format 'SPEC001' (SPEC + 3 digits).")
                return

            # Check if specialization already exists
            existing_specs = self.dao.list_specialization()
            for spec in existing_specs:
                if spec['specialization_id'].upper() == specialization_id:
                    print(f"❌ Specialization with ID '{specialization_id}' already exists.")
                    return
                if spec['specialization_name'].upper() == specialization_name.upper():
                    print(f"❌ Specialization '{specialization_name}' already exists.")
                    return

            self.dao.create_specialization(specialization_id, specialization_name, description)
            print(f"✅ Specialization '{specialization_name}' created successfully!")

        except Exception as e:
            print(f"❌ Error creating specialization: {e}")

    def list_specialization(self):
        try:
            specs = self.dao.list_specialization()
            if not specs:
                print("⚠ No specializations found.")
            else:
                print("\n" + "="*70)
                print("                    SPECIALIZATIONS LIST")
                print("="*70)
                print(f"{'ID':<10} {'Name':<25} {'Description':<30}")
                print("-"*70)
                for s in specs:
                    desc = s['description'][:27] + "..." if len(s['description']) > 30 else s['description']
                    print(f"{s['specialization_id']:<10} {s['specialization_name']:<25} {desc:<30}")
                print("="*70)
        except Exception as e:
            print(f"❌ Error listing specializations: {e}")

    # ---------------- UTILITY METHODS ----------------

    @staticmethod
    def hash_password(password):
        """Generate a secure hash for password storage"""
        salt = secrets.token_hex(16)
        password_hash = hashlib.sha256((password + salt).encode()).hexdigest()
        return password_hash, salt

    @staticmethod
    def verify_password(password, stored_hash, salt):
        """Verify a password against stored hash"""
        entered_hash = hashlib.sha256((password + salt).encode()).hexdigest()
        return entered_hash == stored_hash

    def display_menu(self):
        """Display the admin menu"""
        print("\n" + "="*50)
        print("           ADMIN MANAGEMENT SYSTEM")
        print("="*50)
        print("1. Role Management")
        print("   - Create Role")
        print("   - List Roles")
        print("2. Specialization Management")
        print("   - Create Specialization")
        print("   - List Specializations")
        print("3. Exit")
        print("="*50)

    def validate_email(self, email):
        """Basic email validation"""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    def get_yes_no_input(self, prompt):
        """Get yes/no input from user"""
        while True:
            response = input(f"{prompt} (y/n): ").strip().lower()
            if response in ['y', 'yes']:
                return True
            elif response in ['n', 'no']:
                return False
            else:
                print("❌ Please enter 'y' for yes or 'n' for no.")
