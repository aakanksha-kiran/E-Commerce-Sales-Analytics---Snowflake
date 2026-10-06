import streamlit as st
import datetime

conn = st.connection("snowflake")
session = conn.session()


# -----------------------------
# Dashboard Title
# -----------------------------

st.title("E-commerce Sales Dashboard")
st.write("Sales performance overview")


# -----------------------------
# State Filter
# -----------------------------

states_result = session.sql("""
    SELECT DISTINCT state
    FROM ECOMMERCE_DB.SALES.CUSTOMERS
    ORDER BY state
""").collect()

states = [row["STATE"] for row in states_result]

selected_states = st.multiselect(
    "Select States",
    states
)


# -----------------------------
# Category Filter
# -----------------------------

categories_result = session.sql("""
    SELECT DISTINCT category
    FROM ECOMMERCE_DB.SALES.PRODUCTS
    ORDER BY category
""").collect()

categories = [row["CATEGORY"] for row in categories_result]

selected_categories = st.multiselect(
    "Select Categories",
    categories
)


# -----------------------------
# Order Status Filter
# -----------------------------

statuses_result = session.sql("""
    SELECT DISTINCT order_status
    FROM ECOMMERCE_DB.SALES.ORDERS
    ORDER BY order_status
""").collect()

statuses = [row["ORDER_STATUS"] for row in statuses_result]

selected_statuses = st.multiselect(
    "Select Order Status",
    statuses,
    default=["Completed", "Shipped"]
)

# Date Range Filter

st.write("### Date Range")

date_range = st.date_input(
    "Select Date Range",
    value=(
        datetime.date(2026, 1, 1),
        datetime.date(2026, 9, 30)
    ),
    min_value=datetime.date(2026, 1, 1),
    max_value=datetime.date(2026, 9, 30)
)

# -----------------------------
# Build State condition
# -----------------------------

state_condition = ""

if selected_states:
    state_values = ", ".join(
        [f"'{state}'" for state in selected_states]
    )

    state_condition = f"""
        AND state IN ({state_values})
    """


# -----------------------------
# Build Category condition
# -----------------------------

category_condition = ""

if selected_categories:
    category_values = ", ".join(
        [f"'{category}'" for category in selected_categories]
    )

    category_condition = f"""
        AND category IN ({category_values})
    """


# -----------------------------
# Build Status condition
# -----------------------------

status_condition = ""

if selected_statuses:
    status_values = ", ".join(
        [f"'{status}'" for status in selected_statuses]
    )

    status_condition = f"""
        AND order_status IN ({status_values})
    """
# Build Date condition

date_condition = ""

if len(date_range) == 2:

    start_date = date_range[0]
    end_date = date_range[1]

    date_condition = f"""
        AND order_date BETWEEN '{start_date}' AND '{end_date}'
    """

# -----------------------------
# Get KPI data
# -----------------------------
# KPI Query

kpi_result = session.sql(f"""
    SELECT
        COUNT(DISTINCT customer_id) AS total_customers,

        COUNT(DISTINCT order_id) AS total_orders,

        SUM(quantity) AS total_units_sold,

        SUM(revenue) AS sales_revenue,

        ROUND(
            SUM(revenue) / COUNT(DISTINCT order_id),
            2
        ) AS average_order_value

    FROM ECOMMERCE_DB.SALES.SALES_DETAIL_VIEW

    WHERE 1 = 1

    {state_condition}
    {category_condition}
    {status_condition}
    {date_condition}

""").collect()

# -----------------------------
# Get KPI values
# -----------------------------

total_customers = kpi_result[0]["TOTAL_CUSTOMERS"]
total_orders = kpi_result[0]["TOTAL_ORDERS"]
total_units_sold = kpi_result[0]["TOTAL_UNITS_SOLD"]
sales_revenue = kpi_result[0]["SALES_REVENUE"]
average_order_value = kpi_result[0]["AVERAGE_ORDER_VALUE"]


# -----------------------------
# Total Products
# -----------------------------
if selected_categories:

    category_values = ", ".join(
        [f"'{category}'" for category in selected_categories]
    )

    total_products = session.sql(f"""
        SELECT COUNT(*)
        FROM ECOMMERCE_DB.SALES.PRODUCTS
        WHERE category IN ({category_values})
    """).collect()[0][0]

else:

    total_products = session.sql("""
        SELECT COUNT(*)
        FROM ECOMMERCE_DB.SALES.PRODUCTS
    """).collect()[0][0]


# =========================================================
# KPI CARDS
# =========================================================

st.subheader("Sales Overview")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Total Customers",
        f"{total_customers:,}"
    )

with col2:
    st.metric(
        "Total Products",
        f"{total_products:,}"
    )

with col3:
    st.metric(
        "Total Orders",
        f"{total_orders:,}"
    )


col4, col5, col6 = st.columns(3)

with col4:
    st.metric(
        "Units Sold",
        f"{total_units_sold:,}"
    )

with col5:
    st.metric(
        "Sales Revenue",
        f"₹{sales_revenue:,.2f}"
    )

with col6:
    st.metric(
        "Average Order Value",
        f"₹{average_order_value:,.2f}"
    )

# =========================================================
# MONTHLY SALES TREND
# =========================================================

monthly_sales = session.sql(f"""
    SELECT
        DATE_TRUNC('MONTH', order_date) AS sales_month,
        SUM(revenue) AS monthly_revenue

    FROM ECOMMERCE_DB.SALES.SALES_DETAIL_VIEW

    WHERE 1 = 1

    {state_condition}
    {category_condition}
    {status_condition}
    {date_condition}

    GROUP BY DATE_TRUNC('MONTH', order_date)

    ORDER BY sales_month

""").to_pandas()


st.subheader("Monthly Sales Trend")

st.line_chart(
    monthly_sales,
    x="SALES_MONTH",
    y="MONTHLY_REVENUE"
)
# ---------------------------------------------------------
# TOP PRODUCTS + CATEGORY PERFORMANCE
# ---------------------------------------------------------

# Create two columns
product_col, category_col = st.columns(2)


# =========================================================
# TOP 5 PRODUCTS
# =========================================================

with product_col:

    st.subheader("Top 5 Products by Revenue")

    top_products = session.sql(f"""
        SELECT
            product_name,
            SUM(revenue) AS product_revenue

        FROM ECOMMERCE_DB.SALES.SALES_DETAIL_VIEW

        WHERE 1 = 1

        {state_condition}
        {category_condition}
        {status_condition}
        {date_condition}

        GROUP BY product_name

        ORDER BY product_revenue DESC

        LIMIT 5

    """).to_pandas()


    import altair as alt


    # Colors for the five products

    product_colors = [
        "#4C78A8",
        "#F58518",
        "#54A24B",
        "#E45756",
        "#B279A2"
    ]


    # Create product-color mapping

    color_mapping = {
        product: product_colors[i]
        for i, product in enumerate(top_products["PRODUCT_NAME"])
    }


    # Create donut chart

    donut_chart = alt.Chart(top_products).mark_arc(
        innerRadius=75
    ).encode(

        theta=alt.Theta(
            field="PRODUCT_REVENUE",
            type="quantitative"
        ),

        color=alt.Color(
            field="PRODUCT_NAME",
            type="nominal",

            scale=alt.Scale(
                domain=list(color_mapping.keys()),
                range=list(color_mapping.values())
            ),

            legend=None
        ),

        tooltip=[

            alt.Tooltip(
                "PRODUCT_NAME:N",
                title="Product"
            ),

            alt.Tooltip(
                "PRODUCT_REVENUE:Q",
                title="Revenue",
                format=",.2f"
            )
        ]

    ).properties(
        height=350
    )


    # Display donut chart

    st.altair_chart(
        donut_chart,
        use_container_width=True
    )


    # Product and revenue details

    st.write("**Product**                    **Revenue**")


    product_indicators = [
        "🔵",
        "🟠",
        "🟢",
        "🔴",
        "🟣"
    ]


    for i, row in top_products.iterrows():

        product_name = row["PRODUCT_NAME"]
        revenue = row["PRODUCT_REVENUE"]

        indicator = product_indicators[i]

        col_product, col_revenue = st.columns([2, 1])


        with col_product:

            st.write(
                f"{indicator} **{product_name}**"
            )


        with col_revenue:

            st.write(
                f"₹{revenue:,.2f}"
            )
# =========================================================
# CATEGORY PERFORMANCE
# =========================================================

with category_col:

    st.subheader("Sales by Category")

    category_sales = session.sql(f"""
        SELECT
            category,
            SUM(revenue) AS category_revenue

        FROM ECOMMERCE_DB.SALES.SALES_DETAIL_VIEW

        WHERE 1 = 1

        {state_condition}
        {category_condition}
        {status_condition}
        {date_condition}

        GROUP BY category

        ORDER BY category_revenue DESC

    """).to_pandas()


    st.bar_chart(
        category_sales,
        x="CATEGORY",
        y="CATEGORY_REVENUE"
    )
# =========================================================
# CUSTOMER INSIGHTS
# =========================================================

customer_sales = session.sql(f"""
    SELECT
        customer_name,
        city,
        state,

        COUNT(DISTINCT order_id) AS total_orders,

        SUM(revenue) AS customer_revenue

    FROM ECOMMERCE_DB.SALES.SALES_DETAIL_VIEW

    WHERE 1 = 1

    {state_condition}
    {category_condition}
    {status_condition}
    {date_condition}

    GROUP BY
        customer_name,
        city,
        state

    ORDER BY customer_revenue DESC

""").to_pandas()


st.subheader("Customer Insights")


# ---------------------------------------------------------
# TOP 5 CUSTOMERS
# ---------------------------------------------------------

top_customers = customer_sales.head(5)


st.write("### Top 5 Customers by Revenue")


st.bar_chart(
    top_customers,
    x="CUSTOMER_NAME",
    y="CUSTOMER_REVENUE",
    horizontal=True
)


# ---------------------------------------------------------
# CUSTOMER DETAILS
# ---------------------------------------------------------

st.write("### Customer Details")


customer_view = st.selectbox(
    "Choose Customer View",
    [
        "Top 5 Customers",
        "All Customers"
    ]
)


# Select data based on user choice

if customer_view == "Top 5 Customers":

    customer_details = customer_sales.head(5).copy()

else:

    customer_details = customer_sales.copy()


# Select required columns

customer_details = customer_details[
    [
        "CUSTOMER_NAME",
        "CITY",
        "STATE",
        "TOTAL_ORDERS",
        "CUSTOMER_REVENUE"
    ]
].copy()


# Rename columns

customer_details.columns = [
    "Customer",
    "City",
    "State",
    "Orders",
    "Revenue"
]


# Format revenue

customer_details["Revenue"] = customer_details["Revenue"].apply(
    lambda x: f"₹{x:,.2f}"
)


# Display table

st.dataframe(
    customer_details,
    use_container_width=True,
    hide_index=True
)
