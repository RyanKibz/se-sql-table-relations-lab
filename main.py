# STEP 1
# Replace None with your code
df_boston = None

df_boston = pd.read_sql("""
    SELECT
        employees.firstName,
        employees.lastName
    FROM employees
    JOIN offices
        ON employees.officeCode = offices.officeCode
    WHERE offices.city = 'Boston';
""", conn)


# STEP 2
# Replace None with your code
df_zero_emp = None
df_zero_emp = pd.read_sql("""
SELECT offices.city
FROM offices
LEFT JOIN employees
    ON offices.officeCode = employees.officeCode
WHERE employees.officeCode IS NULL;
""", conn)

# STEP 3
# Replace None with your code
df_employee = None
df_employee = pd.read_sql("""
SELECT
    employees.firstName,
    employees.lastName,
    offices.city,
    offices.state
FROM employees
LEFT JOIN offices
    ON employees.officeCode = offices.officeCode
ORDER BY
    employees.firstName ASC,
    employees.lastName ASC;
""", conn)

# STEP 4
# Replace None with your code
df_contacts = None
df_contacts = pd.read_sql("""
SELECT
    customers.contactFirstName,
    customers.contactLastName,
    customers.phone,
    customers.salesRepEmployeeNumber
FROM customers
LEFT JOIN orders
    ON customers.customerNumber = orders.customerNumber
WHERE orders.orderNumber IS NULL
ORDER BY customers.contactLastName ASC;
""", conn)

# STEP 5
# Replace None with your code
df_payment = None
df_payment = pd.read_sql("""
SELECT
    customers.contactFirstName,
    customers.contactLastName,
    payments.amount,
    payments.paymentDate
FROM customers
JOIN payments
    ON customers.customerNumber = payments.customerNumber
ORDER BY CAST(payments.amount AS REAL) DESC;
""", conn)

# STEP 6
# Replace None with your code
df_credit = None
df_credit = pd.read_sql("""
SELECT
    employees.employeeNumber,
    employees.firstName,
    employees.lastName,
    COUNT(customers.customerNumber) AS numcustomers
FROM employees 
JOIN customers
    ON employees.employeeNumber = customers.salesRepEmployeeNumber
GROUP BY
    employees.employeeNumber,
    employees.firstName,
    employees.lastName
HAVING AVG(customers.creditLimit) > 90000
ORDER BY numcustomers DESC
LIMIT 4;
""", conn)

# STEP 7
# Replace None with your code
df_product_sold = None
df_product_sold = pd.read_sql("""
SELECT
    products.productName,
    COUNT(orders.orderNumber) AS numorders,
    SUM(orders.quantityOrdered) AS totalunits
FROM products 
JOIN orderdetails orders
    ON products.productCode = orders.productCode
GROUP BY
    products.productCode,
    products.productName
ORDER BY totalunits DESC;
""", conn)

# STEP 8
# Replace None with your code
df_total_customers = None

df_total_customers = pd.read_sql("""
    SELECT
        products.productName,
        products.productCode,
        COUNT(DISTINCT orders.customerNumber) AS numpurchasers
    FROM products
    JOIN orderdetails od
        ON products.productCode = od.productCode
    JOIN orders
        ON od.orderNumber = orders.orderNumber
    GROUP BY
        products.productName,
        products.productCode
    ORDER BY numpurchasers DESC;
""", conn)


# STEP 9
# Replace None with your code
df_customers = None
df_customers = pd.read_sql("""
    SELECT
        offices.officeCode,
        offices.city,
        COUNT(customers.customerNumber) AS n_customers
    FROM offices
    JOIN employees
        ON offices.officeCode = employees.officeCode
    JOIN customers
        ON employees.employeeNumber = customers.salesRepEmployeeNumber
    GROUP BY offices.officeCode, offices.city
    ORDER BY offices.officeCode;
""", conn)

# STEP 10
# Replace None with your code
df_under_20 = None

df_under_20 = pd.read_sql("""
    WITH underperforming_products AS (
        SELECT od.productCode
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
    ORDER BY e.lastName, e.firstName;
""", conn)

conn.close()