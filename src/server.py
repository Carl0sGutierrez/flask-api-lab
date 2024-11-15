# Import the Flask class from the flask module 
from flask import Flask, make_response, request

# Mock data
data = [
    {
        "id": "3b58aade-8415-49dd-88db-8d7bce14932a",
        "first_name": "Tanya",
        "last_name": "Slad",
        "graduation_year": 1996,
        "address": "043 Heath Hill",
        "city": "Dayton",
        "zip": "45426",
        "country": "United States",
        "avatar": "http://dummyimage.com/139x100.png/cc0000/ffffff",
    },
    {
        "id": "d64efd92-ca8e-40da-b234-47e6403eb167",
        "first_name": "Ferdy",
        "last_name": "Garrow",
        "graduation_year": 1970,
        "address": "10 Wayridge Terrace",
        "city": "North Little Rock",
        "zip": "72199",
        "country": "United States",
        "avatar": "http://dummyimage.com/148x100.png/dddddd/000000",
    },
    {
        "id": "66c09925-589a-43b6-9a5d-d1601cf53287",
        "first_name": "Lilla",
        "last_name": "Aupol",
        "graduation_year": 1985,
        "address": "637 Carey Pass",
        "city": "Gainesville",
        "zip": "32627",
        "country": "United States",
        "avatar": "http://dummyimage.com/174x100.png/ff4444/ffffff",
    },
    {
        "id": "0dd63e57-0b5f-44bc-94ae-5c1b4947cb49",
        "first_name": "Abdel",
        "last_name": "Duke",
        "graduation_year": 1995,
        "address": "2 Lake View Point",
        "city": "Shreveport",
        "zip": "71105",
        "country": "United States",
        "avatar": "http://dummyimage.com/145x100.png/dddddd/000000",
    },
    {
        "id": "a3d8adba-4c20-495f-b4c4-f7de8b9cfb15",
        "first_name": "Corby",
        "last_name": "Tettley",
        "graduation_year": 1984,
        "address": "90329 Amoth Drive",
        "city": "Boulder",
        "zip": "80305",
        "country": "United States",
        "avatar": "http://dummyimage.com/198x100.png/cc0000/ffffff",
    }
]
# Create an instance of the Flask class, passing in the name of the current module
app = Flask(__name__)

# Define a route fot the root URL ("/")

@app.route("/")
def index():
    # Function that handles requests to the root URL
    # Return a plain text response
    return "hello world"

# Send custom HTTP code back with a tuple
@app.route("/no_content")
def no_content():
    message = {"message": "No content"}
    return message, 204

# Send custom HTTP code back to the client with the make_response() method
@app.route("/exp")
def index_explicit():
    res = make_response({"message": "Hello World"})
    res.status_code = 200

    return res

@app.route("/data")
def get_data():
    try:
        # Check if 'data' exists and has a length greater than 0
        if data and len(data) > 0:
            # Return a JSON response with a message indicating the length of the data
            return {"message": f"Data of length {len(data)} found"}
        else:
            # If 'data' is empty, return a JSON response with a 500 Internal Server Error status code
            return {"message": "Data is empty"}, 500
    except NameError:
        # Handle the case where 'data' is not defined
        # Return a JSON response with a 404 Not Found status code
        return {"message": "Data not found"}, 404
    
@app.route("/name_search")
def name_search():
    # Get the 'q' query parameter from the request URL
    query = request.args.get('q')

    # Check if the query parameter 'q' is missing or empty
    if not query:
        # Return a JSON response with a message indicating invalid request input and a 422 Unprocessable Entity state code
        return {"message": "Invalid input parameter"}, 422
    

    # Iterate through the 'data' list to seach for a matching person
    for person in data:
        # Check if the query string is present in the person's first name (case-insensitive)
        if query.lower() in person["first_name"].lower():
            # Return the matching person as a JSON response with a 200 OK status code
            return person
        
# Dynamic URLs

# Create /count method

# Return the total number of person in the data list
@app.route("/count")
def count():
    data_count = len(data)
    return {"data count" : data_count}, 200

# Create GET /person/id endpoint

@app.route("/person/<uuid:id>")
def find_by_uuid(id):
    
    for person in data:
        # Check if the 'id' field of the person matches the 'var_name' parameter
        if person["id"] == str(id):
            # Return the person as JSON response if a match found
            return person
        
    # Return a JSON response with a message and a 404 Not Found status code if no matching person is found
    return {"message": "Person not found"}, 404

@app.route("/person/<uuid:id>", methods=['DELETE'])
def delete_by_uuid(id):
    for person in data:
        if person["id"] == str(id):
            # Remove the person from data list
            data.remove(person)
            
            # Return a JSON response with a message and HTTP status code 200 (OK)
            return {"message": f"Person with {id} deleted"}, 200
    
    # If no person with the given ID is found, return a JSON response with a message and HTTP status code 404 (Not found)
    return {"message": "Person not found"}, 404


# Parse JSON from the Request body

@app.route("/person", methods=['POST'])
def add_by_uuid():
    new_person = request.json

    # Check if the required data was provided
    if not new_person:
        return {"message": "Invalid input parameter"}, 422
    try:
        data.append(new_person)
    except:
         return {"message": "data not defined"}, 500
        
    return {"message": f"{new_person['id']}"}, 200

# Add Error handlers
@app.errorhandler(404)
def api_not_found(error):
    # This function is a custom error handler for 404 Not Found errors
    # It is triggered whenever a 404 error occurs within the Flask application
    return {"message": "API not found"}, 404