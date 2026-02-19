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


# Step 2: Base course fee
course_fee = 200000

# Step 3: Analytics fee
def analytics_cost(subject, analytics, course_fee):
    if analytics == "Y":
        if subject != "DS":
            return course_fee * 0.10
        else:
            print("Analytics not available for DS")
            return 0
    return 0
analytics_fee = analytics_cost(subject, analytics, course_fee)


# Step 4: Hostel fee
def hostel_cost(hostel):
    if hostel == "Y":
        return 200000
    return 0
hostel_fee = hostel_cost(hostel)


# Step 5: Food fee
def food_cost(months):
    return months * 2000

food_fee = food_cost(food_months)

# Step 6: Transportation fee
def transport_cost(transport):
    if transport == "semester":
        return 13000
    elif transport == "annual":
        return 26000
    else:
        return 0
    
transport_fee = transport_cost(transport)

# Step 7: Total cost
total_cost = (
    course_fee +
    analytics_fee +
    hostel_fee +
    food_fee +
    transport_fee
)

# Step 8: Save bill to txt file
def save_bill(name,course_fee, analytics_fee, hostel_fee, food_fee, transport_fee, total):
    with open("annual_bill.txt", "a") as f:
        f.write("\n========================================================\n")
        f.write("--- Annual Cost Breakdown ---\n")
        f.write("Student Name: " + name + "\n")
        f.write("Course Fee: " + str(course_fee) + "\n")
        f.write("Analytics Fee: " + str(analytics_fee) + "\n")
        f.write("Hostel Fee: " + str(hostel_fee) + "\n")
        f.write("Food Fee: " + str(food_fee) + "\n")
        f.write("Transportation Fee: " + str(transport_fee) + "\n")
        f.write("Total Annual Cost: " + str(total) + "\n")

save_bill(name,course_fee, analytics_fee, hostel_fee, food_fee, transport_fee, total_cost)
