import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
class Item:
    def __init__(self, name, qty, price, category, expiry):
        self.name = name
        self.qty = qty
        self.price = price
        self.category = category
        self.expiry = expiry

    def update_qty(self, used):
        if used > self.qty:
            print("Not enough stock!")
        else:
            self.qty -= used
            print(f"{used} used. Remaining: {self.qty}")

    def value(self):
        return self.qty * self.price
inventory = []
def save_inventory():
    data = [vars(i) for i in inventory]
    with open("inventory.json", "w") as f:
        json.dump(data, f)
    print("Inventory saved!")

def load_inventory():
    try:
        with open("inventory.json") as f:
            data = json.load(f)
            for d in data:
                inventory.append(Item(**d))
        print("Inventory loaded!")
    except:
        print("No previous data found.")
def safe_float(msg):
    while True:
        try:
            return float(input(msg))
        except:
            print("Enter valid number!")

def safe_int(msg):
    while True:
        try:
            return int(input(msg))
        except:
            print("Enter valid integer!")
def add_item():
    name = input("Name: ")
    qty = safe_float("Qty: ")
    price = safe_float("Price: ")
    category = input("Category: ")
    expiry = input("Expiry: ")

    inventory.append(Item(name, qty, price, category, expiry))
    print("Item added!")

def view_items():
    if not inventory:
        print("No items")
        return
    for i in inventory:
        print(i.name, i.qty, i.price, i.category, i.expiry)
def consume_item():
    name = input("Item to consume: ")

    for i in inventory:
        if i.name.lower() == name.lower():
            used = safe_float("Qty used: ")
            i.update_qty(used)

            # prediction
            if used != 0:
                days = i.qty / used
                print(f"Will last approx {days:.1f} days")

            # log
            log = {
                "name": i.name,
                "used": used,
                "date": datetime.today().strftime("%Y-%m-%d")
            }
            print("Log:", log)
            return

    print("Item not found")
def numpy_analytics():
    if not inventory:
        print("No data")
        return

    prices = np.array([i.price for i in inventory])
    qtys = np.array([i.qty for i in inventory])

    print("Total Value:", np.sum(prices * qtys))
    print("Average Qty:", np.mean(qtys))
    print("Max Value:", np.max(prices * qtys))
def pandas_analytics():
    if not inventory:
        print("No data")
        return

    df = pd.DataFrame({
        "Name": [i.name for i in inventory],
        "Qty": [i.qty for i in inventory],
        "Price": [i.price for i in inventory],
        "Category": [i.category for i in inventory]
    })

    df["Total"] = df["Qty"] * df["Price"]

    print("\nInventory Table:")
    print(df)

    print("\nCategory Spending:")
    print(df.groupby("Category")["Total"].sum())
def show_charts():
    if not inventory:
        print("No data")
        return

    names = [i.name for i in inventory]
    prices = [i.price for i in inventory]

    plt.bar(names, prices)
    plt.title("Price Chart")
    plt.show()

    plt.hist(prices)
    plt.title("Price Distribution")
    plt.show()
load_inventory()

while True:
    print("\n===== HI-CAS MENU =====")
    print("1. Add Item")
    print("2. View Inventory")
    print("3. Consume Item")
    print("4. NumPy Analytics")
    print("5. Pandas Analytics")
    print("6. Show Charts")
    print("7. Save Data")
    print("8. Exit")

    ch = safe_int("Enter choice: ")

    if ch == 1:
        add_item()
    elif ch == 2:
        view_items()
    elif ch == 3:
        consume_item()
    elif ch == 4:
        numpy_analytics()
    elif ch == 5:
        pandas_analytics()
    elif ch == 6:
        show_charts()
    elif ch == 7:

        save_inventory()
    elif ch == 8:
        save_inventory()
        print("Exiting...")
        break
    else:
        print("Invalid choice!")