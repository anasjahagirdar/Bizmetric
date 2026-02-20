import pyodbc

def get_user_input():
    name = input("Enter student name: ").strip()
    subject = input("Enter subject (HR / Finance / Marketing / DS): ").strip()
    analytics = input("Do you want Analytics? Press (Y/N): ").strip().upper()
    hostel = input("Do you want Hostel? Press (Y/N): ").strip().upper()

    if hostel == "Y":
        try:
            food_months = int(input("Enter number of food for months (0 if no food): "))
            if food_months < 0:
                food_months = 0
        except ValueError:
            food_months = 0
        transport = input("Transportation as per your (Semester/Annual): ").strip().lower()
    else:
        food_months = 0
        transport = "none"
    return name, subject, analytics, hostel, food_months, transport

name, subject, analytics, hostel, food_months, transport = get_user_input()

conn = pyodbc.connect(
    'DRIVER={SQL Server};'
    'SERVER=LAPTOP-NUB4LAN9\SQLEXPRESS;'
    'DATABASE=College_Project_DB;'
    'Trusted_Connection=yes;'
)
cursor = conn.cursor()

<<<<<<< HEAD
=======
#########################################################################################################################################
>>>>>>> 7a689d9 (updated project)
course_fee = 200000


def analytics_cost(subject, analytics, course_fee):
    if analytics == "Y":
        if subject != "DS":
            return course_fee * 0.10
        else:
            print("Analytics not available for DS")
            return 0
    return 0
analytics_fee = analytics_cost(subject, analytics, course_fee)



def hostel_cost(hostel):
    if hostel == "Y":
        return 200000
    return 0
hostel_fee = hostel_cost(hostel)



def food_cost(months):
    return months * 2000

food_fee = food_cost(food_months)

<<<<<<< HEAD
=======

>>>>>>> 7a689d9 (updated project)
def transport_cost(transport):
    if transport == "semester":
        return 13000
    elif transport == "annual":
        return 26000
    else:
        return 0
    
transport_fee = transport_cost(transport)

<<<<<<< HEAD
=======

>>>>>>> 7a689d9 (updated project)
total_cost = (
    course_fee +
    analytics_fee +
    hostel_fee +
    food_fee +
    transport_fee
)

<<<<<<< HEAD
=======

import os

>>>>>>> 7a689d9 (updated project)
def save_bill(name,course_fee, analytics_fee, hostel_fee, food_fee, transport_fee, total):
    filename = f"{name}_bill.txt" 
    folder = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(folder, filename)

    with open(filepath, "w") as f:
        f.write("\n========================================================\n")
        f.write("--- Annual Cost Of your College is ----\n")
        f.write("Student Name: " + name + "\n")
        f.write("Course Fee: " + str(course_fee) + "\n")
        f.write("Analytics Fee: " + str(analytics_fee) + "\n")
        f.write("Hostel Fee: " + str(hostel_fee) + "\n")
        f.write("Food Fee: " + str(food_fee) + "\n")
        f.write("Transportation Fee: " + str(transport_fee) + "\n")
        f.write("Total Annual Cost: " + str(total) + "\n")

    print("Bill saved:", filepath)


cursor.execute("""
INSERT INTO student_bill
(name, subject, analytics, hostel, food_months, transport, total_fee)
VALUES (?, ?, ?, ?, ?, ?, ?)
""", name, subject, analytics, hostel, food_months, transport, total_cost)

conn.commit()
print("Saved to database successfully!")

save_bill(name, course_fee, analytics_fee, hostel_fee, food_fee, transport_fee, total_cost) 
