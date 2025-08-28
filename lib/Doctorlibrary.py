from dao.doctorDao import DoctorDao





class DoctorLibrary:
    def __init__(self):
        self.dao = DoctorDao()

    def add_doctor(self):
        try:
            doctor_id = self.dao.get_next_doctor_id()   # Auto doctor ID
            staff_id = input("Enter Staff ID: ")
            specialization_id = input("Enter Specialization ID: ")
            consultation_fee = float(input("Enter Consultation Fee: "))
            working_hours_start = input("Enter Working Hours Start (HH:MM:SS): ")
            working_hours_end = input("Enter Working Hours End (HH:MM:SS): ")

            print(f"Generated Doctor ID: {doctor_id}")

            # Save doctor to DB
            self.dao.add_doctor(
                doctor_id,
                staff_id,
                specialization_id,
                consultation_fee,
                working_hours_start,
                working_hours_end,
                1   # is_available = 1 by default
            )

            print("✅ Doctor added successfully.")
        except ValueError as ve:
            print(f"❌ Validation Error: {ve}")
        except Exception as e:
            print(f"❌ Unexpected Error: {e}")

    def update_doctor(self):
        doctor_id = input("Enter Doctor ID to update: ")
        consultation_fee = float(input("Enter new Consultation Fee: "))
        is_available = int(input("Enter Availability (1 = Available, 0 = Not Available): "))
        self.dao.update_doctor(doctor_id, consultation_fee, is_available)
        print("✅ Doctor updated successfully.")

    def deactivate_doctor(self):
        doctor_id = input("Enter Doctor ID to deactivate: ")
        self.dao.deactivate_doctor(doctor_id)
        print("⚠ Doctor deactivated (availability set to 0).")

    def list_doctors(self):
        doctor_list = self.dao.list_doctors()
        if not doctor_list:
            print("⚠ No doctors found.")
        else:
            print("\n--- Doctors ---")
            for d in doctor_list:
                print(f"ID: {d['doctor_id']}, Staff ID: {d['staff_id']}, "
                      f"Specialization: {d['specialization_id']}, Fee: {d['consultation_fee']}, "
                      f"Hours: {d['working_hours_start']} - {d['working_hours_end']}, "
                      f"Available: {d['is_available']}")

                      
    def search_doctor_by_id(self):
        doctor_id = input("Enter Doctor ID to search: ")
        result = self.dao.search_doctor_by_id(doctor_id)
        if not result:
            print(f"⚠ No doctor found with ID {doctor_id}.")
        else:
            print("\n--- Doctor Details ---")
            print(f"ID: {result['doctor_id']}, Name: {result['staff_name']}, "
                  f"Specialization: {result['specialization_name']}, "
                  f"Fee: {result['consultation_fee']}, "
                  f"Hours: {result['working_hours_start']} - {result['working_hours_end']}, "
                  f"Available: {result['is_available']}")
             