class Appointments:
    def __init__(self, patient_id, patient_name, doctor_id, appointment_date, token_number, specialization_id,
                 appointment_id=None, status="SCHEDULED"):
        self.__appointment_id = appointment_id  # DB will assign this
        self.__patient_id = patient_id
        self.__patient_name = patient_name
        self.__specialization_id = specialization_id
        self.__doctor_id = doctor_id
        self.__appointment_date = appointment_date
        self.__token_number = token_number
        self.__status = status   # Default is "SCHEDULED"

    # getters
    @property
    def appointment_id(self):
        return self.__appointment_id
    @property
    def patient_id(self):
        return self.__patient_id
    @property
    def patient_name(self):
        return self.__patient_name
    @property
    def specialization_id(self):
        return self.__specialization_id
    @property
    def doctor_id(self):
        return self.__doctor_id
    @property
    def appointment_date(self):
        return self.__appointment_date
    @property
    def token_number(self):
        return self.__token_number
    @property
    def status(self):
        return self.__status

    def __str__(self):
        return (f'Appointment ID : {self.__appointment_id}\n'
                f'Patient ID     : {self.__patient_id}\n' 
                f'Patient Name   : {self.__patient_name}\n' 
                f'Specialization ID:{self.__specialization_id}\n'
                f'Doctor ID      : {self.__doctor_id}\n'
                f'Appointment Date: {self.__appointment_date}\n'
                f'Token Number   : {self.__token_number}\n'
                f'Status         : {self.__status}')
