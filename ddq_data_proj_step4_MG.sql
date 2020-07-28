# Name: Ben Nordstrom, Max Grier
# Date: Jul-26-2020
# CS 340 - 400 - Summer 2020
# Project Group 49 - The Castaways

-- MySQL dump 10.13  Distrib 5.1.66, for redhat-linux-gnu (x86_64)
--
-- Host: mysql.eecs.oregonstate.edu    Database: cs340_grierm
-- ------------------------------------------------------
-- Server version	5.1.65-community-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `castaway bike shop`
--


# Create the table for invoices
DROP TABLE IF EXISTS `invoices`;
CREATE TABLE `invoices` (
	`customer_ID` int(11) NOT NULL,
	`invoice_ID` int(11) NOT NULL,
	`employee_ID` int(11) NOT NULL,
	`payment_date_year` int(11) NOT NULL,
    `payment_date_month` int(11) NOT NULL,
    `payment_date_dayOfMonth` int(11) NOT NULL,
    `payment_amount` int(11) NOT NULL,
    `payment_method` VARCHAR(255) NOT NULL,
    `invoice_amount` int(11) NOT NULL,
	PRIMARY KEY (`invoice_id`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;


# Create table for product_inventory
DROP TABLE IF EXISTS `product_inventory`;
CREATE TABLE `product_inventory` (
	`product_serial_number` int(11) NOT NULL,
    `product_type` varchar(255) NOT NULL,
    `product_brand` varchar(255) NOT NULL,
    `product_year` int(11) NOT NULL,
    `product_model` varchar(255),
    `product_invoice_price` int(11) NOT NULL,
    `product_retail_price` int(11) NOT NULL,
    `product_size` int(11) NOT NULL,
	PRIMARY KEY (`product_serial_number`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;


# Create table for warehouse_locations
DROP TABLE IF EXISTS `warehouse_locations`;
CREATE TABLE `warehouse_locations` (
	`location_ID` int(11) NOT NULL,
    `location_street_address` varchar(255) NOT NULL,
    `location_city` varchar(255) NOT NULL,
    `location_state` varchar(255) NOT NULL,
    `location_ZIP` int(11) NOT NULL
)ENGINE=InnoDB DEFAULT CHARSET=utf8;


# -------------- Ben's tables --------

# Create the table for customers
DROP TABLE IF EXISTS `customers`;
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
	PRIMARY KEY (`customer_ID`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;


# Create table for orders
DROP TABLE IF EXISTS `orders`;
CREATE TABLE `orders` (
	`invoice_ID` int(11) NOT NULL,
	`order_ID` int(11) NOT NULL AUTO_INCREMENT,
	`order_date_year` int(11) NOT NULL,
	`order_date_month` int(11) NOT NULL,
	`order_date_dayOfMonth` int(11) NOT NULL,
	`order_amount` int(11) NOT NULL,
	`order_quantity` int(11) NOT NULL,
	`product_serial_number` int(11) NOT NULL,
	PRIMARY KEY (`order_ID`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;


# Create table for warehouse inventory
DROP TABLE IF EXISTS `warehouse_inventory`;
CREATE TABLE `warehouse_inventory` (
	`location_ID` int(11) NOT NULL,
	`product_serial_number` int(11) NOT NULL,
    PRIMARY KEY (`location_ID`, `product_serial_number`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Create table for employees
DROP TABLE IF EXISTS `employees`;
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
	`location_ID` varchar(255) NOT NULL,
	PRIMARY KEY (`employee_ID`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;


# ----------------------------------------
# Insert data - customers



# Insert data - orders



# Insert data - warehouse inventory




# Insert data - employees


# -----------------------------------------
ALTER TABLE invoices
    ADD FOREIGN KEY (customer_ID) 
    REFERENCES customers (customer_ID)
    ON DELETE CASCADE
    ON UPDATE CASCADE;

ALTER TABLE invoices
    ADD FOREIGN KEY (employee_ID) 
    REFERENCES employees (employee_ID)
    ON DELETE CASCADE
    ON UPDATE CASCADE;

ALTER TABLE product_inventory
    ADD FOREIGN KEY (product_serial_number)
    REFERENCES warehouse_inventory (product_serial_number)
    ON DELETE CASCADE
    ON UPDATE CASCADE;

ALTER TABLE warehouse_locations
    ADD FOREIGN KEY (location_ID)
    REFERENCES warehouse_inventory (location_ID)
    ON DELETE CASCADE
    ON UPDATE CASCADE;

ALTER TABLE warehouse_locations
    ADD FOREIGN KEY (location_ID)
    REFERENCES employees (location_ID)
    ON DELETE CASCADE
    ON UPDATE CASCADE;

ALTER TABLE customers
    ADD FOREIGN KEY (employee_ID)
    REFERENCES employees (employee_ID)
    ON DELETE CASCADE
    ON UPDATE CASCADE;

ALTER TABLE orders
    ADD FOREIGN KEY (invoice_ID)
    REFERENCES invoices (invoice_ID)
    ON DELETE CASCADE
    ON UPDATE CASCADE;

ALTER TABLE warehouse_inventory
    ADD FOREIGN KEY (location_ID)
    REFERENCES warehouse_locations (location_ID)
    ON DELETE CASCADE
    ON UPDATE CASCADE;

ALTER TABLE warehouse_inventory
    ADD FOREIGN KEY (product_serial_number)
    REFERENCES product_inventory (product_serial_number)
    ON DELETE CASCADE
    ON UPDATE CASCADE;

ALTER TABLE employees
    ADD FOREIGN KEY (customer_ID)
    REFERENCES customers (customer_ID)
    ON DELETE CASCADE
    ON UPDATE CASCADE;

# ----------------------------------------
# Insert data - invoices
INSERT INTO invoices(`customer_ID`, `invoice_ID`, `employee_ID`, `payment_date_year`, `payment_date_month`, 
`payment_date_dayOfMonth`, `payment_amount`, `payment_method`, `invoice_amount`)VALUES
(1, 1, 2020, 2, 15, 500, 'Credit Card', 500),
(2, 1, 2020, 3, 15, 1000, 'Credit Card', 1700),
(2, 1, 2020, 3, 15, 700, 'Credit Card', 1700)

# Insert data - product_inventory
INSERT INTO procuct_inventory(`product_serial_number`, `product_type`, `product_brand`, `product_year`,
`product_model`, `product_invoice_price`, `product_retail_price`, `product_size`)VALUES
(1234, 'Road', 'Schwinn', 2020, NULL, 1000, 1100, 21),
(1010, 'Mountain', 'Santa Cruz', 2020, 'Chameleon', 3500, 3299, 27.5),
(2345, 'Electric', 'RadRunner', 2020, NULL, 1200, 1199, 25)


# Insert data - warehouse_locations
INSERT INTO warehouse_locations(`location_ID`, `location_street_address`,
`location_city`, `location_state`,`location_ZIP`) VALUES
(1, '123 N Mississippi Ave', 'Portland', 'OR', 97205),
(2, '4567 Howard St', 'San Francisco', 'CA', 94103),
(3, '1221 24th Ave E', 'Seattle', 'WA', 98112)

# ----------------------------------------
# Select data - invocies
SELECT * 
FROM invoices;


# Select data - product_inventory
SELECT * 
FROM product_inventory
WHERE product_type=id_input;


# Select data - warehouse_locations
SELECT *
FROM warehouse_locations;

# ----------------------------------------
# Update data - invocies
UPDATE invocies
SET customer_ID = customer_ID_input, invoice_ID = invoice_ID_input, employee_ID = employee_ID_input, 
payment_date_year = payment_date_year_input, payment_date_month = payment_date_month_input, 
payment_date_dayOfMonth = payment_date_dayOfMonth_input, payment_amount = payment_amount_input, 
payment_method = payment_method_input, invoice_amount = invoice_amount_input;


# Update data - product_inventory
UPDATE product_inventory
SET product_serial_number = product_serial_number_input, product_type = product_type_input, 
product_brand = product_brand_input, product_year = product_year_input, 
product_model = product_model_input, product_invoice_price = product_invoice_price_input, 
product_retail_price = product_retail_price_input, product_size = product_size_input;


# Update data - warehouse_locations
UPDATE warehouse_locations
SET location_ID = location_ID_input, location_street_address = location_street_address_input,
location_city = location_city_input, location_state = location_state_input,
location_ZIP = location_ZIP_input;