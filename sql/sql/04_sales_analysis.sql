-- E-Commerce Sales Analytics
-- Sales Analysis

USE DATABASE ECOMMERCE_DB;
USE SCHEMA SALES;


-- 1. Total Sales Revenue
-- Completed and Shipped orders are considered valid sales

SELECT
    SUM(oi.quantity * p.price) AS sales_revenue
FROM ORDERS o
JOIN ORDER_ITEMS oi
    ON o.order_id = oi.order_id
JOIN PRODUCTS p
    ON oi.product_id = p.product_id
WHERE o.order_status IN ('Completed', 'Shipped');


-- 2. Revenue by Category

SELECT
    p.category,
    SUM(oi.quantity * p.price) AS category_revenue
FROM ORDERS o
JOIN ORDER_ITEMS oi
    ON o.order_id = oi.order_id
JOIN PRODUCTS p
    ON oi.product_id = p.product_id
WHERE o.order_status IN ('Completed', 'Shipped')
GROUP BY p.category
ORDER BY category_revenue DESC;


-- 3. Revenue by Product

SELECT
    p.product_name,
    p.category,
    SUM(oi.quantity) AS units_sold,
    SUM(oi.quantity * p.price) AS product_revenue
FROM ORDERS o
JOIN ORDER_ITEMS oi
    ON o.order_id = oi.order_id
JOIN PRODUCTS p
    ON oi.product_id = p.product_id
WHERE o.order_status IN ('Completed', 'Shipped')
GROUP BY
    p.product_name,
    p.category
ORDER BY product_revenue DESC;


-- 4. Monthly Sales Revenue

SELECT
    DATE_TRUNC('MONTH', o.order_date) AS sales_month,
    SUM(oi.quantity * p.price) AS monthly_revenue
FROM ORDERS o
JOIN ORDER_ITEMS oi
    ON o.order_id = oi.order_id
JOIN PRODUCTS p
    ON oi.product_id = p.product_id
WHERE o.order_status IN ('Completed', 'Shipped')
GROUP BY DATE_TRUNC('MONTH', o.order_date)
ORDER BY sales_month;


-- 5. Monthly Order Count

SELECT
    DATE_TRUNC('MONTH', order_date) AS sales_month,
    COUNT(DISTINCT order_id) AS total_orders
FROM ORDERS
WHERE order_status IN ('Completed', 'Shipped')
GROUP BY DATE_TRUNC('MONTH', order_date)
ORDER BY sales_month;


-- 6. Average Order Value (AOV)

SELECT
    ROUND(
        SUM(oi.quantity * p.price)
        / COUNT(DISTINCT o.order_id),
        2
    ) AS average_order_value
FROM ORDERS o
JOIN ORDER_ITEMS oi
    ON o.order_id = oi.order_id
JOIN PRODUCTS p
    ON oi.product_id = p.product_id
WHERE o.order_status IN ('Completed', 'Shipped');


-- 7. Customer Revenue

SELECT
    c.customer_name,
    c.city,
    c.state,
    COUNT(DISTINCT o.order_id) AS total_orders,
    SUM(oi.quantity * p.price) AS customer_revenue
FROM CUSTOMERS c
JOIN ORDERS o
    ON c.customer_id = o.customer_id
JOIN ORDER_ITEMS oi
    ON o.order_id = oi.order_id
JOIN PRODUCTS p
    ON oi.product_id = p.product_id
WHERE o.order_status IN ('Completed', 'Shipped')
GROUP BY
    c.customer_name,
    c.city,
    c.state
ORDER BY customer_revenue DESC;


-- 8. Regional Sales by State

SELECT
    c.state,
    SUM(oi.quantity * p.price) AS state_revenue
FROM CUSTOMERS c
JOIN ORDERS o
    ON c.customer_id = o.customer_id
JOIN ORDER_ITEMS oi
    ON o.order_id = oi.order_id
JOIN PRODUCTS p
    ON oi.product_id = p.product_id
WHERE o.order_status IN ('Completed', 'Shipped')
GROUP BY c.state
ORDER BY state_revenue DESC;


-- 9. Order Status Summary

SELECT
    order_status,
    COUNT(*) AS total_orders
FROM ORDERS
GROUP BY order_status
ORDER BY total_orders DESC;
