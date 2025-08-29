# lib/menudriven.py
from dao.Doctor_implement import Implementation
from dao.abstractDoctor import abstractdao
from models.appointments import Appointments
from models.consultation import Consultation
from models.prescription import Prescriptions, Med_prescriptions, Test_prescriptions

class DoctorServices:
    dao_services: abstractdao = Implementation()

    # small helpers for validated inputs (used in CLI)
    @staticmethod
    def _get_int(prompt: str, min_value: int = None) -> int:
        while True:
            raw = input(prompt).strip()
            try:
                val = int(raw)
                if min_value is not None and val < min_value:
                    print(f"❌ Value must be >= {min_value}")
                    continue
                return val
            except ValueError:
                print("❌ Please enter a valid number.")

    @staticmethod
    def _get_non_empty(prompt: str, max_len: int = None) -> str:
        while True:
            val = input(prompt).strip()
            if not val:
                print("❌ This field cannot be empty.")
                continue
            if max_len and len(val) > max_len:
                print(f"❌ Max length is {max_len} characters.")
                continue
            return val

    @staticmethod
    def display_appointments():
        doc_id = DoctorServices._get_int("Enter doctor id: ", 1)
        if not DoctorServices.dao_services.check_doctor_exists(doc_id):
            print(f"⚠ Doctor id {doc_id} does not exist.")
            return

        appointments = DoctorServices.dao_services.view_all_appointments(doc_id)
        if not appointments:
            print("⚠ No appointments found.")
            return

        print(f"\n--- Appointments for Doctor ID {doc_id} ---")
        for a in appointments:
            print(
                f"Token: {a.token_number}\t"
                f"Patient: {a.patient_name} (ID: {a.patient_id})\t"
                f"Appointment ID: {a.appointment_id}\t"
                f"Date: {a.appointment_date}\t"
                f"Status: {a.status}"
            )




    # Consultations
    @staticmethod
    def create_new_consultation():
        try:
            appointment_id = DoctorServices._get_int("Enter appointment id: ", 1)
            # fetch appointment record to validate and get doctor id
            appt = DoctorServices.dao_services.get_appointment_by_id(appointment_id)
            if not appt:
                print(f"⚠ Appointment id {appointment_id} not found.")
                return
            doctor_id = DoctorServices._get_int("Enter doctor id: ", 1)
            if not DoctorServices.dao_services.check_doctor_exists(doctor_id):
                print(f"⚠ Doctor id {doctor_id} does not exist.")
                return
            # Ensure appointment belongs to this doctor
            if int(appt.doctor_id) != int(doctor_id):
                print("⚠ This appointment does not belong to the given doctor.")
                return

            symptoms = DoctorServices._get_non_empty("Enter symptoms: ", 500)
            diagnosis = DoctorServices._get_non_empty("Enter diagnosis (max 100 words): ", 1000)
            consultation_notes = DoctorServices._get_non_empty("Enter consultation notes (max 100 words): ", 1000)

            consult = Consultation(
                appointment_id=appointment_id,
                symptoms=symptoms,
                diagnosis=diagnosis,
                consultation_notes=consultation_notes,
                doctor_id=doctor_id
            )
            ok = DoctorServices.dao_services.create_consultation(consult)
            if ok:
                print("✔ Consultation inserted successfully!")
            else:
                print("❌ Something went wrong while inserting consultation!")
        except Exception as e:
            print("Error while validating input:", e)

    @staticmethod
    def view_doctors_consultation():
        doctor_id = DoctorServices._get_int("Enter doctor id: ", 1)
        if not DoctorServices.dao_services.check_doctor_exists(doctor_id):
            print(f"⚠ Doctor id {doctor_id} does not exist.")
            return
        cs = DoctorServices.dao_services.view_consultation_of_doctor(doctor_id)
        if not cs:
            print("⚠ No consultations found.")
            return
        for c in cs:
            print(c)

    @staticmethod
    def view_patient_consultation():
        patient_id = DoctorServices._get_int("Enter patient id: ", 1)
        doctor_id = DoctorServices._get_int("Enter doctor id: ", 1)
        if not DoctorServices.dao_services.check_doctor_exists(doctor_id):
            print(f"⚠ Doctor id {doctor_id} does not exist.")
            return
        cs = DoctorServices.dao_services.view_consultation(patient_id, doctor_id)
        if not cs:
            print("⚠ No consultations found for this patient & doctor.")
            return
        for c in cs:
            print(c)

    # Prescriptions

    # ---------- Helper method ----------
    @staticmethod
    def _get_int(prompt: str, min_val: int = None) -> int:
        """Safe integer input with optional minimum value validation."""
        while True:
            try:
                value = int(input(prompt).strip())
                if min_val is not None and value < min_val:
                    print(f"⚠ Value must be >= {min_val}")
                    continue
                return value
            except ValueError:
                print("⚠ Invalid input! Please enter a valid number.")

   # ---------- Prescription Menu ----------
    @staticmethod
    def create_prescription_menu():
        """Menu for creating/fetching a prescription"""
        try:
            appointment_id = DoctorServices._get_int("Enter patient appointment id: ", 1)

            # check appointment exists
            appt = DoctorServices.dao_services.get_appointment_by_id(appointment_id)
            if not appt:
                print(f"⚠ Appointment id {appointment_id} does not exist.")
                input("\nPress Enter to continue...")
                return

            consultation_id = DoctorServices._get_int("Enter consultation id (0 if none): ", 0)
            if consultation_id == 0:
                consultation_id = None

            # create or get prescription
            prescription_id = DoctorServices.dao_services.get_or_create_prescription_for_appointment(
                appointment_id=appointment_id, consultation_id=consultation_id
            )

            if not prescription_id:
                print("❌ Something went wrong while creating prescription!")
                input("\nPress Enter to continue...")
                return

            print("✔ Prescription created / found successfully!")
            print(f"Prescription ID: {prescription_id}")

            # ----- Add Medicines / Tests -----
            while True:
                print("\n---- AVAILABLE PRESCRIPTIONS ----")
                print("1. Add medicine prescription")
                print("2. Add test prescription")
                print("3. Go back")
                choice = input("Choose (1/2/3): ").strip()
                if choice == '1':
                    DoctorServices.add_medicine_prescription(prescription_id)
                elif choice == '2':
                    DoctorServices.add_test_prescription(prescription_id)
                elif choice == '3':
                    break
                else:
                    print("⚠ Invalid choice!")

        except Exception as e:
            print("⚠ Error while creating prescription:", e)

    # ---------- Add Medicine Prescription ----------
    @staticmethod
    def add_medicine_prescription(prescription_id: int):
        """Add one or more medicine prescriptions"""
        try:
            while True:
                medicine_name = input("Enter medicine name: ").strip()
                if not medicine_name:
                    print("❌ Medicine name cannot be empty.")
                    continue

                medicine_quantity = DoctorServices._get_int("Enter medicine quantity: ", 1)
                dosage = input("Enter dosage instructions: ").strip()
                if not dosage:
                    print("❌ Dosage instructions cannot be empty.")
                    continue

                med_pres = Med_prescriptions(
                    prescription_id=prescription_id,
                    medicine_name=medicine_name,
                    medicine_quantity=medicine_quantity,
                    dosage=dosage,
                )

                if DoctorServices.dao_services.create_med_prescription(med_pres):
                    print("✔ Medicine prescription inserted successfully!!")
                else:
                    print("❌ Failed to insert medicine prescription!")

                ch = input("Add more medicines? (Y/N): ").strip().lower()
                if ch == 'n':
                    break
                elif ch != 'y':
                    print("⚠ Invalid choice! Exiting medicine entry.")
                    break

        except Exception as e:
            print("⚠ Error while validating medicine prescription:", e)

    # ---------- Add Test Prescription ----------
    @staticmethod
    def add_test_prescription(prescription_id: int):
        """Add one or more test prescriptions"""
        try:
            while True:
                test_name = input("Enter test name: ").strip()
                if not test_name:
                    print("❌ Test name cannot be empty.")
                    continue

                instructions = input("Enter instructions: ").strip()
                if not instructions:
                    print("❌ Instructions cannot be empty.")
                    continue

                test_pres = Test_prescriptions(
                    prescription_id=prescription_id,
                    test_name=test_name,
                    instructions=instructions,
                )

                if DoctorServices.dao_services.create_test_prescription(test_pres):
                    print("✔ Lab test inserted successfully!!")
                else:
                    print("❌ Failed to insert test prescription!")

                ch = input("Add more tests? (Y/N): ").strip().lower()
                if ch == 'n':
                    break
                elif ch != 'y':
                    print("⚠ Invalid choice! Exiting test entry.")
                    break

        except Exception as e:
            print("⚠ Error while validating test prescription:", e)
    

    @staticmethod
    def view_prescription_by_patient_id():
        """Display all prescriptions and their medicines/tests for a given patient ID."""
        try:
            patient_id = DoctorServices._get_int("Enter patient id: ", 1)

            # Fetch prescriptions for the patient
            prescriptions = DoctorServices.dao_services.get_prescriptions_by_patient_id(patient_id)

            if not prescriptions:
                print(f"⚠ No prescriptions found for patient id {patient_id}.")
                return

            # Display each prescription with medicines and tests
            print(f"\n--- Prescriptions for Patient ID {patient_id} ---")
            for pres in prescriptions:
                pres_id = pres['prescription_id']
                print(f"\nPrescription ID: {pres_id}")
                print(f"Appointment ID: {pres['appointment_id']}")
                print(f"Consultation ID: {pres.get('consultation_id', 'N/A')}")

                # Fetch and display medicines
                meds = DoctorServices.dao_services.get_med_prescriptions_by_prescription_id(pres_id)
                if meds:
                    print("💊 Medicines:")
                    for m in meds:
                        print(f"  - {m['medicine_name']} | Qty: {m['medicine_quantity']} | Dosage: {m['dosage']}")
                else:
                    print("💊 Medicines: None")

                # Fetch and display tests
                tests = DoctorServices.dao_services.get_test_prescriptions_by_prescription_id(pres_id)
                if tests:
                    print("🧪 Tests:")
                    for t in tests:
                        print(f"  - {t['test_name']} | Instructions: {t['instructions']}")
                else:
                    print("🧪 Tests: None")

        except Exception as e:
            print("⚠ Error while fetching prescriptions:", e)

