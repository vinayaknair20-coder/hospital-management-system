class Prescriptions:
    def __init__(self,prescription_id=None,appointment_id=None):
        self.__prescription_id=prescription_id
        self.__appointment_id=appointment_id
        


    # getters
    @property
    def prescription_id(self):
        return self.__prescription_id

    @property
    def appointment_id(self):
        return self.__appointment_id
    

    def __str__(self):
        return f'prescription_id:{self.__prescription_id},appointment_id:{self.__appointment_id}'



