# models/prescriptions.py
class Prescriptions:
    def __init__(self, prescription_id=None, appointment_id=None, patient_id=None, patient_name=None):
        self.__prescription_id = prescription_id
        self.__appointment_id = appointment_id
        self.__patient_id = patient_id
        self.__patient_name = patient_name

    @property
    def prescription_id(self):
        return self.__prescription_id

    @prescription_id.setter
    def prescription_id(self, value):
        self.__prescription_id = value

    @property
    def appointment_id(self):
        return self.__appointment_id

    @property
    def patient_id(self):
        return self.__patient_id

    @property
    def patient_name(self):
        return self.__patient_name

    def __str__(self):
        return (f"prescription_id:{self.__prescription_id},"
                f"appointment_id:{self.__appointment_id},"
                f"patient_id:{self.__patient_id},"
                f"patient_name:{self.__patient_name}")

class Med_prescriptions(Prescriptions):
    def __init__(self, prescription_id=None, medicine_name=None, medicine_quantity=None, dosage=None):
        super().__init__(prescription_id=prescription_id)
        self.__medicine_name = medicine_name
        self.__medicine_quantity = medicine_quantity
        self.__dosage = dosage

    @property
    def medicine_name(self):
        return self.__medicine_name

    @property
    def medicine_quantity(self):
        return self.__medicine_quantity

    @property
    def dosage(self):
        return self.__dosage

    def __str__(self):
        return (super().__str__() + f", medicine_name:{self.__medicine_name}, medicine_quantity:{self.__medicine_quantity}, dosage:{self.__dosage}")

class Test_prescriptions(Prescriptions):
    def __init__(self, prescription_id=None, test_name=None, instructions=None):
        super().__init__(prescription_id=prescription_id)
        self.__test_name = test_name
        self.__instructions = instructions

    @property
    def test_name(self):
        return self.__test_name

    @property
    def instructions(self):
        return self.__instructions

    def __str__(self):
        return (super().__str__() + f", test_name:{self.__test_name}, instructions:{self.__instructions}")
