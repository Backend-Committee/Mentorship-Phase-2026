from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship, declarative_base


#engine = create_engine('sqlite:///data/mydatabase.db')
Base = declarative_base()

class Doctor(Base):
    __tablename__ = 'doctors'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    specialization = Column(String, nullable=False)
    schedule = Column(String, nullable=False)
    password = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)

    appointments = relationship('Appointment', back_populates='doctor')

    def __repr__(self):
        return f"Doctor:\nid={self.id} \nname='{self.name}' \nspecialization='{self.specialization}' \nschedule='{self.schedule}' \nphone_number='{self.phone_number}'\n"

class Patient(Base):
    __tablename__ = 'patients'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    age = Column(Integer, nullable=False)
    gender = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    diseases_history = Column(String, nullable=True, default="None")

    appointments = relationship('Appointment', back_populates='patient')

    def __repr__(self):
        return f"Patient:\nid={self.id} \nname='{self.name}' \nage={self.age} \ngender='{self.gender}' \nphone_number='{self.phone_number}' \ndiseases_history='{self.diseases_history}'\n"   

class Appointment(Base):
    __tablename__ = 'appointments'

    id = Column(Integer, primary_key=True)
    doctor_id = Column(Integer, ForeignKey('doctors.id'), nullable=False)
    patient_id = Column(Integer, ForeignKey('patients.id'), nullable=False)
    date_time = Column(DateTime, nullable=False)
    reason = Column(String, nullable=False)
    caneled_flag = Column(Boolean, nullable=False, default=False)

    doctor = relationship('Doctor', back_populates='appointments')
    patient = relationship('Patient', back_populates='appointments')

    def __repr__(self):
        return f"Appointment:\ndoctor_id={self.doctor_id} \npatient_id={self.patient_id} \ndate_time='{self.date_time}' \nreason='{self.reason}' \ncaneled_flag={self.caneled_flag}\n"