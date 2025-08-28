from dao.abstractDoctor import abstractdao
from db.db_connection import DBConnection
from models.consultation import Consultation
from models.appointments import Appointments
from models.prescription import Prescriptions
from pymysql.cursors import DictCursor
class Implementation(abstractdao):
    '''handles all database operations'''
    view_appointments='select * from appointments where doctor_id=%s'
    view_app_count=" SELECT 25 - COUNT(*) FROM appointments WHERE doctor_id = %s AND appointment_date = CURDATE();"
    insert_consultation='insert into consultation (appointment_id,symptoms,diagnosis,consultation_notes,doctor_id) values(%s,%s,%s,%s,%s)'
    view_consultations='select * from consultation c join appointments a on c.appointment_id=a.appointment_id where a.patient_id=%s '
    insert_prescription= 'insert into prescriptions (appointment_id) values(%s)'
    view_prescription_by_appoint_id='select * from prescriptions where appointment_id=%s'

    # update_status='update appointments set status="active" where appointment_id=%s'

    # constructor to create connection object
    def __init__(self):
        self.conn=DBConnection().get_connection()

    def view_all_appointments(self,doc_id):
        cursor=None
        try:
            appointments=[]
            cursor=self.conn.cursor(DictCursor)
            cursor.execute(self.view_appointments,(doc_id))
            rows=cursor.fetchall()
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
            print('error while displaying appointments ',e)
        finally:
            cursor.close()
        return appointments
            

    def create_consulatation(self,consult:Consultation):
        cursor=None
        try:
            cursor=self.conn.cursor()
            cursor.execute(self.insert_consultation,(consult.appointment_id,consult.symptoms,consult.diagonis,consult.consultation_notes,consult.doctor_id))
            self.conn.commit()
            return cursor.rowcount==1
        except Exception as e:
            print('error while inserting consultation : ',e)
            return False
        finally:
            cursor.close()


    def view_consultation(self,patient_id):
        try:
            consultation=[]
            cursor=self.conn.cursor(DictCursor)
            cursor.execute(self.view_consultations,(patient_id,))
            rows=cursor.fetchall()
            for row in rows:
                consultation.append(Consultation(appointment_id=row['appointment_id'],
                                                symptoms=row['symptoms'],
                                                diagnosis=row['diagnosis'],
                                                consultation_notes=row['consultation_notes'],
                                                doctor_id=row['doctor_id']))
        except Exception as e:
            print('error while displaying consultations: ', e)
        finally:
            cursor.close()
        return consultation


    def view_count(self,doctor_id):
        cursor=self.conn.cursor()
        cursor.execute(self.view_app_count,(doctor_id,))
        count=cursor.fetchone()
        return f'total_count={count}'
    
    def create_prescription(self,prescription:Prescriptions):
        cursor=None
        try:
            cursor=self.conn.cursor()
            cursor.execute(self.insert_prescription,(prescription.appointment_id))
            self.conn.commit()
            return cursor.rowcount==1
        except Exception as e:
            print('error while inserting prescription: ',e)
            return False
        finally:
            cursor.close()

    def display_prescription(self,prescription:Prescriptions):
        cursor=None
        prescriptions=[]
        try:
            cursor=self.conn.cursor(DictCursor)
            cursor.execute(self.view_prescription_by_appoint_id,(prescription.appointment_id,))
            rows=cursor.fetchall()
            for row in rows:
                prescriptions.append(Prescriptions(row['prescription_id'], 
                                                   row['appointment_id']))
                
        except Exception as e:
            print('error while displaying: ', e)

        finally:
            cursor.close()
        return prescriptions
