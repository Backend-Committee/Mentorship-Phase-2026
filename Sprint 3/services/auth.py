from ..repositories.patient_repo import PatientRepository
from ..repositories.doctor_repo import DoctorRepository
class AuthService:
    def __init__(self):
        self.patient_repo = PatientRepository()
        self.doctor_repo = DoctorRepository()

    def authenticate_patient(self, name, password):
        patient = self.patient_repo.get_patient_by_name(name)
        if patient and patient.password == password:
            return patient
        return None

    def authenticate_doctor(self, name, password):
        doctor = self.doctor_repo.get_doctor_by_name(name)
        if doctor and doctor.password == password:
            return doctor
        return None