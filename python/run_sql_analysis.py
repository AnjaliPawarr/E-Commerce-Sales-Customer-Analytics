import sqlite3

connection = sqlite3.connect("../data/ecommerce.db")

cursor = connection.cursor()

# 1. Total Revenue
cursor.execute("""
    SELECT ROUND(SUM(total_amount), 2)
    FROM orders
""")

total_revenue = cursor.fetchone()[0]

# 2. Total Orders
cursor.execute("""
    SELECT COUNT(DISTINCT order_id)
    FROM orders
""")

total_orders = cursor.fetchone()[0]

# 3. Average Order Value
cursor.execute("""
    SELECT ROUND(AVG(total_amount), 2)
    FROM orders
""")

average_order_value = cursor.fetchone()[0]

print("===== SQL BUSINESS ANALYSIS =====")
print(f"Total Revenue: ₹{total_revenue:,.2f}")
print(f"Total Orders: {total_orders:,}")
print(f"Average Order Value: ₹{average_order_value:,.2f}")

# 4. Category Revenue
cursor.execute("""
    SELECT
        p.category,
        ROUND(SUM(o.total_amount), 2) AS revenue
    FROM orders o
    JOIN products p
        ON o.product_id = p.product_id
    GROUP BY p.category
    ORDER BY revenue DESC
""")

print("\n===== CATEGORY REVENUE =====")

for category, revenue in cursor.fetchall():
    print(f"{category}: ₹{revenue:,.2f}")

# 5. Top 10 Customers
cursor.execute("""
    SELECT
        customer_id,
        ROUND(SUM(total_amount), 2) AS total_spend
    FROM orders
    GROUP BY customer_id
    ORDER BY total_spend DESC
    LIMIT 10
""")

print("\n===== TOP 10 CUSTOMERS =====")

for customer_id, spend in cursor.fetchall():
    print(f"Customer {customer_id}: ₹{spend:,.2f}")

# ==========================================
# ADVANCED SQL
# ==========================================

# 1. Customer Ranking
cursor.execute("""
WITH customer_revenue AS (
    SELECT
        customer_id,
        SUM(total_amount) AS total_spend
    FROM orders
    GROUP BY customer_id
)
SELECT
    customer_id,
    ROUND(total_spend, 2) AS total_spend,
    RANK() OVER (ORDER BY total_spend DESC) AS customer_rank
FROM customer_revenue
ORDER BY customer_rank
LIMIT 10
""")

print("\n===== TOP 10 CUSTOMER RANKING =====")

for customer_id, spend, rank in cursor.fetchall():
    print(f"Rank {rank}: Customer {customer_id} - ₹{spend:,.2f}")


# 2. Category Ranking
cursor.execute("""
WITH category_revenue AS (
    SELECT
        p.category,
        SUM(o.total_amount) AS revenue
    FROM orders o
    JOIN products p
        ON o.product_id = p.product_id
    GROUP BY p.category
)
SELECT
    category,
    ROUND(revenue, 2) AS revenue,
    RANK() OVER (ORDER BY revenue DESC) AS category_rank
FROM category_revenue
ORDER BY category_rank
""")

print("\n===== CATEGORY RANKING =====")

for category, revenue, rank in cursor.fetchall():
    print(f"Rank {rank}: {category} - ₹{revenue:,.2f}")


# 3. Month-over-Month Revenue
cursor.execute("""
WITH monthly_sales AS (
    SELECT
        strftime('%Y-%m', order_date) AS month,
        SUM(total_amount) AS revenue
    FROM orders
    GROUP BY strftime('%Y-%m', order_date)
)
SELECT
    month,
    ROUND(revenue, 2) AS revenue,
    ROUND(
        LAG(revenue) OVER (ORDER BY month),
        2
    ) AS previous_month_revenue
FROM monthly_sales
ORDER BY month
""")

print("\n===== MONTHLY REVENUE COMPARISON =====")

for month, revenue, previous_revenue in cursor.fetchall():

    if previous_revenue is None:
        previous_revenue_text = "N/A"
    else:
        previous_revenue_text = f"₹{previous_revenue:,.2f}"

    print(
        f"{month}: ₹{revenue:,.2f} | "
        f"Previous Month: {previous_revenue_text}"
    )
    # Repeat vs One-Time Customers

cursor.execute("""
WITH customer_orders AS (
    SELECT
        customer_id,
        COUNT(DISTINCT order_id) AS order_count
    FROM orders
    GROUP BY customer_id
)
SELECT
    CASE
        WHEN order_count = 1 THEN 'One-Time Customer'
        ELSE 'Repeat Customer'
    END AS customer_type,
    COUNT(*) AS customer_count
FROM customer_orders
GROUP BY customer_type
""")

print("\n===== CUSTOMER RETENTION ANALYSIS =====")

for customer_type, customer_count in cursor.fetchall():
    print(f"{customer_type}: {customer_count:,}")
connection.close()