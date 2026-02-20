import pyodbc
import os

# Using the Decorator as maam asked 
def log(func):
    def wrapper(self, *args, **kwargs):
        print("\nCalculating bill...")
        result = func(self, *args, **kwargs)
        print("Calculation finished!\n")
        return result
    return wrapper

class StudentBill:
    def __init__(self):
        self.course_fee = 200000
    def get_user_input(self):
        name = input("Enter student name : ").strip()
        subject = input("Enter subject you want (HR / Finance / Marketing / DS) : ").strip()
        analytics = input("Do you want Analytics as an extra add on ? Press (Y/N) : ").strip().upper()
        hostel = input("Do you want to stay in Hostel ? Press (Y/N) : ").strip().upper()

        if hostel == "Y":
            try:
                food_months = int(input("Enter number of food months (0 if no food): "))
                if food_months < 0:
                    food_months = 0
            except ValueError:
                food_months = 0
            transport = input("Transportation (Semester/Annual): ").strip().lower()
        else:
            food_months = 0
            transport = "none"

        self.name = name
        self.subject = subject
        self.analytics = analytics
        self.hostel = hostel
        self.food_months = food_months
        self.transport = transport

    def analytics_cost(self):
        if self.analytics == "Y":
            if self.subject != "DS":
                return self.course_fee * 0.10
            else:
                print("Analytics not available for DS")
        return 0

    def hostel_cost(self):
        if self.hostel == "Y":
            return 200000
        return 0

    def food_cost(self):
        return self.food_months * 2000

    def transport_cost(self):
        if self.transport == "semester":
            return 13000
        elif self.transport == "annual":
            return 26000
        return 0

    @log
    def calculate_total(self):

        self.analytics_fee = self.analytics_cost()
        self.hostel_fee = self.hostel_cost()
        self.food_fee = self.food_cost()
        self.transport_fee = self.transport_cost()
        self.total = (
            self.course_fee +
            self.analytics_fee +
            self.hostel_fee +
            self.food_fee +
            self.transport_fee
        )

    def save_bill(self):
        filename = f"{self.name}_bill.txt"
        folder = os.path.dirname(os.path.abspath(__file__))
        filepath = os.path.join(folder, filename)

        with open(filepath, "w") as f:
            f.write("\n========================================================\n")
            f.write("--- Annual Cost Of your College is ----\n")
            f.write("Student Name: " + self.name + "\n")
            f.write("Course Fee: " + str(self.course_fee) + "\n")
            f.write("Analytics Fee: " + str(self.analytics_fee) + "\n")
            f.write("Hostel Fee: " + str(self.hostel_fee) + "\n")
            f.write("Food Fee: " + str(self.food_fee) + "\n")
            f.write("Transportation Fee: " + str(self.transport_fee) + "\n")
            f.write("Total Annual Cost: " + str(self.total) + "\n")

        print("Bill saved:", filepath)

    def save_to_database(self):
        conn = pyodbc.connect(
            r'DRIVER={SQL Server};'
            r'SERVER=LAPTOP-NUB4LAN9\SQLEXPRESS;'
            r'DATABASE=College_Project_DB;'
            r'Trusted_Connection=yes;'
        )

        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO student_bill
        (name, subject, analytics, hostel, food_months, transport, total_fee)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        self.name,
        self.subject,
        self.analytics,
        self.hostel,
        self.food_months,
        self.transport,
        self.total
        )
        conn.commit()
        conn.close()
        print("Saved to database successfully!")

student = StudentBill()
student.get_user_input()
student.calculate_total()
student.save_to_database()
student.save_bill()
