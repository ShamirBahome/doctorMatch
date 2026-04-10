from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime

db = SQLAlchemy()
bcrypt = Bcrypt()


class Doctor(db.Model):
    __tablename__ = 'doctors'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(20))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(255))
    website = db.Column(db.String(500))
    clinic_name = db.Column(db.String(255))
    address = db.Column(db.String(500))
    city = db.Column(db.String(100), default='Guelph')
    postal_code = db.Column(db.String(10))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    accepting_new_patients = db.Column(db.Boolean, default=False)
    wait_time_weeks = db.Column(db.Integer)
    languages = db.Column(db.String(500), default='English')
    specializations = db.Column(db.String(500), default='Family Medicine')
    education = db.Column(db.String(500))
    years_of_experience = db.Column(db.Integer)
    cpso_number = db.Column(db.String(50), unique=True)
    verified = db.Column(db.Boolean, default=False)
    monday_hours = db.Column(db.String(50), default='9:00 AM - 5:00 PM')
    tuesday_hours = db.Column(db.String(50), default='9:00 AM - 5:00 PM')
    wednesday_hours = db.Column(db.String(50), default='9:00 AM - 5:00 PM')
    thursday_hours = db.Column(db.String(50), default='9:00 AM - 5:00 PM')
    friday_hours = db.Column(db.String(50), default='9:00 AM - 5:00 PM')
    saturday_hours = db.Column(db.String(50), default='Closed')
    sunday_hours = db.Column(db.String(50), default='Closed')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    reviews = db.relationship('Review', backref='doctor', lazy=True)

    @property
    def full_name(self):
        return f"Dr. {self.first_name} {self.last_name}"

    @property
    def languages_list(self):
        if self.languages:
            return [lang.strip() for lang in self.languages.split(',')]
        return ['English']

    @property
    def average_rating(self):
        if not self.reviews:
            return 0.0
        total = sum(r.rating for r in self.reviews)
        return round(total / len(self.reviews), 1)

    @property
    def review_count(self):
        return len(self.reviews)

    @property
    def clinic_hours(self):
        return {
            'Monday': self.monday_hours,
            'Tuesday': self.tuesday_hours,
            'Wednesday': self.wednesday_hours,
            'Thursday': self.thursday_hours,
            'Friday': self.friday_hours,
            'Saturday': self.saturday_hours,
            'Sunday': self.sunday_hours,
        }

    def to_dict(self):
        return {
            'id': self.id,
            'full_name': self.full_name,
            'gender': self.gender,
            'phone': self.phone,
            'clinic_name': self.clinic_name,
            'address': self.address,
            'accepting_new_patients': self.accepting_new_patients,
            'wait_time_weeks': self.wait_time_weeks,
            'languages': self.languages_list,
            'average_rating': self.average_rating,
            'review_count': self.review_count,
            'latitude': self.latitude,
            'longitude': self.longitude,
        }


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    postal_code = db.Column(db.String(10))
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    reviews = db.relationship('Review', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)


class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(255))
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'rating': self.rating,
            'title': self.title,
            'comment': self.comment,
            'user_name': self.user.first_name if self.user else 'Anonymous',
            'created_at': self.created_at.strftime('%B %d, %Y'),
        }


class WalkinClinic(db.Model):
    __tablename__ = 'walkin_clinics'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(500))
    phone = db.Column(db.String(20))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    current_wait_minutes = db.Column(db.Integer, default=0)
    is_open = db.Column(db.Boolean, default=False)
    hours = db.Column(db.String(255))
    website = db.Column(db.String(500))

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'phone': self.phone,
            'current_wait_minutes': self.current_wait_minutes,
            'is_open': self.is_open,
            'hours': self.hours,
        }
