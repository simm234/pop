class StockItem:
    # Class variable
    stock_category = "Car accessories"

    def __init__(self, stock_code, quantity, price):
        self.__stock_code = stock_code
        self.__quantity = quantity
        self.__price = price

    # Getters
    def get_stock_name(self):
        return "Unknown Stock Name"

    def get_stock_description(self):
        return "Unknown Stock Description"

    def get_price_without_vat(self):
        return self.__price

    def get_price_with_vat(self):
        vat_rate = self.get_vat()
        return round(self.__price * (1 + vat_rate / 100), 2)

    # Setters
    def set_price(self, new_price):
        if new_price > 0:
            self.__price = new_price

    # Methods
    def increase_stock(self, amount):
        if amount < 1:
            print("Error: Increased item must be greater than or equal to one.")
        elif self.__quantity + amount > 100:
            print("Error: Stock exceeds the maximum limit of 100.")
        else:
            self.__quantity += amount

    def sell_stock(self, amount):
        if amount < 1:
            print("Error: Sold amount must be greater than or equal to one.")
            return False
        elif amount <= self.__quantity:
            self.__quantity -= amount
            return True
        else:
            print("Error: Not enough stock to sell.")
            return False

    def get_vat(self):
        return 17.5  # Standard VAT rate

    def __str__(self):
        return (f"Stock Category: {StockItem.stock_category}\n"
                f"Stock Type: {self.get_stock_name()}\n"
                f"Description: {self.get_stock_description()}\n"
                f"StockCode: {self.__stock_code}\n"
                f"PriceWithoutVAT: {self.get_price_without_vat()}\n"
                f"PriceWithVAT: {self.get_price_with_vat()}\n"
                f"Total unit in stock: {self.__quantity}")


class NavSys(StockItem):
    def __init__(self, stock_code, quantity, price, brand):
        super().__init__(stock_code, quantity, price)
        self.__brand = brand

    # Overridden methods
    def get_stock_name(self):
        return "Navigation system"

    def get_stock_description(self):
        return "GeoVision Sat Nav"

    def __str__(self):
        return (super().__str__() +
                f"\nBrand: {self.__brand}")


# Example Usage
if __name__ == "__main__":
    # Creating a stock item
    stock = StockItem("W101", 10, 99.99)
    print(stock)
    print("\nIncreasing stock by 10...")
    stock.increase_stock(10)
    print(stock)
    print("\nSelling 2 units...")
    stock.sell_stock(2)
    print(stock)
    print("\nSetting new price to 100.99...")
    stock.set_price(100.99)
    print(stock)

    # Creating a NavSys item
    print("\nCreating a navigation system item...")
    navsys = NavSys("NS101", 10, 99.99, "TomTom")
    print(navsys)
    print("\nIncreasing stock by 10...")
    navsys.increase_stock(10)
    print(navsys)
    print("\nSelling 2 units...")
    navsys.sell_stock(2)
    print(navsys)
    print("\nSetting new price to 100.99...")
    navsys.set_price(100.99)
    print(navsys)
