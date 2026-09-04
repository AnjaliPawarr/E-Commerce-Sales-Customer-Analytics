import pandas as pd
import numpy as np

np.random.seed(42)

# -----------------------------
# 1. CUSTOMERS DATA
# -----------------------------
num_customers = 5000

customers = pd.DataFrame({
    "customer_id": range(1, num_customers + 1),
    "customer_name": [f"Customer_{i}" for i in range(1, num_customers + 1)],
    "age": np.random.randint(18, 65, num_customers),
    "city": np.random.choice(
        ["Delhi", "Mumbai", "Bangalore", "Pune", "Hyderabad", "Chennai"],
        num_customers
    ),
    "gender": np.random.choice(
        ["Male", "Female"],
        num_customers
    )
})

# -----------------------------
# 2. PRODUCTS DATA
# -----------------------------
num_products = 100

products = pd.DataFrame({
    "product_id": range(1, num_products + 1),
    "product_name": [f"Product_{i}" for i in range(1, num_products + 1)],
    "category": np.random.choice(
        ["Electronics", "Clothing", "Home", "Beauty", "Sports"],
        num_products
    ),
    "price": np.round(
        np.random.uniform(200, 50000, num_products),
        2
    )
})

# -----------------------------
# 3. ORDERS DATA
# -----------------------------
num_orders = 50000

orders = pd.DataFrame({
    "order_id": range(1, num_orders + 1),
    "customer_id": np.random.randint(1, num_customers + 1, num_orders),
    "product_id": np.random.randint(1, num_products + 1, num_orders),
    "order_date": pd.to_datetime(
        np.random.choice(
            pd.date_range("2025-01-01", "2026-08-31"),
            num_orders
        )
    ),
    "quantity": np.random.randint(1, 5, num_orders)
})

# 3. ORDERS
num_orders = 50000

# Customers ko different purchase behavior dena
customer_weights = np.random.choice(
    [0, 1, 2, 3],
    size=num_customers,
    p=[0.10, 0.20, 0.30, 0.40]
)

customer_order_counts = np.random.multinomial(
    num_orders,
    np.ones(num_customers) / num_customers
)

# Kuch customers ko zyada orders assign karna
customer_order_counts = (
        customer_order_counts + customer_weights
)

# Total orders ko exactly 50,000 rakhna
difference = customer_order_counts.sum() - num_orders

if difference > 0:
    for _ in range(difference):
        customer_id = np.random.choice(np.where(customer_order_counts > 1)[0])
        customer_order_counts[customer_id] -= 1
else:
    for _ in range(abs(difference)):
        customer_id = np.random.randint(0, num_customers)
        customer_order_counts[customer_id] += 1

customer_ids = []

for customer_index, order_count in enumerate(customer_order_counts):
    customer_ids.extend(
        [customer_index + 1] * order_count
    )

np.random.shuffle(customer_ids)

orders = pd.DataFrame({
    "order_id": range(1, num_orders + 1),
    "customer_id": customer_ids,
    "product_id": np.random.randint(1, num_products + 1, num_orders),
    "order_date": pd.to_datetime(
        np.random.choice(
            pd.date_range("2025-01-01", "2026-08-31"),
            num_orders
        )
    ),
    "quantity": np.random.randint(1, 5, num_orders)
})

orders = orders.merge(
    products[["product_id", "price"]],
    on="product_id",
    how="left"
)

orders["total_amount"] = np.round(
    orders["quantity"] * orders["price"],
    2
)
# -----------------------------
# 4. SAVE CSV FILES
# -----------------------------
customers.to_csv("../data/customers.csv", index=False)
products.to_csv("../data/products.csv", index=False)
orders.to_csv("../data/orders.csv", index=False)

print("Dataset generated successfully!")
print(f"Customers: {len(customers)}")
print(f"Products: {len(products)}")
print(f"Orders: {len(orders)}")
