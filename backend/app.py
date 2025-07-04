from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin
from flask_cors import CORS
from flask_migrate import Migrate
from datetime import datetime, timedelta
import pytz
import redis
from celery import Celery
import os
from werkzeug.security import generate_password_hash, check_password_hash
import json
import uuid

app = Flask(__name__)

# IST timezone configuration - CRITICAL FIX
IST = pytz.timezone('Asia/Kolkata')

def get_ist_now():
    """Get current time in IST - ALWAYS returns IST time"""
    utc_now = datetime.utcnow()
    utc_aware = pytz.UTC.localize(utc_now)
    ist_time = utc_aware.astimezone(IST)
    return ist_time

def get_ist_naive():
    """Get current IST time as naive datetime for database storage"""
    ist_time = get_ist_now()
    return ist_time.replace(tzinfo=None)

def format_ist_datetime(dt):
    """Format datetime in IST for JSON serialization"""
    if dt is None:
        return None
    
    # If it's a naive datetime, assume it's already in IST
    if dt.tzinfo is None:
        # Create IST-aware datetime
        ist_aware = IST.localize(dt)
    else:
        # Convert to IST if it has timezone info
        ist_aware = dt.astimezone(IST)
    
    return ist_aware.strftime('%d/%m/%Y, %I:%M:%S %p IST')

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///parking_system.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECURITY_PASSWORD_SALT'] = os.environ.get('SECURITY_PASSWORD_SALT', 'your-salt-here-change-in-production')
app.config['SECURITY_REGISTERABLE'] = True
app.config['SECURITY_SEND_REGISTER_EMAIL'] = False
app.config['SECURITY_SEND_PASSWORD_CHANGE_EMAIL'] = False
app.config['SECURITY_SEND_PASSWORD_RESET_EMAIL'] = False

# Redis Configuration
app.config['REDIS_URL'] = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')

# Celery Configuration
app.config['CELERY_BROKER_URL'] = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
app.config['CELERY_RESULT_BACKEND'] = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')

# Initialize extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# CORS Configuration - Allow all origins for now to fix the issue
CORS(app, 
     origins=["*"],
     allow_headers=["Content-Type", "Authorization", "Access-Control-Allow-Credentials"],
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
     supports_credentials=True)

# Redis client (will work when Redis is available)
try:
    redis_client = redis.from_url(app.config['REDIS_URL'])
    redis_client.ping()
except:
    redis_client = None

# Celery (will work when Redis is available)
def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)
    return celery

try:
    celery = make_celery(app)
except:
    celery = None

# Models
roles_users = db.Table('roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    fullname = db.Column(db.String(255), nullable=False)
    address = db.Column(db.Text)
    pin_code = db.Column(db.String(10))
    active = db.Column(db.Boolean(), default=True)
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=get_ist_naive)
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))

class ParkingLot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    address = db.Column(db.Text, nullable=False)
    total_spots = db.Column(db.Integer, nullable=False)
    available_spots = db.Column(db.Integer, nullable=False)
    price_per_hour = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=get_ist_naive)
    
    spots = db.relationship('ParkingSpot', backref='lot', lazy=True, cascade='all, delete-orphan')

class ParkingSpot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lot_id = db.Column(db.Integer, db.ForeignKey('parking_lot.id'), nullable=False)
    spot_number = db.Column(db.String(10), nullable=False)
    status = db.Column(db.String(20), default='available')  # available, occupied, reserved
    occupied_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    vehicle_number = db.Column(db.String(20))
    booked_at = db.Column(db.DateTime)
    release_time = db.Column(db.DateTime)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    lot_id = db.Column(db.Integer, db.ForeignKey('parking_lot.id'), nullable=False)
    spot_id = db.Column(db.Integer, db.ForeignKey('parking_spot.id'), nullable=False)
    vehicle_number = db.Column(db.String(20), nullable=False)
    start_time = db.Column(db.DateTime, default=get_ist_naive)
    end_time = db.Column(db.DateTime)
    duration_hours = db.Column(db.Float, nullable=False)  # Store actual duration
    total_cost = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='active')  # active, completed
    
    user = db.relationship('User', backref='bookings')
    lot = db.relationship('ParkingLot', backref='bookings')
    spot = db.relationship('ParkingSpot', backref='bookings')

# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

# Celery Tasks
if celery:
    @celery.task
    def cleanup_expired_bookings():
        """Clean up expired parking bookings"""
        current_time = get_ist_naive()
        expired_spots = ParkingSpot.query.filter(
            ParkingSpot.status == 'occupied',
            ParkingSpot.release_time < current_time
        ).all()
        
        for spot in expired_spots:
            # Release the spot
            spot.status = 'available'
            spot.occupied_by = None
            spot.vehicle_number = None
            spot.booked_at = None
            spot.release_time = None
            
            # Update lot availability
            lot = ParkingLot.query.get(spot.lot_id)
            lot.available_spots += 1
            
            # Update booking status
            booking = Booking.query.filter_by(
                spot_id=spot.id,
                status='active'
            ).first()
            if booking:
                booking.status = 'completed'
                booking.end_time = current_time
        
        db.session.commit()
        return f"Cleaned up {len(expired_spots)} expired bookings"

# Cache helper functions
def get_from_cache(key):
    if redis_client:
        try:
            data = redis_client.get(key)
            return json.loads(data) if data else None
        except:
            return None
    return None

def set_cache(key, data, expires=300):
    if redis_client:
        try:
            redis_client.setex(key, expires, json.dumps(data))
        except:
            pass

# Add CORS headers to all responses
@app.after_request
def after_request(response):
    origin = request.headers.get('Origin')
    if origin:
        response.headers.add('Access-Control-Allow-Origin', origin)
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response

# API Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/health')
def health_check():
    current_time = get_ist_now()
    return jsonify({
        'status': 'healthy', 
        'timestamp': current_time.isoformat(),
        'timezone': 'Asia/Kolkata (IST)',
        'current_ist_time': current_time.strftime('%d/%m/%Y, %I:%M:%S %p IST'),
        'server_time': datetime.now().isoformat(),
        'environment': os.environ.get('RAILWAY_ENVIRONMENT', 'development')
    })

@app.route('/api/auth/login', methods=['POST', 'OPTIONS'])
def login():
    if request.method == 'OPTIONS':
        return '', 200
        
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'message': 'No data provided'}), 400
            
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({'success': False, 'message': 'Email and password required'}), 400
        
        # Check for admin login
        if email == 'admin@parking.com' and password == 'admin':
            admin_user = {
                'id': 'admin',
                'email': 'admin@parking.com',
                'fullname': 'Administrator',
                'address': 'Bangalore Parking Authority, Vidhana Soudha, Bangalore',
                'pin_code': '560001',
                'is_admin': True,
                'created_at': format_ist_datetime(get_ist_now())
            }
            return jsonify({'success': True, 'user': admin_user})
        
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            is_admin = any(role.name == 'admin' for role in user.roles)
            user_data = {
                'id': str(user.id),
                'email': user.email,
                'fullname': user.fullname,
                'address': user.address,
                'pin_code': user.pin_code,
                'is_admin': is_admin,
                'created_at': format_ist_datetime(user.created_at)
            }
            return jsonify({'success': True, 'user': user_data})
        
        return jsonify({'success': False, 'message': 'Invalid credentials'}), 401
        
    except Exception as e:
        print(f"Login error: {str(e)}")
        return jsonify({'success': False, 'message': 'Server error'}), 500

@app.route('/api/auth/register', methods=['POST', 'OPTIONS'])
def register():
    if request.method == 'OPTIONS':
        return '', 200
        
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'message': 'No data provided'}), 400
        
        # Check if user exists
        existing_user = User.query.filter_by(email=data['email']).first()
        if existing_user:
            return jsonify({'success': False, 'message': 'Email already exists'}), 400
        
        # Generate unique identifier for Flask-Security
        fs_uniquifier = str(uuid.uuid4())
        
        # Create new user with IST timestamp
        current_time = get_ist_naive()
        user = User(
            email=data['email'],
            password=generate_password_hash(data['password']),
            fullname=data['fullname'],
            address=data['address'],
            pin_code=data['pin_code'],
            fs_uniquifier=fs_uniquifier,
            created_at=current_time
        )
        
        db.session.add(user)
        db.session.commit()
        
        user_data = {
            'id': str(user.id),
            'email': user.email,
            'fullname': user.fullname,
            'address': user.address,
            'pin_code': user.pin_code,
            'is_admin': False,
            'created_at': format_ist_datetime(user.created_at)
        }
        
        return jsonify({'success': True, 'user': user_data})
        
    except Exception as e:
        print(f"Registration error: {str(e)}")
        return jsonify({'success': False, 'message': 'Server error'}), 500

@app.route('/api/parking-lots', methods=['GET'])
def get_parking_lots():
    # Try cache first
    cache_key = 'parking_lots'
    cached_data = get_from_cache(cache_key)
    if cached_data:
        return jsonify(cached_data)
    
    lots = ParkingLot.query.all()
    lots_data = []
    for lot in lots:
        lots_data.append({
            'id': str(lot.id),
            'name': lot.name,
            'location': lot.location,
            'address': lot.address,
            'total_spots': lot.total_spots,
            'available_spots': lot.available_spots,
            'price_per_hour': lot.price_per_hour,
            'created_at': format_ist_datetime(lot.created_at)
        })
    
    # Cache for 5 minutes
    set_cache(cache_key, lots_data, 300)
    return jsonify(lots_data)

@app.route('/api/parking-lots', methods=['POST'])
def create_parking_lot():
    data = request.get_json()
    
    current_time = get_ist_naive()
    lot = ParkingLot(
        name=data['name'],
        location=data['location'],
        address=data['address'],
        total_spots=data['total_spots'],
        available_spots=data['total_spots'],
        price_per_hour=data['price_per_hour'],
        created_at=current_time
    )
    
    db.session.add(lot)
    db.session.flush()
    
    # Create parking spots
    for i in range(1, data['total_spots'] + 1):
        spot = ParkingSpot(
            lot_id=lot.id,
            spot_number=f"{i:03d}",
            status='available'
        )
        db.session.add(spot)
    
    db.session.commit()
    
    # Clear cache
    if redis_client:
        try:
            redis_client.delete('parking_lots')
        except:
            pass
    
    return jsonify({'success': True, 'id': str(lot.id)})

@app.route('/api/parking-lots/<int:lot_id>', methods=['PUT'])
def update_parking_lot(lot_id):
    data = request.get_json()
    lot = ParkingLot.query.get_or_404(lot_id)
    
    lot.name = data.get('name', lot.name)
    lot.location = data.get('location', lot.location)
    lot.address = data.get('address', lot.address)
    lot.price_per_hour = data.get('price_per_hour', lot.price_per_hour)
    
    db.session.commit()
    
    # Clear cache
    if redis_client:
        try:
            redis_client.delete('parking_lots')
        except:
            pass
    
    return jsonify({'success': True})

@app.route('/api/parking-lots/<int:lot_id>', methods=['DELETE'])
def delete_parking_lot(lot_id):
    lot = ParkingLot.query.get_or_404(lot_id)
    db.session.delete(lot)
    db.session.commit()
    
    # Clear cache
    if redis_client:
        try:
            redis_client.delete('parking_lots')
        except:
            pass
    
    return jsonify({'success': True})

@app.route('/api/parking-lots/<int:lot_id>/spots', methods=['GET'])
def get_parking_spots(lot_id):
    cache_key = f'parking_spots_{lot_id}'
    cached_data = get_from_cache(cache_key)
    if cached_data:
        return jsonify(cached_data)
    
    spots = ParkingSpot.query.filter_by(lot_id=lot_id).all()
    spots_data = []
    for spot in spots:
        spot_data = {
            'id': str(spot.id),
            'lot_id': str(spot.lot_id),
            'spot_number': spot.spot_number,
            'status': spot.status,
            'occupied_by': str(spot.occupied_by) if spot.occupied_by else None,
            'vehicle_number': spot.vehicle_number,
            'booked_at': format_ist_datetime(spot.booked_at),
            'release_time': format_ist_datetime(spot.release_time)
        }
        
        # Add user details if occupied (for admin view)
        if spot.occupied_by:
            user = User.query.get(spot.occupied_by)
            if user:
                spot_data['user_details'] = {
                    'id': str(user.id),
                    'fullname': user.fullname,
                    'email': user.email,
                    'address': user.address,
                    'pin_code': user.pin_code
                }
                
                # Get booking details
                booking = Booking.query.filter_by(
                    spot_id=spot.id,
                    status='active'
                ).first()
                if booking:
                    spot_data['booking_details'] = {
                        'id': str(booking.id),
                        'duration_hours': booking.duration_hours,
                        'total_cost': booking.total_cost,
                        'start_time': format_ist_datetime(booking.start_time)
                    }
        
        spots_data.append(spot_data)
    
    # Cache for 1 minute (more frequent updates needed)
    set_cache(cache_key, spots_data, 60)
    return jsonify(spots_data)

@app.route('/api/bookings', methods=['POST'])
def create_booking():
    data = request.get_json()
    
    spot = ParkingSpot.query.get(data['spot_id'])
    lot = ParkingLot.query.get(data['lot_id'])
    
    if not spot or spot.status != 'available':
        return jsonify({'success': False, 'message': 'Spot not available'}), 400
    
    # Get the actual hours from the request
    hours = float(data.get('hours', 1))
    total_cost = lot.price_per_hour * hours
    
    current_time = get_ist_naive()
    
    # Create booking with actual duration
    booking = Booking(
        user_id=data['user_id'],
        lot_id=data['lot_id'],
        spot_id=data['spot_id'],
        vehicle_number=data['vehicle_number'],
        duration_hours=hours,  # Store the actual duration
        total_cost=total_cost,
        status='active',
        start_time=current_time
    )
    
    # Update spot
    spot.status = 'occupied'
    spot.occupied_by = data['user_id']
    spot.vehicle_number = data['vehicle_number']
    spot.booked_at = current_time
    spot.release_time = current_time + timedelta(hours=hours)  # Use actual hours
    
    # Update lot availability
    lot.available_spots = max(0, lot.available_spots - 1)
    
    db.session.add(booking)
    db.session.commit()
    
    # Clear relevant caches
    if redis_client:
        try:
            redis_client.delete('parking_lots')
            redis_client.delete(f'parking_spots_{lot.id}')
        except:
            pass
    
    return jsonify({'success': True, 'booking_id': str(booking.id)})

@app.route('/api/bookings/<int:booking_id>/release', methods=['POST'])
def release_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    
    if booking.status != 'active':
        return jsonify({'success': False, 'message': 'Booking already completed'}), 400
    
    current_time = get_ist_naive()
    
    # Update booking
    booking.status = 'completed'
    booking.end_time = current_time
    
    # Update spot
    spot = ParkingSpot.query.get(booking.spot_id)
    spot.status = 'available'
    spot.occupied_by = None
    spot.vehicle_number = None
    spot.booked_at = None
    spot.release_time = None
    
    # Update lot availability
    lot = ParkingLot.query.get(booking.lot_id)
    lot.available_spots = min(lot.total_spots, lot.available_spots + 1)
    
    db.session.commit()
    
    # Clear relevant caches
    if redis_client:
        try:
            redis_client.delete('parking_lots')
            redis_client.delete(f'parking_spots_{lot.id}')
        except:
            pass
    
    return jsonify({'success': True})

@app.route('/api/users/<int:user_id>/bookings', methods=['GET'])
def get_user_bookings(user_id):
    bookings = Booking.query.filter_by(user_id=user_id).order_by(Booking.start_time.desc()).all()
    bookings_data = []
    
    for booking in bookings:
        spot = ParkingSpot.query.get(booking.spot_id)
        lot = ParkingLot.query.get(booking.lot_id)
        
        bookings_data.append({
            'id': str(booking.id),
            'lot_name': lot.name,
            'spot_number': spot.spot_number,
            'vehicle_number': booking.vehicle_number,
            'start_time': format_ist_datetime(booking.start_time),
            'end_time': format_ist_datetime(booking.end_time),
            'duration_hours': booking.duration_hours,
            'total_cost': booking.total_cost,
            'status': booking.status
        })
    
    return jsonify(bookings_data)

@app.route('/api/users', methods=['GET'])
def get_users():
    users = User.query.all()
    users_data = []
    
    for user in users:
        bookings_count = Booking.query.filter_by(user_id=user.id).count()
        active_bookings = Booking.query.filter_by(user_id=user.id, status='active').count()
        
        users_data.append({
            'id': str(user.id),
            'email': user.email,
            'fullname': user.fullname,
            'address': user.address,
            'pin_code': user.pin_code,
            'created_at': format_ist_datetime(user.created_at),
            'bookings_count': bookings_count,
            'active_bookings': active_bookings
        })
    
    return jsonify(users_data)

@app.route('/api/analytics', methods=['GET'])
def get_analytics():
    cache_key = 'analytics_data'
    cached_data = get_from_cache(cache_key)
    if cached_data:
        return jsonify(cached_data)
    
    # Calculate analytics
    total_lots = ParkingLot.query.count()
    total_spots = db.session.query(db.func.sum(ParkingLot.total_spots)).scalar() or 0
    occupied_spots = ParkingSpot.query.filter_by(status='occupied').count()
    total_bookings = Booking.query.count()
    active_bookings = Booking.query.filter_by(status='active').count()
    total_revenue = db.session.query(db.func.sum(Booking.total_cost)).filter_by(status='completed').scalar() or 0
    
    occupancy_rate = (occupied_spots / total_spots * 100) if total_spots > 0 else 0
    
    # Revenue by month (last 6 months) - using IST
    revenue_data = []
    current_time = get_ist_naive()
    for i in range(6):
        month_start = current_time.replace(day=1) - timedelta(days=30*i)
        month_end = month_start + timedelta(days=30)
        
        month_revenue = db.session.query(db.func.sum(Booking.total_cost)).filter(
            Booking.status == 'completed',
            Booking.start_time >= month_start,
            Booking.start_time < month_end
        ).scalar() or 0
        
        revenue_data.append({
            'month': month_start.strftime('%b %Y'),
            'revenue': month_revenue
        })
    
    revenue_data.reverse()
    
    analytics_data = {
        'total_lots': total_lots,
        'total_spots': total_spots,
        'occupied_spots': occupied_spots,
        'occupancy_rate': round(occupancy_rate, 1),
        'total_bookings': total_bookings,
        'active_bookings': active_bookings,
        'total_revenue': round(total_revenue, 2),
        'revenue_by_month': revenue_data,
        'timezone': 'Asia/Kolkata (IST)',
        'last_updated': format_ist_datetime(current_time)
    }
    
    # Cache for 5 minutes
    set_cache(cache_key, analytics_data, 300)
    return jsonify(analytics_data)

# Initialize database
def create_tables():
    with app.app_context():
        db.create_all()
        
        # Create admin role if not exists
        admin_role = Role.query.filter_by(name='admin').first()
        if not admin_role:
            admin_role = Role(name='admin', description='Administrator')
            db.session.add(admin_role)
            db.session.commit()
        
        # Create sample data if database is empty
        if ParkingLot.query.count() == 0:
            # Bangalore-specific parking lots
            current_time = get_ist_naive()
            lots_data = [
                {
                    'name': 'UB City Mall Parking',
                    'location': 'UB City, Vittal Mallya Road',
                    'address': 'UB City Mall, 24, Vittal Mallya Road, KG Halli, Shanthala Nagar, Ashok Nagar, Bengaluru, Karnataka 560001',
                    'total_spots': 120,
                    'price_per_hour': 40.0
                },
                {
                    'name': 'Brigade Road Shopping Complex',
                    'location': 'Brigade Road, Central Bangalore',
                    'address': 'Brigade Road, Shanthala Nagar, Ashok Nagar, Bengaluru, Karnataka 560025',
                    'total_spots': 80,
                    'price_per_hour': 30.0
                },
                {
                    'name': 'Indiranagar Metro Station Parking',
                    'location': 'Indiranagar, East Bangalore',
                    'address': 'Indiranagar Metro Station, 100 Feet Road, Indiranagar, Bengaluru, Karnataka 560038',
                    'total_spots': 150,
                    'price_per_hour': 25.0
                },
                {
                    'name': 'Koramangala Forum Mall',
                    'location': 'Koramangala, South Bangalore',
                    'address': 'Forum Mall, 21, Hosur Road, Adugodi, Bengaluru, Karnataka 560030',
                    'total_spots': 200,
                    'price_per_hour': 35.0
                },
                {
                    'name': 'Electronic City Tech Park',
                    'location': 'Electronic City, South Bangalore',
                    'address': 'Electronic City Phase 1, Hosur Road, Bengaluru, Karnataka 560100',
                    'total_spots': 300,
                    'price_per_hour': 20.0
                },
                {
                    'name': 'Whitefield IT Hub Parking',
                    'location': 'Whitefield, East Bangalore',
                    'address': 'ITPL Main Road, Whitefield, Bengaluru, Karnataka 560066',
                    'total_spots': 250,
                    'price_per_hour': 25.0
                },
                {
                    'name': 'Malleshwaram Shopping District',
                    'location': 'Malleshwaram, North Bangalore',
                    'address': 'Sampige Road, Malleshwaram, Bengaluru, Karnataka 560003',
                    'total_spots': 60,
                    'price_per_hour': 30.0
                },
                {
                    'name': 'Jayanagar 4th Block Complex',
                    'location': 'Jayanagar, South Bangalore',
                    'address': '4th Block, Jayanagar, Bengaluru, Karnataka 560011',
                    'total_spots': 90,
                    'price_per_hour': 25.0
                }
            ]
            
            for lot_data in lots_data:
                lot = ParkingLot(
                    name=lot_data['name'],
                    location=lot_data['location'],
                    address=lot_data['address'],
                    total_spots=lot_data['total_spots'],
                    available_spots=lot_data['total_spots'],
                    price_per_hour=lot_data['price_per_hour'],
                    created_at=current_time
                )
                db.session.add(lot)
                db.session.flush()
                
                # Create spots for each lot
                for i in range(1, lot_data['total_spots'] + 1):
                    spot = ParkingSpot(
                        lot_id=lot.id,
                        spot_number=f"{i:03d}",
                        status='available'
                    )
                    db.session.add(spot)
            
            db.session.commit()

if __name__ == '__main__':
    create_tables()
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug)