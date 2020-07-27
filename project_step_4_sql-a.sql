# Name: Ben Nordstrom
# Date: Jul-25-2020
# CS 340 - 400 - Summer 2020
# Project Group 49 - The Castaways
# Project Step 4 - Draft - SQL A

# Create the table for customers
CREATE TABLE `customers` (
	`customer_ID` int(11) NOT NULL AUTO_INCREMENT,
	`first_name` varchar(255) NOT NULL,
	`last_name` varchar(255) NOT NULL,
	`email` varchar(255) NOT NULL,
	`phone_number` varchar(255) NOT NULL, # May want to change this to int (7-25-2020)
	`employee_ID` int(11),
	`gender` varchar(255),
	`address_street` varchar(255),
	`address_city` varchar(255),
	`address_state` varchar(255),
	`address_ZIP` int(11) NOT NULL,
	`credit_card_type` varchar(255),
	`credit_card_number` int(11),
	`cc_expiration_month` int(11),
	`cc_expiration_year` int(11),
	`cc_cvv_code` int(11),
	`billing_address_street` varchar(255),
	`billing_address_city` varchar(255),
	`billing_address_state` varchar(255),
	`billing_address_ZIP` int(11),
	PRIMARY KEY (`customer_ID`),
	CONSTRAINT `customer_fk_1` FOREIGN KEY (`employee_ID`) REFERENCES `employee_ID` (`employees`) # ON DELETE SET NULL ON UPDATE CASCADE
);


# Create table for orders
CREATE TABLE `orders` (
	`invoice_ID` int(11) NOT NULL,
	`order_ID` int(11) NOT NULL AUTO_INCREMENT,
	`order_date_year` int(11) NOT NULL,
	`order_date_month` int(11) NOT NULL,
	`order_date_dayOfMonth` int(11) NOT NULL,
	`order_amount` int(11) NOT NULL,
	`order_quantity` int(11) NOT NULL,
	`product_serial_number` int(11) NOT NULL,
	PRIMARY KEY (`order_ID`),
	CONSTRAINT `orders_fk_1` FOREIGN KEY (`invoice_ID`) REFERENCES `invoice_ID` (`invoices`) # ON DELETE SET NULL ON UPDATE CASCADE
);


# Create table for warehouse inventory
CREATE TABLE `warehouse_inventory` (
	`location_ID` int(11) NOT NULL,
	`product_serial_number` int(11) NOT NULL
	CONSTRAINT `wh_inv_fk_1` FOREIGN KEY (`location_ID`) REFERENCES `location_ID` (`warehouse_locations`), # ON DELETE SET NULL ON UPDATE CASCADE
	CONSTRAINT `wh_inv_fk_2` FOREIGN KEY (`product_serial_number`) REFERENCES `product_serial_number` (`product_inventory`) # ON DELETE SET NULL ON UPDATE CASCADE
);



# Create table for employees
CREATE TABLE `employees` (
	`employee_ID` int(11) NOT NULL AUTO_INCREMENT,
	`first_name` varchar(255) NOT NULL,
	`last_name` varchar(255) NOT NULL,
	`start_date_year` int(11) NOT NULL,
	`start_date_month` int(11) NOT NULL,
	`start_date_dayOfMonth` int(11) NOT NULL,
	`end_date_year` int(11),
	`end_date_month` int(11),
	`end_date_dayOfMonth`int(11),
	`job_title` varchar(255) NOT NULL,
	`location_ID` varchar(255) NOT NULL
	PRIMARY KEY (`employee_ID`),
	CONSTRAINT `employee_fk_1` FOREIGN KEY (`customer_ID`) REFERENCES `customer_ID` (`customers`) # ON DELETE SET NULL ON UPDATE CASCADE
);


# ----------------------------------------
# Insert data - customers (start data)
INSERT INTO customers (first_name, last_name, email, phone_number, address_ZIP) 
	VALUES ('Ben', 'Nordstrom', 'fake-email-123@fakeemail.com', '800-867-5309', '99999');
INSERT INTO customers (first_name, last_name, email, phone_number, address_ZIP, employee_ID, gender, address_street, address_city, address_state) 
	VALUES ('Max', 'Grier', 'fakeR-email-321@fakeremail.com', '867-530-9999', '98765', '1', 'Male', '123 Fake Street', 'Fakeville', 'FK');
INSERT INTO customers (first_name, last_name, email, phone_number, address_ZIP) 
	VALUES ('Lance', 'Armstrong', 'i-got-DQed@DQme.race', '312-321-3121', '12345');

# Insert data - orders
INSERT INTO orders (invoice_ID, order_date_year, order_date_month, order_date_dayOfMonth, order_amount, order_quantity, product_serial_number) 
	VALUES (1, 2020, 1, 30, 10, 5, 12345);
INSERT INTO orders (invoice_ID, order_date_year, order_date_month, order_date_dayOfMonth, order_amount, order_quantity, product_serial_number) 
	VALUES (2, 2019, 12, 31, 9000, 9000, 54321);
INSERT INTO orders (invoice_ID, order_date_year, order_date_month, order_date_dayOfMonth, order_amount, order_quantity, product_serial_number) 
	VALUES (3, 2020, 6, 12, 340, 400, 78901);

# Insert data - warehouse inventory
INSERT INTO warehouse_inventory (location_ID, product_serial_number) 
	VALUES (9, 12345);
INSERT INTO warehouse_inventory (location_ID, product_serial_number) 
	VALUES (10, 54321);
INSERT INTO warehouse_inventory (location_ID, product_serial_number) 
	VALUES (9, 78901);

# Insert data - employees
INSERT INTO employees (first_name, last_name, start_date_month, start_date_year, start_date_dayOfMonth, job_title, location_ID) 
	VALUES ('Max', 'Grier', 6, 2020, 12, 'Co-Founder', 9);
INSERT INTO employees (first_name, last_name, start_date_month, start_date_year, start_date_dayOfMonth, job_title, location_ID, end_date_year, end_date_month, end_date_dayOfMonth) 
	VALUES ('Peter', 'Sagan', 1, 2020, 2, 'Brand Ambassador', 10, 2020, 1, 3);
INSERT INTO employees (first_name, last_name, start_date_month, start_date_year, start_date_dayOfMonth, job_title, location_ID) 
	VALUES ('Ted', 'King', 5, 2019, 13, 'Team Racer', 10);