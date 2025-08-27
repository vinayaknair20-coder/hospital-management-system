from dao.Doctor_implement import Implementation
from dao.abstractDoctor import abstractdao
from models.appointments import Appointments 
from models.consultation import Consultation
from models.prescription import Prescriptions
from datetime import datetime

class DoctorServices:
    # creating class variable of abstract type
    dao_services:abstractdao=Implementation()

    @staticmethod
    def display_appointments():
        doc_id=int(input('enter doctor id: '))
        appointments=DoctorServices.dao_services.view_all_appointments(doc_id)
        for appoint in appointments:
            print(appoint)
        count=DoctorServices.dao_services.view_count(doc_id)
        print(count)

    @staticmethod
    def create_new_consultation():
            try:
                appointment_id=int(input('enter appointment id: '))
                # validation
                symptoms=input('enter symptoms:')
                diagnosis=input('enter diagnosis(max:100 words): ')
                consultation_notes=input('enter consultation_notes(max:100 words): ')
                doctor_id=int(input('enter doctor id: '))
                consult= Consultation(appointment_id=appointment_id,symptoms=symptoms,diagnosis=diagnosis,consultation_notes=consultation_notes,doctor_id=doctor_id)
                if DoctorServices.dao_services.create_consulatation(consult):
                    print('inserted successfully!!')
                else:
                    print('something went wrong!!')
            except Exception as e:
                 print('error while validating input: ',e)

    @staticmethod
    def view_patient_consultation():
        patient_id=int(input('enter patient id:' ))
        #  doc_id=int(input('enter doctor id: '))
        consultations=DoctorServices.dao_services.view_consultation(patient_id)
        for consult in consultations:
             print(consult)

    @staticmethod
    def create_prescription():
        try:
            appointment_id=int(input('enter patient appointment id: '))
            prescription=Prescriptions(appointment_id=appointment_id)
            if DoctorServices.dao_services.create_prescription(prescription):
                print('prescription inserted succesfully!')
            else:
                print('something went wrong!!')
        except Exception as e:
            print('error while validating input: ',e)

    
    @staticmethod
    def view_prescription_by_app_id():
        try:
            appointment_id=int(input('enter patient appointment id: '))
            prescription=Prescriptions(appointment_id=appointment_id)
            total_prescription=DoctorServices.dao_services.display_prescription(prescription)
            for a in total_prescription:
                print(a)
        except Exception as e:
            print('error while validating input: ',e)
