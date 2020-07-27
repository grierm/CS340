# Name: Ben Nordstrom, Max Grier
# Date: Jul-26-2020
# CS 340 - 400 - Summer 2020
# Project Group 49 - The Castaways

# Create the table for invoices
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
	PRIMARY KEY (`invoice_id`),
	CONSTRAINT `invoices_fk_1` FOREIGN KEY (`customer_ID`) REFERENCES `customer_ID` (`customers`),
    CONSTRAINT `invoices_fk_2` FOREIGN KEY (`employee_ID`) REFERENCES `employee_ID` (`employees`)
);


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
	PRIMARY KEY (`product_serial_number`),
	CONSTRAINT `product_inventory_fk_1` FOREIGN KEY (`product_serial_number`) REFERENCES `product_serial_number` (`warehouse_inventory`)
);


# Create table for warehouse_locations
CREATE TABLE `warehouse_locations` (
	`location_ID` int(11) NOT NULL AUTO_INCREMENT,
    `location_street_address` varchar(255) NOT NULL,
    `location_city` varchar(255) NOT NULL,
    `location_state` varchar(255) NOT NULL,
    `location_ZIP` int(11) NOT NULL,
	CONSTRAINT `wh_locations_fk_1` FOREIGN KEY (`location_ID`) REFERENCES `location_ID` (`warehouse_inventory`),
	CONSTRAINT `wh_locations_fk_2` FOREIGN KEY (`location_ID`) REFERENCES `location_ID` (`employees`)
);


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
WHERE product_type=:id_input;


# Select data - warehouse_locations
SELECT *
FROM warehouse_locations;

# ----------------------------------------
# Update data - invocies



# Update data - product_inventory



# Update data - warehouse_locations
