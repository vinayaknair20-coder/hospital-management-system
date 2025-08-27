from validation.receptionist_validation import validate_name,validate_DOB,validate_age,validate_gender,validate_blood_group,validate_phone_number,validate_email,validate_address,validate_emergency_contact
class Patient:
    def __init__(self,patient_id,patient_name =None,DOB=None,age = None,gender = None,blood_group = None,phone_number = None,email=None,address = None,emergency_contact=None,is_active='1'):
        self.__patient_id = patient_id
        self.__patient_name = patient_name
        self.__DOB = DOB
        self.__age = age
        self.__gender = gender
        self.__blood_group = blood_group
        self.__phone_number = phone_number
        self.__email = email
        self.__address = address
        self.__emergency_contact = emergency_contact
        self.__is_active= is_active

    @property
    def patient_id(self):
          return self.__patient_id

    @property
    def patient_name(self):
          return self.__patient_name
    @patient_name.setter
    def patient_name(self,value):
          validate_name(value)
          self.__patient_name = value

    @property
    def DOB(self):
          return self.__DOB
    @DOB.setter
    def DOB(self,value):
          validate_DOB(value)
          self.__DOB = value

    @property
    def age(self):
          return self.__age 
    @age.setter
    def age(self,value):
          validate_age(value)
          self.__age = value

    @property
    def gender(self):
          return self.__gender 
    @gender.setter
    def gender(self,value):
          validate_gender(value)
          self.__gender = value

    @property
    def blood_group(self):
          return self.__blood_group 
    @blood_group.setter
    def blood_group(self,value):
          validate_blood_group(value)
          self.__blood_group = value

    @property
    def phone_number(self):
          return self.__phone_number
    @phone_number.setter
    def phone_number(self,value):
          validate_phone_number(value)
          self.__phone_number = value
    

    @property
    def email(self):
          return self.__email
    @email.setter
    def email(self,value):
          validate_email(value)
          self.__email = value

    @property
    def address(self):
          return self.__address
    @address.setter
    def address(self,value):
          validate_address(value)
          self.__address = value

    @property
    def emergency_contact(self):
          return self.__emergency_contact
    @emergency_contact.setter
    def emergency_contact(self,value):
          validate_emergency_contact(value)
          self.__emergency_contact = value

    @property
    def is_active(self):
          return self.__is_active
    @is_active.setter
    def is_active(self,value):
          self.__is_active = value

    def __str__(self):
        return f"Patient_ID: {self.__patient_id},PatientName :{self.__patient_name},Date_Of_Birth:{self.__DOB}, PatientAge :{self.__age}, Gender :{self.__gender},BloodGroup: {self.__blood_group}, PhoneNumber :{self.__phone_number},Email :{self.__email},PatientAddress :{self.__address}, EmergencyContact:{self.__emergency_contact}, is_active:{self.__is_active}"