CUSTOMERS = [
    {
      "id": 1,
      "name": "Hannah Hall",
      "address": "7002 Chestnut Ct"
    },
    {
      "id": 2,
      "name": "Bob Johnson",
      "address": "123 Main Street"
    }
]

def get_all_customers():
    return CUSTOMERS


def get_single_customer(id):
    requested_customer = None

    for customer in CUSTOMERS:
        if customer["id"] == id:
            requested_customer = customer
    return requested_customer


def delete_customer(id):
	customer_index = -1

	for index, customer in enumerate(CUSTOMERS):
		if customer["id"] == id:
			customer_index = index
	
	if customer_index >= 0:
		CUSTOMERS.pop(customer_index)