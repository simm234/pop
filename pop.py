import os
import json

class CarAccessory:
    def __init__(self, name, code, description, remaining_items, price_excl_vat):
        self.__name = name
        self.__code = code
        self.__description = description
        self.__remaining_items = remaining_items
        self.__price_excl_vat = price_excl_vat
        self.__price_incl_vat = self.__calculate_price_with_vat()

    def __calculate_price_with_vat(self):
        vat_rate = 0.15
        return round(self.__price_excl_vat * (1 + vat_rate), 2)

    def to_dict(self):
        return {
            "name": self.__name,
            "code": self.__code,
            "description": self.__description,
            "remaining_items": self.__remaining_items,  # Include remaining items
            "price_excl_vat": self.__price_excl_vat,
            "price_incl_vat": self.__price_incl_vat
        }

 

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data['name'],
            code=data['code'],
            description=data['description'],
            remaining_items=data['remaining_items'],
            price_excl_vat=data['price_excl_vat']
        )

car_accessories = [
    CarAccessory("Car Cover", "A001", "Protective cover for cars.", 200, 50.00),
    CarAccessory("Seat Covers", "A002", "Comfortable seat covers for all models.", 150, 30.00),
    CarAccessory("Steering Wheel Cover", "A003", "Grip-friendly steering wheel cover.", 100, 15.00),
    CarAccessory("Floor Mats", "A004", "Durable floor mats for cleanliness.", 450, 25.00),
    CarAccessory("Car Vacuum Cleaner", "A005", "Compact vacuum cleaner for cars.", 80, 40.00),
    CarAccessory("Air Freshener", "A006", "Long-lasting car air freshener.", 70, 5.00),
    CarAccessory("Sunshade", "A007", "Foldable sunshade for windshield.", 20, 20.00),
    CarAccessory("Phone Holder", "A008", "Adjustable phone holder for dashboard.", 530, 10.00),
    CarAccessory("Jump Starter", "A009", "Portable car jump starter.", 60, 70.00),
    CarAccessory("Car Battery Charger", "A010", "Efficient car battery charger.", 90, 60.00),
    CarAccessory("LED Headlights", "A011", "Bright and energy-efficient headlights.", 75, 80.00),
    CarAccessory("Tire Inflator", "A012", "Portable tire inflator pump.", 90, 35.00),
    CarAccessory("Dash Cam", "A013", "High-definition dash camera.", 45, 100.00),
    CarAccessory("Roof Rack", "A014", "Strong roof rack for luggage.", 30, 150.00),
    CarAccessory("Car Wash Kit", "A015", "Complete car cleaning kit.", 20, 325.00),
    CarAccessory("Wheel Covers", "A016", "Stylish wheel covers for all sizes.", 90, 50.00),
    CarAccessory("Backup Camera", "A017", "Rearview backup camera system.", 70, 120.00),
    CarAccessory("Tow Rope", "A018", "Heavy-duty tow rope.", 25, 30.00),
    CarAccessory("Car Organizer", "A019", "Multi-pocket car organizer.", 35, 15.00),
    CarAccessory("GPS Tracker", "A020", "Real-time GPS tracking device.", 60, 90.00),
    CarAccessory("Car Polisher", "A021", "Electric car polishing machine.", 40, 110.00),
    CarAccessory("Brake Pads", "A022", "High-performance brake pads.", 10, 445.00),
    CarAccessory("Car Jack", "A023", "Hydraulic car jack.", 80, 55.00),
    CarAccessory("Oil Filter", "A024", "Durable oil filter.", 20, 20.00),
    CarAccessory("Spark Plugs", "A025", "Efficient spark plugs.", 40, 10.00),
    CarAccessory("Fuel Additive", "A026", "Engine performance fuel additive.", 360, 15.00),
    CarAccessory("Windshield Wipers", "A027", "All-weather windshield wipers.", 50, 25.00),
    CarAccessory("Car Battery", "A028", "Long-lasting car battery.", 50, 200.00),
    CarAccessory("Exhaust Tip", "A029", "Stylish exhaust tip.", 20, 35.00),
    CarAccessory("Car Cover Lock", "A030", "Anti-theft car cover lock.", 50, 12.00),
    CarAccessory("Seat Belt Cushion", "A031", "Comfortable seat belt cushion.", 60, 8.00),
    CarAccessory("Rearview Mirror", "A032", "Wide-angle rearview mirror.", 100, 18.00),
    CarAccessory("License Plate Frame", "A033", "Stylish license plate frame.", 90, 10.00),
    CarAccessory("Anti-slip Mat", "A034", "Dashboard anti-slip mat.", 150, 6.00),
    CarAccessory("Car Alarm System", "A035", "Advanced car alarm system.", 30, 250.00),
    CarAccessory("Tire Pressure Monitor", "A036", "Real-time tire pressure monitor.", 50, 75.00),
    CarAccessory("Car Cleaning Gel", "A037", "Reusable car cleaning gel.", 100, 5.00),
    CarAccessory("Keyless Entry System", "A038", "Smart keyless entry system.", 20, 300.00),
    CarAccessory("Side Window Deflectors", "A039", "Rain guard side window deflectors.", 100, 40.00),
    CarAccessory("Underbody Coating", "A040", "Protective underbody coating.", 70, 100.00),
    CarAccessory("Car Paint Pen", "A041", "Scratch repair car paint pen.", 400, 12.00),
    CarAccessory("Portable Fridge", "A042", "Compact portable fridge for cars.", 50, 250.00),
    CarAccessory("Car Bluetooth Adapter", "A043", "Wireless car Bluetooth adapter.", 30, 20.00),
    CarAccessory("Headrest Pillow", "A044", "Ergonomic headrest pillow.", 25, 15.00),
    CarAccessory("Cup Holder Organizer", "A045", "Multi-functional cup holder organizer.", 50, 10.00),
    CarAccessory("Emergency Kit", "A046", "Complete car emergency kit.", 60, 80.00),
    CarAccessory("Car Wax", "A047", "Premium car wax for shine.", 15, 20.00),
    CarAccessory("Fog Lights", "A048", "Bright fog lights for safety.", 60, 70.00),
    CarAccessory("Cargo Net", "A049", "Stretchable cargo net for trunks.", 55, 25.00),
    CarAccessory("Roof Box", "A050", "Spacious roof box for storage.", 3, 500.00)
]


def read_accessories_from_file(filename):
    if not os.path.exists(filename):
        return []  # Return empty list if file does not exist
    
    with open(filename, 'r') as file:
        try:
            data_dicts = json.load(file)
            data = [CarAccessory(
                name=item['name'], 
                code=item['code'], 
                description=item['description'], 
                remaining_items=item['remaining_items'],
                price_excl_vat=item['price_excl_vat']
            ) for item in data_dicts]
        except json.JSONDecodeError:
            return []  # Return empty list if JSON decoding fails (e.g., empty file)
    return data

def write_accessories_to_file(filename, data):
    try:
        data_dicts = [item.to_dict() for item in data]
        with open(filename, 'w') as file:
            json.dump(data_dicts, file, indent=4)
    except Exception as e:
        print(f"Error writing to file: {e}")


def add_accessory(name, code, description, remaining_items, price_excl_vat, filename):
    accessories = read_accessories_from_file(filename)
    new_accessory = CarAccessory(name, code, description, remaining_items, price_excl_vat)
    accessories.append(new_accessory)
    write_accessories_to_file(filename, accessories)
    print(f"Added accessory: {new_accessory.to_dict()}")
# File to store accessories
filename = "pop.txt"






# File to store accessories
filename = "pop.txt"
write_accessories_to_file(filename, car_accessories)

def update_price(code, new_price):
    accessories = read_accessories_from_file(filename)
    for accessory in accessories:
        if accessory.to_dict()['code'] == code:
            accessory._CarAccessory__price_excl_vat = new_price  # Accessing the private attribute directly
            accessory._CarAccessory__price_incl_vat = round(new_price * 1.15, 2)
            break
    write_accessories_to_file(filename, accessories)


def delete_accessory(code):
    accessories = read_accessories_from_file(filename)
    accessories = [acc for acc in accessories if acc.to_dict()['code'] != code]
    write_accessories_to_file(filename, accessories)


# Read car accessories from pop.txt
def load_car_accessories(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            data = json.load(file)
            return [CarAccessory.from_dict(item) for item in data]
    else:
        print("File not found!")
        return []

# Load car accessories from pop.txt
car_accessories = load_car_accessories("pop.txt")

# You can now access car_accessories, which is a list of CarAccessory objects
for accessory in car_accessories:
    print(accessory.to_dict()) 

# Test read functionality
if __name__ == "__main__":
    accessories = read_accessories_from_file(filename)