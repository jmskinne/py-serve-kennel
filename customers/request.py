import sqlite3
import json

from models import Customer



def get_all_customers():
	# Open a connection to the database
	with sqlite3.connect("./kennel.db") as conn:

		# Just use these. It's a Black Box.
		conn.row_factory = sqlite3.Row
		db_cursor = conn.cursor()

		db_cursor.execute("""
		SELECT
			c.id,
			c.name,
			c.address,
			c.email,
			c.password
		FROM customer c
		""")
			
		

		customers = []

		dataset = db_cursor.fetchall()

		for row in dataset:
			customer = Customer(row['id'],row['name'], row['address'],  row['email'], row['password'])
		
			customers.append(customer.__dict__)

	return json.dumps(customers)


def get_single_customer(id):
	with sqlite3.connect("./kennel.db") as conn:
		conn.row_factory = sqlite3.Row
		db_cursor = conn.cursor()

		db_cursor.execute("""
		SELECT
			c.id,
			c.name,
			c.address,
			c.email,
			c.password
		FROM customer c
		WHERE c.id = ?
		""", (id, ))

		data = db_cursor.fetchone()

		customer = Customer(data['id'], data['address'], data['name'], data['email'], data['password'])

		return json.dumps(customer.__dict__)


def get_customer_by_email(email):

    with sqlite3.connect("./kennel.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        select
            c.id,
            c.name,
            c.address,
            c.email,
            c.password
        from Customer c
        WHERE c.email = ?
        """, ( email, )) #this email is from the request_handler where email = value users email address

        data = db_cursor.fetchall()
        customers = []
        
        for row in data:
            customer = Customer(row['id'],row['name'], row['address'], row['email'],row['password'])
         
            customers.append(customer.__dict__)
       
    return json.dumps(customers) 


# def delete_customer(id):
# 	customer_index = -1

# 	for index, customer in enumerate(CUSTOMERS):
# 		if customer["id"] == id:
# 			customer_index = index
	
# 	if customer_index >= 0:
# 		CUSTOMERS.pop(customer_index)



# def update_customer(id, new_customer):
# 	for index, customer in enumerate(CUSTOMERS):
# 		if customer["id"] == id:
# 			CUSTOMERS[index] = new_customer
# 			break