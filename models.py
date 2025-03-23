from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()
    
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(20), nullable=False, default='customer')  # 'customer' or 'provider'
    
    # Provider-specific fields
    company_name = db.Column(db.String(100))
    description = db.Column(db.Text)
    services = db.Column(db.String(500))  # Comma-separated list of services
    location = db.Column(db.String(100))
    rating = db.Column(db.Float, default=0.0)
    reviews_count = db.Column(db.Integer, default=0)
    price_from = db.Column(db.Float)
    verified = db.Column(db.Boolean, default=False)
    availability = db.Column(db.String(500))  # JSON string of available time slots

    # Relationships
    bookings_received = db.relationship('Booking', backref='provider', foreign_keys='Booking.provider_id')
    bookings_made = db.relationship('Booking', backref='customer', foreign_keys='Booking.customer_id')
    service_offers = db.relationship('ServiceOffer', backref='provider', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_provider_dict(self):
        """Convert provider data to dictionary format for the search results"""
        if self.role != 'provider':
            return None
        
        return {
            'id': self.id,
            'name': self.company_name or self.username,
            'image': 'default_provider.jpg',  # You can add profile image handling later
            'rating': self.rating,
            'reviews': self.reviews_count,
            'description': self.description,
            'services': self.services.split(',') if self.services else [],
            'price_from': self.price_from,
            'verified': self.verified,
            'availability': self.availability,
            'service_offers': [offer.to_dict() for offer in self.service_offers if offer.is_active]
        }

    def __repr__(self):
        return f'User: {self.username}'

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    provider_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    service_type = db.Column(db.String(100), nullable=False)
    booking_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, confirmed, completed, cancelled
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    notes = db.Column(db.Text)
    price = db.Column(db.Float)

    def to_dict(self):
        return {
            'id': self.id,
            'provider': self.provider.to_provider_dict(),
            'service_type': self.service_type,
            'booking_date': self.booking_date.strftime('%Y-%m-%d %H:%M'),
            'status': self.status,
            'notes': self.notes,
            'price': self.price
        }

class ServiceOffer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    provider_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    service_type = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    duration = db.Column(db.Integer)  # Duration in minutes
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

    def to_dict(self):
        return {
            'id': self.id,
            'service_type': self.service_type,
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'duration': self.duration,
            'is_active': self.is_active
        }