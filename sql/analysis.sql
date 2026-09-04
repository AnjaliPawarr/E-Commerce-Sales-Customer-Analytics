-- ==========================================
-- E-COMMERCE SALES & CUSTOMER ANALYTICS
-- SQL ANALYSIS
-- ==========================================


-- 1. TOTAL REVENUE
SELECT
    SUM(total_amount) AS total_revenue
FROM orders;


-- 2. TOTAL ORDERS
SELECT
    COUNT(DISTINCT order_id) AS total_orders
FROM orders;


-- 3. AVERAGE ORDER VALUE
SELECT
    ROUND(AVG(total_amount), 2) AS average_order_value
FROM orders;


-- 4. MONTHLY REVENUE
SELECT
    DATE_FORMAT(order_date, '%Y-%m') AS month,
    ROUND(SUM(total_amount), 2) AS revenue
FROM orders
GROUP BY DATE_FORMAT(order_date, '%Y-%m')
ORDER BY month;


-- 5. CATEGORY-WISE REVENUE
SELECT
    p.category,
    ROUND(SUM(o.total_amount), 2) AS revenue
FROM orders o
JOIN products p
    ON o.product_id = p.product_id
GROUP BY p.category
ORDER BY revenue DESC;


-- 6. TOP 10 CUSTOMERS BY REVENUE
SELECT
    customer_id,
    ROUND(SUM(total_amount), 2) AS total_spend
FROM orders
GROUP BY customer_id
ORDER BY total_spend DESC
LIMIT 10;


-- 7. CUSTOMER ORDER FREQUENCY
SELECT
    customer_id,
    COUNT(order_id) AS total_orders
FROM orders
GROUP BY customer_id
ORDER BY total_orders DESC
LIMIT 10;


-- 8. TOP 10 PRODUCTS BY REVENUE
SELECT
    p.product_id,
    p.product_name,
    p.category,
    ROUND(SUM(o.total_amount), 2) AS revenue
FROM orders o
JOIN products p
    ON o.product_id = p.product_id
GROUP BY
    p.product_id,
    p.product_name,
    p.category
ORDER BY revenue DESC
LIMIT 10;


-- 9. REVENUE BY CITY
SELECT
    c.city,
    ROUND(SUM(o.total_amount), 2) AS revenue
FROM orders o
JOIN customers c
    ON o.customer_id = c.customer_id
GROUP BY c.city
ORDER BY revenue DESC;


-- 10. GENDER-WISE REVENUE
SELECT
    c.gender,
    ROUND(SUM(o.total_amount), 2) AS revenue
FROM orders o
JOIN customers c
    ON o.customer_id = c.customer_id
GROUP BY c.gender
ORDER BY revenue DESC;
-- ==========================================
-- ADVANCED SQL ANALYSIS
-- ==========================================


-- 11. CUSTOMER REVENUE RANKING
-- Rank customers based on total spending

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
LIMIT 10;


-- 12. CATEGORY REVENUE RANKING
-- Rank categories based on revenue

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
ORDER BY category_rank;


-- 13. MONTHLY REVENUE WITH PREVIOUS MONTH
-- Compare current month revenue with previous month

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
ORDER BY month;


-- 14. CUSTOMER SPENDING TIERS

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
    CASE
        WHEN total_spend >= 1000000 THEN 'High Spender'
        WHEN total_spend >= 500000 THEN 'Medium Spender'
        ELSE 'Low Spender'
    END AS spending_tier
FROM customer_revenue
ORDER BY total_spend DESC;
-- REPEAT VS ONE-TIME CUSTOMERS
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
GROUP BY customer_type;