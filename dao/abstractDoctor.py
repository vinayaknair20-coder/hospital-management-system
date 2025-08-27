from abc import ABC,abstractmethod

class abstractdao(ABC):
    '''all methods for doctor implementation'''

    @abstractmethod
    def view_all_appointments(self):
        '''to view all patient appointments created by receptionist'''
        pass

    @abstractmethod
    def view_count(self):
        '''to view appointment count'''
        pass

    @abstractmethod
    def create_consulatation(self)->bool:
        '''method for creating the consultation of a patient'''
        pass

    @abstractmethod
    def view_consultation(self):
        '''method to view inserted consultations'''
        pass

    @abstractmethod
    def create_prescription(self):
        '''method to create prescription'''
        pass

    @abstractmethod
    def display_prescription(self):
        '''method to display appointments with prescription'''
        pass
   