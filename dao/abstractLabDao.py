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
        '''fetch all test in the  lab '''
        pass
    @abstractmethod
    def find_by_test_id(self,test_id:int) -> LabTech:
        '''find a test by ID'''
        pass
    @abstractmethod
    def update_test(self, labtech: LabTech, test_id: str) -> bool:
        """Update a test by its ID"""
        pass

    @abstractmethod
    def delete_test(self, test_id: str) -> bool:
        """Disable (soft delete) a test in labtest table"""
        pass
    @abstractmethod
    def view_prescription_results(self):
        """Fetch all prescriptions and their results"""
        pass

    @abstractmethod
    def add_test_result(self, test_prescription_id: int, test_value: str, 
                        result_status: str, tested_date: str, lab_resultcol: str) -> bool:
        """Insert a new test result into lab_results"""
        pass