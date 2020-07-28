# Name: Ben Nordstrom, Max Grier
# Date: Jul-26-2020
# CS 340 - 400 - Summer 2020
# Project Group 49 - The Castaways

-- MySQL dump 10.13  Distrib 5.1.66, for redhat-linux-gnu (x86_64)
--
-- Host: mysql.eecs.oregonstate.edu    Database: cs340_grierm
-- ------------------------------------------------------
-- Server version   5.1.65-community-log

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
SET FOREIGN_KEY_CHECKS=0;
DROP TABLE IF EXISTS invoices;
DROP TABLE IF EXISTS product_inventory;
DROP TABLE IF EXISTS warehouse_locations;
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS warehouse_inventory;
DROP TABLE IF EXISTS employees;
SET FOREIGN_KEY_CHECKS=1;

# Create the table for invoices
CREATE TABLE `invoices` (
    `customer_ID` int(11),
    `invoice_ID` int(11) NOT NULL,
    `employee_ID` int(11),
    `payment_date_year` int(11) NOT NULL,
    `payment_date_month` int(11) NOT NULL,
    `payment_date_dayOfMonth` int(11) NOT NULL,
    `payment_amount` int(11) NOT NULL,
    `payment_method` VARCHAR(255) NOT NULL,
    `invoice_amount` int(11) NOT NULL,
    PRIMARY KEY (`invoice_id`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;


# Create table for product_inventory
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
CREATE TABLE `warehouse_locations` (
    `location_ID` int(11) NOT NULL AUTO_INCREMENT,
    `location_street_address` varchar(255) NOT NULL,
    `location_city` varchar(255) NOT NULL,
    `location_state` varchar(255) NOT NULL,
    `location_ZIP` int(11) NOT NULL,
    PRIMARY KEY (`location_ID`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;


# -------------- Ben's tables --------

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
    PRIMARY KEY (`customer_ID`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;


# Create table for orders
CREATE TABLE `orders` (
    `invoice_ID` int(11),
    `order_ID` int(11) NOT NULL AUTO_INCREMENT,
    `order_date_year` int(11) NOT NULL,
    `order_date_month` int(11) NOT NULL,
    `order_date_dayOfMonth` int(11) NOT NULL,
    `order_amount` int(11) NOT NULL,
    `order_quantity` int(11) NOT NULL,
    `product_serial_number` int(11),
    PRIMARY KEY (`order_ID`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;


# Create table for warehouse inventory
CREATE TABLE `warehouse_inventory` (
    `location_ID` int(11),
    `product_serial_number` int(11)
   #PRIMARY KEY (`location_ID`, `product_serial_number`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;



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
    `location_ID` int(11),
    PRIMARY KEY (`employee_ID`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;




# -----------------------------------------
ALTER TABLE customers
    ADD FOREIGN KEY (employee_ID)
    REFERENCES employees (employee_ID)
    ON DELETE SET NULL
    ON UPDATE CASCADE;

ALTER TABLE employees
    ADD CONSTRAINT FOREIGN KEY (location_ID)
    REFERENCES warehouse_locations (location_ID)
    ON DELETE SET NULL
    ON UPDATE CASCADE;

ALTER TABLE invoices
    ADD CONSTRAINT FOREIGN KEY (customer_ID) 
    REFERENCES customers (customer_ID)
    ON DELETE SET NULL
    ON UPDATE CASCADE;

ALTER TABLE invoices
    ADD CONSTRAINT FOREIGN KEY (employee_ID) 
    REFERENCES employees (employee_ID)
    ON DELETE SET NULL
    ON UPDATE CASCADE;

ALTER TABLE orders
    ADD CONSTRAINT FOREIGN KEY (invoice_ID)
    REFERENCES invoices (invoice_ID)
    ON DELETE SET NULL
    ON UPDATE CASCADE;

ALTER TABLE orders
    ADD CONSTRAINT FOREIGN KEY (product_serial_number)
    REFERENCES product_inventory (product_serial_number)
    ON DELETE SET NULL
    ON UPDATE CASCADE;

ALTER TABLE warehouse_inventory
    ADD CONSTRAINT FOREIGN KEY (location_ID)
    REFERENCES warehouse_locations (location_ID)
    ON DELETE SET NULL
    ON UPDATE CASCADE;

ALTER TABLE warehouse_inventory
    ADD CONSTRAINT FOREIGN KEY (product_serial_number)
    REFERENCES product_inventory (product_serial_number)
    ON DELETE CASCADE
    ON UPDATE CASCADE;


# ----------------------------------------
# Insert data
# step 1 - locations - green
INSERT INTO warehouse_locations(`location_ID`, `location_street_address`,
`location_city`, `location_state`,`location_ZIP`) VALUES
(1, '123 N Mississippi Ave', 'Portland', 'OR', 97205),
(2, '4567 Howard St', 'San Francisco', 'CA', 94103),
(3, '1221 24th Ave E', 'Seattle', 'WA', 98112);

# step 2 - inventory - green
INSERT INTO product_inventory(`product_serial_number`, `product_type`, `product_brand`, `product_year`,
`product_model`, `product_invoice_price`, `product_retail_price`, `product_size`) VALUES
(1234, 'Road', 'Schwinn', 2020, 'Cruiser', 1000, 1100, 21),
(1010, 'Mountain', 'Santa Cruz', 2020, 'Chameleon', 3500, 3299, 27.5),
(2345, 'Electric', 'RadRunner', 2020, 'Voltage', 1200, 1199, 25);

# 3 - w/h inventory - green
INSERT INTO warehouse_inventory (location_ID, product_serial_number) 
    VALUES 
    (1, 1010),  
    (2, 1234),
    (1, 2345);

# 4 - employees - green
INSERT INTO employees (first_name, last_name, start_date_month, start_date_year, start_date_dayOfMonth, job_title, location_ID) 
    VALUES ('Max', 'Grier', 6, 2020, 12, 'Co-Founder', 1);
INSERT INTO employees (first_name, last_name, start_date_month, start_date_year, start_date_dayOfMonth, job_title, location_ID, end_date_year, end_date_month, end_date_dayOfMonth) 
    VALUES ('Peter', 'Sagan', 1, 2020, 2, 'Brand Ambassador', 3, 2020, 1, 3);
INSERT INTO employees (first_name, last_name, start_date_month, start_date_year, start_date_dayOfMonth, job_title, location_ID) 
    VALUES ('Ted', 'King', 5, 2019, 13, 'Team Racer', 2);

# 5 - customers - green
INSERT INTO customers (first_name, last_name, email, phone_number, address_ZIP) 
    VALUES ('Ben', 'Nordstrom', 'fake-email-123@fakeemail.com', '800-867-5309', '99999');
INSERT INTO customers (first_name, last_name, email, phone_number, address_ZIP, employee_ID, gender, address_street, address_city, address_state) 
    VALUES ('Max', 'Grier', 'fakeR-email-321@fakeremail.com', '867-530-9999', '98765', 4, 'Male', '123 Fake Street', 'Fakeville', 'FK');
INSERT INTO customers (first_name, last_name, email, phone_number, address_ZIP) 
    VALUES ('Lance', 'Armstrong', 'i-got-DQed@DQme.race', '312-321-3121', '12345');

# 6 - invoices - green
INSERT INTO invoices(`customer_ID`, `invoice_ID`, `employee_ID`, `payment_date_year`, `payment_date_month`, 
`payment_date_dayOfMonth`, `payment_amount`, `payment_method`, `invoice_amount`) VALUES
(1, 1, 4, 2020, 4, 15, 500, 'Credit Card', 500),
(2, 2, 5, 2020, 5, 15, 1000, 'Credit Card', 1700),
(2, 3, 5, 2020, 5, 15, 700, 'Credit Card', 1700);

# 7 - orders - green
INSERT INTO orders (invoice_ID, order_date_year, order_date_month, order_date_dayOfMonth, order_amount, order_quantity, product_serial_number) 
    VALUES 
    (1, 2020, 1, 30, 10, 5, 1010),
    (2, 2019, 12, 31, 9000, 9000, 1234),
    (3, 2020, 6, 12, 340, 400, 2345);

