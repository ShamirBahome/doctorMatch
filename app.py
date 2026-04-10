from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///doctors.db'
db = SQLAlchemy(app)

class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    specialty = db.Column(db.String(50), nullable=False)
    rating = db.Column(db.Float, nullable=False)

@app.route('/api/doctors', methods=['GET'])
def get_doctors():
    doctors = Doctor.query.all()
    return jsonify([{'id': doctor.id, 'name': doctor.name, 'specialty': doctor.specialty, 'rating': doctor.rating} for doctor in doctors])

if __name__ == '__main__':
    app.run(debug=True)