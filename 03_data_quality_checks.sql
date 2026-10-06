-- E-Commerce Sales Analytics
-- Data Quality Checks

USE DATABASE ECOMMERCE_DB;
USE SCHEMA SALES;

-- 1. Check for duplicate customer IDs
SELECT
    customer_id,
    COUNT(*) AS duplicate_count
FROM CUSTOMERS
GROUP BY customer_id
HAVING COUNT(*) > 1;


-- 2. Check for missing customer IDs
SELECT *
FROM CUSTOMERS
WHERE customer_id IS NULL;


-- 3. Check for invalid customer references in orders
SELECT o.*
FROM ORDERS o
LEFT JOIN CUSTOMERS c
    ON o.customer_id = c.customer_id
WHERE c.customer_id IS NULL;


-- 4. Check for duplicate order IDs
SELECT
    order_id,
    COUNT(*) AS duplicate_count
FROM ORDERS
GROUP BY order_id
HAVING COUNT(*) > 1;


-- 5. Check for invalid order references in order items
SELECT oi.*
FROM ORDER_ITEMS oi
LEFT JOIN ORDERS o
    ON oi.order_id = o.order_id
WHERE o.order_id IS NULL;


-- 6. Check for duplicate product IDs
SELECT
    product_id,
    COUNT(*) AS duplicate_count
FROM PRODUCTS
GROUP BY product_id
HAVING COUNT(*) > 1;


-- 7. Check for missing product IDs
SELECT *
FROM PRODUCTS
WHERE product_id IS NULL;


-- 8. Check for invalid product references in order items
SELECT oi.*
FROM ORDER_ITEMS oi
LEFT JOIN PRODUCTS p
    ON oi.product_id = p.product_id
WHERE p.product_id IS NULL;


-- 9. Check for invalid quantities
SELECT *
FROM ORDER_ITEMS
WHERE quantity <= 0;


-- 10. Check for invalid product prices
SELECT *
FROM PRODUCTS
WHERE price <= 0;
