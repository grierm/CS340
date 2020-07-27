# Name: Ben Nordstrom
# Date: Jul-25-2020
# CS 340 - 400 - Summer 2020
# Project Group 49 - The Castaways
# Project Step 4 - Draft - SQL B

# HTML interface for insert, select, delete, update

# Selects
# update to display select columns (Limit dispaly and edit funcitonality?)
SELECT * FROM customers;

SELECT * FROM orders;

SELECT * FROM warehouse_inventory;

SELECT * FROM employees;


# Inserts
#Customers
#need to think about if any of this information is null/not entered what gets input
INSERT INTO customers (first_name, last_name, email, phone_number, address_ZIP, employee_ID, gender, address_street, address_city, address_state)
VALUES (:fname, :lname, :email, :phone, :add_ZIP, :emp_ID, :gender, :add_street, :add_city, :add_state);

#orders
INSERT INTO orders (invoice_ID, order_date_year, order_date_month, order_date_dayOfMonth, order_amount, order_quantity, product_serial_number)
VALUES ();

#w/h inv
INSERT INTO warehouse_inventory (location_ID, product_serial_number) 
	VALUES (:loc_ID, :prod_serNo);

#employees
INSERT INTO employees (first_name, last_name, start_date_month, start_date_year, start_date_dayOfMonth, job_title, location_ID, end_date_year, end_date_month, end_date_dayOfMonth)
VALUES (:fname, :lname, :sDate_mo, :sDate_yr, :sDate_DOM, :title, :loc_ID, :end_year, :end_mo, :end_DOM);

# Deletes
#Customers
DELETE FROM customers WHERE customer_ID = (:cust_ID);

#orders
DELETE FROM customers WHERE order_ID = (:ord_ID);

#w/h inv
DELETE FROM warehouse_inventory WHERE location_ID = (:loc_ID);

#employees
DELETE FROM employees WHERE employee_ID = (:emp_ID);

#Updates
#Customers
UPDATE customers SET first_name = (:fname), last_name = (:lname), email = (:email), phone_number = (:phone), gender = (:gender), employee_ID = (:emp_ID), 
address_street = (:add_st), address_city = (:add_city), address_state = (:add_state), address_ZIP = (:add_ZIP), credit_card_type = (:cc_type), credit_card_number = (:cc_num),
cc_expiration_month = (:cc_exp_mo), cc_expiration_year = (:cc_exp_yr), cc_cvv_code = (:cc_cvv), billing_address_street = (:bill_street),
billing_address_city = (:bill_city), billing_address_state = (:bill_state), billing_address_ZIP = (:bill_ZIP) WHERE customer_ID = (:cust_id);

#orders
UPDATE orders SET order_date_year = (:ord_yr), order_date_month = (:ord_mo), order_date_dayOfMonth = (:ord_DOM), order_amount = (:ord_amt), order_quantity = (:ord_qty) WHERE order_ID = (:ord_id);

#w/h inv
UPDATE warehouse_inventory SET location_ID = (:loc_ID), product_serial_number = (:prod_serNo) WHERE location_ID = (:loc_id);

#employees
UPDATE employees SET first_name = (:fname), last_name = (:lname), start_date_year = (:sDate_yr), start_date_month = (:sDate_mo), start_date_dayOfMonth = (:sDate_DOM),
end_date_year = (:eDate_yr), end_date_month = (:eDate_mo), end_date_dayOfMonth = (:eDate_DOM), job_title = (:title), location_ID = (:loc_ID) WHERE employee_ID = (:emp_id);
