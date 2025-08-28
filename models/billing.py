class Billing:
    def __init__(self, patient_id, appointment_id, doctor_id, consultation_fee,
                 payment_status="PENDING", payment_method=None, payment_date=None, bill_id=None):
        # bill_id will be auto-generated in DB
        self.__bill_id = bill_id
        self.__patient_id = patient_id
        self.__appointment_id = appointment_id
        self.__doctor_id = doctor_id
        self.__consultation_fee = consultation_fee
        self.__payment_status = payment_status  # Default set to "PENDING"
        self.__payment_method = payment_method
        self.__payment_date = payment_date

    # ---------- Getters ----------
    @property
    def bill_id(self):
        return self.__bill_id

    @property
    def patient_id(self):
        return self.__patient_id

    @property
    def appointment_id(self):
        return self.__appointment_id

    @property
    def doctor_id(self):
        return self.__doctor_id

    @property
    def consultation_fee(self):
        return self.__consultation_fee

    @property
    def payment_status(self):
        return self.__payment_status

    @property
    def payment_method(self):
        return self.__payment_method

    @property
    def payment_date(self):
        return self.__payment_date

    # ---------- Setters ----------
    @payment_status.setter
    def payment_status(self, status):
        self.__payment_status = status

    @payment_method.setter
    def payment_method(self, method):
        self.__payment_method = method

    @payment_date.setter
    def payment_date(self, date):
        self.__payment_date = date


    # --- Setters (only for fields that may change, like payment) ---
    @payment_status.setter
    def payment_status(self, status):
        self.__payment_status = status

    @payment_method.setter
    def payment_method(self, method):
        self.__payment_method = method

    @payment_date.setter
    def payment_date(self, date):
        self.__payment_date = date

    # --- String Representation ---
    def __str__(self):
        return (f'Bill ID         : {self.__bill_id}\n'
                f'Patient ID      : {self.__patient_id}\n'
                f'Appointment ID  : {self.__appointment_id}\n'
                f'Doctor ID       : {self.__doctor_id}\n'
                f'Consultation Fee: {self.__consultation_fee}\n'
                f'Payment Status  : {self.__payment_status}\n'
                f'Payment Method  : {self.__payment_method}\n'
                f'Payment Date    : {self.__payment_date}')
