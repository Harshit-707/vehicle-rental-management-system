# PS No. 66 - Vehicle Rental Management System
# Language: Python 3
# Concepts: OOP, Lists, Dictionaries, File Handling

FILE_NAME = "vehicles.txt"   # file where all vehicles are saved


# ---------------------------------------------------------
# CLASS 1: Vehicle
# Stores the details of ONE vehicle (id, type, model, rate, availability)
# ---------------------------------------------------------
class Vehicle:
    def __init__(self, vid, vtype, model, rate, available=True):
        self.id = vid
        self.type = vtype
        self.model = model
        self.rate = rate
        self.available = available

    # Returns the text used when we print a vehicle
    def show(self):
        if self.available:
            status = "Available"
        else:
            status = "Rented"
        return self.id + " | " + self.type + " | " + self.model + " | Rs. " + str(self.rate) + "/day | " + status


# ---------------------------------------------------------
# CLASS 2: Rental
# Manages all vehicles: add, rent, return, view, save, load
# ---------------------------------------------------------
class Rental:
    def __init__(self):
        self.vehicles = []   # LIST  -> keeps all Vehicle objects
        self.rentals = {}    # DICTIONARY -> vehicle ID : [customer name, days]

    # Find a vehicle in the list using its ID (returns None if not found)
    def find(self, vid):
        for v in self.vehicles:
            if v.id.upper() == vid.upper():
                return v
        return None

    # 1. ADD VEHICLE
    def add_vehicle(self, vtype, model, rate):
        new_id = "V" + str(len(self.vehicles) + 1)    # V1, V2, V3 ...
        v = Vehicle(new_id, vtype, model, rate)
        self.vehicles.append(v)
        self.save()
        print("Vehicle added. " + v.show())

    # 2. RENT VEHICLE
    def rent(self, vid, customer, days):
        v = self.find(vid)

        if v is None:
            print("Vehicle " + vid + " not found.")
        elif not v.available:                          # already rented -> block it
            print("Vehicle " + v.id + " is not available.")
        elif days < 1:                                 # days must be 1 or more
            print("Days must be 1 or more.")
        else:
            bill = v.rate * days                       # bill = rate per day x days
            if days >= 7:                              # 10% discount for 7 or more days
                bill = bill - bill * 10 // 100
                discount_text = " 10% discount applied."
            else:
                discount_text = ""

            v.available = False                        # vehicle is now rented
            self.rentals[v.id] = [customer, days]      # store rental details in dictionary
            self.save()
            print(v.id + " rented to " + customer + " for " + str(days) + " days." + discount_text + " Bill: Rs. " + str(bill))

    # 3. RETURN VEHICLE
    def return_vehicle(self, vid):
        v = self.find(vid)

        if v is None:
            print("Vehicle " + vid + " not found.")
        elif v.available:
            print("Vehicle " + v.id + " is not rented.")
        else:
            v.available = True                         # vehicle is free again
            del self.rentals[v.id]                     # remove rental details from dictionary
            self.save()
            print(v.id + " returned. Status: Available")

    # 4. VIEW AVAILABLE VEHICLES
    def view_available(self):
        found = False
        for v in self.vehicles:
            if v.available:
                if not found:
                    print("Available vehicles:")
                    found = True
                print(v.show())
        if not found:
            print("No vehicles available.")

    # FILE HANDLING: save every vehicle in vehicles.txt (one line per vehicle)
    def save(self):
        file = open(FILE_NAME, "w")
        for v in self.vehicles:
            customer = "-"
            days = 0
            if v.id in self.rentals:
                customer = self.rentals[v.id][0]
                days = self.rentals[v.id][1]
            line = v.id + "|" + v.type + "|" + v.model + "|" + str(v.rate) + "|" + str(v.available) + "|" + customer + "|" + str(days)
            file.write(line + "\n")
        file.close()

    # FILE HANDLING: load vehicles from vehicles.txt when the program starts
    def load(self):
        try:
            file = open(FILE_NAME, "r")
        except FileNotFoundError:                      # first run -> no file yet
            return
        for line in file:
            p = line.strip().split("|")
            if len(p) == 7:
                available = (p[4] == "True")
                self.vehicles.append(Vehicle(p[0], p[1], p[2], int(p[3]), available))
                if not available:
                    self.rentals[p[0]] = [p[5], int(p[6])]
        file.close()


# ---------------------------------------------------------
# MAIN PROGRAM: shows the menu and calls the right method
# ---------------------------------------------------------
shop = Rental()
shop.load()                                            # load saved data at start

while True:
    print("\n===== Vehicle Rental Management System =====")
    print("1. Add vehicle")
    print("2. Rent vehicle")
    print("3. Return vehicle")
    print("4. View available vehicles")
    print("5. Exit")
    choice = input("Enter your choice: ")
    

    if choice == "1":
        vtype = input("Type: ")
        model = input("Model: ")
        rate = input("Rate per day: ")
        if rate.isdigit() and int(rate) > 0:
            shop.add_vehicle(vtype, model, int(rate))
        else:
            print("Invalid rate.")

    elif choice == "2":
        vid = input("Vehicle ID: ")
        customer = input("Customer: ")
        days = input("Days: ")
        if days.isdigit():
            shop.rent(vid, customer, int(days))
        else:
            print("Invalid number of days.")

    elif choice == "3":
        vid = input("Vehicle ID: ")
        shop.return_vehicle(vid)

    elif choice == "4":
        shop.view_available()

    elif choice == "5":
        print("Thank you!")
        break

    else:
        print("Invalid choice. Please try again.")
