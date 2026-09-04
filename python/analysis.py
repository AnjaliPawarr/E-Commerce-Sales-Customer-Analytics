import pandas as pd
import matplotlib.pyplot as plt
# Load datasets
customers = pd.read_csv("../data/customers.csv")
products = pd.read_csv("../data/products.csv")
orders = pd.read_csv("../data/orders.csv")

# Convert order_date to datetime
orders["order_date"] = pd.to_datetime(orders["order_date"])

print("===== DATASET OVERVIEW =====")
print("Customers:", customers.shape)
print("Products:", products.shape)
print("Orders:", orders.shape)

print("\n===== CUSTOMER DATA =====")
print(customers.head())

print("\n===== PRODUCT DATA =====")
print(products.head())

print("\n===== ORDER DATA =====")
print(orders.head())

# Basic business metrics
total_revenue = orders["total_amount"].sum()
total_orders = orders["order_id"].nunique()
total_customers = orders["customer_id"].nunique()
average_order_value = total_revenue / total_orders

print("\n===== BUSINESS METRICS =====")
print(f"Total Revenue: ₹{total_revenue:,.2f}")
print(f"Total Orders: {total_orders:,}")
print(f"Unique Customers: {total_customers:,}")
print(f"Average Order Value: ₹{average_order_value:,.2f}")

# Top product categories
orders_products = orders.merge(
    products,
    on="product_id",
    how="left"
)

category_sales = (
    orders_products
    .groupby("category")["total_amount"]
    .sum()
    .sort_values(ascending=False)
)

print("\n===== SALES BY CATEGORY =====")
print(category_sales)

# Top 10 customers by revenue
customer_sales = (
    orders.groupby("customer_id")["total_amount"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print("\n===== TOP 10 CUSTOMERS =====")
print(customer_sales)


# -----------------------------
# MONTHLY REVENUE TREND
# -----------------------------

orders["month"] = orders["order_date"].dt.to_period("M").astype(str)

monthly_revenue = (
    orders.groupby("month")["total_amount"]
    .sum()
    .reset_index()
)

plt.figure(figsize=(12, 6))

plt.plot(
    monthly_revenue["month"],
    monthly_revenue["total_amount"],
    marker="o"
)

plt.title("Monthly Revenue Trend")
plt.xlabel("Month")
plt.ylabel("Revenue (₹)")
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig("../outputs/monthly_revenue.png")
#plt.show()
# -----------------------------
# CATEGORY-WISE SALES
# -----------------------------

category_sales = (
    orders_products
    .groupby("category")["total_amount"]
    .sum()
    .sort_values(ascending=False)
)

plt.figure(figsize=(10, 6))

category_sales.plot(kind="bar")

plt.title("Sales by Product Category")
plt.xlabel("Category")
plt.ylabel("Revenue (₹)")
plt.xticks(rotation=0)
plt.tight_layout()

plt.savefig("../outputs/category_sales.png")
# -----------------------------
# TOP 10 CUSTOMERS BY REVENUE
# -----------------------------

top_customers = (
    orders.groupby("customer_id")["total_amount"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .sort_values()
)

plt.figure(figsize=(10, 6))

top_customers.plot(kind="barh")

plt.title("Top 10 Customers by Revenue")
plt.xlabel("Revenue (₹)")
plt.ylabel("Customer ID")
plt.tight_layout()

plt.savefig("../outputs/top_10_customers.png")
# -----------------------------
# RFM CUSTOMER ANALYSIS
# -----------------------------

# Reference date = day after the last order
reference_date = orders["order_date"].max() + pd.Timedelta(days=1)

rfm = orders.groupby("customer_id").agg(
    recency=("order_date", lambda x: (reference_date - x.max()).days),
    frequency=("order_id", "count"),
    monetary=("total_amount", "sum")
).reset_index()

print("\n===== RFM ANALYSIS =====")
print(rfm.head())

# Create RFM scores
rfm["recency_score"] = pd.qcut(
    rfm["recency"],
    4,
    labels=[4, 3, 2, 1]
).astype(int)

rfm["frequency_score"] = pd.qcut(
    rfm["frequency"].rank(method="first"),
    4,
    labels=[1, 2, 3, 4]
).astype(int)

rfm["monetary_score"] = pd.qcut(
    rfm["monetary"].rank(method="first"),
    4,
    labels=[1, 2, 3, 4]
).astype(int)

# Overall RFM score
rfm["rfm_score"] = (
        rfm["recency_score"]
        + rfm["frequency_score"]
        + rfm["monetary_score"]
)

# Customer segmentation
def segment_customer(score):
    if score >= 10:
        return "High Value"
    elif score >= 7:
        return "Medium Value"
    else:
        return "Low Value"

rfm["customer_segment"] = rfm["rfm_score"].apply(segment_customer)

print("\n===== CUSTOMER SEGMENTS =====")
print(rfm["customer_segment"].value_counts())

# Save RFM analysis
rfm.to_csv("../outputs/customer_rfm_analysis.csv", index=False)

print("\nRFM analysis saved successfully!")
# -----------------------------
# CUSTOMER SEGMENT DISTRIBUTION
# -----------------------------

segment_counts = rfm["customer_segment"].value_counts()

plt.figure(figsize=(8, 6))

segment_counts.plot(kind="bar")

plt.title("Customer Segment Distribution")
plt.xlabel("Customer Segment")
plt.ylabel("Number of Customers")
plt.xticks(rotation=0)
plt.tight_layout()

plt.savefig("../outputs/customer_segments.png")

plt.show()
