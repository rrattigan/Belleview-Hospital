# Belleview-Hospital
This Repository entails all the code for my Hospital Management System

======================================
BELLEVIEW HOSPITAL (BH) - README
======================================

Romario Rattigan - 20243502
July 20th, 2025
Programming Techniques: ITT103
https://github.com/rrattigan

1. PURPOSE OF THE PROGRAM
-------------------------
This program is a command-line based Hospital Management System (HMS) developed in Python. It simulates the core administrative functions of a hospital to streamline operations and improve data management. The system is designed to handle patient registration, doctor administration, appointment scheduling, and billing in an efficient, menu-driven interface. It serves as a practical demonstration of Object-Oriented Programming (OOP), modular design, and exception handling in Python.


2. HOW TO RUN IT
----------------
To run this application, you need to have Python 3 installed on your system.

1. Save the code: Save the provided Python code into a file named `Belleview_Hospital.py`.
2. Open a terminal/command prompt:
   - On Windows, open Command Prompt or PowerShell.
   - On macOS or Linux, open the Terminal.
3. Navigate to the file's directory: Use the `cd` command to change to the directory where you saved `Belleview_Hospital.py`.
   Example: cd C:\Users\YourUser\Documents
4. Run the program: Execute the following command in the terminal:
   python Belleview_Hospital.py

The program will start, and you will be greeted with the main menu. Follow the on-screen prompts to interact with the system.


3. PROGRAM FUNCTIONALITIES
--------------------------
The system is navigated through a series of menus.

A. Patient Management
   - Register New Patient: Allows the user to enter a new patient's name, age, and gender. The system automatically assigns a unique patient ID (e.g., P101) and confirms the registration.
   - View Patient Details: Prompts for a patient ID and displays the patient's full profile, including personal details and a list of all their scheduled or past appointments.

B. Doctor Management
   - Add New Doctor: Allows the user to add a new doctor by providing their name, age, gender, and specialty. The user can also define the doctor's weekly schedule by entering dates (YYYY-MM-DD) and available time slots (HH:MM). A unique doctor ID (e.g., D201) is auto-generated.
   - View Doctor Profiles & Schedule: Lists all available doctors. The user can then choose to view the detailed profile and availability of a specific doctor.

C. Appointment Management
   - Book New Appointment: Guides the user through booking an appointment. It requires selecting a registered patient and an available doctor. The system displays the doctor's schedule and prevents booking an appointment in a slot that is already taken or does not exist. Upon success, a confirmation message with a unique appointment ID (e.g., A301) is displayed.
   - View/Cancel Scheduled Appointments: Displays a formatted list of all appointments in the system with their status (Scheduled, Completed, Cancelled). The user can select an appointment by its ID to cancel it. Cancelling an appointment makes the doctor's time slot available again.

D. Generate Patient Bill
   - This option allows the user to generate a final bill for a 'Scheduled' appointment. After selecting an appointment, the system automatically adds a fixed consultation fee (JMD$ 3000). The user can then manually add any number of additional services and their costs (e.g., lab tests, medication).
   - Once all charges are entered, a well-formatted receipt is printed directly to the console, displaying the hospital name, patient/doctor details, an itemized list of services, and the total amount due. The appointment's status is then changed to 'Completed'.


4. REQUIRED MODIFICATIONS (FOR FUTURE DEVELOPMENT)
--------------------------------------------------
- Data Persistence: The current system stores all data in memory. This means all patient, doctor, and appointment information is lost when the program is closed. To make this a persistent application, data should be stored in a file (e.g., using JSON, CSV, or Pickle) or a database (e.g., SQLite, PostgreSQL).
- Date/Time Validation: The date and time inputs rely on user-provided strings. More robust validation could be added using Python's `datetime` library to ensure logical consistency (e.g., cannot book appointments in the past).
- User Authentication: The system is open to any user. A login system with different roles (e.g., admin, receptionist) could be implemented to control access to different functionalities.


5. ASSUMPTIONS OR LIMITATIONS
-----------------------------
- In-Memory Data: As mentioned, all data is volatile and exists only for the duration of the program's execution.
- Single-User System: The application is designed for a single user interacting via one console. It does not support concurrent operations.
- ID Generation: IDs are generated sequentially and are unique only within a single run of the program. They will reset every time the program starts.
- Fixed Currency: The billing system uses a hardcoded currency (JMD$). This would need modification to be used in other regions.
- No GUI: The interface is entirely text-based and runs in the command line.
