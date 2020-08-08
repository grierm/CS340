# Name: Ben Nordstrom
# Date: Jul-25-2020
# CS 340 - 400 - Summer 2020
# Project Group 49 - The Castaways
# Project Step 4 - Draft - SQL B

# HTML interface for insert, select, delete, update
# -------------------------------------------------------------- #
# customers table queries
# -------------------------------------------------------------- #
# Select
SELECT customer_id, first_name, last_name, email, phone_number FROM customers;

# Insert (add data)
INSERT INTO customers (first_name, last_name, email, phone_number) VALUES (%s, %s, %s, %s)
data = (f_name, l_name, email, phone)

# Update
UPDATE customers SET first_name = %s, last_name = %s, email = %s, phone_number = %s WHERE customer_id = %s
data = (fname, lname, email, phone, cust_id)


# -------------------------------------------------------------- #
# invoices table queries
# -------------------------------------------------------------- #

# Select (note we did a join on wh locations to display city within html)
SELECT employees.employee_ID, employees.first_name, employees.last_name, employees.job_title, 
    warehouse_locations.location_city, warehouse_locations.location_ID FROM employees LEFT JOIN warehouse_locations
    ON employees.location_ID = warehouse_locations.location_ID;

# Insert
INSERT INTO employees (first_name, last_name, job_title, location_ID) VALUES (%s, %s, %s, %s)
data = (f_name, l_name, title, loc)


# -------------------------------------------------------------- #
# orders table queries
# -------------------------------------------------------------- #

# Select
SELECT order_ID, invoice_ID, order_amount, product_serial_number FROM orders;

# Insert
INSERT INTO orders (invoice_ID, order_amount, product_serial_number) VALUES (%s, %s, %s);

#Update (1:M nullify relationship point)
UPDATE orders SET invoice_ID = %s, order_amount = %s, product_serial_number = %s WHERE order_id = %s;
data = (inv_id, ord_amt, prod_serNo, ord_id)


# -------------------------------------------------------------- #
# product_inventory table queries
# -------------------------------------------------------------- #

# Select (note this is where filter functionality is implemented)
SELECT product_serial_number, product_type, product_brand, product_year, product_model, 
product_invoice_price, product_retail_price, product_size from product_inventory
WHERE product_type = %s;

# Insert
INSERT INTO product_inventory (product_serial_number, product_type, product_brand, product_year,
product_model, product_invoice_price, product_retail_price, product_size)
VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
data = (product_serial_number, product_type, product_brand, product_year,
product_model, product_invoice_price, product_retail_price, product_size)


# -------------------------------------------------------------- #
# warehouse_inventory table queries
# Note: This is our M:M implementation and where the delete
# M:M functionality is implemented
# -------------------------------------------------------------- #

# Select
SELECT warehouse_inventory.location_ID, warehouse_inventory.product_serial_number, warehouse_locations.location_city, 
    product_inventory.product_brand, product_inventory.product_model, warehouse_inventory.inventory_ID
FROM `warehouse_inventory` LEFT JOIN warehouse_locations ON warehouse_inventory.location_ID = warehouse_locations.location_ID 
LEFT JOIN product_inventory ON warehouse_inventory.product_serial_number = product_inventory.product_serial_number;

# Insert
INSERT INTO warehouse_inventory (location_ID, product_serial_number) VALUES (%s, %s);
data = (loc_ID, prod_serNo)

# Delete (M:M functionality)
DELETE FROM warehouse_inventory WHERE inventory_ID = %s
data = (id, ) # "(, )" included to satisfy tuple pass requirement

# -------------------------------------------------------------- #
# warehouse_locations table queries
# -------------------------------------------------------------- #

# Select
SELECT location_ID, location_street_address, location_city, location_state, location_zip from warehouse_locations;

# Insert
INSERT INTO warehouse_locations (location_ID, location_street_address, location_city, location_state, location_zip) 
VALUES (%s,%s,%s,%s,%s);
data = (location_ID, location_street_address, location_city, location_state, location_zip)

# -------------------------------------------------------------- #
# employees table queries
# -------------------------------------------------------------- #

# Select
SELECT employees.employee_ID, employees.first_name, employees.last_name, employees.job_title, 
    warehouse_locations.location_city, warehouse_locations.location_ID FROM employees LEFT JOIN warehouse_locations
    ON employees.location_ID = warehouse_locations.location_ID;

# Insert (location can be null)
INSERT INTO employees (first_name, last_name, job_title, location_ID) VALUES (%s, %s, %s, %s)
data = (f_name, l_name, title, loc)

