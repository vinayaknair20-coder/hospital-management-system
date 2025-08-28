from dao.abstractpatientdao import PatientDaoService
from dao.patientDaoImp import PatientDaoImplementation
from models.patient import Patient
from models.appointments import Appointments
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

    #_________________________APPOINMENTS_____________________

   

    @staticmethod
    def book_appointment():
        try:
            # Get patient ID and validate
            patient_id = int(input('Enter Patient ID: '))
            patient = ReceptionistServices.dao_services.find_by_patient_id(patient_id)
            if not patient:
                print("Patient not found! Please add the patient first.")
                return

            print(f"Patient Name for ID {patient_id}: {patient.patient_name}")

            # Patient name validation
            while True:
                entered_name = input('Enter the patient name: ')
                if entered_name.strip().lower() == patient.patient_name.strip().lower():
                    patient_name = entered_name
                    break
                else:
                    print("Entered name does not match. Please try again.")

            # Get specializations
            specializations = ReceptionistServices.dao_services.get_specializations()
            if not specializations:
                print("No specializations available.")
                return

            print("Available Specializations:")
            for spec in specializations:
                print(f"{spec['specialization_id']} - {spec['specialization_name']}")

            # Get specialization choice
            while True:
                try:
                    specialization_id = int(input('Enter the specialization id: '))
                    if any(spec['specialization_id'] == specialization_id for spec in specializations):
                        break
                    print("Invalid specialization id!")
                except ValueError:
                    print("Please enter a valid number.")

            # Get appointment date
            while True:
                appointment_date = input("Enter the appointment date (YYYY-MM-DD): ")
                try:
                    appt_date_obj = datetime.strptime(appointment_date, "%Y-%m-%d").date()
                    if appt_date_obj >= datetime.today().date():
                        break
                    else:
                        print("Date cannot be in the past!")
                except ValueError:
                    print("Invalid date format!")

            # Get doctors for specialization
            doctors = ReceptionistServices.dao_services.get_doctors()
            filtered_doctors = [doc for doc in doctors if doc['specialization_id'] == specialization_id]
            
            if not filtered_doctors:
                print("No doctors available for this specialization.")
                return

            print("Available Doctors:")
            for doc in filtered_doctors:
                print(f"Doctor ID: {doc['doctor_id']}")

            # Get doctor choice
            while True:
                try:
                    doctor_id = int(input("Enter Doctor ID: "))
                    if any(doc['doctor_id'] == doctor_id for doc in filtered_doctors):
                        break
                    print("Invalid Doctor ID!")
                except ValueError:
                    print("Please enter a valid number.")

            # Get token number
            while True:
                try:
                    token_number = int(input("Enter token number (1-25): "))
                    if 1 <= token_number <= 25:
                        break
                    print("Token must be between 1-25!")
                except ValueError:
                    print("Please enter a valid number.")

            # Create and save appointment
            appointment = Appointments(
                patient_id=patient_id,
                patient_name=patient_name,
                appointment_date=appt_date_obj,
                doctor_id=doctor_id,
                token_number=token_number,
                specialization_id=specialization_id,
                status="SCHEDULED"
            )

            if ReceptionistServices.dao_services.add_appointment(appointment):
                print("Appointment booked successfully!")
            else:
                print("Failed to book appointment.")

        except Exception as e:
            print(f"Error while booking appointment: {e}")



        

    @staticmethod
    def display_all_appointments():
        appointments = ReceptionistServices.dao_services.display_all_appointments()
        if not appointments:
            print("No appointments found.")
        for appointment in appointments:
            print(appointment)
    

    @staticmethod
    def cancel_appointment():
        try:
            appointment_id = int(input("Enter Appointment ID to cancel: "))
            if ReceptionistServices.dao_services.cancel_appointment(appointment_id):
                print("Appointment cancelled successfully!")
            else:
                print("Error cancelling appointment. Please check the Appointment ID and try again.")
        except Exception as e:
            print("Error while cancelling appointment:", e)


    @staticmethod
    def reschedule_appointment():
        try:
            while True:
                try:
                    appointment_id = int(input("Enter Appointment ID to reschedule: "))
                    # Validate appointment exists
                    appointments = ReceptionistServices.dao_services.display_all_appointments()
                    appointment = next((a for a in appointments if a.appointment_id == appointment_id), None)

                    if not appointment:
                        print("Appointment not found!")
                        return

                    while True:
                        try:
                            new_date = input("Enter new appointment date (YYYY-MM-DD): ")
                            new_date_obj = datetime.strptime(new_date, "%Y-%m-%d").date()
                            today = datetime.today().date()
                            if new_date_obj >= today:
                                break
                            else:
                                print("Appointment date cannot be in the past! Please enter today or a future date.")
                        except ValueError:
                            print("Invalid date format! Please enter in YYYY-MM-DD format.")

                    if ReceptionistServices.dao_services.reschedule_appointment(appointment_id, str(new_date_obj)):
                        print("Appointment rescheduled successfully!")
                    else:
                        print("Failed to reschedule appointment.")
                    break
                except ValueError:
                    print("Invalid input! Please enter a numeric Appointment ID.")
        except Exception as e:
            print("Error while rescheduling appointment:", e)


    @staticmethod
    def search_appointment():
        try:
            patient_id = int(input("Enter Patient ID to search appointments: "))
            appointments = ReceptionistServices.dao_services.search_appointment_by_patient_id(patient_id)
            if not appointments:
                print("No appointments found for this patient.")
            for appointment in appointments:
                print(appointment)
        except Exception as e:
            print("Error while searching appointments:", e)



            