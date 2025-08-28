class Doctor:
    def __init__(self, doctor_id, staff_id, specialization_id, consultation_fee,
                 working_hours_start, working_hours_end, is_available=None):
        self.doctor_id = doctor_id
        self.staff_id = staff_id
        self.specialization_id = specialization_id
        self.consultation_fee = consultation_fee
        self.working_hours_start = working_hours_start
        self.working_hours_end = working_hours_end
        self.is_available = is_available  # None = let DB default handle it

    def __str__(self):
        status = "Available" if self.is_available in (True, 1) else "Not Available"
        return (f"[{self.doctor_id}] Staff: {self.staff_id} | "
                f"Specialization ID: {self.specialization_id} | "
                f"Fee: {self.consultation_fee} | "
                f"Working Hours: {self.working_hours_start} - {self.working_hours_end} | "
                f"Status: {status}")
