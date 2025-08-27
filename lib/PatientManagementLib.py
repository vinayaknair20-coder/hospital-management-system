from dao.abstractpatientdao import PatientDaoService
from dao.patientDaoImp import PatientDaoImplementation
from models.patient import Patient
from datetime import datetime
from validation.receptionist_validation import validate_name,validate_DOB,validate_age,validate_gender,validate_blood_group,validate_phone_number,validate_email,validate_address,validate_emergency_contact

class ReceptionistServices:
    # creating abstract variaable to access implementation
    dao_services:PatientDaoService=PatientDaoImplementation()

    @staticmethod
    def add_patients():
        try:
            # Patient Name
            while True:
                try:
                    patient_name = input('Enter Patient Name: ')
                    validate_name(patient_name)
                    break
                except ValueError as e:
                    print(e)

            # DOB
            while True:
                try:
                    dob = input("Enter the DOB in YYYY/MM/DD format: ")
                    dob = validate_DOB(dob)   
                    break
                except ValueError as e:
                    print(e)

            # Age
            while True:
                try:
                    age = int(input('Enter Patient Age: '))
                    validate_age(age)
                    break
                except ValueError as e:
                    print(e)

            # Gender
            while True:
                try:
                    gender = input('Enter Patient Gender (M/F): ')
                    validate_gender(gender)
                    break
                except ValueError as e:
                    print(e)

            # Blood Group
            while True:
                try:
                    blood_group = input("Enter Patient Blood Group: ")
                    validate_blood_group(blood_group)
                    break
                except ValueError as e:
                    print(e)

            # Phone Number
            while True:
                try:
                    phone_num = input('Enter Phone Number: ')
                    validate_phone_number(phone_num)
                    break
                except ValueError as e:
                    print(e)

            # Email
            while True:
                try:
                    email = input('Enter Email ID: ')
                    validate_email(email)
                    break
                except ValueError as e:
                    print(e)

            # Address
            while True:
                try:
                    address = input('Enter Address: ')
                    validate_address(address)
                    break
                except ValueError as e:
                    print(e)

            # Emergency Contact
            while True:
                try:
                    emergency_contact_number = input('Enter Emergency Contact: ')
                    validate_emergency_contact(emergency_contact_number)
                    break
                except ValueError as e:
                    print(e)
            patient = Patient(
                patient_name=patient_name,
                DOB=dob,
                age=age,
                gender=gender,
                blood_group=blood_group,
                phone_number=phone_num,
                email=email,
                address=address,
                emergency_contact=emergency_contact_number
            )

            if ReceptionistServices.dao_services.insert_patients(patient):
                print('Patient inserted successfully!!')
            else:
                print('Something went wrong!!')

        except Exception as e:
            print('Error while adding patients:', e)

    @staticmethod
    def display_all():
        patients = ReceptionistServices.dao_services.display_all_patients()
        if not patients:
            print("No patients found.")
        for patient in patients:
            print(patient)
    
    @staticmethod
    def update_patient():
        try:
            search_id=int(input('Enter Patient ID to update:'))
            patients = ReceptionistServices.dao_services.find_by_patient_id(search_id)
            if not patients:
                print("Patient not found !!!")
                return
            print("current Record:",patients)

            confirm = input("Do you want to edit this data? (y/n): ")
            if confirm.lower() == 'y':
                new_name = input("Enter new name (leave blank to keep same): ")
                new_age = input("Enter new age (leave blank to keep same): ")

                if new_name.strip():
                    patients.patient_name = new_name
                if new_age.strip():
                    patients.age = int(new_age)

                if ReceptionistServices.dao_services.update_patient(patient=patients,patient_id=search_id):
                    print("Patient updated successfully.")
                else:
                    print("Something went wrong while updating patient.")
        except Exception as e:
            print("Error while updating patient:", e)

    @staticmethod
    def search_patient():
        try:
            search_id = int(input("Enter the Patient ID to search: "))
            patient = ReceptionistServices.dao_services.find_by_patient_id(search_id)
            if not patient:
                print("Patient not found.")
                return
            print(patient)
        except Exception as e:
            print("Error while searching patient:", e)


            