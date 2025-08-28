from abc import ABC, abstractmethod
from typing import List
from models.patient import Patient
from models.appointments import Appointments

class PatientDaoService(ABC):
    @abstractmethod
    def display_all_patients(self)->List[Patient]:
        pass

    @abstractmethod
    def insert_patients(self, patient:Patient)->bool:
        pass

    @abstractmethod
    def find_by_patient_id(self, patient_id:int) ->Patient:   # fixed
        pass

    @abstractmethod
    def update_patient(self, patient:Patient, patient_id:int)->bool:  # fixed
        pass
     #________________________________________
    @abstractmethod
    def add_appointment(self,appointments:Appointments)->bool:
        pass
    
    @abstractmethod
    def get_specializations(self):
        pass

    @abstractmethod
    def get_doctors(self):
        pass
    @abstractmethod
    def get_booked_tokens(self):
        pass
    @abstractmethod
    def display_all_appointments(self):
        pass
    @abstractmethod
    def cancel_appointment(self, appointment_id: int) -> bool:
        pass
    @abstractmethod
    def reschedule_appointment(self, appointment_id: int, new_date: str) -> bool:
        pass
    @abstractmethod
    def search_appointment_by_patient_id(self, patient_id: int):
        pass

  
   
