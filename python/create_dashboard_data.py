import pandas as pd

# Load data
customers = pd.read_csv("../data/customers.csv")
products = pd.read_csv("../data/products.csv")
orders = pd.read_csv("../data/orders.csv")

# Convert date
orders["order_date"] = pd.to_datetime(orders["order_date"])

# Merge orders with customer and product information
dashboard_data = orders.merge(
    customers,
    on="customer_id",
    how="left"
)

dashboard_data = dashboard_data.merge(
    products,
    on="product_id",
    how="left",
    suffixes=("_order", "_product")
)

# Create useful date columns
dashboard_data["year"] = dashboard_data["order_date"].dt.year
dashboard_data["month"] = dashboard_data["order_date"].dt.month
dashboard_data["month_name"] = dashboard_data["order_date"].dt.strftime("%b")
dashboard_data["year_month"] = dashboard_data["order_date"].dt.strftime("%Y-%m")

# Save final dashboard dataset
dashboard_data.to_csv(
    "../outputs/dashboard_data.csv",
    index=False
)

print("Dashboard dataset created successfully!")
print("Rows:", len(dashboard_data))
print("Columns:", len(dashboard_data.columns))
print("Saved to: outputs/dashboard_data.csv")