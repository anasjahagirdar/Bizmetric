import pyodbc
import os

class DataBase:
    def __init__(self):
        self.conn = pyodbc.connect(
            r"DRIVER={ODBC Driver 17 for SQL Server};"
            r"SERVER=LAPTOP-NUB4LAN9\SQLEXPRESS;"
            r"DATABASE=hotel_bill_printing;"
            r"Trusted_Connection=yes;"
        )
        self.cursor = self.conn.cursor()
        print("Database Connected")

class Hotel(DataBase):
    def __init__(self):
        super().__init__()
        self.menu = {}
        self.load_menu()

    def load_menu(self):
        self.menu.clear()
        self.cursor.execute("SELECT menu_name, price FROM menu")
        for name, price in self.cursor.fetchall():
            self.menu[name.strip().lower()] = int(price)

    def show_menu(self):
        if not self.menu:
            print("Menu empty")
            return

        print("\n========= MENU =========")
        for item, price in self.menu.items():
            print(f"{item.title():15} : {price}")

    def add_item(self):
        name = input("Enter new item name: ").strip().lower()

        while True:
            try:
                price = int(input("Enter price: "))
                if price <= 0:
                    print("Price must be positive")
                    continue
                break
            except:
                print("Enter valid number")

        self.cursor.execute(
            "INSERT INTO menu(menu_name,price) VALUES (?,?)",
            (name, price)
        )
        self.conn.commit()

        print("Item Added Successfully")
        self.load_menu()

class Order:
    def __init__(self, hotel):
        self.hotel = hotel
        self.items = {}
        self.name = ""
    def take(self):
        self.name = input("Customer name: ").strip()
        while True:
            item = input("Enter food item (type DONE to finish): ").strip().lower()

            if item in ["done", "exit"]:
                if not self.items:
                    print("No items added yet")
                    continue
                break

            if item not in self.hotel.menu:
                print("Item not available")
                continue

            while True:
                try:
                    qty = int(input("Quantity: "))
                    if qty <= 0:
                        print("Enter quantity > 0")
                        continue
                    break
                except:
                    print("Enter valid quantity")

            self.items[item] = self.items.get(item, 0) + qty
            print(" Added")

    def save(self):
        if not self.items:
            print("Empty order not saved")
            return

        total = 0
        for item, qty in self.items.items():
            price = self.hotel.menu[item] * qty
            total += price

            self.hotel.cursor.execute(
                "INSERT INTO orders(cust_name,menu_name,quantity,price) VALUES(?,?,?,?)",
                (self.name, item, qty, price)
            )

        self.hotel.cursor.execute(
            "INSERT INTO bill(cust_name,total) VALUES (?,?)",
            (self.name, total)
        )

        self.hotel.conn.commit()

    def print_bill(self):
        count = 1
        while True:
            filename = f"{self.name}_Bill{count}.txt"
            if not os.path.exists(filename):
                break
            count += 1
        filename = f"{self.name}_HotelBill.txt"

        with open(filename, "w") as f:
            print("\n======= HOTEL BILL =======")
            f.write("======= HOTEL BILL =======\n")
            f.write(f"Customer: {self.name}\n")
            print("Customer:", self.name)
            f.write("-------------------------\n")

            total = 0
            for item, qty in self.items.items():
                price = self.hotel.menu[item] * qty
                total += price

                line = f"{item.title():15} {qty:3}   {price}"
                print(line)
                f.write(line + "\n")

            print("-------------------------")
            print("TOTAL =", total)

            f.write("-------------------------\n")
            f.write("TOTAL = " + str(total))

        print("Bill saved at:", os.path.abspath(filename))

def main():
    hotel = Hotel()

    while True:
        print("""
========= HOTEL SYSTEM =========
1 Show Menu
2 Add Item
3 Take Order
4 Exit
""")

        choice = input("Enter choice (1-4): ").strip()
        if choice == "1":
            hotel.show_menu()
        elif choice == "2":
            hotel.add_item()
        elif choice == "3":
            order = Order(hotel)
            order.take()
            if order.items:
                order.save()
                order.print_bill()
        elif choice == "4":
            print("Thank you please visit again ")
            break
        else:
            print("Invalid option")


main()