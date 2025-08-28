# dao/doctorDao.py
import mysql.connector
from mysql.connector import Error
from db.db_connection import DBConnection



class DoctorDao:
    def __init__(self, host="localhost", database="hospital_db", user="root", password="faith"):
        self.host = host
        self.database = database
        self.user = user
        self.password = password

    def connect(self):
        return mysql.connector.connect(
            host=self.host,
            database=self.database,
            user=self.user,
            password=self.password
        )

    def get_next_doctor_id(self):
        """Generate next doctor_id (max + 1)"""
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT IFNULL(MAX(doctor_id), 0) + 1 FROM doctors")
        next_id = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return next_id

    def add_doctor(self, doctor_id, staff_id, specialization_id,
                   consultation_fee, working_hours_start, working_hours_end,
                   is_available=1):
        """Insert a new doctor"""
        query = """
            INSERT INTO doctors 
                (doctor_id, staff_id, specialization_id, consultation_fee, 
                 working_hours_start, working_hours_end, is_available)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        values = (doctor_id, staff_id, specialization_id, consultation_fee,
                  working_hours_start, working_hours_end, is_available)

        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(query, values)
        conn.commit()
        cursor.close()
        conn.close()

    def update_doctor(self, doctor_id, consultation_fee, is_available):
        """Update doctor details"""
        query = """
            UPDATE doctors
            SET consultation_fee = %s,
                is_available = %s
            WHERE doctor_id = %s
        """
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(query, (consultation_fee, is_available, doctor_id))
        conn.commit()
        cursor.close()
        conn.close()

    def deactivate_doctor(self, doctor_id):
        """Set availability to 0"""
        query = """
            UPDATE doctors
            SET is_available = 0
            WHERE doctor_id = %s
        """
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(query, (doctor_id,))
        conn.commit()
        cursor.close()
        conn.close()

    def list_doctors(self):
        """Return list of all doctors"""
        query = "SELECT * FROM doctors WHERE is_available = '1'"
        conn = self.connect()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return results
    
    def search_doctor_by_id(self, doctor_id):
        """Search doctor by ID, return doctor name and specialization"""
        query = """
            SELECT d.doctor_id, s.staff_name, sp.specialization_name, 
                   d.consultation_fee, d.working_hours_start, 
                   d.working_hours_end, d.is_available
            FROM doctors d
            JOIN staff s ON d.staff_id = s.staff_id
            JOIN specializations sp ON d.specialization_id = sp.specialization_id
            WHERE d.doctor_id = %s
        """
        conn = self.connect()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, (doctor_id,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result
