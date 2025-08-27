from abc import ABC,abstractmethod
from models.labtech import LabTech
from typing import List

class AbstractLabDao(ABC):

    @abstractmethod
    def create_test(self):
        '''create test in the labtest'''
        pass
    
    @abstractmethod
    def display_test(self)->List[LabTech]:
        '''fetch all lab test'''
        pass

    # @abstractmethod
    # def update_test(self):
    #     '''update test in the labtest'''
    #     pass

    # @abstractmethod
    # def search_test(self):
    #     '''search test in the labtest'''
    #     pass
