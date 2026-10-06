# E-Commerce Sales Analytics using Snowflake & Streamlit

## Project Overview

The **E-Commerce Sales Analytics** project is an end-to-end data analytics solution developed to store, process, analyze, and visualize e-commerce sales data.

The project uses **Snowflake** for data storage, SQL-based analysis, data quality validation, and analytical views, while **Streamlit** is used to build an interactive dashboard for visualizing business insights.

The dashboard enables users to explore sales performance based on **state, product category, order status, and date range**.

---

## Objectives

- Store and manage e-commerce data using Snowflake.
- Perform data ingestion and data quality checks.
- Analyze sales and customer data using SQL.
- Calculate important business KPIs.
- Identify top-performing products and categories.
- Analyze customer and regional sales performance.
- Build an interactive dashboard using Streamlit.
- Provide meaningful insights for business decision-making.

---

## Technologies Used

- **Snowflake** – Cloud data warehouse
- **SQL** – Data analysis, transformation, and views
- **Python** – Data generation and application logic
- **Snowpark Python** – Snowflake data interaction
- **Streamlit** – Interactive dashboard
- **CSV** – Source data format

---

## Project Architecture

```text
CSV Data
   │
   ▼
Snowflake Stage
   │
   ▼
Snowflake Tables
   │
   ├── CUSTOMERS
   ├── PRODUCTS
   ├── ORDERS
   └── ORDER_ITEMS
   │
   ▼
SQL Analysis & Data Quality Checks
   │
   ▼
Analytical Views
   │
   └── SALES_DETAIL_VIEW
   │
   ▼
Streamlit Dashboard
   │
   ├── KPIs
   ├── Sales Trends
   ├── Product Analysis
   ├── Category Analysis
   └── Customer Insights
```

---

## Dataset

The project uses four main datasets:

| Dataset | Description |
|---|---|
| `customers.csv` | Customer details such as name, email, city and state |
| `products.csv` | Product details including category and price |
| `orders.csv` | Order information including customer, date and status |
| `order_items.csv` | Products and quantities associated with each order |

### Dataset Size

- **100 Customers**
- **50 Products**
- **300 Orders**
- **600 Order Items**

---

## Snowflake Data Model

The project contains four main tables:

```text
CUSTOMERS
    │
    │ customer_id
    ▼
ORDERS
    │
    │ order_id
    ▼
ORDER_ITEMS
    │
    │ product_id
    ▼
PRODUCTS
```

### Main Relationships

- `CUSTOMERS.customer_id` → `ORDERS.customer_id`
- `ORDERS.order_id` → `ORDER_ITEMS.order_id`
- `ORDER_ITEMS.product_id` → `PRODUCTS.product_id`

---

## Data Quality Checks

Several checks were performed to validate the data:

- Duplicate customer IDs
- Missing customer IDs
- Invalid customer references
- Duplicate order IDs
- Invalid order references
- Duplicate product IDs
- Missing product IDs
- Invalid product references
- Invalid quantities
- Invalid product prices

The checks confirmed that the project data maintained valid relationships and acceptable values.

---

## Key Performance Indicators

The dashboard provides the following KPIs:

- Total Customers
- Total Products
- Total Orders
- Units Sold
- Sales Revenue
- Average Order Value (AOV)

For sales analysis, **Completed** and **Shipped** orders are considered valid sales, while **Pending** and **Cancelled** orders are excluded from sales revenue calculations.

---

## Dashboard Features

The Streamlit dashboard provides:

### Filters

- State
- Product Category
- Order Status
- Date Range

### Visualizations

- Monthly Sales Trend
- Top 5 Products by Revenue
- Sales by Category
- Top 5 Customers by Revenue
- Customer Details

The dashboard updates dynamically based on the selected filters.

---

## Analytical Views

The project includes analytical Snowflake views such as:

- `SALES_DETAIL_VIEW`
- `MONTHLY_SALES_VIEW`
- `PRODUCT_SALES_VIEW`
- `CUSTOMER_SALES_VIEW`

These views simplify analysis and provide a structured data layer for the dashboard.

---

## Project Structure

```text
ecommerce-sales-analytics-snowflake/
│
├── README.md
│
├── data/
│   ├── customers.csv
│   ├── products.csv
│   ├── orders.csv
│   └── order_items.csv
│
├── sql/
│   ├── 01_create_database_schema.sql
│   ├── 02_create_tables.sql
│   ├── 03_data_quality_checks.sql
│   ├── 04_sales_analysis.sql
│   └── 05_create_views.sql
│
├── streamlit/
│   └── streamlit_app.py
│
├── screenshots/
│   ├── dashboard_overview.png
│   ├── filters.png
│   └── customer_insights.png
│
└── docs/
    └── project_documentation.md
```

---

## Outcome

The project successfully demonstrates an end-to-end analytics workflow, starting from raw e-commerce data ingestion and validation in Snowflake to SQL-based analysis and interactive visualization through Streamlit.

It provides a practical view of sales performance, product performance, category contribution, customer behavior, and sales trends.

---

## Future Enhancements

- Add automated data pipelines for continuous data ingestion.
- Add sales forecasting using machine learning.
- Add customer segmentation.
- Add advanced business KPIs.
- Deploy the dashboard for wider access.

---

## Project Demo

A demo of the interactive dashboard is available through the project demo video.

**Demo:** Scan the QR code below to view the project demo videos.

---

## Author
**Aakanksha K**

E-Commerce Sales Analytics Project  
Snowflake | SQL | Python | Streamlit
