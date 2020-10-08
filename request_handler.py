from http.server import BaseHTTPRequestHandler, HTTPServer

from animals import get_all_animals, get_single_animal, create_animal, delete_animal, update_animal
from locations import get_all_locations, get_single_location, create_location, delete_location, update_location
from employees import get_all_employees, get_single_employee, create_employee, delete_employee, update_employee
from customers import get_all_customers, get_single_customer, delete_customer, update_customer

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
        id = None

        # Try to get the item at index 2
        try:
            id = int(path_params[2])
        except IndexError:
            pass  # No route parameter exists: /animals it cannot change an empty string to an integer
        except ValueError:
            pass  # Request had trailing slash: /animals/

        return (resource, id)  # This is a tuple

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
        (resource, id) = self.parse_url(self.path)
        # It's an if..else statement
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

        self.wfile.write(response.encode())  

    # Here's a method on the class that overrides the parent's method.
    # It handles any POST request.
    def do_POST(self):
        # Set response code to 'Created'
        self._set_headers(201)

        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)

        post_body = json.loads(post_body)

        (resource, id) = self.parse_url(self.path)

        new_animal = None
        new_location = None
        new_employee = None

        if resource == "animals":
            new_animal = create_animal(post_body)
            
            self.wfile.write(f"{new_animal}".encode())
        
        elif resource == "locations":
            new_location = create_location(post_body) 

            self.wfile.write(f"{new_location}".encode())
        
        elif resource == "employees":
            new_employee = create_employee(post_body)

            self.wfile.write(f"{new_employee}".encode())

        


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

        elif resource == "locations":
            update_location(id, post_body)
            
        elif resource == "employees":
            update_employee(id, post_body)
            
        elif resource == "customers":
            update_customer(id, post_body)


        self.wfile.write("".encode())


    #deleting 
    def do_DELETE(self):
        self._set_headers(204)

        (resource, id) = self.parse_url(self.path)

        if resource == "animals":
            delete_animal(id)
        
        elif resource == "locations":
            delete_location(id)
        
        elif resource == "employees":
            delete_employee(id)

        elif resource == "customers":
            delete_customer(id)
        
        self.wfile.write("".encode())

# This function is not inside the class. It is the starting
# point of this application.
def main():
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()


if __name__ == "__main__":
    main()