# Name: Ben Nordstrom, Max Grier
# Date: Jul-25-2020
# CS 340 - 400 - Summer 2020
# Project Group 49 - The Castaways

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
	CONSTRAINT `customer_fk_1` FOREIGN KEY (`employee_ID`) REFERENCES `employee_ID` (`employees`)
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
	`product_serial_number`,
	PRIMARY KEY (`order_ID`),
	CONSTRAINT `orders_fk_1` FOREIGN KEY (`invoice_ID`) REFERENCES `invoice_ID` (`invoices`)
);


# Create table for warehouse inventory
CREATE TABLE `warehouse_inventory` (
	`location_ID` int(11) NOT NULL,
	`product_serial_number` int(11) NOT NULL
	CONSTRAINT `wh_inv_fk_1` FOREIGN KEY (`location_ID`) REFERENCES `location_ID` (`warehouse_locations`),
	CONSTRAINT `wh_inv_fk_2` FOREIGN KEY (`product_serial_number`) REFERENCES `product_serial_number` (`product_inventory`)
);



# Create table for employees
CREATE TABLE `employees` (
	`employee_ID` int(11) NOT NULL AUTO_INCREMENT,
	`first_name` varchar(255) NOT NULL,
	`last_name` varchar(255) NOT NULL,
	`start_date_year` int(11) NOT NULL,
	`start_date_month` int(11) NOT NULL,
	`tart_date_dayOfMonth` int(11) NOT NULL,
	`end_date_year` int(11),
	`end_date_month` int(11),
	`end_date_dayOfMonth`int(11),
	`job_title` varchar(255) NOT NULL,
	`location_ID` varchar(255) NOT NULL
	PRIMARY KEY (`employee_ID`),
	CONSTRAINT `employee_fk_1` FOREIGN KEY (`customer_ID`) REFERENCES `customer_ID` (`customers`)
);


# ----------------------------------------
# Insert data - customers



# Insert data - orders



# Insert data - warehouse inventory




# Insert data - employees
