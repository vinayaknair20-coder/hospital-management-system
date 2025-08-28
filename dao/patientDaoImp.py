from datetime import datetime
from db.db_connection import DBConnection
from dao.abstractpatientdao import PatientDaoService
from models.patient import Patient
from models.appointments import Appointments
from models.billing import Billing
from typing import List
from pymysql.cursors import DictCursor

class PatientDaoImplementation(PatientDaoService):
    ADD_PATIENT = "INSERT INTO patients(patient_name,DOB,age,gender,blood_group,phone_number,email,address,emergency_contact) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    DISPLAY_ALL = "SELECT * from patients"
    FIND_BY_ID = "SELECT * from patients WHERE patient_id =%s"
    UPDATE_PATIENT = "UPDATE patients set patient_name=%s, age=%s WHERE patient_id =%s"
    INSERT_APPOINTMENT = "INSERT INTO appointments (patient_id, patient_name, appointment_date, doctor_id, status, token_number, specialization_id) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    DISPLAY_ALL_APPOINTMENTS = "SELECT * FROM appointments"
    CANCEL_APPOINTMENT = "UPDATE appointments SET status='CANCELLED' WHERE appointment_id=%s"
    RESCHEDULE_APPOINTMENT = "UPDATE appointments SET appointment_date=%s WHERE appointment_id=%s"
    SEARCH_APPOINTMENT_BY_PATIENT_ID = "SELECT * FROM appointments WHERE patient_id=%s"
    INSERT_BILL = "INSERT INTO receptionist_billing (patient_id, appointment_id, doctor_id, consultation_fee, payment_status, payment_method, payment_date) VALUES(%s,%s,%s,%s,%s,%s,%s)"
    VIEW_BILL = "SELECT bill_id, patient_id, appointment_id, doctor_id, consultation_fee, payment_status, payment_method, payment_date FROM receptionist_billing WHERE patient_id=%s"




    def __init__(self):
        self.conn = DBConnection().get_connection() 

    def insert_patients(self,patient:Patient)->bool:
        try:
            cursor = self.conn.cursor(DictCursor)
            cursor.execute(self.ADD_PATIENT, (patient.patient_name,patient.DOB,patient.age,patient.gender,patient.blood_group,patient.phone_number,patient.email,patient.address,patient.emergency_contact))
            self.conn.commit()
            return cursor.rowcount == 1 
        except Exception as e:
            print("Error adding patients:",e)
            return False
        finally:
            cursor.close()

    def display_all_patients(self)->List[Patient]:
        patients=[]
        try:
            cursor = self.conn.cursor(DictCursor)
            cursor.execute(self.DISPLAY_ALL)
            rows = cursor.fetchall()
            for row in rows:
                patients.append(Patient(patient_id=row["patient_id"],
                                        patient_name = row["patient_name"],
                                        DOB= row["DOB"],
                                        age= row["age"],
                                        gender = row["gender"],
                                        blood_group =row["blood_group"],
                                        phone_number=row["phone_number"],
                                        email=row["email"],
                                        address=row["address"],
                                        emergency_contact=row["emergency_contact"],
                                        is_active=row["is_active"]))
        except Exception as e:
            print("Error fetching patients:",e)
        finally:
            cursor.close()
        return patients

    def find_by_patient_id(self, patient_id:int):
        patient = None
        try:
            cursor = self.conn.cursor(DictCursor)
            cursor.execute(self.FIND_BY_ID,(patient_id,))
            row = cursor.fetchone()
            if row:
                patient =Patient(patient_id=row["patient_id"],
                                 patient_name = row["patient_name"],
                                 DOB = row["DOB"],
                                 age= row["age"],
                                 gender = row["gender"],
                                 blood_group =row["blood_group"],
                                 phone_number=row["phone_number"],
                                 email=row["email"],
                                 address=row["address"],
                                 emergency_contact=row["emergency_contact"]) 
        except Exception as e:
            print("Error finding patient:",e)
        finally:
            cursor.close()
        return patient
        
    def update_patient(self,patient:Patient,patient_id:int)->bool:
        try:
            cursor = self.conn.cursor(DictCursor)
            cursor.execute(self.UPDATE_PATIENT,
                           (patient.patient_name,
                           patient.age,patient_id))
            self.conn.commit()
            return cursor.rowcount ==1
        except Exception as e:
            print("Error updating patient:",e)
            return False
        finally:
            cursor.close()
 
    # Appointments
    def get_specializations(self):
        """
        Fetch all specializations from DB and return as list of dictionaries.
        """
        try:
            cursor = self.conn.cursor(DictCursor)
            cursor.execute("SELECT specialization_id, specialization_name FROM specializations")
            specializations = cursor.fetchall()
            return specializations
        except Exception as e:
            print("Error fetching specializations:", e)
            return []
        finally:
            cursor.close()

    def get_doctors(self):
        """
        Fetch all doctors from DB and return as list of dictionaries.
        """
        try:
            cursor = self.conn.cursor(DictCursor)
            cursor.execute("SELECT doctor_id, staff_id, specialization_id, consultation_fee, working_hours_start, working_hours_end, is_available FROM doctors")
            doctors = cursor.fetchall()
            return doctors
        except Exception as e:
            print("Error fetching doctors:", e)
            return []
        finally:
            cursor.close()

    def get_booked_tokens(self, doctor_id, appointment_date):
        """
        Returns a list of token_numbers already booked for the given doctor and date.
        """
        try:
            cursor = self.conn.cursor(DictCursor)
            cursor.execute(
                "SELECT token_number FROM appointments WHERE doctor_id=%s AND appointment_date=%s",
                (doctor_id, appointment_date)
            )
            rows = cursor.fetchall()
            # Fix: Access dictionary values correctly
            booked = [row['token_number'] for row in rows]
            return booked
        except Exception as e:
            print("Error fetching booked tokens:", e)
            return []
        finally:
            cursor.close()

    def add_appointment(self, appointment: Appointments):
        cursor = None
        try:
            # Ensure connection is active
            self.conn.ping(reconnect=True)
            cursor = self.conn.cursor(DictCursor)
            
            print(f"DEBUG: Attempting to insert appointment for patient {appointment.patient_id}")
            
            # Check if token is already booked
            cursor.execute(
                "SELECT COUNT(*) FROM appointments WHERE doctor_id=%s AND appointment_date=%s AND token_number=%s",
                (appointment.doctor_id, appointment.appointment_date, appointment.token_number)
            )
            if cursor.fetchone()['COUNT(*)'] > 0:
                print("ERROR: Token number already booked for this doctor and date!")
                return False

            # Execute the INSERT statement
            print(f"DEBUG: Executing INSERT with params: {appointment.patient_id}, {appointment.patient_name}, {appointment.appointment_date}, {appointment.doctor_id}, {appointment.status}, {appointment.token_number}, {appointment.specialization_id}")
            
            cursor.execute(self.INSERT_APPOINTMENT, (
                appointment.patient_id,
                appointment.patient_name,
                str(appointment.appointment_date),  # Convert date to string
                appointment.doctor_id,
                appointment.status,
                appointment.token_number,
                appointment.specialization_id
            ))
            
            # Commit the transaction immediately
            self.conn.commit()
            
            rows_affected = cursor.rowcount
            print(f"DEBUG: Rows affected: {rows_affected}")
            
            if rows_affected == 1:
                print("SUCCESS: Appointment inserted successfully!")
                return True
            else:
                print(f"WARNING: INSERT affected {rows_affected} rows instead of 1")
                return False

        except Exception as e:
            print(f"ERROR: Database exception occurred")
            print(f"ERROR: Exception type: {type(e).__name__}")
            print(f"ERROR: Exception message: {str(e)}")
            print(f"ERROR: Exception args: {e.args}")
            
            # Rollback transaction on error
            if self.conn:
                try:
                    self.conn.rollback()
                    print("DEBUG: Transaction rolled back")
                except:
                    pass
            return False
        finally:
            if cursor:
                cursor.close()

    def display_all_appointments(self) -> List[Appointments]:
        appointments = []
        try:
            cursor = self.conn.cursor(DictCursor)
            cursor.execute("SELECT * FROM appointments")
            rows = cursor.fetchall()
            for row in rows:
                appointments.append(Appointments(
                    appointment_id=row["appointment_id"],
                    patient_id=row["patient_id"],
                    patient_name=row["patient_name"],
                    doctor_id=row["doctor_id"],
                    appointment_date=row["appointment_date"],
                    token_number=row["token_number"],
                    specialization_id=row["specialization_id"],
                    status=row["status"]
                ))
        except Exception as e:
            print("Error fetching appointments:", e)
        finally:
            cursor.close()
        return appointments
    
    def cancel_appointment(self, appointment_id: int) -> bool:
        try:
            cursor = self.conn.cursor(DictCursor)
            cursor.execute(self.CANCEL_APPOINTMENT, (appointment_id,))
            self.conn.commit()
            return cursor.rowcount == 1
        except Exception as e:
            print("Error cancelling appointment:", e)
            return False
        finally:
            cursor.close()

    def reschedule_appointment(self, appointment_id: int, new_date: str) -> bool:
        try:
            cursor = self.conn.cursor(DictCursor)
            cursor.execute(self.RESCHEDULE_APPOINTMENT, (new_date, appointment_id))
            self.conn.commit()
            return cursor.rowcount == 1
        except Exception as e:
            print("Error rescheduling appointment:", e)
            return False
        finally:
            cursor.close()

    def search_appointment_by_patient_id(self, patient_id: int):
        try:
            cursor = self.conn.cursor(DictCursor)
            cursor.execute(self.SEARCH_APPOINTMENT_BY_PATIENT_ID, (patient_id,))
            rows = cursor.fetchall()
            appointments = []
            for row in rows:
                appointments.append(Appointments(
                    appointment_id=row["appointment_id"],
                    patient_id=row["patient_id"],
                    patient_name=row["patient_name"],
                    doctor_id=row["doctor_id"],
                    appointment_date=row["appointment_date"],
                    token_number=row["token_number"],
                    specialization_id=row["specialization_id"],
                    status=row["status"]
                ))
            return appointments
        except Exception as e:
            print("Error searching appointments:", e)
            return []
        finally:
            cursor.close()
#-------------BILLING-----------------------------
    def search_appointment_by_id(self, appointment_id: int):
        """
        Fetch a single appointment by appointment_id.
        Returns an Appointments object or None if not found.
        """
        try:
            cursor = self.conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM appointments WHERE appointment_id = %s", (appointment_id,))
            row = cursor.fetchone()
            if row:
                return Appointments(
                    appointment_id=row["appointment_id"],
                    patient_id=row["patient_id"],
                    patient_name=row["patient_name"],
                    doctor_id=row["doctor_id"],
                    appointment_date=row["appointment_date"],
                    token_number=row["token_number"],
                    specialization_id=row["specialization_id"],
                    status=row["status"]
                )
            else:
                return None
        except Exception as e:
            print("Error fetching appointment by ID:", e)
            return None
        finally:
            cursor.close()

    
    def insert_bill(self, bill: Billing) -> bool:
        try:
            cursor = self.conn.cursor()

            # Step 1: Fetch patient_id and doctor_id from appointments
            cursor.execute("SELECT patient_id, doctor_id FROM appointments WHERE appointment_id = %s",
                        (bill.appointment_id,))
            appointment = cursor.fetchone()
            if not appointment:
                print("Invalid Appointment ID!")
                return False
            patient_id, doctor_id = appointment

            # Step 2: Fetch consultation fee from doctors table
            cursor.execute("SELECT consultation_fee FROM doctors WHERE doctor_id = %s", (doctor_id,))
            doc = cursor.fetchone()
            if not doc:
                print("Doctor not found!")
                return False
            consultation_fee = doc[0]

            # Step 3: Set payment status automatically
            payment_status = "COMPLETED" if bill.consultation_fee >= consultation_fee else "PENDING"

            # Step 4: Insert into billing table
            cursor.execute(self.INSERT_BILL, (
                patient_id,
                bill.appointment_id,
                doctor_id,
                consultation_fee,
                payment_status,
                bill.payment_method,
                bill.payment_date
            ))
            self.conn.commit()
            return cursor.rowcount == 1

        except Exception as e:
            print("Error adding bill:", e)
            return False
        finally:
            cursor.close()


    def view_bill(self, patient_id: int) -> List[Billing]:
        bills = []
        try:
            cursor = self.conn.cursor(dictionary=True)
            cursor.execute(self.VIEW_BILL, (patient_id,))
            rows = cursor.fetchall()
            for row in rows:
                bills.append(Billing(bill_id=row["bill_id"],
                                     patient_id=row["patient_id"],
                                     appointment_id=row["appointment_id"],
                                     doctor_id=row["doctor_id"],
                                     consultation_fee=row["consultation_fee"],
                                     payment_status=row["payment_status"],
                                     payment_method=row["payment_method"],
                                     payment_date=row["payment_date"]))
        except Exception as e:
            print("Error fetching bills:", e)
        finally:
            cursor.close()
        return bills

