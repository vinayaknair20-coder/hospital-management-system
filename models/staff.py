class Staff:
    def __init__(self, staff_id, staff_name, role_id, age, phone_number, email, date_of_joining, password_hash, is_active=True):
        self.staff_id = staff_id
        self.staff_name = staff_name
        self.role_id = role_id
        self.age = age
        self.phone_number = phone_number
        self.email = email
        self.date_of_joining = date_of_joining
        self.password_hash = password_hash
        self.is_active = is_active

    def __str__(self):
        status = "Active" if self.is_active else "Inactive"
        return (f"[{self.staff_id}] {self.staff_name} | Role: {self.role_id} | "
                f"Age: {self.age} | Phone: {self.phone_number} | Email: {self.email} | "
                f"DOJ: {self.date_of_joining} | Status: {status}")
