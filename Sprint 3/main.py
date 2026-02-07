from services.auth import AuthService
from services.opeerations import OperationsService

def doctor():
    auth_service = AuthService()
    operations_service = OperationsService()
    while True:
        print("\n1- Login\n2- sign up\nPress 0 to back to main menu...")
        sub_choice = input("Enter your choice: ")
        if sub_choice == '1':
            name = input("Enter your name: ")
            password = input("Enter your password: ")
            doctor = auth_service.authenticate_doctor(name, password)
            if doctor:
                doctor_menu(doctor)
            else:
                print("Invalid credentials for doctor.")
        elif sub_choice == '2':
            name = input("Enter your name: ")
            specialization = input("Enter your specialization: ")
            schedule = input("Enter your schedule: ")
            password = input("Enter your password: ")
            phone_number = input("Enter your phone number: ")
            new_doctor = operations_service.sign_up_doctor(name=name, specialization=specialization, schedule=schedule, password=password, phone_number=phone_number)
            print("Doctor registered successfully.")
            doctor_menu(new_doctor)
        elif sub_choice == '0':
            break

def patient():
    auth_service = AuthService()
    operations_service = OperationsService()
    while True:
        print("\n1- Login\n2- sign up\nPress 0 to back to main menu...")
        sub_choice = input("Enter your choice: ")
        if sub_choice == '1':
            name = input("Enter your name: ")
            password = input("Enter your password: ")
            patient = auth_service.authenticate_patient(name, password)
            if patient:
                patient_menu(patient)
            else:
                print("Invalid credentials for patient.")
        elif sub_choice == '2':
            name = input("Enter your name: ")
            age = int(input("Enter your age: "))
            password = input("Enter your password: ")
            phone_number = input("Enter your phone number: ")
            diseases_history = input("Enter your diseases history (or leave blank if none): ")
            new_patient = operations_service.sign_up_patient(name=name, age=age, password=password, phone_number=phone_number, diseases_history=diseases_history)
            print("Patient registered successfully.")
            patient_menu(new_patient)
        elif sub_choice == '0':
            break

def view_appointments_for_doctor(doctor_id):
    operations_service = OperationsService()
    appointments = operations_service.view_appointments_for_doctor(doctor_id)
    for appt in appointments:
        print(appt)
    print("\n")
    while True:
        print("1- View Patient Details\nPress 0 to back to main menu...")
        sub_choice = input("Enter your choice: ")
        if sub_choice == '1':
            patient_id = int(input("Enter the patient ID to view details: "))
            patient_details = operations_service.view_patient_details(patient_id)
            if patient_details:
                print(patient_details)
            else:
                print("Patient not found.")
        elif sub_choice == '0':
            break

def cancel_appointment(appointment_id):
    operations_service = OperationsService()
    canceled_appointment = operations_service.cancel_appointment(appointment_id)
    if canceled_appointment:
        print("Appointment canceled successfully.")
    else:
        print("Failed to cancel appointment.")

def update_doctor(doctor):
    operations_service = OperationsService()
    while True:
        print("What do you want to update?")
        print("1- Name\n2- Specialization\n3- Schedule\n4- Password\n5- Phone Number\nPress 0 to back to main menu...")
        update_choice = input("Enter your choice: ")
        if update_choice == '1':
            new_name = input("Enter new name: ")
            operations_service.update_doctor(doctor.id, name=new_name)
            doctor.name = new_name
        elif update_choice == '2':
            new_specialization = input("Enter new specialization: ")
            operations_service.update_doctor(doctor.id, specialization=new_specialization)
            doctor.specialization = new_specialization
        elif update_choice == '3':
            new_schedule = input("Enter new schedule: ")
            operations_service.update_doctor(doctor.id, schedule=new_schedule)
            doctor.schedule = new_schedule
        elif update_choice == '4':
            new_password = input("Enter new password: ")
            operations_service.update_doctor(doctor.id, password=new_password)
            doctor.password = new_password
        elif update_choice == '5':
            new_phone_number = input("Enter new phone number: ")
            operations_service.update_doctor(doctor.id, phone_number=new_phone_number)
            doctor.phone_number = new_phone_number
        elif update_choice == '0':
            break

def search_doctors():
    operations_service = OperationsService()
    while True:
        print("1- Search by specialization\n2- Search by doctor name\nPress 0 to back to main menu...")
        search_choice = input("Enter your choice: ")
        if search_choice == '1':
            print("Available specializations: Cardiology, Dermatology, Neurology, Pediatrics, Psychiatry")
            specialization = input("Enter specialization to search: ")
            doctors = operations_service.search_doctors_by_specialization(specialization)
            if doctors:
                for doctor in doctors:
                    print(doctor)
            else:
                print("No doctors found for this specialization.")
        elif search_choice == '2':
            name = input("Enter doctor name to search: ")
            doctor = operations_service.search_doctors_by_name(name)
            if doctor:
                print(doctor)
            else:
                print("No doctor found with this name.")
        elif search_choice == '0':
            break

def view_appointments_for_patient(patient_id):
    operations_service = OperationsService()
    appointments = operations_service.view_appointments_for_patient(patient_id)
    if appointments:
        for appt in appointments:
            print(appt)
    else:
        print("No appointments found for this patient.")

def update_patient(patient):
    operations_service = OperationsService()
    while True:
        print("What do you want to update?")
        print("1- Name\n2- Age\n3- Password\n4- Phone Number\n5- Diseases History\nPress 0 to back to main menu...")
        update_choice = input("Enter your choice: ")
        if update_choice == '1':
            new_name = input("Enter new name: ")
            operations_service.update_patient(patient.id, name=new_name)
            patient.name = new_name
        elif update_choice == '2':
            new_age = int(input("Enter new age: "))
            operations_service.update_patient(patient.id, age=new_age)
            patient.age = new_age
        elif update_choice == '3':
            new_password = input("Enter new password: ")
            operations_service.update_patient(patient.id, password=new_password)
            patient.password = new_password
        elif update_choice == '4':
            new_phone_number = input("Enter new phone number: ")
            operations_service.update_patient(patient.id, phone_number=new_phone_number)
            patient.phone_number = new_phone_number
        elif update_choice == '5':
            new_diseases_history = input("Enter new diseases history: ")
            operations_service.update_patient(patient.id, diseases_history=new_diseases_history)
            patient.diseases_history = new_diseases_history
        elif update_choice == '0':
            break

def book_appointment(patient_id, doctor_id):
    operations_service = OperationsService()
    appointment_time = input("Enter appointment time (e.g., 2024-07-01 10:00): ")
    new_appointment = operations_service.book_appointment(patient_id, doctor_id, appointment_time)
    if new_appointment:
        print("Appointment booked successfully.")
    else:        
        print("Failed to book appointment. Please check doctor availability and try again.")

def doctor_menu(doctor):
    print(f"\nWelcome Dr. {doctor.name}!")
    while True:
        print("1- View Appointments\n2- Update\n3- Cancel Appoinment\nPress 0 to log out...")
        choice = input("Enter your choice: ")
        if choice == '1':
            view_appointments_for_doctor(doctor.id)
        elif choice == '2':
            update_doctor(doctor)
        elif choice == '3':
            appointment_id = int(input("Enter the appointment ID to cancel: "))
            cancel_appointment(appointment_id)
        elif choice == '0':
            print(f"Goodbye, Dr. {doctor.name}!")
            break

def patient_menu(patient):
    print(f"\nWelcome {patient.name}!")
    while True:
        print("1- Search\n2- View My Appointments\n3- Cancel Appointment\n4- Book Appointment\n5- Update Profile\nPress 0 to log out...")
        choice = input("Enter your choice: ")
        if choice == '1':
            search_doctors()
        elif choice == '2':
            view_appointments_for_patient(patient.id)
        elif choice == '3':
            appointment_id = int(input("Enter the appointment ID to cancel: "))
            cancel_appointment(appointment_id)
        elif choice == '4':
            doctor_id = int(input("Enter the doctor ID to book an appointment with: "))
            book_appointment(patient.id, doctor_id)
        elif choice == '5':
            update_patient(patient)
            
def main():
    while True:
        print("1- Doctor\n2- Patient\nPress 0 to exit...")
        choice = input("Enter your choice: ")
        if choice == '1':
            doctor()
        elif choice == '2':
           patient()
        elif choice == '0':
            print("Exiting the application. Goodbye!")
            break




if __name__ == "__main__":
    print("\n\n==================================================")
    print("================== Tabibak Site ==================")
    print("==================================================\n\n")
    main()
