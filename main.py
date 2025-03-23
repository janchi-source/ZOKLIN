from flask import Flask, render_template, url_for, redirect, request, flash, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user
from forms import RegistrationForm, LoginForm, BookingForm, ProviderProfileForm, ServiceOfferForm
from models import db, User, Booking, ServiceOffer
import os
from datetime import datetime, timedelta

app = Flask(__name__)

# Configuration
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'clanky.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'klucik'  # This is needed for CSRF protection

# Initialize extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Context processor for templates
@app.context_processor
def utility_processor():
    return {'now': datetime.now()}

# Create database tables
def init_db():
    with app.app_context():
        print("Creating database tables...")
        db.create_all()
        print(f"Database file should be at: {os.path.join(basedir, 'clanky.db')}")
        if os.path.exists(os.path.join(basedir, 'clanky.db')):
            print("Database file was created successfully!")
            
            # Add synthetic data if the database is empty
            if User.query.count() == 0:
                create_synthetic_data()
        else:
            print("Warning: Database file was not created!")

def create_synthetic_data():
    print("Creating synthetic data...")
    
    # Create test customers
    customers = [
        {
            'username': 'john_doe',
            'email': 'john@example.com',
            'password': 'password123',
            'role': 'customer'
        },
        {
            'username': 'alice_smith',
            'email': 'alice@example.com',
            'password': 'password123',
            'role': 'customer'
        }
    ]
    
    # Create test providers
    providers = [
        {
            'username': 'clean_masters',
            'email': 'cleanmasters@example.com',
            'password': 'password123',
            'role': 'provider',
            'company_name': 'Clean Masters Pro',
            'description': 'Professional cleaning service with 10 years of experience. We specialize in residential and commercial cleaning.',
            'services': 'house,office',
            'location': 'bratislava',
            'rating': 4.8,
            'reviews_count': 156,
            'price_from': 80,
            'verified': True,
            'availability': '{"monday": "9:00-17:00", "tuesday": "9:00-17:00", "wednesday": "9:00-17:00", "thursday": "9:00-17:00", "friday": "9:00-17:00"}'
        },
        {
            'username': 'garden_pros',
            'email': 'gardenpros@example.com',
            'password': 'password123',
            'role': 'provider',
            'company_name': 'Garden Professionals',
            'description': 'Expert garden maintenance and landscaping services. Making your outdoor space beautiful.',
            'services': 'garden',
            'location': 'pezinok',
            'rating': 4.9,
            'reviews_count': 89,
            'price_from': 120,
            'verified': True,
            'availability': '{"monday": "8:00-16:00", "wednesday": "8:00-16:00", "friday": "8:00-16:00"}'
        },
        {
            'username': 'car_wash_experts',
            'email': 'carwash@example.com',
            'password': 'password123',
            'role': 'provider',
            'company_name': 'Car Wash Experts',
            'description': 'Premium car cleaning and detailing services. We treat your car like our own.',
            'services': 'car',
            'location': 'bratislava',
            'rating': 4.7,
            'reviews_count': 203,
            'price_from': 50,
            'verified': True,
            'availability': '{"monday": "8:00-20:00", "tuesday": "8:00-20:00", "wednesday": "8:00-20:00", "thursday": "8:00-20:00", "friday": "8:00-20:00", "saturday": "9:00-15:00"}'
        },
        {
            'username': 'mind_cleaners',
            'email': 'mindclean@example.com',
            'password': 'password123',
            'role': 'provider',
            'company_name': 'Mind & Space Organization',
            'description': 'Professional mental space organization and decluttering services. Find clarity in chaos.',
            'services': 'mental',
            'location': 'bratislava',
            'rating': 4.95,
            'reviews_count': 45,
            'price_from': 150,
            'verified': True,
            'availability': '{"tuesday": "10:00-18:00", "thursday": "10:00-18:00", "saturday": "10:00-15:00"}'
        }
    ]
    
    # Add customers to database
    for customer_data in customers:
        customer = User(
            username=customer_data['username'],
            email=customer_data['email'],
            role=customer_data['role']
        )
        customer.set_password(customer_data['password'])
        db.session.add(customer)
    
    # Add providers to database
    for provider_data in providers:
        provider = User(
            username=provider_data['username'],
            email=provider_data['email'],
            role=provider_data['role'],
            company_name=provider_data['company_name'],
            description=provider_data['description'],
            services=provider_data['services'],
            location=provider_data['location'],
            rating=provider_data['rating'],
            reviews_count=provider_data['reviews_count'],
            price_from=provider_data['price_from'],
            verified=provider_data['verified'],
            availability=provider_data['availability']
        )
        provider.set_password(provider_data['password'])
        db.session.add(provider)
    
    # Create some sample bookings
    try:
        db.session.commit()
        
        # Now create bookings (after users are committed to get their IDs)
        john = User.query.filter_by(username='john_doe').first()
        alice = User.query.filter_by(username='alice_smith').first()
        clean_masters = User.query.filter_by(username='clean_masters').first()
        garden_pros = User.query.filter_by(username='garden_pros').first()
        
        bookings = [
            {
                'customer': john,
                'provider': clean_masters,
                'service_type': 'house',
                'booking_date': datetime.now() + timedelta(days=3),
                'status': 'confirmed',
                'notes': 'Please bring eco-friendly cleaning products',
                'price': 100
            },
            {
                'customer': alice,
                'provider': garden_pros,
                'service_type': 'garden',
                'booking_date': datetime.now() + timedelta(days=5),
                'status': 'pending',
                'notes': 'Front yard needs special attention',
                'price': 150
            },
            {
                'customer': john,
                'provider': clean_masters,
                'service_type': 'office',
                'booking_date': datetime.now() - timedelta(days=2),
                'status': 'completed',
                'notes': 'Regular office cleaning',
                'price': 120
            }
        ]
        
        for booking_data in bookings:
            booking = Booking(
                provider_id=booking_data['provider'].id,
                customer_id=booking_data['customer'].id,
                service_type=booking_data['service_type'],
                booking_date=booking_data['booking_date'],
                status=booking_data['status'],
                notes=booking_data['notes'],
                price=booking_data['price']
            )
            db.session.add(booking)
        
        db.session.commit()
        print("Synthetic data created successfully!")
        
    except Exception as e:
        print(f"Error creating synthetic data: {e}")
        db.session.rollback()

init_db()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/privacy-policy')
def privacy_policy():
    return render_template('legal/privacy_policy.html')

@app.route('/terms-of-service')
def terms_of_service():
    return render_template('legal/terms_of_service.html')

@app.route('/cookie-policy')
def cookie_policy():
    return render_template('legal/cookie_policy.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Here you would typically process the form data
        # For now, we'll just show a success message
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')
        
        # You could send an email here
        # For now, just flash a success message
        flash('Thank you for your message! We will get back to you soon.')
        return redirect(url_for('contact'))
    
    return render_template('contact.html')

@app.route('/house')
def house():
    return render_template('services/house.html')

@app.route('/car')
def car():
    return render_template('services/car.html')

@app.route('/garden')
def garden():
    return render_template('services/garden.html')

@app.route('/office')
def office():
    return render_template('services/office.html')

@app.route('/mental')
@login_required
def mental():
    return render_template('services/mental.html')

@app.route('/search')
def search():
    service_type = request.args.get('service_type', 'all')
    query = request.args.get('query', '')
    location = request.args.get('location', 'bratislava')
    price_range = request.args.get('price_range', '0-500')
    page = int(request.args.get('page', 1))
    
    # Query providers from the database
    providers_query = User.query.filter_by(role='provider')
    
    # Apply filters
    if service_type != 'all':
        providers_query = providers_query.filter(User.services.like(f'%{service_type}%'))
    if location:
        providers_query = providers_query.filter_by(location=location)
    if query:
        providers_query = providers_query.filter(
            db.or_(
                User.company_name.like(f'%{query}%'),
                User.description.like(f'%{query}%'),
                User.services.like(f'%{query}%')
            )
        )
    
    # Handle price range filter
    if price_range != '1000+':
        min_price, max_price = map(int, price_range.split('-'))
        providers_query = providers_query.filter(User.price_from >= min_price)
        if max_price:
            providers_query = providers_query.filter(User.price_from <= max_price)
    
    # Pagination
    items_per_page = 10
    providers_paginated = providers_query.paginate(page=page, per_page=items_per_page, error_out=False)
    
    # Convert provider data to the format expected by the template
    providers = [p.to_provider_dict() for p in providers_paginated.items]
    
    return render_template('search_results.html',
                         providers=providers,
                         page=page,
                         total_pages=providers_paginated.pages)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Check if user already exists
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            flash('Email address already registered.')
            return redirect(url_for('register'))
        
        # Create new user
        new_user = User(
            username=form.username.data,
            email=form.email.data,
            role=form.role.data
        )
        new_user.set_password(form.password.data)
        
        # Add provider-specific information if registering as a provider
        if form.role.data == 'provider':
            new_user.company_name = form.company_name.data
            new_user.description = form.description.data
            new_user.services = form.services.data
            new_user.location = form.location.data
            new_user.price_from = form.price_from.data
        
        # Save to database
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful! Please log in.')
        return redirect(url_for('login'))
    
    return render_template('RegistrationPage.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page if next_page else url_for('home'))
        else:
            flash('Invalid email or password')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/book/<int:provider_id>', methods=['GET', 'POST'])
@login_required
def book_service(provider_id):
    if current_user.role != 'customer':
        flash('Only customers can book services.')
        return redirect(url_for('search'))
    
    provider = User.query.get_or_404(provider_id)
    if provider.role != 'provider':
        flash('Invalid provider.')
        return redirect(url_for('search'))
    
    form = BookingForm()
    if form.validate_on_submit():
        try:
            booking_date = datetime.strptime(form.booking_date.data, '%Y-%m-%dT%H:%M')
            booking = Booking(
                provider_id=provider_id,
                customer_id=current_user.id,
                service_type=form.service_type.data,
                booking_date=booking_date,
                notes=form.notes.data,
                price=provider.price_from  # You might want to adjust this based on service type
            )
            db.session.add(booking)
            db.session.commit()
            
            flash('Booking request sent successfully! The provider will confirm your booking.')
            return redirect(url_for('my_bookings'))
        except ValueError:
            flash('Invalid date format. Please use the date picker.')
            return render_template('booking.html', form=form, provider=provider)
    
    return render_template('booking.html', form=form, provider=provider)

@app.route('/my-bookings')
@login_required
def my_bookings():
    if current_user.role == 'customer':
        bookings = Booking.query.filter_by(customer_id=current_user.id).order_by(Booking.booking_date.desc()).all()
    else:
        bookings = Booking.query.filter_by(provider_id=current_user.id).order_by(Booking.booking_date.desc()).all()
    return render_template('my_bookings.html', bookings=bookings)

@app.route('/provider/profile', methods=['GET', 'POST'])
@login_required
def provider_profile():
    if current_user.role != 'provider':
        flash('Access denied. Provider account required.')
        return redirect(url_for('home'))
    
    form = ProviderProfileForm(obj=current_user)
    if form.validate_on_submit():
        current_user.company_name = form.company_name.data
        current_user.description = form.description.data
        current_user.services = form.services.data
        current_user.location = form.location.data
        current_user.price_from = form.price_from.data
        current_user.availability = form.availability.data
        
        db.session.commit()
        flash('Your profile has been updated.')
        return redirect(url_for('provider_profile'))
    
    return render_template('provider_profile.html', form=form)

@app.route('/booking/<int:booking_id>/status', methods=['POST'])
@login_required
def update_booking_status(booking_id):
    if current_user.role != 'provider':
        return jsonify({'error': 'Access denied'}), 403
    
    booking = Booking.query.get_or_404(booking_id)
    if booking.provider_id != current_user.id:
        return jsonify({'error': 'Access denied'}), 403
    
    status = request.json.get('status')
    if status not in ['confirmed', 'completed', 'cancelled']:
        return jsonify({'error': 'Invalid status'}), 400
    
    booking.status = status
    db.session.commit()
    
    return jsonify({'message': 'Booking status updated successfully'})

@app.route('/provider/offers', methods=['GET', 'POST'])
@login_required
def manage_offers():
    if current_user.role != 'provider':
        flash('Access denied. Provider account required.')
        return redirect(url_for('home'))
    
    form = ServiceOfferForm()
    if form.validate_on_submit():
        offer = ServiceOffer(
            provider_id=current_user.id,
            service_type=form.service_type.data,
            title=form.title.data,
            description=form.description.data,
            price=form.price.data,
            duration=form.duration.data,
            is_active=form.is_active.data
        )
        db.session.add(offer)
        db.session.commit()
        flash('Service offer created successfully!')
        return redirect(url_for('manage_offers'))
    
    offers = ServiceOffer.query.filter_by(provider_id=current_user.id).order_by(ServiceOffer.created_at.desc()).all()
    return render_template('manage_offers.html', form=form, offers=offers)

@app.route('/provider/offers/<int:offer_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_offer(offer_id):
    if current_user.role != 'provider':
        flash('Access denied. Provider account required.')
        return redirect(url_for('home'))
    
    offer = ServiceOffer.query.get_or_404(offer_id)
    if offer.provider_id != current_user.id:
        flash('Access denied. You can only edit your own offers.')
        return redirect(url_for('manage_offers'))
    
    form = ServiceOfferForm(obj=offer)
    if form.validate_on_submit():
        offer.service_type = form.service_type.data
        offer.title = form.title.data
        offer.description = form.description.data
        offer.price = form.price.data
        offer.duration = form.duration.data
        offer.is_active = form.is_active.data
        
        db.session.commit()
        flash('Service offer updated successfully!')
        return redirect(url_for('manage_offers'))
    
    return render_template('edit_offer.html', form=form, offer=offer)

@app.route('/provider/offers/<int:offer_id>/toggle', methods=['POST'])
@login_required
def toggle_offer(offer_id):
    if current_user.role != 'provider':
        return jsonify({'error': 'Access denied'}), 403
    
    offer = ServiceOffer.query.get_or_404(offer_id)
    if offer.provider_id != current_user.id:
        return jsonify({'error': 'Access denied'}), 403
    
    offer.is_active = not offer.is_active
    db.session.commit()
    
    flash(f'Offer {"activated" if offer.is_active else "deactivated"} successfully!')
    return redirect(url_for('manage_offers'))

@app.route('/provider/requests')
@login_required
def provider_requests():
    if current_user.role != 'provider':
        flash('Access denied. Provider account required.')
        return redirect(url_for('home'))
    
    # Get all bookings for the provider with customer information
    bookings = Booking.query.filter_by(provider_id=current_user.id)\
        .join(User, Booking.customer_id == User.id)\
        .order_by(Booking.created_at.desc())\
        .all()
    
    return render_template('provider_requests.html', bookings=bookings)

if __name__ == '__main__':
    app.run(debug=True)