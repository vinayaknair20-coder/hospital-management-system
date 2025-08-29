from abc import ABC, abstractmethod
from models.consultation import Consultation
from models.appointments import Appointments
from models.prescription import Med_prescriptions, Test_prescriptions

class abstractdao(ABC):
    """Abstract DAO for Doctor operations"""

    # ---------------- Appointments ----------------
    @abstractmethod
    def view_all_appointments(self, doc_id: int) -> list:
        """Return all appointments for a doctor as a list of Appointments objects"""
        pass

    @abstractmethod
    def get_appointment_by_id(self, appointment_id: int):
        """Return an Appointments object for a given appointment_id, or None if not found"""
        pass

    # ---------------- Consultations ----------------
    @abstractmethod
    def create_consultation(self, consult: Consultation) -> bool:
        """Create a new consultation record. Returns True if successful."""
        pass

    @abstractmethod
    def view_consultation_of_doctor(self, doctor_id: int) -> list:
        """Return all consultations for a given doctor_id as a list of Consultation objects"""
        pass

    @abstractmethod
    def view_consultation(self, patient_id: int, doctor_id: int) -> list:
        """Return consultations for a given patient and doctor as a list of Consultation objects"""
        pass

    # ---------------- Prescriptions ----------------
    @abstractmethod
    def get_or_create_prescription_for_appointment(
        self, appointment_id: int, consultation_id: int = None
    ) -> int | None:
        """Return prescription_id for appointment. Creates new if doesn't exist."""
        pass

    @abstractmethod
    def create_med_prescription(self, med_pres: Med_prescriptions) -> bool:
        """Insert a medicine prescription record. Returns True if successful."""
        pass

    @abstractmethod
    def create_test_prescription(self, test_pres: Test_prescriptions) -> bool:
        """Insert a lab test prescription record. Returns True if successful."""
        pass

    @abstractmethod
    def get_prescriptions_by_patient_id(self, patient_id: int) -> list:
        """Fetch prescription info by ID ..wrong"""
        pass

    # ---------------- Helper Methods ----------------
    @abstractmethod
    def check_doctor_exists(self, doctor_id: int) -> bool:
        """Return True if doctor exists in doctor table"""
        pass

    @abstractmethod
    def get_patient_id_by_appointment(self, appointment_id: int):
        """Return patient_id for a given appointment_id, or None if not found"""
        pass


    @abstractmethod
    def get_med_prescriptions_by_prescription_id(self, prescription_id: int) -> list:
        '''get med prescription by pres id'''
        pass

    @abstractmethod
    def get_test_prescriptions_by_prescription_id(self, prescription_id: int) -> list:
        '''def get_test_prescriptions_by_prescription_id'''
        pass