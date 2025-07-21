# BelleView Hospital.py

import datetime

# --- Helper Functions ---
def print_header(title):
    """Prints a formatted header for sections."""
    print("\n" + "="*50)
    print(f"{title.center(50)}")
    print("="*50)

def get_valid_input(prompt, type_func):
    """Generic function to get validated input from the user."""
    while True:
        try:
            value = type_func(input(prompt))
            if type_func == int and value <= 0:
                print("Invalid input. Please enter a positive number.")
                continue
            return value
        except ValueError:
            print(f"Invalid input. Please enter a valid {type_func.__name__}.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

# --- Class Definitions ---

class Appointment:
    """Represents a single appointment."""
    def __init__(self, appointment_id, patient, doctor, date, time):
        self.appointment_id = appointment_id
        self.patient = patient
        self.doctor = doctor
        self.date = date
        self.time = time
        self.status = "Scheduled"  # Statuses: Scheduled, Completed, Cancelled
        self.bill = None

    def confirm(self):
        """Confirms the appointment."""
        self.status = "Scheduled"
        print(f"Appointment {self.appointment_id} has been confirmed.")

    def cancel(self):
        """Cancels the appointment."""
        self.status = "Cancelled"
        print(f"Appointment {self.appointment_id} has been cancelled.")
    
    def complete(self):
        """Marks the appointment as completed."""
        self.status = "Completed"

    def display_details(self):
        print(f"{self.appointment_id:<15} | {self.patient.name:<20} | Dr. {self.doctor.name:<20} | {self.date:<12} | {self.time:<8} | {self.status:<12}")

class Person:
    """Base class representing a person with common attributes."""
    def __init__(self, name, age, gender):
        if not isinstance(age, int) or age <= 0:
            raise ValueError("Age must be a positive integer.")
        self.name = name
        self.age = age
        self.gender = gender

    def display_info(self):
        """Displays the basic information of the person."""
        print(f"Name: {self.name}")
        print(f"Age: {self.age}")
        print(f"Gender: {self.gender}")

class Patient(Person):
    """Represents a patient, inheriting from Person."""
    def __init__(self, name, age, gender, patient_id):
        super().__init__(name, age, gender)
        self.patient_id = patient_id
        self.appointment_list = []

    def book_appointment(self, appointment):
        """Adds an appointment to the patient's record."""
        self.appointment_list.append(appointment)

    def view_profile(self):
        """Displays the full patient profile."""
        print_header(f"Patient Profile: {self.patient_id}")
        super().display_info()
        print("\n--- Appointments ---")
        if not self.appointment_list:
            print("No appointments scheduled.")
        else:
            for appt in self.appointment_list:
                print(f"ID: {appt.appointment_id}, Dr. {appt.doctor.name}, Date: {appt.date}, Time: {appt.time}, Status: {appt.status}")

class Doctor(Person):
    """Represents a doctor, inheriting from Person."""
    def __init__(self, name, age, gender, doctor_id, specialty, schedule=None):
        super().__init__(name, age, gender)
        self.doctor_id = doctor_id
        self.specialty = specialty
        # Schedule is a dictionary: {'YYYY-MM-DD': ['HH:MM', 'HH:MM']}
        self.schedule = schedule if schedule is not None else {}

    def is_available(self, date, time):
        """Checks if the doctor is available at a specific date and time."""
        return date in self.schedule and time in self.schedule[date]

    def view_schedule(self):
        """Displays the doctor's available schedule."""
        print_header(f"Dr. {self.name}'s Schedule")
        super().display_info()
        print(f"Specialty: {self.specialty}")
        print("\n--- Availability ---")
        if not self.schedule:
            print("No available slots.")
        else:
            for date, times in sorted(self.schedule.items()):
                if times: # Only show dates with available slots
                    print(f"Date: {date}")
                    for time in sorted(times):
                        print(f"  - {time}")

    def add_schedule_slot(self, date, time):
        """Adds an available slot back to the schedule."""
        if date not in self.schedule:
            self.schedule[date] = []
        if time not in self.schedule[date]:
            self.schedule[date].append(time)

    def remove_schedule_slot(self, date, time):
        """Removes a booked slot from the schedule."""
        if self.is_available(date, time):
            self.schedule[date].remove(time)
            # If a date has no more slots, remove it for cleanliness
            if not self.schedule[date]:
                del self.schedule[date]

class BelleViewHospitalSystem:
    """The main class to manage the hospital operations."""
    def __init__(self):
        self.patients = {}  # Dict for O(1) lookups: {patient_id: patient_obj}
        self.doctors = {}   # Dict for O(1) lookups: {doctor_id: doctor_obj}
        self.appointments = {} # Dict for O(1) lookups: {appt_id: appt_obj}
        self._patient_id_counter = 100
        self._doctor_id_counter = 200
        self._appointment_id_counter = 300

    def _generate_id(self, prefix):
        """Generates a unique ID for patients, doctors, or appointments."""
        if prefix == "P":
            self._patient_id_counter += 1
            return f"P{self._patient_id_counter}"
        elif prefix == "D":
            self._doctor_id_counter += 1
            return f"D{self._doctor_id_counter}"
        elif prefix == "A":
            self._appointment_id_counter += 1
            return f"A{self._appointment_id_counter}"
        return None

    # --- Patient Management ---
    def add_patient(self):
        print_header("Register New Patient")
        name = input("Enter patient's full name: ")
        age = get_valid_input("Enter patient's age: ", int)
        gender = input("Enter patient's gender: ")

        patient_id = self._generate_id("P")
        new_patient = Patient(name, age, gender, patient_id)
        self.patients[patient_id] = new_patient
        print(f"\nPatient '{name}' registered successfully with Patient ID: {patient_id}")

    def view_patient_details(self):
        print_header("View Patient Details")
        if not self.patients:
            print("No patients registered in the system.")
            return
            
        patient_id = input("Enter Patient ID to view details: ").upper()
        patient = self.patients.get(patient_id)
        if patient:
            patient.view_profile()
        else:
            print(f"Error: Patient with ID '{patient_id}' not found.")

    # --- Doctor Management ---
    def add_doctor(self):
        print_header("Add New Doctor")
        name = input("Enter doctor's full name: ")
        age = get_valid_input("Enter doctor's age: ", int)
        gender = input("Enter doctor's gender: ")
        specialty = input("Enter doctor's specialty: ")
        
        doctor_id = self._generate_id("D")
        
        # Add schedule
        schedule = {}
        print("\nEnter doctor's availability (type 'done' when finished):")
        while True:
            date_str = input("Enter date (YYYY-MM-DD) or 'done': ")
            if date_str.lower() == 'done':
                break
            try:
                datetime.datetime.strptime(date_str, '%Y-%m-%d')
                times_str = input(f"Enter available times for {date_str} (HH:MM, space-separated): ")
                times = [t.strip() for t in times_str.split()]
                schedule[date_str] = times
            except ValueError:
                print("Invalid date format. Please use YYYY-MM-DD.")

        new_doctor = Doctor(name, age, gender, doctor_id, specialty, schedule)
        self.doctors[doctor_id] = new_doctor
        print(f"\nDr. '{name}' added successfully with Doctor ID: {doctor_id}")

    def view_doctor_details(self):
        print_header("View Doctor Profiles")
        if not self.doctors:
            print("No doctors registered in the system.")
            return

        print("Available Doctors:")
        for doc_id, doctor in self.doctors.items():
            print(f"  - {doc_id}: Dr. {doctor.name} ({doctor.specialty})")
        
        doc_id_to_view = input("Enter Doctor ID to view schedule or 'all' to list all: ").upper()
        if doc_id_to_view.lower() == 'all':
            for doctor in self.doctors.values():
                doctor.view_schedule()
        else:
            doctor = self.doctors.get(doc_id_to_view)
            if doctor:
                doctor.view_schedule()
            else:
                print(f"Error: Doctor with ID '{doc_id_to_view}' not found.")
    
    # --- Appointment Management ---
    def book_appointment(self):
        print_header("Book an Appointment")
        if not self.patients or not self.doctors:
            print("Error: Please register at least one patient and one doctor first.")
            return

        # List patients and doctors
        print("Registered Patients:")
        for pid, patient in self.patients.items(): print(f"  - {pid}: {patient.name}")
        patient_id = input("Enter Patient ID: ").upper()
        
        print("\nAvailable Doctors:")
        for did, doctor in self.doctors.items(): print(f"  - {did}: Dr. {doctor.name} ({doctor.specialty})")
        doctor_id = input("Enter Doctor ID: ").upper()
        
        try:
            patient = self.patients[patient_id]
            doctor = self.doctors[doctor_id]
        except KeyError:
            print("Error: Invalid Patient or Doctor ID.")
            return
            
        print("\n--- Viewing Doctor's Schedule ---")
        doctor.view_schedule()
        
        date = input("Enter desired appointment date (YYYY-MM-DD): ")
        time = input("Enter desired appointment time (HH:MM): ")

        # Check for conflicts
        if not doctor.is_available(date, time):
            print(f"Error: Dr. {doctor.name} is not available at the specified date and time.")
            return

        # Create and book appointment
        appointment_id = self._generate_id("A")
        appointment = Appointment(appointment_id, patient, doctor, date, time)
        self.appointments[appointment_id] = appointment
        patient.book_appointment(appointment)
        doctor.remove_schedule_slot(date, time) # Make slot unavailable
        
        appointment.confirm()
        print(f"Appointment booked for {patient.name} with Dr. {doctor.name} on {date} at {time}.")

    def view_or_cancel_appointment(self):
        print_header("View/Cancel Appointments")
        if not self.appointments:
            print("No appointments have been scheduled.")
            return

        print(f"{'Appointment ID':<15} | {'Patient Name':<20} | {'Doctor Name':<23} | {'Date':<12} | {'Time':<8} | {'Status':<12}")
        print("-" * 105)
        for appt in self.appointments.values():
            appt.display_details()
        
        appt_id = input("\nEnter Appointment ID to cancel (or press Enter to return): ").upper()
        if not appt_id:
            return
            
        appointment = self.appointments.get(appt_id)
        if not appointment:
            print(f"Error: Appointment with ID '{appt_id}' not found.")
            return
        
        if appointment.status == "Cancelled":
            print("This appointment has already been cancelled.")
            return
        
        # Cancel and restore schedule
        appointment.cancel()
        appointment.doctor.add_schedule_slot(appointment.date, appointment.time)
        print(f"The slot {appointment.date} at {appointment.time} has been made available again for Dr. {appointment.doctor.name}.")

    # --- Billing System ---
    def generate_bill(self):
        print_header("Generate The Patient's Bill")
        if not self.appointments:
            print("No appointments available to generate a bill.")
            return
            
        print("Select an appointment to generate a bill for (only 'Scheduled' appointments shown):")
        billable_appts = {aid: appt for aid, appt in self.appointments.items() if appt.status == "Scheduled"}
        
        if not billable_appts:
            print("No appointments are currently scheduled. A bill can only be generated for a 'Scheduled' appointment.")
            return

        for aid, appt in billable_appts.items():
            print(f"  - {aid}: Patient {appt.patient.name} with Dr. {appt.doctor.name} on {appt.date}")
        
        appt_id = input("Enter Appointment ID: ").upper()
        appointment = self.appointments.get(appt_id)

        if not appointment:
            print("Error: Appointment not found.")
            return
        if appointment.status != "Scheduled":
            print(f"Error: Cannot generate a bill for an appointment with status '{appointment.status}'.")
            return
            
        # Fees
        consultation_fee = 3000.00
        additional_charges = []
        total_additional = 0

        print("\nEnter additional services/charges (type 'done' when finished):")
        while True:
            service = input("Enter service name (e.g., Psychiatric Evaluation, Medication) or 'done': ")
            if service.lower() == 'done':
                break
            try:
                cost = get_valid_input(f"Enter cost for '{service}': JMD$ ", float)
                additional_charges.append({"service": service, "cost": cost})
                total_additional += cost
            except ValueError:
                print("Invalid cost. Please enter a number.")
        
        total_bill = consultation_fee + total_additional
        
        # Mark appointment as completed
        appointment.complete()
        
        # Display Receipt
        print("\n\n" + "*"*60)
        print("*" + "BELLEVIEW HOSPITAL - RECEIPT".center(58) + "*")
        print("*"*60)
        print(f"  Receipt for Appointment: {appointment.appointment_id}")
        print(f"  Date Issued: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("-" * 60)
        print(f"  Patient Name: {appointment.patient.name} (ID: {appointment.patient.patient_id})")
        print(f"  Consulting Doctor: Dr. {appointment.doctor.name} (ID: {appointment.doctor.doctor_id})")
        print("-" * 60)
        print("  SERVICES RENDERED:")
        print(f"    {'Consultation Fee':<30} JMD$ {consultation_fee:10.2f}")
        for item in additional_charges:
            print(f"    {item['service']:<30} JMD$ {item['cost']:10.2f}")
        print("-" * 60)
        print(f"  {'TOTAL AMOUNT DUE':<30} JMD$ {total_bill:10.2f}")
        print("*"*60)
        print("Thank you for choosing our hospital. Wishing you Strenght and Well-Being.".center(60))
        print("*"*60 + "\n")


# --- Main Application Loop ---

def main():
    BH = BelleViewHospitalSystem()
    print("Remember To Drink Water!")

    while True:
        choice = main_menu()
        try:
            if choice == '1':
                patient_menu(BH)
            elif choice == '2':
                doctor_menu(BH)
            elif choice == '3':
                appointment_menu(BH)
            elif choice == '4':
                BH.generate_bill()
            elif choice == '5':
                print("Thanks for your time. Goodbye!")
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 5.")
        except Exception as e:
            print(f"\nAn unexpected error occurred: {e}")
            print("Please check your input and try again.")
            
def main_menu():
    print("\n" + "—"*28)
    print("  BELLEVIEW HOSPITAL")
    print("—"*28)
    print("1. Patient Management")
    print("2. Doctor Management")
    print("3. Appointment Management")
    print("4. Generate The Patient's Bill")
    print("5. Exit")
    return input("Pick your poison [1-5]: ")

def patient_menu(BH):
    while True:
        print("\n--- Patient's ---")
        print("1. Register New Patient")
        print("2. View Patient Details")
        print("3. Back to Main Menu")
        choice = input("Enter choice: ")
        if choice == '1': BH.add_patient()
        elif choice == '2': BH.view_patient_details()
        elif choice == '3': break
        else: print("Invalid choice. Try again.")

def doctor_menu(BH):
    while True:
        print("\n--- Doctor's ---")
        print("1. Add New Doctor")
        print("2. View Doctor Profiles & Schedule")
        print("3. Back to Main Menu")
        choice = input("Enter choice: ")
        if choice == '1': BH.add_doctor()
        elif choice == '2': BH.view_doctor_details()
        elif choice == '3': break
        else: print("Invalid choice. Try again.")

def appointment_menu(BH):
    while True:
        print("\n--- Appointment's ---")
        print("1. Book New Appointment")
        print("2. View/Cancel Scheduled Appointments")
        print("3. Back to Main Menu")
        choice = input("Enter choice: ")
        if choice == '1': BH.book_appointment()
        elif choice == '2': BH.view_or_cancel_appointment()
        elif choice == '3': break
        else: print("Invalid choice. Try again.")




if __name__ == "__main__":
    main()
