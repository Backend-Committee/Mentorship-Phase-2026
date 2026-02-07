from ..database.db import Session
from ..database.models import Patient, Doctor, Appointment

class AppointmentRepository:
    def __init__(self):
        self.session = Session()

    def add_appointment(self, appointment):
        self.session.add(appointment)
        self.session.commit()

    def get_appointment_by_id(self, appointment_id):
        return self.session.query(Appointment).filter_by(id=appointment_id).first()
    
    def get_appointments_by_doctor_id(self, doctor_id):
        return self.session.query(Appointment).filter_by(doctor_id=doctor_id).all()
    
    def get_appointments_by_patient_id(self, patient_id):
        return self.session.query(Appointment).filter_by(patient_id=patient_id).all()

    def get_all_appointments(self):
        return self.session.query(Appointment).all()

    def update_appointment(self, appointment_id, **kwargs):
        appointment = self.get_appointment_by_id(appointment_id)
        if appointment:
            for key, value in kwargs.items():
                setattr(appointment, key, value)
            self.session.commit()
            return appointment
        return None

    def delete_appointment(self, appointment_id):
        appointment = self.get_appointment_by_id(appointment_id)
        if appointment:
            self.session.delete(appointment)
            self.session.commit()
            return True
        return False