from database.models import Doctor
from database.db import Session

class DoctorRepository:
    def __init__(self):
        self.session = Session()

    def add_doctor(self, doctor):
        self.session.add(doctor)
        self.session.commit()

    def get_doctor_by_id(self, doctor_id):
        return self.session.query(Doctor).filter_by(id=doctor_id).first()
    
    def get_doctor_by_name(self, doctor_name):
        return self.session.query(Doctor).filter_by(name=doctor_name).all()
    
    def get_doctor_by_specialization(self, specialization):
        return self.session.query(Doctor).filter_by(specialization=specialization).all()

    def get_all_doctors(self):
        return self.session.query(Doctor).all()

    def update_doctor(self, doctor_id, **kwargs):
        doctor = self.get_doctor_by_id(doctor_id)
        if doctor:
            for key, value in kwargs.items():
                setattr(doctor, key, value)
            self.session.commit()
            return doctor
        return None

    def delete_doctor(self, doctor_id):
        doctor = self.get_doctor_by_id(doctor_id)
        if doctor:
            self.session.delete(doctor)
            self.session.commit()
            return True
        return False
    
    def display_doctor_appointments(self, doctor_id):
        doctor = self.get_doctor_by_id(doctor_id)
        if doctor:
            print(f"Appointments for Dr. {doctor.name}:")
            for appointment in doctor.appointments:
                if not appointment.caneled_flag:
                    print(f" - {appointment.date_time}: {appointment.reason} with patient {appointment.patient.name}")
        return None
    
    def display_doctor_schedule(self, doctor_id):
        doctor = self.get_doctor_by_id(doctor_id)
        if doctor:
            print(f"Schedule for Dr. {doctor.name}: {doctor.schedule}")
        return None
    
    def display_doctor_info(self, doctor_id):
        doctor = self.get_doctor_by_id(doctor_id)
        if doctor:
            print(doctor)
        return None
    
    """ def display_patient_diseases_history(self, doctor_id):
        doctor = self.get_doctor_by_id(doctor_id)
        if doctor:
            for appointment in doctor.appointments:
                if not appointment.caneled_flag:
                    print(f"Patient {appointment.patient.name} has diseases: {appointment.patient.diseases_history}")
        return None """
    
    def cancel_appointment(self, doctor_id, appointment_id):
        doctor = self.get_doctor_by_id(doctor_id)
        if doctor:
            for appointment in doctor.appointments and not appointment.caneled_flag:
                if appointment.id == appointment_id:
                    appointment.caneled_flag = True
                    self.session.commit()
                    print(f"Appointment {appointment_id} has been canceled.")
                    return True
        print(f"Appointment {appointment_id} not found for Dr. {doctor.name}, or it has already been canceled.")
        return False
    
