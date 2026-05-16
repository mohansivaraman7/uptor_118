import sqlite3
from datetime import datetime

# connect to database
conn = sqlite3.connect("purchases.db")
cursor = conn.cursor()

# create tables
cursor.execute(""" CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, 
                 password TEXT)""")
cursor.execute(""" CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY,name TEXT,
                    price REAL, quantity INTEGER)""")
cursor.execute(""" CREATE TABLE IF NOT EXISTS customers (id INTEGER PRIMARY KEY,
                    name TEXT, phone TEXT, email TEXT)""")
cursor.execute(""" CREATE TABLE IF NOT EXISTS orders (id INTEGER PRIMARY KEY,
                    customer_id INTEGER, total REAL, date TEXT)""")

conn.commit()

# login system

def login():
    username = input("Username: ")
    password = input("Password: ")

    cursor.execute("SELECT * FROM users WHERE username = ? AND password=?",
                   (username,password))
    user = cursor.fetchone()
    if user:
        print("Login Successful")
        return True
    else:
        print("Invalid login")
        return False

#     product functions

def add_product():
    name = input("Product name: ")
    price = float(input("Product price: "))
    quantity = int(input("Product quantity: "))
    cursor.execute("INSERT INTO products (name,price,quantity VALUES (?,?,?)",
                   (name,price,quantity))
    conn.commit()

    print("Product added successfully")

def show_products():
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()

    print("\n___Product List___")
    for p in products:
        print(p)


# customer functions

def add_customer():
    name = input("Customer name: ")
    phone = input("Customer phone: ")
    email = input("Customer email: ")
    cursor.execute("INSERT INTO customers (name,phone,email) VALUES (?,?,?)",
                   (name,phone,email))
    conn.commit()
    print("Customer added successfully")



#     order system


def create_order():
    customer_id = input("Customer ID: ")

    total = 0
    items = []

    while True:
        product_id = int(input("Product ID (0 to finish): "))
        if product_id == 0:
            break

        quantity = int(input("Quantity:"))

        cursor.execute("SELECT name,price,quantity FROM products WHERE id = ?",
                       (product_id,))
        product = cursor.fetchone()

        if product:
            name,price,stock = product

        if stock >= quantity:
            total+=price+quantity
            items.append([product_id,name,price,quantity])

            cursor.execute("UPDATE products SET price = ? WHERE id = ?",
                           (stock-quantity,product_id))
        else:
            print("Not enough stock")


        date = datetime.now().strftime("%y-%m-%d %H:%M:%S:")

        cursor.execute("INSERT INTO orders (customer_id,total,date) VALUES (?,?,?)",
                       (customer_id,total,date))
        conn.commit()
        print("\nOrder created successfully")
        print("Total bill", total)


#         Reports

def sales_report():
    cursor.execute("SELECT * FROM orders")
    orders = cursor.fetchall()

    print("\n___Sales Report___")
    for o in orders:
        print(o)



# Main Menu


def main_menu():
    while True:

        print("\n===SHOP MANAGEMENT===")
        print("1. Add product")
        print("2. Show products")
        print("3. Add customer")
        print("5 Sales Report")
        print("6 Exit")


        choice = input("Choose:")
        if choice == "1":
            add_product()

        elif choice == "2":
            show_products()

        elif choice == "3":
            add_customer()

        elif choice == "4":
            create_order()

        elif choice == "5":
            sales_report()

        elif choice == "6":
            break


# Default Admin

cursor.execute("INSERT OR IGNORE INTO users VALUES('admin','1234')")
conn.commit()



if login():
    main_menu()


conn.close()








