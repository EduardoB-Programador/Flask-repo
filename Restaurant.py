# Intending to model a restaurant
class Order():
    id:int = 1
    order:list

    def __init__(self):
        self.id = Order.id
        self.order = []
        Order.id += 1

    # Adds food to the order
    def add(self, food):
        self.order.append(food)



class Customer():
    id:int = 1
    customer_name:str
    order:Order

    def __init__(self, name):
        self.customer_name = name
        self.id = Customer.id
        Customer.id += 1
        self.order = None

    def setOrder(self, order:Order):
        self.order = order

    def delete_order(self):
        self.order = None



class Local_customer(Customer):
    table:int

    def __init__(self, name, table_number):

        super().__init__(name)
        self.table = table_number



class Delivery_customer(Customer):
    address:str

    def __init__(self, name, address):

        super().__init__(name)
        self.address = address