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
    query = "SELECT customer_id, first_name, last_name, email, phone_number, employee_ID FROM customers;"
    cur.execute(query)
    result=cur.fetchall()
    print(result)
    print("query pull success")

    # data for employee records to tie to new customer
    query_emp = "SELECT employee_ID, first_name, last_name FROM employees;"
    cur1 = mysql.connection.cursor()
    cur1.execute(query_emp)
    result_emp=cur1.fetchall()
    return render_template('customers.html', customers = result, emp_list = result_emp)

@app.route('/add_customer', methods=["GET", "POST"])
def add_customer():
    print("Adding a customer")
    f_name = request.form["first_name"]
    l_name = request.form["last_name"]
    email = request.form["email"]
    phone = request.form["phone_number"]
    emp_ID = request.form["employee_id"]
    print("First name ", f_name)

    db_connection = connect_to_database()

    #check if an employee_ID was entered
    if emp_ID == "NULL":
        query = "INSERT INTO customers (first_name, last_name, email, phone_number) VALUES (%s, %s, %s, %s)"
        data = (f_name, l_name, email, phone)
        result = execute_query(db_connection, query, data)
        print("Insert result, null emp - ", result)
    else:
        query = "INSERT INTO customers (first_name, last_name, email, phone_number, employee_ID) VALUES (%s, %s, %s, %s, %s)"
        data = (f_name, l_name, email, phone, emp_ID)
        result = execute_query(db_connection, query, data)
        print("Insert result, NOT null emp - ", result)

    print("Customer added")
    return redirect(url_for('customers'))

@app.route('/update_customer/<int:id>', methods=["GET", "POST"])
def update_customer(id):
    db_connection = connect_to_database()
    print("Update customer start")
    if request.method == "GET":
        print("Getting customer record")
        cust_q = "SELECT customer_ID, first_name, last_name, email, phone_number, employee_ID FROM customers WHERE customer_ID = %s" % (id)
        cust_result = execute_query(db_connection, cust_q).fetchone()

        if cust_result == None:
            return "Could not find customer"

        emp_q = "SELECT employee_ID, first_name, last_name FROM employees"
        emp_result = execute_query(db_connection, emp_q).fetchall()
        print("Employee results for update customer")
        print(emp_result)

        return render_template('customer_update.html', customer = cust_result, emp_list = emp_result)

    elif request.method == "POST":

        print("Updating customer")

        # Get data from the user edit on page
        cust_id = id
        fname = request.form['first_name']
        lname = request.form['last_name']
        email = request.form['email']
        phone = request.form['phone_number']
        emp_ID = request.form['employee_id']

        print("Printing form fields")
        print(request.form)

        if emp_ID == "NULL":
            print("User trying to set NULL employee")
            query = """UPDATE customers SET employee_ID = NULL, first_name = %s, last_name = %s, email = %s, phone_number = %s
            WHERE customer_id = %s"""
            data = (fname, lname, email, phone, cust_id)
            result = execute_query(db_connection, query, data)
        else:
            print("User not setting NULL employee")
            query = "UPDATE customers SET first_name = %s, last_name = %s, email = %s, phone_number = %s, employee_ID = %s WHERE customer_id = %s"
            data = (fname, lname, email, phone, emp_ID, cust_id)
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
    query = """SELECT employees.employee_ID, employees.first_name, employees.last_name, employees.job_title, 
    warehouse_locations.location_city, warehouse_locations.location_ID FROM employees LEFT JOIN warehouse_locations
    ON employees.location_ID = warehouse_locations.location_ID;"""
    cur.execute(query)
    result = cur.fetchall()
    print(result)
    print("employee query pull success")

    query_loc = "SELECT location_ID, location_city FROM warehouse_locations;"
    db_connection = connect_to_database()
    result_loc = execute_query(db_connection, query_loc)
    print("Location Results for form fill")
    print(result_loc)

    return render_template('employees.html', employees = result, locations = result_loc)


@app.route('/add_emp', methods=["GET", "POST"])
def add_emp():
    print("Adding an employee")
    f_name = request.form["first_name"]
    l_name = request.form["last_name"]
    title = request.form["job_title"]
    loc = request.form["location"]
    print("First name is: ", f_name)

    if loc == "NULL":
        print("Employee does not have a location")
        query = "INSERT INTO employees (first_name, last_name, job_title) VALUES (%s, %s, %s)"
        data = (f_name, l_name, title)
    else:
        query = "INSERT INTO employees (first_name, last_name, job_title, location_ID) VALUES (%s, %s, %s, %s)"
        data = (f_name, l_name, title, loc)
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
    query_prod = "SELECT product_serial_number, product_brand, product_model FROM product_inventory"
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
    db_connection = connect_to_database()

    if inv_ID == "NULL":
        print("User trying to set null invoice")
        query = """INSERT INTO orders (invoice_ID, order_amount, product_serial_number) VALUES (NULL, %s, %s)"""
        data = (ord_amt, prod_serNo)
        result = execute_query(db_connection, query, data)
    else:
        print("User not trying to set null")
        query = """INSERT INTO orders (invoice_ID, order_amount, product_serial_number) VALUES (%s, %s, %s)"""
        data = (inv_ID, ord_amt, prod_serNo)
        result = execute_query(db_connection, query, data)

    print("New order added!")
    return redirect(url_for('orders'))


@app.route('/update_order/<int:id>', methods=["GET","POST"])
def update_order(id):
    db_connection = connect_to_database()
    print("Update order start")
    if request.method == "GET":
        print("Getting order record")
        ord_q = "SELECT order_ID, invoice_ID, order_amount, product_serial_number FROM orders WHERE order_ID = %s" % (id)
        ord_result = execute_query(db_connection, ord_q).fetchone()

        inv_list_q = "SELECT invoice_ID FROM invoices"
        inv_list_r = execute_query(db_connection, inv_list_q).fetchall()

        prod_serNo_q = "SELECT product_serial_number, product_brand, product_model FROM product_inventory"
        prod_serNo_r = execute_query(db_connection, prod_serNo_q).fetchall()

        print("Invoice results: ")
        print(inv_list_r)

        print("Product results: ")
        print(prod_serNo_r)

        if ord_result == None:
            return "Could not find order"

        return render_template('update_order.html', order = ord_result, inv_list = inv_list_r, prods = prod_serNo_r)

    elif request.method == "POST":

        print("Updating order")

        # Get data from the user edit on page
        ord_id = id
        inv_id = request.form['invoice_id']
        ord_amt = request.form['order_amt']
        prod_serNo = request.form['prod_serNo']

        print("Request form: ")
        print(request.form)

        if inv_id == "NULL":
            print("User trying to set null")
            query = """UPDATE orders SET invoice_ID = NULL, order_amount = %s, product_serial_number = %s
            WHERE order_id = %s"""
            data = (ord_amt, prod_serNo, ord_id)
            result = execute_query(db_connection, query, data)
        else:
            print("User not trying to set null")
            query = """UPDATE orders SET invoice_ID = %s, order_amount = %s, product_serial_number = %s 
            WHERE order_id = %s"""
            data = (inv_id, ord_amt, prod_serNo, ord_id)
            result = execute_query(db_connection, query, data)

        print("Order updated")
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
    product_inventory.product_brand, product_inventory.product_model, warehouse_inventory.inventory_ID, warehouse_inventory.stock_quantity
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
    prod_qty = request.form["stock_quantity"]
    print("TEST: location is ", loc_ID)

    query = "INSERT INTO warehouse_inventory (location_ID, product_serial_number, stock_quantity) VALUES (%s, %s, %s)"
    data = (loc_ID, prod_serNo, prod_qty)
    db_connection = connect_to_database()
    execute_query(db_connection, query, data)

    return redirect(url_for('wh_inv'))

@app.route('/delete_whInv/<int:id>', methods = ["GET", "POST"])
def delete_whInv(id):
    print("Deleting inventory from location")
    query = "DELETE FROM warehouse_inventory WHERE inventory_ID = %s"
    data = (id, )
    db_connection = connect_to_database()
    execute_query(db_connection, query, data)


    return redirect(url_for('wh_inv'))

'''
----------------------------------------------------------------------
This section covers the INVOICES routing/query handling
----------------------------------------------------------------------
'''

@app.route('/Invoices')
def browse_invoices():
    """This function displays the invoices from Invoices.html"""
    print("Fetching and rendering invoices web page")
    db_connection = connect_to_database()

    query = """SELECT customer_id, invoice_id, employee_id, payment_date_year, payment_date_month,
            payment_date_dayOfMonth, payment_amount, payment_method, invoice_amount from invoices;"""

    result = execute_query(db_connection, query).fetchall()
    print(result)

    query_emp = "SELECT employee_ID, first_name, last_name FROM employees;"
    result_emp = execute_query(db_connection, query_emp).fetchall()

    print("Employee names:")
    print(result_emp)

    return render_template('Invoices.html', rows=result, employees=result_emp)


@app.route('/Invoices', methods=['POST'])
def add_new_invoice():
    """This adds the form functionality to insert into the invoices table"""
    db_connection = connect_to_database()
    print("Add new invoice!")


    employee_id = request.form['employee_id']
    payment_date_year = request.form['payment_date_year']
    payment_date_month = request.form['payment_date_month']
    payment_date_dayOfMonth = request.form['payment_date_dayOfMonth']
    payment_amount = request.form['payment_amount']
    payment_method = request.form['payment_method']
    invoice_amount = request.form['invoice_amount']

    query = """INSERT INTO invoices (employee_id, payment_date_year, payment_date_month,
            payment_date_dayOfMonth, payment_amount, payment_method, invoice_amount) 
            VALUES (%s,%s,%s,%s,%s,%s,%s)"""

    data = (employee_id, payment_date_year, payment_date_month,
            payment_date_dayOfMonth, payment_amount, payment_method, invoice_amount)
    execute_query(db_connection, query, data)

    print("Invoice added")
    return redirect(url_for('browse_invoices')) # redirect goes to the defined function, not the app.route name


'''
----------------------------------------------------------------------
This section covers the PRODUCT INVENTORY routing/query handling
----------------------------------------------------------------------
'''
@app.route('/product_inventory', methods=['GET'])
def browse_products():
    """Display all the products and also has functionality for the drop down list."""
    print("Fetching and rendering product inventory web page")
    db_connection = connect_to_database()
    type_filter = request.args.get('type_filter')

    # dropdown menu items pull for filter on page
    type_q = "SELECT product_type FROM product_inventory;"
    result_types = execute_query(db_connection, type_q).fetchall()
    print("Bike types for dropdown: ", result_types)

    if type_filter == "All" or type_filter is None:
        query = """SELECT product_serial_number, product_type, product_brand, product_year, product_model,
                product_invoice_price, product_retail_price, product_size 
                FROM product_inventory;"""

        result = execute_query(db_connection, query).fetchall()
        print(result)
        if type_filter is None:
            type_filter = "All"
        print("Type filter is: ", type_filter)
        return render_template('product_inventory.html', rows=result, types=result_types, filter=type_filter)
    else:
        query = """SELECT product_serial_number, product_type, product_brand, product_year, product_model,
                product_invoice_price, product_retail_price, product_size 
                FROM product_inventory
                WHERE product_type = %s;"""
        data = (type_filter,)
        result = execute_query(db_connection, query, data).fetchall()

        print(result)
        print("Type filter is: ", type_filter)
        return render_template('product_inventory.html', rows=result, types=result_types, filter=type_filter)


@app.route('/product_inventory', methods=['POST'])
def add_product():
    """Function for inserting inventory into the product table."""
    db_connection = connect_to_database()
    print("Add new product!")

    #product_serial_number = request.form['product_serial_number']
    product_type = request.form['product_type']
    product_brand = request.form['product_brand']
    product_year = request.form['product_year']
    product_model = request.form['product_model']
    product_invoice_price = request.form['product_invoice_price']
    product_retail_price = request.form['product_retail_price']
    product_size = request.form['product_size']

    query = """INSERT INTO product_inventory (product_type, product_brand, product_year,
            product_model, product_invoice_price, product_retail_price, product_size)
            VALUES (%s,%s,%s,%s,%s,%s,%s)"""

    data = (product_type, product_brand, product_year,
            product_model, product_invoice_price, product_retail_price, product_size)
    execute_query(db_connection, query, data)

    print("Product added!")
    return redirect(url_for('browse_products'))
    # redirect goes to the defined function, not the app.route name


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
    query = """SELECT location_ID, location_street_address, location_city, location_state, location_zip
            from warehouse_locations;"""
    result = execute_query(db_connection, query).fetchall()
    print(result)
    return render_template('warehouse_locations.html', rows=result)


@app.route('/warehouse_locations', methods=['POST'])
def add_new_location():
    """Functionality to add locations via the form."""
    db_connection = connect_to_database()
    print("Add new location!")

    #location_ID = request.form['location_ID']
    location_street_address = request.form['location_street_address']
    location_city = request.form['location_city']
    location_state = request.form['location_state']
    location_zip = request.form['location_zip']

    query = """INSERT INTO warehouse_locations (location_street_address, location_city, location_state,
            location_zip) VALUES (%s,%s,%s,%s)"""

    data = (location_street_address, location_city, location_state, location_zip)
    execute_query(db_connection, query, data)

    print("Location added!")
    return redirect(url_for('browse_locations'))
    # redirect goes to the defined function, not the app.route name


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
