from database.models import Doctor, Patient
from repositories.appoinment_repo import AppointmentRepository
from repositories.patient_repo import PatientRepository
from repositories.doctor_repo import DoctorRepository
class OperationService:
    def __init__(self):
        self.appoinment_repo = AppointmentRepository()
        self.patient_repo = PatientRepository()
        self.doctor_repo = DoctorRepository()

    def sign_up_doctor(self, name, specialization, schedule, password, phone_number):
        new_doctor = Doctor(name=name, specialization=specialization, schedule=schedule, password=password, phone_number=phone_number)
        self.doctor_repo.add_doctor(new_doctor)
        return new_doctor

    def view_appointments_for_doctor(self, doctor_id):
        doctor = self.doctor_repo.get_doctor_by_id(doctor_id)
        if doctor:
            return doctor.appointments
        return None
    
    def update_doctor(self, doctor_id, **kwargs):
        doctor = self.doctor_repo.get_doctor_by_id(doctor_id)
        if doctor:
            for key, value in kwargs.items():
                setattr(doctor, key, value)
            self.doctor_repo.update_doctor(doctor_id, **kwargs)
            return doctor
        return None
    
    def cancel_appointment(self, appointment_id):
        appointment = self.appoinment_repo.get_appointment_by_id(appointment_id)
        if appointment and not appointment.caneled_flag:
            appointment.caneled_flag = True
            self.appoinment_repo.update_appointment(appointment_id, caneled_flag=True)
            return appointment
        return None
    
    def view_patient_details(self, patient_id):
        patient = self.patient_repo.get_patient_by_id(patient_id)
        if patient:
            return patient
        return None
    
    def patient_sign_up(self, name, age, password, phone_number, diseases_history):
        new_patient = Patient(name=name, age=age, password=password, phone_number=phone_number, diseases_history=diseases_history)
        self.patient_repo.add_patient(new_patient)
        return new_patient
    
    def search_doctors_by_specialization(self, specialization):
        return self.doctor_repo.get_doctor_by_specialization(specialization)
    
    def search_doctors_by_name(self, name):
        return self.doctor_repo.get_doctor_by_name(name)
    
    def view_appointments_for_patient(self, patient_id):
        patient = self.patient_repo.get_patient_by_id(patient_id)
        if patient:
            return patient.appointments
        return None
    
    def update_patient(self, patient_id, **kwargs):
        patient = self.patient_repo.get_patient_by_id(patient_id)
        if patient:
            for key, value in kwargs.items():
                setattr(patient, key, value)
            self.patient_repo.update_patient(patient_id, **kwargs)
            return patient
        return None
    
    def book_appointment(self, patient_id, doctor_id, appointment_time):
        patient = self.patient_repo.get_patient_by_id(patient_id)
        doctor = self.doctor_repo.get_doctor_by_id(doctor_id)
        if patient and doctor:
            new_appointment = self.appoinment_repo.create_appointment(patient_id=patient_id, doctor_id=doctor_id, appointment_time=appointment_time)
            return new_appointment
        return None
    
    def view_doctor_schedule(self, doctor_id):
        doctor = self.doctor_repo.get_doctor_by_id(doctor_id)
        if doctor:
            return doctor.schedule
        return None