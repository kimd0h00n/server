from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/dbname'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    total = db.Column(db.Float, nullable=False)
    items = db.Column(db.String, nullable=False)  # JSON string or better yet, a relationship to an Item model

    def __init__(self, total, items):
        self.total = total
        self.items = items

@app.route('/api/orders', methods=['POST'])
def receive_order():
    data = request.get_json()
    new_order = Order(total=data['total'], items=str(data['items']))
    db.session.add(new_order)
    db.session.commit()
    return jsonify({"message": "Order received", "id": new_order.id}), 201

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True, port=5001)
