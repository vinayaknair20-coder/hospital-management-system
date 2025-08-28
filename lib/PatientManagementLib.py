from dao.abstractpatientdao import PatientDaoService
from dao.patientDaoImp import PatientDaoImplementation
from models.patient import Patient
from models.appointments import Appointments
from models.billing import Billing
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
            patient_id = int(input('Enter Patient ID: '))
            patient = ReceptionistServices.dao_services.find_by_patient_id(patient_id)
            if not patient:
                print("Patient not found! Please add the patient first.")
                return

            print(f"Patient Name for ID {patient_id}: {patient.patient_name}")

            # Patient name validation loop
            while True:
                entered_name = input('Enter the patient name: ')
                if entered_name.strip().lower() == patient.patient_name.strip().lower():
                    patient_name = entered_name
                    break
                else:
                    print("Entered name does not match the name for this Patient ID. Please try again.")

            # Specialization validation
            specializations = ReceptionistServices.dao_services.get_specializations()
            spec_ids = [spec[0] for spec in specializations]
            print("Available Specializations:")
            for spec in specializations:
                print(f"{spec[0]} - {spec[1]}")
            while True:
                specialization_id = int(input('Enter the specialization id: '))
                if specialization_id in spec_ids:
                    break
                print("Invalid specialization id! Please choose a valid one from the list above.")

            # Appointment date validation
            while True:
                appointment_date = input("Enter the appointment date (YYYY-MM-DD): ")
                try:
                    appt_date_obj = datetime.strptime(appointment_date, "%Y-%m-%d").date()
                    today = datetime.today().date()
                    if appt_date_obj >= today:
                        break
                    else:
                        print("Appointment date cannot be in the past! Please enter today or a future date.")
                except ValueError:
                    print("Invalid date format! Please enter in YYYY-MM-DD format.")

            # Doctor validation
            doctors = ReceptionistServices.dao_services.get_doctors()
            filtered_doctors = [doc for doc in doctors if doc[2] == specialization_id]
            valid_doctor_ids = [doc[0] for doc in filtered_doctors]
            print("Available Doctors with selected specialization:")
            for doc in filtered_doctors:
                print(f"{doc[0]} - {doc[2]}")
            while True:
                doctor_id = int(input("Enter Doctor ID: "))
                if doctor_id in valid_doctor_ids:
                    break
                print("Invalid Doctor ID! Please choose from the list above.")

            # Token selection + booking loop
            all_tokens = list(range(1, 26))  # 1–25 tokens

            while True:   # loop until appointment booked successfully
                booked_tokens = ReceptionistServices.dao_services.get_booked_tokens(doctor_id, appointment_date)

                print(f"Tokens for Doctor {doctor_id} on {appointment_date}:")
                print(f"Booked tokens: {booked_tokens}")

                try:
                    token_number = int(input("Enter the token number (1-25): "))

                    if token_number not in all_tokens:
                        print("Invalid token! Please enter a number between 1 and 25.")
                        continue
                    elif token_number in booked_tokens:
                        print(f"Token {token_number} is already taken! Please choose another one.")
                        continue

                    # Create appointment object
                    appointment = Appointments(
                        patient_id=patient_id,
                        patient_name=patient_name,
                        appointment_date=appt_date_obj,
                        doctor_id=doctor_id,
                        token_number=token_number,
                        specialization_id=specialization_id
                    )

                    #  Try booking
                    if ReceptionistServices.dao_services.add_appointment(appointment):
                        print("Appointment booked successfully.")
                        break  
                    else:
                        print("Failed to book appointment. Please try another token.")
                        continue

                except ValueError:
                    print("Invalid input! Please enter a numeric token number.")
        except Exception as e:
                print("Error while booking appointment:", e)
                print("Please try entering another token.")


        

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
#-----------BILLING----------------------------------------
    @staticmethod
    def add_bill():
        try:
            appointment_id = int(input("Enter Appointment ID: "))

            # Step 1: Fetch appointment details
            appointment = ReceptionistServices.dao_services.search_appointment_by_patient_id(appointment_id)
            if not appointment:
                print("Appointment not found! Please check the ID.")
                return
            patient_id = appointment.patient_id
            patient_name = appointment.patient_name
            doctor_id = appointment.doctor_id

            # Step 2: Fetch doctor consultation fee
            doctors = ReceptionistServices.dao_services.get_doctors()
            consultation_fee = None
            for doc in doctors:
                if doc[0] == doctor_id:
                    consultation_fee = doc[3]  # consultation_fee
                    break

            if consultation_fee is None:
                print("Doctor not found! Cannot fetch consultation fee.")
                return

            # Step 3: Display details
            print("\nAppointment Details:")
            print(f"Patient ID         : {patient_id}")
            print(f"Patient Name       : {patient_name}")
            print(f"Doctor ID          : {doctor_id}")
            print(f"Consultation Fee   : {consultation_fee}")

            # Step 4: Choose payment method
            payment_methods = ["Cash", "Card", "UPI"]
            print("Payment Methods:")
            for idx, method in enumerate(payment_methods, 1):
                print(f"{idx}. {method}")

            while True:
                try:
                    choice = int(input("Choose Payment Method (1-3): "))
                    if 1 <= choice <= 3:
                        payment_method = payment_methods[choice - 1]
                        break
                    else:
                        print("Invalid choice! Select 1, 2, or 3.")
                except ValueError:
                    print("Enter numeric choice only!")

            # Step 5: Insert bill
            bill = Billing(
                appointment_id=appointment_id,
                patient_id=appointment.patient_id,
                doctor_id=doctor_id,
                consultation_fee=consultation_fee,
                payment_method=payment_method,
                payment_status="",  # will be decided in DAO
                payment_date=datetime.now()
            )

            if ReceptionistServices.dao_services.insert_bill(bill):
                print("Bill inserted successfully!")
            else:
                print("Failed to insert bill!")

        except Exception as e:
            print("Error while adding bill:", e)

    @staticmethod
    def show_bill():
        try:
            patient_id = int(input("Enter Patient ID to view bills: "))
            bills = ReceptionistServices.dao_services.view_bill(patient_id)
            if not bills:
                print("No bills found for this patient.")
                return
            for bill in bills:
                print(bill)
        except Exception as e:
            print("Error while viewing bills:", e)


            