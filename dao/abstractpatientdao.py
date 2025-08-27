from abc import ABC, abstractmethod
from typing import List
from models.patient import Patient

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

  
   
