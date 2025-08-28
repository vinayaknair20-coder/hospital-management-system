from abc import ABC,abstractmethod
from typing import List
from models.medicine import Medicine

class MedecineDaoService(ABC):
    @abstractmethod
    def display_all_medicine(self)->List[Medicine]:
        '''display all medicine'''
        pass

    @abstractmethod
    def add_medicine(self)->bool:
        '''insert medecine '''
        pass

    @abstractmethod
    def update_medicine(self,medicine:Medicine,medicine_id:int)->bool:
        '''update a medicine by its ID'''
        pass

    @abstractmethod
    def disable_medicine(self,medicine:Medicine,medicine_id:int)->bool:
        '''disable medicine by medicine id'''

    @abstractmethod
    def find_by_medicine_id(self,medicine_id:int)-> Medicine:
        '''find a medicine by ID'''