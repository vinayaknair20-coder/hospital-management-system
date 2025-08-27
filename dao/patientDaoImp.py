from datetime import datetime
from db.db_connection import DBConnection
from dao.abstractpatientdao import PatientDaoService
from models.patient import Patient
from typing import List
import pymysql

class PatientDaoImplementation(PatientDaoService):
    ADD_PATIENT = "INSERT INTO patients(patient_name,DOB,age,gender,blood_group,phone_number,email,address,emergency_contact) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    DISPLAY_ALL = "SELECT * from patients"
    FIND_BY_ID = "SELECT * from patients WHERE patient_id =%s"
    UPDATE_PATIENT = "UPDATE patients set patient_name=%s, age=%s WHERE patient_id =%s"
    def __init__(self):
        self.conn = DBConnection().get_connection() 

    def insert_patients(self,patient:Patient)->bool:
            try:
                cursor = self.conn.cursor()  #create a cursor object to connect it with databse 
                cursor.execute(self.ADD_PATIENT, (patient.patient_name,patient.DOB,patient.age,patient.gender,patient.blood_group,patient.phone_number,patient.email,patient.address,patient.emergency_contact))
                self.conn.commit()
                return cursor.rowcount == 1 
            except Exception as e:
                print("Error adding patients:",e)
                return False
            finally:
                cursor.close()

    def display_all_patients(self)->List[Patient]:
            patients=[]  #to store the records from db
            try:
                cursor = self.conn.cursor(pymysql.cursors.DictCursor)  #return data in dic 
                cursor.execute(self.DISPLAY_ALL) #fire the query
                rows = cursor.fetchall()
                for row in rows:
                    patients.append(Patient(patient_id=row["patient_id"],
                                            patient_name = row["patient_name"],#red names should be same as insert names which v r going to insrt as column name
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
                cursor = self.conn.cursor(pymysql.cursors.DictCursor)
                cursor.execute(self.FIND_BY_ID,(patient_id,))    #we put comma bcoz in tuple single value pass cheyumbo we should put comma
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
                cursor = self.conn.cursor(pymysql.cursors.DictCursor)
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


