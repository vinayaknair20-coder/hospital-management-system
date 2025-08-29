# dao/implement.py
from dao.abstractDoctor import abstractdao
from db.db_connection import DBConnection
from models.consultation import Consultation
from models.appointments import Appointments
from models.prescription import Prescriptions, Med_prescriptions, Test_prescriptions
from pymysql.cursors import DictCursor

class Implementation(abstractdao):
    """
    Concrete DAO. Update table/column names in the CONFIG below if your schema differs.
    """
    # SQL / table config (change names here if your DB uses different column names)
    CONFIG = {
        "table_appointments": "appointments",
        "table_consultation": "consultation",
        "table_prescriptions": "prescriptions",
        "table_med_prescription": "med_prescription",
        "table_test_prescription": "test_prescription",
        "table_doctor": "doctor"
    }

    # prepared SQL using the above names (format at runtime)
    def __init__(self):
        self.conn = DBConnection().get_connection()

    def _t(self, name):
        return self.CONFIG[name]

    # ---------- helper low-level checks ----------
    def check_doctor_exists(self, doctor_id: int) -> bool:
        """
        Check if a doctor exists in the 'doctors' table.
        """
        cursor = None
        try:
            cursor = self.conn.cursor(DictCursor)
            sql = f"SELECT doctor_id FROM doctors WHERE doctor_id=%s"
            cursor.execute(sql, (doctor_id,))
            row = cursor.fetchone()
            if row:
                return True
            else:
                # Debug: list all doctor IDs in table
                print(f"Doctor id {doctor_id} not found. Current doctor IDs:")
                cursor.execute("SELECT doctor_id FROM doctors")
                all_docs = cursor.fetchall()
                print([r['doctor_id'] for r in all_docs])
                return False
        except Exception as e:
            print("Error checking doctor existence:", e)
            return False
        finally:
            if cursor:
                cursor.close()


    def get_appointment_by_id(self, appointment_id: int):
        cursor = None
        try:
            cursor = self.conn.cursor(DictCursor)
            sql = f"SELECT * FROM {self._t('table_appointments')} WHERE appointment_id=%s"
            cursor.execute(sql, (appointment_id,))
            row = cursor.fetchone()
            if not row:
                return None
            return Appointments(
                appointment_id=row['appointment_id'],
                patient_id=row['patient_id'],
                patient_name=row.get('patient_name'),
                doctor_id=row['doctor_id'],
                token_number=row.get('token_number'),
                appointment_date=row.get('appointment_date'),
                specialization_id=row.get('specialization_id'),
                status=row.get('status')
            )
        except Exception as e:
            print("Error while fetching appointment:", e)
            return None
        finally:
            if cursor:
                cursor.close()

        # ---------- appointments ----------
    def view_all_appointments(self, doc_id):
        cursor = None
        try:
            cursor = self.conn.cursor(DictCursor)

            # fast check if doctor has appointments
            sql_check = f"SELECT 1 FROM {self._t('table_appointments')} WHERE doctor_id=%s LIMIT 1"
            cursor.execute(sql_check, (doc_id,))
            if not cursor.fetchone():
                return []

            # fetch all appointments for doctor with patient name
            sql = f"""
                SELECT a.appointment_id, a.patient_id, p.patient_name, a.doctor_id,
                    a.token_number, a.appointment_date, a.status, a.specialization_id
                FROM {self._t('table_appointments')} a
                JOIN patients p ON a.patient_id = p.patient_id
                WHERE a.doctor_id=%s
                ORDER BY a.appointment_date, a.token_number
            """
            cursor.execute(sql, (doc_id,))
            rows = cursor.fetchall()

            appointments = []
            for row in rows:
                appointments.append(Appointments(
                    appointment_id=row['appointment_id'],
                    patient_id=row['patient_id'],
                    doctor_id=row['doctor_id'],
                    token_number=row.get('token_number'),
                    appointment_date=row.get('appointment_date'),
                    status=row.get('status'),
                    specialization_id=row.get('specialization_id'),
                    patient_name=row.get('patient_name')  # add patient_name for display
                ))

            return appointments

        except Exception as e:
            print("Error while displaying appointments:", e)
            return []

        finally:
            if cursor:
                cursor.close()


    # ---------- consultations ----------
    def create_consultation(self, consult: Consultation) -> bool:
        cursor = None
        try:
            cursor = self.conn.cursor()
            
            # validate appointment exists
            sql_check = f"""
                SELECT doctor_id 
                FROM {self._t('table_appointments')} 
                WHERE appointment_id=%s
            """
            cursor.execute(sql_check, (consult.appointment_id,))
            r = cursor.fetchone()
            
            if not r:
                print(f"Error: appointment_id {consult.appointment_id} does not exist.")
                return False

            # Handle dict or tuple safely
            doctor_id = r['doctor_id'] if isinstance(r, dict) else r[0]

            if int(doctor_id) != int(consult.doctor_id):
                print("Error: appointment does not belong to the provided doctor.")
                return False

            cursor.close()

            # insert consultation
            cursor = self.conn.cursor()
            sql = f"""
                INSERT INTO {self._t('table_consultation')}
                (appointment_id, symptoms, diagnosis, consultation_notes, doctor_id)
                VALUES (%s,%s,%s,%s,%s)
            """
            cursor.execute(sql, (
                consult.appointment_id,
                consult.symptoms,
                consult.diagnosis,
                consult.consultation_notes,
                consult.doctor_id
            ))
            self.conn.commit()
            
            print("Consultation created successfully!")
            return cursor.rowcount == 1

        except Exception as e:
            print("Error while inserting consultation:", e)
            return False
        finally:
            if cursor:
                cursor.close()


    def view_consultation_of_doctor(self, doctor_id):
        cursor = None
        try:
            cursor = self.conn.cursor(DictCursor)
            sql_check = f"SELECT 1 FROM {self._t('table_appointments')} WHERE doctor_id=%s LIMIT 1"
            cursor.execute(sql_check, (doctor_id,))
            if not cursor.fetchone():
                return []
            sql = f"SELECT c.*, a.specialization_id FROM {self._t('table_consultation')} c JOIN {self._t('table_appointments')} a ON c.appointment_id=a.appointment_id WHERE c.doctor_id=%s"
            cursor.execute(sql, (doctor_id,))
            rows = cursor.fetchall()
            res = []
            for row in rows:
                res.append(Consultation(
                    appointment_id=row['appointment_id'],
                    symptoms=row['symptoms'],
                    diagnosis=row['diagnosis'],
                    consultation_notes=row['consultation_notes'],
                    doctor_id=row['doctor_id'],
                    specialization_id=row['specialization_id']
                ))
            return res
        except Exception as e:
            print("Error while displaying consultations:", e)
            return []
        finally:
            if cursor:
                cursor.close()

    def view_consultation(self, patient_id, doctor_id):
        cursor = None
        try:
            cursor = self.conn.cursor(DictCursor)
            sql = f"SELECT c.*, a.specialization_id FROM {self._t('table_consultation')} c JOIN {self._t('table_appointments')} a ON c.appointment_id=a.appointment_id WHERE a.patient_id=%s AND a.doctor_id=%s"
            cursor.execute(sql, (patient_id, doctor_id))
            rows = cursor.fetchall()
            res = []
            for row in rows:
                res.append(Consultation(
                    appointment_id=row['appointment_id'],
                    symptoms=row['symptoms'],
                    diagnosis=row['diagnosis'],
                    consultation_notes=row['consultation_notes'],
                    doctor_id=row['doctor_id'],
                    specialization_id=row['specialization_id']
                ))
            return res
        except Exception as e:
            print("Error while displaying consultations:", e)
            return []
        finally:
            if cursor:
                cursor.close()

    # ---------- Prescription-related Methods ----------
    def get_or_create_prescription_for_appointment(self, appointment_id: int, consultation_id: int = None) -> int | None:
        """
        Checks if a prescription exists for a given appointment.
        If not, inserts a new one and returns prescription_id.
        Note: consultation_id parameter is kept for compatibility but not used in database.
        """
        cursor = None
        try:
            cursor = self.conn.cursor()
            # check existing
            cursor.execute(
                "SELECT prescription_id FROM prescriptions WHERE appointment_id=%s",
                (appointment_id,)
            )
            row = cursor.fetchone()
            if row:
                return row[0]  # existing prescription

            # insert new
            cursor.execute(
                "INSERT INTO prescriptions (appointment_id) VALUES (%s)",
                (appointment_id,)
            )
            self.conn.commit()
            return cursor.lastrowid
        except Exception as e:
            print("Error while creating prescription:", e)
            return None
        finally:
            if cursor:
                cursor.close()

    def create_med_prescription(self, med_pres: Med_prescriptions) -> bool:
        cursor = None
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "INSERT INTO med_prescription (prescription_id, medicine_name, medicine_quantity, dosage) "
                "VALUES (%s, %s, %s, %s)",
                (med_pres.prescription_id, med_pres.medicine_name, med_pres.medicine_quantity, med_pres.dosage)
            )
            self.conn.commit()
            return cursor.rowcount == 1
        except Exception as e:
            print("Error while inserting medicine prescription:", e)
            return False
        finally:
            if cursor:
                cursor.close()

    def create_test_prescription(self, test_pres: Test_prescriptions) -> bool:
        cursor = None
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "INSERT INTO test_prescription (prescription_id, test_name) "
                "VALUES (%s, %s)",
                (test_pres.prescription_id, test_pres.test_name)
            )
            self.conn.commit()
            return cursor.rowcount == 1
        except Exception as e:
            print("Error while inserting test prescription:", e)
            return False
        finally:
            if cursor:
                cursor.close()


    def get_patient_id_by_appointment(self, appointment_id):
        # return patient_id or None
        cursor = None
        try:
            cursor = self.conn.cursor()
            sql = f"SELECT patient_id FROM {self._t('table_appointments')} WHERE appointment_id=%s"
            cursor.execute(sql, (appointment_id,))
            row = cursor.fetchone()
            if not row:
                return None
            # row can be dict
            return row.get('patient_id') if isinstance(row, dict) else row[0]
        except Exception as e:
            print("Error while fetching patient_id:", e)
            return None
        finally:
            if cursor:
                cursor.close()
 

    def get_prescriptions_by_patient_id(self, patient_id: int) -> list:
        """
        Fetch all prescriptions for a given patient ID.
        Returns a list of dictionaries with prescription details.
        """
        cursor = None
        try:
            cursor = self.conn.cursor(DictCursor)
            sql = """
                SELECT prescription_id, appointment_id
                FROM prescriptions
                WHERE appointment_id IN (
                    SELECT appointment_id
                    FROM appointments
                    WHERE patient_id=%s
                )
            """
            cursor.execute(sql, (patient_id,))
            rows = cursor.fetchall()
            return rows if rows else []
        except Exception as e:
            print("Error fetching prescriptions by patient ID:", e)
            return []
        finally:
            if cursor:
                cursor.close()



    def get_med_prescriptions_by_prescription_id(self, prescription_id: int) -> list:
        cursor = None
        try:
            cursor = self.conn.cursor(DictCursor)
            sql = "SELECT medicine_name, medicine_quantity, dosage FROM med_prescription WHERE prescription_id=%s"
            cursor.execute(sql, (prescription_id,))
            return cursor.fetchall() or []
        except Exception as e:
            print("Error fetching medicine prescriptions:", e)
            return []
        finally:
            if cursor:
                cursor.close()

    def get_test_prescriptions_by_prescription_id(self, prescription_id: int) -> list:
        cursor = None
        try:
            cursor = self.conn.cursor(DictCursor)
            sql = "SELECT test_name FROM test_prescription WHERE prescription_id=%s"
            cursor.execute(sql, (prescription_id,))
            return cursor.fetchall() or []
        except Exception as e:
            print("Error fetching test prescriptions:", e)
            return []
        finally:
            if cursor:
                cursor.close()
