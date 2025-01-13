from flask import Flask,request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

class Drink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(120))

    def __repr__(self):
        return f"{self.name} - {self.description}"

@app.route('/')
def index():
    return 'Hello!'

@app.route('/drinks', methods=['GET'])
def get_drinks():
    drinks = Drink.query.all()
    output = []
    for drink in drinks:
        drink_data = {
            "id": drink.id,  # Include the 'id' field
            "name": drink.name,
            "description": drink.description
        }
        output.append(drink_data)
    return {"drinks": output}
        
    
# # Endpoint to add a new drink
# @app.route('/drink', methods=['POST'])
# def add_drink():
#     # Get data from the request
#     drink_data = request.json  # Expecting JSON data
#     new_drink = Drink(name=drink_data['name'], description=drink_data['description'])
    
#     # Add the new drink to the database
#     db.session.add(new_drink)
#     db.session.commit()
    
#     return jsonify({"message": "Drink added successfully!", "drink": {"name": new_drink.name, "description": new_drink.description}}), 201
# Endpoint to add a new drink
@app.route('/add_drink', methods=['GET', 'POST'])
def add_drink():
    if request.method == 'GET':
        # Render a form for adding drinks when accessed via GET
        return render_template('add_drink.html')  # Replace with your form HTML

    elif request.method == 'POST':
        # Handle form data sent via POST
        name = request.form['name']
        description = request.form['description']
        new_drink = Drink(name=name, description=description)

        # Add the new drink to the database
        db.session.add(new_drink)
        db.session.commit()

        return jsonify({
            "message": "Drink added successfully!",
            "drink": {"name": new_drink.name, "description": new_drink.description}
        }), 201



@app.route('/drinks/<id>', methods=['GET'])
def get_drink_by_id(id):
    print(f"Fetching drink with ID: {id}")  # Debugging

    # Query the database for the drink by ID
    drink = Drink.query.get(id)
    if not drink:
        print(f"Drink with ID {id} not found")  # Debugging
        return {"error": f"Drink with ID {id} not found"}, 404

    drink_data = {
        "id": drink.id,
        "name": drink.name,
        "description": drink.description
    }
    print(f"Returning drink data: {drink_data}")  # Debugging
    return {"drink": drink_data}

@app.route('/drinks/<int:id>', methods=['PATCH'])
def partial_update_drink(id):
    drink = Drink.query.get(id)
    if not drink:
        return {"error": f"Drink with ID {id} not found"}, 404

    data = request.json

    if 'name' in data:
        drink.name = data['name']
    if 'description' in data:
        drink.description = data['description']

    db.session.commit()

    return {
        "message": f"Drink with ID {id} partially updated successfully!",
        "drink": {
            "id": drink.id,
            "name": drink.name,
            "description": drink.description
        }
    }

@app.route("/drinks/<int:id>",methods=['PUT'])
def fully_update(id):
    drink=Drink.query.get(id)
    if not drink:
        return {"error": f"Drink with ID {id} not found"}, 404
    
    data=request.json

    if 'name' in data:
        drink.name = data['name']
    if 'description' in data:
        drink.description = data['description']

    #  # Ensure all required fields are present
    # if 'name' not in data or 'description' not in data:
    #     return {"error": "Both 'name' and 'description' are required fields"}, 400

    # # Update the drink with new data
    # drink.name = data['name']
    # drink.description = data['description']
    
    db.session.commit()

    return f"Successfully updated data"

@app.route('/drinks/<int:id>', methods=['DELETE'])
def delete_drink(id):
    # Query the database for the drink by ID
    drink = Drink.query.get(id)

    # Check if the drink exists
    if not drink:
        return {"error": f"Drink with ID {id} not found"}, 404

    # Delete the drink from the database
    db.session.delete(drink)
    db.session.commit()

    return {"message": f"Drink with ID {id} deleted successfully!"}, 200

if __name__ == "__main__":
    # Create tables before running the app
    # with app.app_context():
    #     db.create_all()
    #     print("Database tables created!")
    app.run(debug=True)




# @app.route('/')
# def index():
#     return 'Hello!'

# @app.route('/drinks',methods=['GET'])
# def get_drinks():
#     return drinks

# @app.route('/drinks/drinkid=<int:drinkid>', methods=['GET'])
# def get_specific_drinks(drinkid):
#     for drink in drinks:
#         if drink["id"]==drinkid:
#             return drink





















