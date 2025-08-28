from abc import ABC, abstractmethod
from typing import List
from models.medicine import Medicine

class MedecineDaoService(ABC):
    @abstractmethod
    def display_all_medicine(self) -> List[Medicine]: pass
    @abstractmethod
    def add_medicine(self, medicine: Medicine) -> bool: pass
    @abstractmethod
    def update_medicine(self, medicine: Medicine, medicine_id: int) -> bool: pass
    @abstractmethod
    def disable_medicine(self, medicine_id: int) -> bool: pass
    @abstractmethod
    def find_by_medicine_id(self, medicine_id: int) -> Medicine: pass
    @abstractmethod
    def find_by_medicine_type(self, medicine_type: str) -> List[Medicine]: pass
    @abstractmethod
    def get_medicine_types(self) -> List[str]: pass
    @abstractmethod
    def get_critical_stock_medicines(self) -> List[Medicine]: pass
