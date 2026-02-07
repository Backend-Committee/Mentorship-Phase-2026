from ..database.db import Session
from ..database.models import Patient

class PatientRepository:
    def __init__(self):
        self.session = Session()

    def add_patient(self, patient):
        self.session.add(patient)
        self.session.commit()

    def get_patient_by_id(self, patient_id):
        return self.session.query(Patient).filter_by(id=patient_id).first()
    
    def get_patient_by_name(self, patient_name):
        return self.session.query(Patient).filter_by(name=patient_name).first()
    
    """ def get_patient_diseases_history(self, patient_id):
        patient = self.get_patient_by_id(patient_id)
        if patient:
            return patient.diseases_history
        return None """

    def get_all_patients(self):
        return self.session.query(Patient).all()

    def update_patient(self, patient_id, **kwargs):
        patient = self.get_patient_by_id(patient_id)
        if patient:
            for key, value in kwargs.items():
                setattr(patient, key, value)
            self.session.commit()
            return patient
        return None

    def delete_patient(self, patient_id):
        patient = self.get_patient_by_id(patient_id)
        if patient:
            self.session.delete(patient)
            self.session.commit()
            return True
        return False
    
    def cancel_patient_appointment(self, patient_id, appointment_id):
        patient = self.get_patient_by_id(patient_id)
        if patient:
            for appointment in patient.appointments and not appointment.caneled_flag:
                if appointment.id == appointment_id:
                    appointment.caneled_flag = True
                    self.session.commit()
                    print(f"Appointment {appointment_id} for patient {patient.name} has been canceled.")
                    return True
        print(f"Appointment {appointment_id} not found for patient {patient.name} or already canceled.")
        return False