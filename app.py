# Never forget to use the correct interpreter
from flask import Flask, render_template, jsonify, abort, json, request
from Restaurant import *

app = Flask(__name__)

# No database, yet, so local lists storing data
local_customers:list = []
local_orders:list = []

####################################
def find_order(id:int):

    for o in local_orders:

        if o.get("id") == id:
            return o
        
    abort(404, 'Order Not Found.')


def find_customer_by_id(id:int):

    for c in local_customers:

        if c.id == id:
            return c
        
    abort(404, 'Customer not found.')


# Defining if the customer is local or delivery
def define_customer_type(data:dict):

    # Gets the data needed to make a new customer
    name = data.get('name')
    address = data.get('address')
    table = data.get('table')

    # The customer should input either an address or the table's number
    if table and address:
        abort(400, 'Invalid data input.')

    # returns d, which stands for delivery_customer
    if type(name) == str and type(address) == str:
        return ('d', [name, address])
    
    # returns l, which stands for local_customer
    if type(name) == str and type(table) == int:
        return ('l', [name, table])
    
    abort(400, 'Invalid data input.')

def create_customer(type:tuple):

    if type[0] == 'l':

        info:list = type[1]
        lc = Local_customer(info[0], info[1])
        local_customers.append(lc)
        return lc
    
    if type[0] == 'd':
        
        info:list = type[1]
        dc = Delivery_customer(info[0], info[1])
        local_customers.append(dc)
        return dc
    
def update_data(customer:Local_customer|Delivery_customer, data):
    
    name = data.get('name')
    address = data.get('address')
    table = data.get('table')
    order = data.get('order')

    if address and table:
        abort(400, 'Invalid data input.')

    if name:
        customer.customer_name = name

    if address and type(customer) == Delivery_customer:
        customer.address = address

    if table and type(customer) == Local_customer:
        customer.table = table

    if order:
        customer.order = order

    
def set_customer_order(customer:Customer, order:dict):

    if order.get('order'):
        o:Order = Order()
        o.add(order.get('order'))

        local_orders.append(o.__dict__)
        customer.setOrder(o.__dict__)

    else:
        abort(400, 'Invalid input.')

####################################
@app.errorhandler(400)
def Invalid(error):
    data:dict = {'error': str(error)}

    return (jsonify(data), 400)

@app.errorhandler(404)
def NotFound(error):
    data:dict = {'error': str(error)}

    return (jsonify(data), 404)


####################################
# Home page
@app.route('/')
def home():

    return render_template('home.html')

# Json of all the orders
@app.route('/orders/')
def all_orders():
    
    data:list = []

    for o in local_orders:
        data.append(o)

    return jsonify(data)

# Json of a specific order
@app.route('/orders/<int:id>/')
def single_order(id):

    data = find_order(id)

    return jsonify(data)

# json of all customers
@app.route('/customers/')
def all_customers():

    data:list = []

    for c in local_customers:
        data.append(c.__dict__)

    return jsonify(data)

# json of a specific customer
@app.route('/customers/<int:id>/')
def single_customer(id):

    data = find_customer_by_id(id)

    return jsonify(data.__dict__)

# Uses a Json to make a customer
@app.route('/customers/', methods=['POST'])
def customer_POST():
    data:dict = json.loads(request.data)

    customer_data:tuple = define_customer_type(data)

    customer:Customer = create_customer(customer_data)

    return jsonify(customer.__dict__)

# Creates an order for the specific customer
@app.route('/customers/<int:id>/order/', methods=['POST'])
def customer_order_POST(id):
    data = json.loads(request.data)

    customer:Customer = find_customer_by_id(id)

    set_customer_order(customer, data)

    return jsonify(customer.__dict__)
    
# Update info
@app.route('/customers/<int:id>/', methods=['PUT', 'PATCH'])
def update_customer_info(id):
    data = json.loads(request.data)

    customer:Customer = find_customer_by_id(id)

    update_data(customer, data)

    return jsonify(customer.__dict__)

# Delete customer
@app.route('/customers/<int:id>/', methods=['DELETE'])
def delete_customer(id):

    customer:Customer = find_customer_by_id(id)

    local_customers.remove(customer)

    return jsonify(customer.__dict__)

# Delete order
@app.route('/orders/<int:id>/', methods= ['DELETE'])
def delete_order(id):

    order:Order = find_order(id)
    customer:Customer = find_customer_by_id(id)
    customer.delete_order()

    local_orders.remove(order)

    return jsonify(order)