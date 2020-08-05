from flask import Flask, render_template
from flask import request, redirect
from db_connector.db_connector import connect_to_database, execute_query

#create the web application
webapp = Flask(__name__)

@webapp.route('/Invoices')
def browse_invoices():
    """This function displays the invoices from Invoices.html"""
    print("Fetching and rendering people web page")
    db_connection = connect_to_database()

    query = 'SELECT customer_id, invoice_id, employee_id, payment_date_year, payment_date_month, ' \
            'payment_date_dayOfMonth, payment_amount, payment_method, invoice_amount from invoices;'

    result = execute_query(db_connection, query).fetchall()
    print(result)

    return render_template('Invoices.html', rows=result)


@webapp.route('/Invoices', methods=['POST'])
def add_new_invoice():
    """This adds the form functionality to insert into the invoices table"""
    db_connection = connect_to_database()
    print("Add new invoice!")

    invoice_id = request.form['invoice_id']
    employee_id = request.form['employee_id']
    payment_date_year = request.form['payment_date_year']
    payment_date_month = request.form['payment_date_month']
    payment_date_dayOfMonth = request.form['payment_date_dayOfMonth']
    payment_amount = request.form['payment_amount']
    payment_method = request.form['payment_method']
    invoice_amount = request.form['invoice_amount']

    query = 'INSERT INTO invoices (invoice_id, employee_id, payment_date_year, payment_date_month, ' \
            'payment_date_dayOfMonth, payment_amount, payment_method, invoice_amount) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)'

    data = (invoice_id, employee_id, payment_date_year, payment_date_month,
            payment_date_dayOfMonth, payment_amount, payment_method, invoice_amount)
    execute_query(db_connection, query, data)

    return ('Invoice added!')


@webapp.route('/product_inventory', methods=['GET'])
def browse_products():
    """Display all the products and also has functionality for the drop down list."""
    print("Fetching and rendering people web page")
    db_connection = connect_to_database()
    type_filter = request.args.get('type_filter')

    if type_filter == "All" or type_filter is None:
        query = 'SELECT product_serial_number, product_type, product_brand, product_year, product_model, ' \
                'product_invoice_price, product_retail_price, product_size from product_inventory;'

        result = execute_query(db_connection, query).fetchall()
        print(result)
        return render_template('product_inventory.html', rows=result)
    else:
        query = 'SELECT product_serial_number, product_type, product_brand, product_year, product_model, ' \
                'product_invoice_price, product_retail_price, product_size from product_inventory ' \
                'WHERE product_type = %s;'
        data = (type_filter,)
        result = execute_query(db_connection, query, data).fetchall()

        print(result)
        return render_template('product_inventory.html', rows=result)


@webapp.route('/product_inventory', methods=['POST'])
def add_product():
    """Function for inserting inventory into the product table."""
    db_connection = connect_to_database()
    print("Add new product!")

    product_serial_number = request.form['product_serial_number']
    product_type = request.form['product_type']
    product_brand = request.form['product_brand']
    product_year = request.form['product_year']
    product_model = request.form['product_model']
    product_invoice_price = request.form['product_invoice_price']
    product_retail_price = request.form['product_retail_price']
    product_size = request.form['product_size']

    query = 'INSERT INTO product_inventory (product_serial_number, product_type, product_brand, product_year, ' \
            'product_model, product_invoice_price, product_retail_price, product_size) ' \
            'VALUES (%s,%s,%s,%s,%s,%s,%s,%s)'

    data = (product_serial_number, product_type, product_brand, product_year,
            product_model, product_invoice_price, product_retail_price, product_size)
    execute_query(db_connection, query, data)

    return 'Product added!'

@webapp.route('/warehouse_locations')
def browse_locations():
    """Display the warehouse locations."""
    print("Fetching and rendering people web page")
    db_connection = connect_to_database()
    query = 'SELECT location_ID, location_street_address, location_city, location_state, location_zip ' \
            'from warehouse_locations;'
    result = execute_query(db_connection, query).fetchall()
    print(result)
    return render_template('warehouse_locations.html', rows=result)


@webapp.route('/warehouse_locations', methods=['POST'])
def add_new_location():
    """Functionality to add locations via the form."""
    db_connection = connect_to_database()
    print("Add new location!")

    location_ID = request.form['location_ID']
    location_street_address = request.form['location_street_address']
    location_city = request.form['location_city']
    location_state = request.form['location_state']
    location_zip = request.form['location_zip']

    query = 'INSERT INTO warehouse_locations (location_ID, location_street_address, location_city, location_state, ' \
            'location_zip) VALUES (%s,%s,%s,%s,%s)'

    data = (location_ID, location_street_address, location_city, location_state, location_zip)
    execute_query(db_connection, query, data)

    return 'Location added!'
