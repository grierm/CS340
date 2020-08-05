from flask import Flask, render_template
from flask import request, redirect
from db_connector.db_connector import connect_to_database, execute_query
#create the web application
webapp = Flask(__name__)

#provide a route where requests on the web application can be addressed
@webapp.route('/hello')
#provide a view (fancy name for a function) which responds to any requests on this route
def hello():
    return "Hello World!"

@webapp.route('/Invoices')
#the name of this function is just a cosmetic thing
def browse_invoices():
    print("Fetching and rendering people web page")
    db_connection = connect_to_database()
    query = 'SELECT customer_id, invoice_id, employee_id, payment_date_year, payment_date_month, ' \
            'payment_date_dayOfMonth, payment_amount, payment_method, invoice_amount from invoices;'
    result = execute_query(db_connection, query).fetchall()
    print(result)
    return render_template('Invoices.html', rows=result)


@webapp.route('/Invoices', methods=['POST'])
def add_new_invoice():
    db_connection = connect_to_database()
    # if request.method == 'GET':
    #     query = 'SELECT customer_id, invoice_id, employee_id, payment_date_year, payment_date_month, " \
    #         "payment_date_dayOfMonth, payment_amount, payment_method, invoice_amount from invoices;'
    #     result = execute_query(db_connection, query).fetchall()
    #     print(result)
    #
    #     return render_template('Invoices.html', invoices=result)
#if request.method == 'POST':
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
#the name of this function is just a cosmetic thing
def browse_products():
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
    db_connection = connect_to_database()
    # if request.method == 'GET':
    #     query = 'SELECT customer_id, invoice_id, employee_id, payment_date_year, payment_date_month, " \
    #         "payment_date_dayOfMonth, payment_amount, payment_method, invoice_amount from invoices;'
    #     result = execute_query(db_connection, query).fetchall()
    #     print(result)
    #
    #     return render_template('Invoices.html', invoices=result)
#if request.method == 'POST':
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
    return ('Product added!')

@webapp.route('/warehouse_locations')
#the name of this function is just a cosmetic thing
def browse_locations():
    print("Fetching and rendering people web page")
    db_connection = connect_to_database()
    query = 'SELECT location_ID, location_street_address, location_city, location_state, location_zip ' \
            'from warehouse_locations;'
    result = execute_query(db_connection, query).fetchall()
    print(result)
    return render_template('warehouse_locations.html', rows=result)


@webapp.route('/warehouse_locations', methods=['POST'])
def add_new_location():
    db_connection = connect_to_database()
    # if request.method == 'GET':
    #     query = 'SELECT customer_id, invoice_id, employee_id, payment_date_year, payment_date_month, " \
    #         "payment_date_dayOfMonth, payment_amount, payment_method, invoice_amount from invoices;'
    #     result = execute_query(db_connection, query).fetchall()
    #     print(result)
    #
    #     return render_template('Invoices.html', invoices=result)
#if request.method == 'POST':
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
    return ('Location added!')

#
# @webapp.route('/add_new_people', methods=['POST','GET'])
# def add_new_people():
#     db_connection = connect_to_database()
#     if request.method == 'GET':
#         query = 'SELECT id, name from bsg_planets'
#         result = execute_query(db_connection, query).fetchall()
#         print(result)
#
#         return render_template('people_add_new.html', planets = result)
#     elif request.method == 'POST':
#         print("Add new people!")
#         fname = request.form['fname']
#         lname = request.form['lname']
#         age = request.form['age']
#         homeworld = request.form['homeworld']
#
#         query = 'INSERT INTO bsg_people (fname, lname, age, homeworld) VALUES (%s,%s,%s,%s)'
#         data = (fname, lname, age, homeworld)
#         execute_query(db_connection, query, data)
#         return ('Person added!')
#
# @webapp.route('/')
# def index():
#     return "<p>Are you looking for /db_test or /hello or <a href='/browse_bsg_people'>/browse_bsg_people</a> or /add_new_people or /update_people/id or /delete_people/id </p>"
#
# @webapp.route('/home')
# def home():
#     db_connection = connect_to_database()
#     query = "DROP TABLE IF EXISTS diagnostic;"
#     execute_query(db_connection, query)
#     query = "CREATE TABLE diagnostic(id INT PRIMARY KEY, text VARCHAR(255) NOT NULL);"
#     execute_query(db_connection, query)
#     query = "INSERT INTO diagnostic (text) VALUES ('MySQL is working');"
#     execute_query(db_connection, query)
#     query = "SELECT * from diagnostic;"
#     result = execute_query(db_connection, query)
#     for r in result:
#         print(f"{r[0]}, {r[1]}")
#     return render_template('home.html', result = result)
#
# @webapp.route('/db_test')
# def test_database_connection():
#     print("Executing a sample query on the database using the credentials from db_credentials.py")
#     db_connection = connect_to_database()
#     query = "SELECT * from bsg_people;"
#     result = execute_query(db_connection, query)
#     return render_template('db_test.html', rows=result)
#
# #display update form and process any updates, using the same function
# @webapp.route('/update_people/<int:id>', methods=['POST','GET'])
# def update_people(id):
#     print('In the function')
#     db_connection = connect_to_database()
#     #display existing data
#     if request.method == 'GET':
#         print('The GET request')
#         people_query = 'SELECT id, fname, lname, homeworld, age from bsg_people WHERE id = %s'  % (id)
#         people_result = execute_query(db_connection, people_query).fetchone()
#
#         if people_result == None:
#             return "No such person found!"
#
#         planets_query = 'SELECT id, name from bsg_planets'
#         planets_results = execute_query(db_connection, planets_query).fetchall()
#
#         print('Returning')
#         return render_template('people_update.html', planets = planets_results, person = people_result)
#     elif request.method == 'POST':
#         print('The POST request')
#         character_id = request.form['character_id']
#         fname = request.form['fname']
#         lname = request.form['lname']
#         age = request.form['age']
#         homeworld = request.form['homeworld']
#
#         query = "UPDATE bsg_people SET fname = %s, lname = %s, age = %s, homeworld = %s WHERE id = %s"
#         data = (fname, lname, age, homeworld, character_id)
#         result = execute_query(db_connection, query, data)
#         print(str(result.rowcount) + " row(s) updated")
#
#         return redirect('/browse_bsg_people')
#
# @webapp.route('/delete_people/<int:id>')
# def delete_people(id):
#     '''deletes a person with the given id'''
#     db_connection = connect_to_database()
#     query = "DELETE FROM bsg_people WHERE id = %s"
#     data = (id,)
#
#     result = execute_query(db_connection, query, data)
#     return (str(result.rowcount) + "row deleted")
