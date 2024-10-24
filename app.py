from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///items.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define a model for the database
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

# Create the database
with app.app_context():  # Use application context when creating the database
    db.create_all()

# Create (POST) a new item
@app.route('/item', methods=['POST'])
def create_item():
    data = request.get_json()
    new_item = Item(name=data['name'])
    db.session.add(new_item)
    db.session.commit()
    return jsonify({'message': 'Item created successfully!'})

# Read (GET) all items
@app.route('/items', methods=['GET'])
def get_items():
    items = Item.query.all()
    output = [{'id': item.id, 'name': item.name} for item in items]
    return jsonify({'items': output})

# Update (PUT) an existing item
@app.route('/item/<int:id>', methods=['PUT'])
def update_item(id):
    data = request.get_json()
    item = Item.query.get(id)
    if item:
        item.name = data['name']
        db.session.commit()
        return jsonify({'message': 'Item updated successfully!'})
    return jsonify({'message': 'Item not found'}), 404

# Delete (DELETE) an item
@app.route('/item/<int:id>', methods=['DELETE'])
def delete_item(id):
    item = Item.query.get(id)
    if item:
        db.session.delete(item)
        db.session.commit()
        return jsonify({'message': 'Item deleted successfully!'})
    return jsonify({'message': 'Item not found'}), 404

# Default route
@app.route('/')
def welcome():
    return jsonify({"message": "Welcome to the Items API!"})

# Route to render HTML page showing all items
@app.route('/display-items')
def display_items():
    items = Item.query.all()  # Query all items
    return render_template('items.html', items=items)  # Render HTML template with items

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')  # Allow access from outside
