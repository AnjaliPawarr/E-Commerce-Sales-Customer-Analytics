import pandas as pd
import sqlite3

# Load CSV files
customers = pd.read_csv("../data/customers.csv")
products = pd.read_csv("../data/products.csv")
orders = pd.read_csv("../data/orders.csv")

# Connect to SQLite database
connection = sqlite3.connect("../data/ecommerce.db")

# Load data into database tables
customers.to_sql("customers", connection, if_exists="replace", index=False)
products.to_sql("products", connection, if_exists="replace", index=False)
orders.to_sql("orders", connection, if_exists="replace", index=False)

connection.close()

print("Database created successfully!")
print("Tables created:")
print("- customers")
print("- products")
print("- orders")