from http.server import BaseHTTPRequestHandler, HTTPServer

from animals import get_all_animals, get_single_animal, delete_animal, get_animal_by_location, get_animal_by_status, update_animal
#  , create_animal, delete_animal, update_animal
from locations import get_all_locations, get_single_location
# create_location, delete_location, update_location
from employees import get_all_employees, get_single_employee, get_employees_by_location
#create_employee, delete_employee, update_employee
from customers import get_all_customers, get_single_customer, get_customer_by_email
#delete_customer, update_customer

import json


# Here's a class. It inherits from another class.
class HandleRequests(BaseHTTPRequestHandler):

    def parse_url(self, path):
        # Just like splitting a string in JavaScript. If the
        # path is "/animals/1", the resulting list will
        # have "" at index 0, "animals" at index 1, and "1"
        # at index 2.
        path_params = path.split("/")
        resource = path_params[1]
        
        if "?" in resource:
            # GIVEN: /customers?email=jenna@solis.com

            param = resource.split("?")[1]  # email=jenna@solis.com
            resource = resource.split("?")[0]  # 'customers'
            pair = param.split("=")  # [ 'email', 'jenna@solis.com' ]
            key = pair[0]  # 'email'
            value = pair[1]  # 'jenna@solis.com'

            return ( resource, key, value )

        # No query string parameter
        else:
            id = None

            try:
                id = int(path_params[2])
            except IndexError:
                pass  # No route parameter exists: /animals
            except ValueError:
                pass  # Request had trailing slash: /animals/

            return (resource, id)

    # Here's a class function
    def _set_headers(self, status):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    # Here's a method on the class that overrides the parent's method.
    # It handles any GET request.
    def do_GET(self):
        # Set the response code to 'Ok'
        self._set_headers(200)
        response = {}
        # Your new console.log() that outputs to the terminal
        print(self.path)

        parsed = self.parse_url(self.path)

        if len(parsed) == 2:
            (resource, id) = parsed 
        
            if resource == "animals":
                if id is not None:
                    response = f"{get_single_animal(id)}"

                else:
                    response = f"{get_all_animals()}"
            
            elif resource == "locations":
                if id is not None:
                    response = f"{get_single_location(id)}"
                else:
                    response = f"{get_all_locations()}"
            
            elif resource == "employees":
                if id is not None:
                    response = f"{get_single_employee(id)}"
                else:
                    response = f"{get_all_employees()}"
            
            elif resource == "customers":
                if id is not None:
                    response = f"{get_single_customer(id)}"
                else:
                    response = f"{get_all_customers()}"
        
        
        elif len(parsed) == 3:
            (resource, key, value) = parsed

            if key == "email" and resource == "customers":
                response = get_customer_by_email(value)
            
            if key =="location_id" and resource == "animals":
                response = get_animal_by_location(value)

            if key =="location_id" and resource == "employees":
                response = get_employees_by_location(value)
            if key == "status" and resource == "animals":
                response = get_animal_by_status(value)
        

        self.wfile.write(response.encode())  

    # Here's a method on the class that overrides the parent's method.
    # It handles any POST request.
    # def do_POST(self):
    #     # Set response code to 'Created'
    #     self._set_headers(201)

    #     content_len = int(self.headers.get('content-length', 0))
    #     post_body = self.rfile.read(content_len)

    #     post_body = json.loads(post_body)

    #     (resource, id) = self.parse_url(self.path)

    #     new_animal = None
    #     new_location = None
    #     new_employee = None

    #     if resource == "animals":
    #         new_animal = create_animal(post_body)
            
    #         self.wfile.write(f"{new_animal}".encode())
        
    #     elif resource == "locations":
    #         new_location = create_location(post_body) 

    #         self.wfile.write(f"{new_location}".encode())
        
    #     elif resource == "employees":
    #         new_employee = create_employee(post_body)

    #         self.wfile.write(f"{new_employee}".encode())

        


    # Here's a method on the class that overrides the parent's method.
    # It handles any PUT request.
    def do_PUT(self):
        
        self._set_headers(204)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

        (resource, id) = self.parse_url(self.path)

        if resource == "animals":
            update_animal(id, post_body)

        # elif resource == "locations":
        #     update_location(id, post_body)
            
        # elif resource == "employees":
        #     update_employee(id, post_body)
            
        # elif resource == "customers":
        #     update_customer(id, post_body)


        self.wfile.write("".encode())


    #deleting 
    def do_DELETE(self):
        self._set_headers(204)

        (resource, id) = self.parse_url(self.path)

        if resource == "animals":
            delete_animal(id)
        
        # elif resource == "locations":
        #     delete_location(id)
        
        # elif resource == "employees":
        #     delete_employee(id)

        # elif resource == "customers":
        #     delete_customer(id)
        
        self.wfile.write("".encode())

# This function is not inside the class. It is the starting
# point of this application.

# def do_OPTIONS(self):
#         self.send_response(200)
#         self.send_header('Access-Control-Allow-Origin', '*')
#         self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE')
#         self.send_header('Access-Control-Allow-Headers', 'X-Requested-With')
#         self.end_headers()

def main():
    host = ''
    port = int(os.environ['PORT'])
    HTTPServer((host, port), HandleRequests).serve_forever()

#test
main()