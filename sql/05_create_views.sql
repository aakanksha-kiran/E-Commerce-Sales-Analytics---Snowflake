-- E-Commerce Sales Analytics
-- Analytical Views

USE DATABASE ECOMMERCE_DB;
USE SCHEMA SALES;


-- 1. Detailed Sales View

CREATE OR REPLACE VIEW SALES_DETAIL_VIEW AS
SELECT
    c.customer_id,
    c.customer_name,
    c.city,
    c.state,
    o.order_id,
    o.order_date,
    o.order_status,
    p.product_id,
    p.product_name,
    p.category,
    p.price,
    oi.order_item_id,
    oi.quantity,
    oi.quantity * p.price AS revenue
FROM CUSTOMERS c
JOIN ORDERS o
    ON c.customer_id = o.customer_id
JOIN ORDER_ITEMS oi
    ON o.order_id = oi.order_id
JOIN PRODUCTS p
    ON oi.product_id = p.product_id;


-- 2. Monthly Sales View

CREATE OR REPLACE VIEW MONTHLY_SALES_VIEW AS
SELECT
    DATE_TRUNC('MONTH', order_date) AS sales_month,
    SUM(revenue) AS monthly_revenue,
    COUNT(DISTINCT order_id) AS total_orders
FROM SALES_DETAIL_VIEW
WHERE order_status IN ('Completed', 'Shipped')
GROUP BY DATE_TRUNC('MONTH', order_date)
ORDER BY sales_month;


-- 3. Product Sales View

CREATE OR REPLACE VIEW PRODUCT_SALES_VIEW AS
SELECT
    product_id,
    product_name,
    category,
    SUM(quantity) AS units_sold,
    SUM(revenue) AS product_revenue
FROM SALES_DETAIL_VIEW
WHERE order_status IN ('Completed', 'Shipped')
GROUP BY
    product_id,
    product_name,
    category
ORDER BY product_revenue DESC;


-- 4. Customer Sales View

CREATE OR REPLACE VIEW CUSTOMER_SALES_VIEW AS
SELECT
    customer_id,
    customer_name,
    city,
    state,
    COUNT(DISTINCT order_id) AS total_orders,
    SUM(revenue) AS customer_revenue
FROM SALES_DETAIL_VIEW
WHERE order_status IN ('Completed', 'Shipped')
GROUP BY
    customer_id,
    customer_name,
    city,
    state
ORDER BY customer_revenue DESC;
