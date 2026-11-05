
import sqlite3
import pandas as pd

# Connect to the database
conn = sqlite3.connect("data.sqlite")


# ==========================================================
# STEP 1: Employees working in Boston
# ==========================================================

df_boston = pd.read_sql("""
    SELECT
        e.firstName,
        e.lastName,
        e.jobTitle
    FROM employees e
    JOIN offices o
        ON e.officeCode = o.officeCode
    WHERE o.city = 'Boston';
""", conn)


# ==========================================================
# STEP 2: Offices with zero employees
# ==========================================================

df_zero_emp = pd.read_sql("""
    SELECT
        o.city
    FROM offices o
    LEFT JOIN employees e
        ON o.officeCode = e.officeCode
    WHERE e.employeeNumber IS NULL;
""", conn)


# ==========================================================
# STEP 3: All employees and their office locations
# ==========================================================

df_employee = pd.read_sql("""
    SELECT
        e.firstName,
        e.lastName,
        o.city,
        o.state
    FROM employees e
    LEFT JOIN offices o
        ON e.officeCode = o.officeCode
    ORDER BY
        e.firstName ASC,
        e.lastName ASC;
""", conn)


# ==========================================================
# STEP 4: Customers who have not placed any orders
# ==========================================================

df_contacts = pd.read_sql("""
    SELECT
        c.contactFirstName,
        c.contactLastName,
        c.phone,
        c.salesRepEmployeeNumber
    FROM customers c
    LEFT JOIN orders o
        ON c.customerNumber = o.customerNumber
    WHERE o.orderNumber IS NULL
    ORDER BY c.contactLastName ASC;
""", conn)


# ==========================================================
# STEP 5: Customer payment details
# ==========================================================

df_payment = pd.read_sql("""
    SELECT
        c.contactFirstName,
        c.contactLastName,
        p.amount,
        p.paymentDate
    FROM customers c
    JOIN payments p
        ON c.customerNumber = p.customerNumber
    ORDER BY CAST(p.amount AS REAL) DESC;
""", conn)


# ==========================================================
# STEP 6: Employees with average customer credit
# limits greater than 90,000
# ==========================================================

df_credit = pd.read_sql("""
    SELECT
        e.employeeNumber,
        e.firstName,
        e.lastName,
        COUNT(c.customerNumber) AS numcustomers
    FROM employees e
    JOIN customers c
        ON e.employeeNumber = c.salesRepEmployeeNumber
    GROUP BY
        e.employeeNumber,
        e.firstName,
        e.lastName
    HAVING AVG(CAST(c.creditLimit AS REAL)) > 90000
    ORDER BY numcustomers DESC;
""", conn)


# ==========================================================
# STEP 7: Best-selling products
# ==========================================================

df_product_sold = pd.read_sql("""
    SELECT
        p.productName,
        COUNT(od.orderNumber) AS numorders,
        SUM(od.quantityOrdered) AS totalunits
    FROM products p
    JOIN orderdetails od
        ON p.productCode = od.productCode
    GROUP BY
        p.productCode,
        p.productName
    ORDER BY totalunits DESC;
""", conn)


# ==========================================================
# STEP 8: Number of unique customers per product
# ==========================================================

df_total_customers = pd.read_sql("""
    SELECT
        p.productName,
        p.productCode,
        COUNT(DISTINCT o.customerNumber) AS numpurchasers
    FROM products p
    JOIN orderdetails od
        ON p.productCode = od.productCode
    JOIN orders o
        ON od.orderNumber = o.orderNumber
    GROUP BY
        p.productCode,
        p.productName
    ORDER BY numpurchasers DESC;
""", conn)


# ==========================================================
# STEP 9: Number of customers per office
# ==========================================================

df_customers = pd.read_sql("""
    SELECT
        o.officeCode,
        o.city,
        COUNT(DISTINCT c.customerNumber) AS n_customers
    FROM offices o
    LEFT JOIN employees e
        ON o.officeCode = e.officeCode
    LEFT JOIN customers c
        ON e.employeeNumber = c.salesRepEmployeeNumber
    GROUP BY
        o.officeCode,
        o.city
    ORDER BY o.officeCode;
""", conn)


# ==========================================================
# STEP 10: Employees who sold products purchased
# by fewer than 20 distinct customers
# ==========================================================

df_under_20 = pd.read_sql("""
    WITH underperforming_products AS (
        SELECT
            od.productCode
        FROM orderdetails od
        JOIN orders o
            ON od.orderNumber = o.orderNumber
        GROUP BY od.productCode
        HAVING COUNT(DISTINCT o.customerNumber) < 20
    )
    SELECT DISTINCT
        e.employeeNumber,
        e.firstName,
        e.lastName,
        ofc.city,
        ofc.officeCode
    FROM employees e
    JOIN customers c
        ON e.employeeNumber = c.salesRepEmployeeNumber
    JOIN orders o
        ON c.customerNumber = o.customerNumber
    JOIN orderdetails od
        ON o.orderNumber = od.orderNumber
    JOIN underperforming_products up
        ON od.productCode = up.productCode
    JOIN offices ofc
        ON e.officeCode = ofc.officeCode
    ORDER BY
        e.lastName,
        e.firstName;
""", conn)


# ==========================================================
# DISPLAY RESULTS
# ==========================================================

results = [
    ("STEP 1: Boston Employees", df_boston),
    ("STEP 2: Offices With Zero Employees", df_zero_emp),
    ("STEP 3: Employees and Office Locations", df_employee),
    ("STEP 4: Customers Without Orders", df_contacts),
    ("STEP 5: Customer Payments", df_payment),
    ("STEP 6: High-Credit Customer Sales Reps", df_credit),
    ("STEP 7: Best-Selling Products", df_product_sold),
    ("STEP 8: Unique Customers Per Product", df_total_customers),
    ("STEP 9: Customers Per Office", df_customers),
    ("STEP 10: Employees Selling Underperforming Products", df_under_20)
]

for heading, dataframe in results:
    print(f"\n{'=' * 60}")
    print(heading)
    print(f"{'=' * 60}")
    print(dataframe.to_string(index=False))
    print(f"\nTotal rows: {len(dataframe)}")


# ==========================================================
# VALIDATE EXPECTED RESULTS
# ==========================================================

print("\nVALIDATION CHECKS")

print(
    f"Step 4: {len(df_contacts)} customers without orders "
    f"(expected: 24)"
)

print(
    f"Step 6: {len(df_credit)} qualifying employees "
    f"(expected: 4)"
)


# ==========================================================
# STEP 11: Close the database connection
# ==========================================================

conn.close()

print("\nDatabase connection closed successfully.")
