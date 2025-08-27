class Appointments:
    def __init__(self,appointment_id,patient_id,doctor_id,token_number):
        self.__appointment_id=appointment_id
        self.__patient_id=patient_id
        self.__doctor_id=doctor_id
        self.__token_number=token_number

    # getters
    @property
    def appointment_id(self):
        return self.__appointment_id
    @property
    def patient_id(self):
        return self.__patient_id
    @property
    def doctor_id(self):
        return self.__doctor_id
    @property
    def token_number(self):
        return self.__token_number
    def __str__(self):
        return f'appointment_id = {self.__appointment_id},patient_id={self.__patient_id},doctor_id={self.__doctor_id},token_number={self.__token_number}'