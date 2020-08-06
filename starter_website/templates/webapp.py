from flask import Flask, render_template
from flask import request, redirect, url_for
from flask_mysqldb import MySQL
from db_credentials import host, user, passwd, db
from db_connector import connect_to_database, execute_query

app = Flask(__name__)

app.config['MYSQL_HOST'] = host
app.config['MYSQL_USER'] = user
app.config['MYSQL_PASSWORD'] = passwd
app.config['MYSQL_DB'] = db
mysql = MySQL(app)

@app.route('/index')
def index():
    return render_template("index.html")

@app.route('/')
def home():
    return render_template("index.html")

def runpersist(environ, start_response):
    data = b'Hello World\n'
    status = '200 OK'
    response_headers = [
        ('Content-type', 'text/plain'),
        ('Content-length', str(len(data)))
    ]
    start_response(status, response_headers)
    return iter([data])

'''
----------------------------------------------------------------------
This section covers the Customers routing/query handling
----------------------------------------------------------------------
'''

@app.route('/customers')
def customers():
    print("Customers page rendering")
    # set the db connection cursor
    cur = mysql.connection.cursor()
    query = "SELECT customer_id, first_name, last_name, email, phone_number FROM customers;"
    cur.execute(query)
    result=cur.fetchall()
    print(result)
    print("query pull success")
    return render_template('customers.html', customers = result)

@app.route('/add_customer', methods=["GET", "POST"])
def add_customer():
    print("Adding a customer")
    f_name = request.form["first_name"]
    l_name = request.form["last_name"]
    email = request.form["email"]
    phone = request.form["phone_number"]
    print("First name ", f_name)

    query = "INSERT INTO customers (first_name, last_name, email, phone_number) VALUES (%s, %s, %s, %s)"
    data = (f_name, l_name, email, phone)
    db_connection = connect_to_database()
    execute_query(db_connection, query, data)

    return redirect(url_for('customers'))

@app.route('/update_customer/<int:id>', methods=["GET", "POST"])
def update_customer(id):
    db_connection = connect_to_database()
    print("Update customer start")
    if request.method == "GET":
        print("Getting customer record")
        cust_q = "SELECT customer_ID, first_name, last_name, email, phone_number FROM customers WHERE customer_ID = %s" % (id)
        cust_result = execute_query(db_connection, cust_q).fetchone()

        if cust_result == None:
            return "Could not find customer"

        return render_template('customer_update.html', customer = cust_result)

    elif request.method == "POST":

        print("Updating customer")

        # Get data from the user edit on page
        cust_id = id
        fname = request.form['first_name']
        lname = request.form['last_name']
        email = request.form['email']
        phone = request.form['phone_number']

        print(request.form)

        query = "UPDATE customers SET first_name = %s, last_name = %s, email = %s, phone_number = %s WHERE customer_id = %s"
        data = (fname, lname, email, phone, cust_id)
        result = execute_query(db_connection, query, data)

        print("Customer updated")
        return redirect(url_for('customers'))
        #return "Customer updated"



'''
----------------------------------------------------------------------
This section covers the Employees routing/query handling
----------------------------------------------------------------------
'''
@app.route('/employees')
def employees():
    print("Employees page rendering")
    cur = mysql.connection.cursor()
    query = "SELECT employee_ID, first_name, last_name, job_title, location_ID FROM employees;"
    cur.execute(query)
    result = cur.fetchall()
    print(result)
    print("employee query pull success")
    return render_template('employees.html', employees = result)


@app.route('/add_emp', methods=["GET", "POST"])
def add_emp():
    print("Adding an employee")
    f_name = request.form["first_name"]
    l_name = request.form["last_name"]
    title = request.form["job_title"]
    print("First name is: ", f_name)

    query = "INSERT INTO employees (first_name, last_name, job_title) VALUES (%s, %s, %s)"
    data = (f_name, l_name, title)
    db_connection = connect_to_database()
    execute_query(db_connection, query, data)

    return redirect(url_for('employees'))


'''
----------------------------------------------------------------------
This section covers the ORDERS routing/query handling
----------------------------------------------------------------------
'''
@app.route('/orders')
def orders():
    print("Orders page rendering")
    cur = mysql.connection.cursor()
    query = "SELECT order_ID, invoice_ID, order_amount, product_serial_number FROM orders;"
    cur.execute(query)
    result = cur.fetchall()
    print(result)
    print("order query pull success")

    print("pulling invoices for add dropdown functionality")
    query_inv = "SELECT invoice_ID FROM invoices;"
    cur.execute(query_inv)
    result_inv = cur.fetchall()
    print(result_inv)

    print("pulling products for add dropdown")
    query_prod = "SELECT product_serial_number FROM product_inventory"
    cur.execute(query_prod)
    result_prod = cur.fetchall()
    print(result_prod)

    return render_template('orders.html', orders = result, invoices = result_inv, products = result_prod)


@app.route('/add_order', methods=["GET", "POST"])
def add_order():
    print("Adding an order")
    inv_ID = request.form["invoice_ID"]
    ord_amt = request.form["order_amount"]
    prod_serNo = request.form["product_serial_number"]
    print("Invoice ID is: ", inv_ID)

    query = "INSERT INTO orders (invoice_ID, order_amount, product_serial_number) VALUES (%s, %s, %s)"
    data = (inv_ID, ord_amt, prod_serNo)
    db_connection = connect_to_database()
    execute_query(db_connection, query, data)

    return redirect(url_for('orders'))


'''
----------------------------------------------------------------------
This section covers the WAREHOUSE INVENTORY routing/query handling
----------------------------------------------------------------------
'''
@app.route('/wh_inv')
def wh_inv():
    print("Warehouse Inventory page rendering")
    cur = mysql.connection.cursor()
    # OLD QUERY: query = "SELECT location_ID, product_serial_number FROM warehouse_inventory;"
    # NEW QUERY WITH JOIN
    query = """SELECT warehouse_inventory.location_ID, warehouse_inventory.product_serial_number, warehouse_locations.location_city, 
    product_inventory.product_brand, product_inventory.product_model, warehouse_inventory.inventory_ID
    FROM `warehouse_inventory` LEFT JOIN warehouse_locations ON warehouse_inventory.location_ID = warehouse_locations.location_ID 
    LEFT JOIN product_inventory ON warehouse_inventory.product_serial_number = product_inventory.product_serial_number;"""
    cur.execute(query)
    result = cur.fetchall()
    print(result)
    print("warehouse Inventory query pull success")

    #query for locations dropdown menu
    query_locs = "SELECT location_ID, location_city FROM warehouse_locations"
    db_connection = connect_to_database()
    result_locs = execute_query(db_connection, query_locs).fetchall()
    print("Location results")
    print(result_locs)


    #query for serial number dropdown menu
    query_serNos = "SELECT product_serial_number, product_brand, product_model FROM product_inventory"
    db_connection = connect_to_database()
    result_serNos = execute_query(db_connection, query_serNos).fetchall()
    print("Product results")
    print(result_serNos)

    return render_template('warehouse_inventory.html', wh_inv = result, locs = result_locs, prods = result_serNos)

@app.route('/add_whInv', methods = ["POST"])
def add_inv():
    print("Adding inventory to a location")
    loc_ID = request.form["location_ID"]
    prod_serNo = request.form["product_serial_number"]
    print("TEST: location is ", loc_ID)

    query = "INSERT INTO warehouse_inventory (location_ID, product_serial_number) VALUES (%s, %s)"
    data = (loc_ID, prod_serNo)
    db_connection = connect_to_database()
    execute_query(db_connection, query, data)

    return redirect(url_for('wh_inv'))

@app.route('/delete_whInv/<int:id>', methods = ["POST"])
def del_inv():
    print("Deleting inventory from location")

    return "Delete success"

'''
----------------------------------------------------------------------
This section covers the INVOICES routing/query handling
----------------------------------------------------------------------
'''

@app.route('/Invoices')
def browse_invoices():
    """This function displays the invoices from Invoices.html"""
    print("Fetching and rendering people web page")
    db_connection = connect_to_database()

    query = 'SELECT customer_id, invoice_id, employee_id, payment_date_year, payment_date_month, ' \
            'payment_date_dayOfMonth, payment_amount, payment_method, invoice_amount from invoices;'

    result = execute_query(db_connection, query).fetchall()
    print(result)

    return render_template('Invoices.html', rows=result)


@app.route('/Invoices', methods=['POST'])
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


'''
----------------------------------------------------------------------
This section covers the PRODUCT INVENTORY routing/query handling
----------------------------------------------------------------------
'''
@app.route('/product_inventory', methods=['GET'])
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


@app.route('/product_inventory', methods=['POST'])
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


'''
----------------------------------------------------------------------
This section covers the WAREHOUSE LOCATIONS routing/query handling
----------------------------------------------------------------------
'''

@app.route('/warehouse_locations')
def browse_locations():
    """Display the warehouse locations."""
    print("Fetching and rendering people web page")
    db_connection = connect_to_database()
    query = 'SELECT location_ID, location_street_address, location_city, location_state, location_zip ' \
            'from warehouse_locations;'
    result = execute_query(db_connection, query).fetchall()
    print(result)
    return render_template('warehouse_locations.html', rows=result)


@app.route('/warehouse_locations', methods=['POST'])
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


'''
----------------------------------------------------------------------
This section covers the errors routing/query handling
----------------------------------------------------------------------
'''
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html')

@app.errorhandler(500)
def page_not_found(error):
    return render_template('500.html')
