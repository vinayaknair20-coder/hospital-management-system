from abc import ABC,abstractmethod
from typing import List
from models.medicine import Medicine

class medecineDaoService(ABC):
    @abstractmethod
    def display_all_medicine(self)->List[Medicine]:
        '''display all medicine'''
        pass

    @abstractmethod
    def add_medicine(self)->bool:
        '''insert medecine '''
        pass