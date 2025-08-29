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
#-----------BILLING----------------------------------------
    @staticmethod
    def add_bill():
        try:
            appointment_id = int(input("Enter Appointment ID: "))

            # Step 1: Check if bill already exists
            if ReceptionistServices.dao_services.check_bill_exists(appointment_id):
                print("A bill already exists for this appointment!")
                print("Each appointment can only have one bill.")
                return
            
            # Step 2: Fetch appointment details with consultation fee
            appointment_details = ReceptionistServices.dao_services.get_appointment_details_for_billing(appointment_id)
            if not appointment_details:
                print("Appointment not found! Please check the ID.")
                return
            
            patient_id = appointment_details['patient_id']
            patient_name = appointment_details['patient_name']
            doctor_id = appointment_details['doctor_id']
            consultation_fee = appointment_details['consultation_fee']

            # Step 2: Display appointment details
            print("\n" + "="*50)
            print("APPOINTMENT DETAILS FOR BILLING")
            print("="*50)
            print(f"Appointment ID     : {appointment_id}")
            print(f"Patient ID         : {patient_id}")
            print(f"Patient Name       : {patient_name}")
            print(f"Doctor ID          : {doctor_id}")
            print(f"Consultation Fee   : ₹{consultation_fee}")
            print("="*50)

            # Step 3: Choose payment method
            payment_methods = ["Cash", "Card", "UPI", "Net Banking"]
            print("\nAvailable Payment Methods:")
            for idx, method in enumerate(payment_methods, 1):
                print(f"{idx}. {method}")

            while True:
                try:
                    choice = int(input("\nChoose Payment Method (1-4): "))
                    if 1 <= choice <= 4:
                        payment_method = payment_methods[choice - 1]
                        break
                    else:
                        print("Invalid choice! Select 1, 2, 3, or 4.")
                except ValueError:
                    print("Enter numeric choice only!")

            # Step 4: Confirm billing
            print(f"\nPayment Method Selected: {payment_method}")
            confirm = input("Proceed with bill generation? (y/n): ").lower().strip()
            
            if confirm != 'y':
                print("Bill generation cancelled.")
                return

            # Step 5: Create and insert bill
            bill = Billing(
                appointment_id=appointment_id,
                patient_id=patient_id,
                doctor_id=doctor_id,
                consultation_fee=consultation_fee,
                payment_method=payment_method,
                payment_status="COMPLETED",
                payment_date=datetime.now()
            )

            print("\nGenerating bill...")
            if ReceptionistServices.dao_services.insert_bill(bill):
                print("Bill generated successfully!")
                print(f"Bill Details:")
                print(f"- Appointment ID: {appointment_id}")
                print(f"- Patient: {patient_name}")
                print(f"- Amount: ₹{consultation_fee}")
                print(f"- Payment Method: {payment_method}")
                print(f"- Status: COMPLETED")
            else:
                print("Failed to generate bill! Please try again.")

        except ValueError as ve:
            print("Invalid input! Please enter a valid appointment ID.")
        except Exception as e:
            print(f"Error while generating bill: {e}")
            print("Please check if the appointment exists and try again.")

    @staticmethod
    def show_bill():
        try:
            patient_id = int(input("Enter Patient ID to view bills: "))
            bills = ReceptionistServices.dao_services.view_bill(patient_id)
            if not bills:
                print("No bills found for this patient.")
                return
            
            print("\n" + "="*60)
            print(f"BILLING HISTORY FOR PATIENT ID: {patient_id}")
            print("="*60)
            
            for i, bill in enumerate(bills, 1):
                print(f"\nBILL #{i}")
                print("-" * 40)
                print(f"Bill ID           : {bill.bill_id}")
                print(f"Appointment ID    : {bill.appointment_id}")
                print(f"Doctor ID         : {bill.doctor_id}")
                print(f"Consultation Fee  : ₹{bill.consultation_fee}")
                print(f"Payment Status    : {bill.payment_status}")
                print(f"Payment Method    : {bill.payment_method}")
                if bill.payment_date:
                    print(f"Bill Date         : {bill.payment_date}")
                print("-" * 40)
            
            print(f"\nTotal Bills Found: {len(bills)}")
            print("="*60)
            
        except ValueError as ve:
            print("Invalid input! Please enter a valid patient ID.")
        except Exception as e:
            print(f"Error while viewing bills: {e}")

    @staticmethod
    def display_all_bills():
        """Display all bills for administrative purposes"""
        try:
            bills = ReceptionistServices.dao_services.get_all_bills()
            if not bills:
                print("No bills found in the system.")
                return
            
            print("\n" + "="*80)
            print("ALL BILLS IN THE SYSTEM")
            print("="*80)
            
            total_revenue = 0
            for i, bill in enumerate(bills, 1):
                print(f"\nBILL #{i}")
                print("-" * 50)
                print(f"Bill ID           : {bill.bill_id}")
                print(f"Appointment ID    : {bill.appointment_id}")
                print(f"Patient ID        : {bill.patient_id}")
                print(f"Doctor ID         : {bill.doctor_id}")
                print(f"Consultation Fee  : ₹{bill.consultation_fee}")
                print(f"Payment Status    : {bill.payment_status}")
                print(f"Payment Method    : {bill.payment_method}")
                if bill.payment_date:
                    print(f"Bill Date         : {bill.payment_date}")
                print("-" * 50)
                total_revenue += bill.consultation_fee
            
            print(f"\nSUMMARY")
            print(f"Total Bills       : {len(bills)}")
            print(f"Total Revenue     : ₹{total_revenue}")
            print("="*80)
            
        except Exception as e:
            print(f"Error while displaying all bills: {e}")

    @staticmethod
    def receptionist_main_menu():
        """Main receptionist menu with all services"""
        while True:
            print("\n========== Welcome to Receptionist Dashboard ==========")
            print("============== SERVICES ================")
            print("1. PATIENT")
            print("2. APPOINTMENTS")
            print("3. BILLING")
            print("4. EXIT")
            
            choice = input("Enter your choice: ").strip()
            
            if choice == "1":
                ReceptionistServices.patient_menu()
            elif choice == "2":
                ReceptionistServices.appointment_menu()
            elif choice == "3":
                ReceptionistServices.billing_menu()
            elif choice == "4":
                print("Logging out from Receptionist Dashboard...")
                break
            else:
                print("Invalid choice! Please select 1, 2, 3, or 4.")

    @staticmethod
    def patient_menu():
        """Patient management submenu"""
        while True:
            print("\n--- PATIENT MANAGEMENT ---")
            print("1. Add Patient")
            print("2. Display All Patients")
            print("3. Update Patient")
            print("4. Search Patient")
            print("5. Back to Main Menu")
            
            choice = input("Enter your choice: ").strip()
            
            if choice == "1":
                ReceptionistServices.add_patients()
            elif choice == "2":
                ReceptionistServices.display_all()
            elif choice == "3":
                ReceptionistServices.update_patient()
            elif choice == "4":
                ReceptionistServices.search_patient()
            elif choice == "5":
                break
            else:
                print("Invalid choice! Please select 1-5.")

    @staticmethod
    def appointment_menu():
        """Appointment management submenu"""
        while True:
            print("\n--- APPOINTMENT MANAGEMENT ---")
            print("1. Book Appointment")
            print("2. Display All Appointments")
            print("3. Cancel Appointment")
            print("4. Reschedule Appointment")
            print("5. Search Appointments by Patient ID")
            print("6. Back to Main Menu")
            
            choice = input("Enter your choice: ").strip()
            
            if choice == "1":
                ReceptionistServices.book_appointment()
            elif choice == "2":
                ReceptionistServices.display_all_appointments()
            elif choice == "3":
                ReceptionistServices.cancel_appointment()
            elif choice == "4":
                ReceptionistServices.reschedule_appointment()
            elif choice == "5":
                ReceptionistServices.search_appointment()
            elif choice == "6":
                break
            else:
                print("Invalid choice! Please select 1-6.")

    @staticmethod
    def billing_menu():
        """Billing management submenu"""
        while True:
            print("\n--- BILLING MANAGEMENT ---")
            print("1. Generate Bill")
            print("2. View Bill by Patient ID")
            print("3. View All Bills")
            print("4. Back to Main Menu")
            
            choice = input("Enter your choice: ").strip()
            
            if choice == "1":
                ReceptionistServices.add_bill()
            elif choice == "2":
                ReceptionistServices.show_bill()
            elif choice == "3":
                ReceptionistServices.display_all_bills()
            elif choice == "4":
                break
            else:
                print("Invalid choice! Please select 1-4.")


            