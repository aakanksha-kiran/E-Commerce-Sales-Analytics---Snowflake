-- E-Commerce Sales Analytics
-- Table Creation

USE DATABASE ECOMMERCE_DB;
USE SCHEMA SALES;

-- Customers table
CREATE TABLE CUSTOMERS (
    customer_id INTEGER,
    customer_name VARCHAR,
    email VARCHAR,
    city VARCHAR,
    state VARCHAR,
    country VARCHAR,
    PRIMARY KEY (customer_id)
);

-- Products table
CREATE TABLE PRODUCTS (
    product_id INTEGER,
    product_name VARCHAR,
    category VARCHAR,
    price DECIMAL(10,2),
    PRIMARY KEY (product_id)
);

-- Orders table
CREATE TABLE ORDERS (
    order_id INTEGER,
    customer_id INTEGER,
    order_date DATE,
    order_status VARCHAR,
    PRIMARY KEY (order_id)
);

-- Order items table
CREATE TABLE ORDER_ITEMS (
    order_item_id INTEGER,
    order_id INTEGER,
    product_id INTEGER,
    quantity INTEGER,
    PRIMARY KEY (order_item_id)
);
