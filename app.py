from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///smartbanking.db'
app.config['JWT_SECRET_KEY'] = 'your-secret-key'

db = SQLAlchemy(app)
jwt = JWTManager(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    new_user = User(phone=data['phone'], password=data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify(message="User registered"), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(phone=data['phone']).first()
    if not user or user.password != data['password']:
        return jsonify({"message": "Invalid credentials"}), 401
    access_token = create_access_token(identity=user.id)
    return jsonify(access_token=access_token), 200

@app.route('/stkpush', methods=['POST'])
@jwt_required()
def stkpush():
    data = request.get_json()
    return jsonify({"message": "STK Push simulated"}), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000)
