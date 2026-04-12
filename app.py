from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
from flask_cors import CORS
from models import db, bcrypt, Doctor, User, Review, WalkinClinic
from config import Config
from seed_data import seed_database
from functools import wraps
from datetime import datetime

# ==========================================
# CREATE APP
# ==========================================
app = Flask(__name__)
app.config.from_object(Config)
CORS(app)
db.init_app(app)
bcrypt.init_app(app)

with app.app_context():
    db.create_all()
    print("✅ Database ready!")


# ==========================================
# HELPERS
# ==========================================
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in first.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated


def get_current_user():
    if 'user_id' in session:
        return User.query.get(session['user_id'])
    return None


@app.context_processor
def inject_user():
    return {'current_user': get_current_user()}


# ==========================================
# PAGE ROUTES
# ==========================================

@app.route('/')
def home():
    total_doctors = Doctor.query.count()
    accepting_count = Doctor.query.filter_by(accepting_new_patients=True).count()
    total_reviews = Review.query.count()
    total_clinics = WalkinClinic.query.count()
    featured = Doctor.query.filter_by(accepting_new_patients=True).limit(3).all()

    return render_template('index.html',
                           total_doctors=total_doctors,
                           accepting_count=accepting_count,
                           total_reviews=total_reviews,
                           total_clinics=total_clinics,
                           featured_doctors=featured)


@app.route('/search')
def search():
    accepting = request.args.get('accepting', '') == 'true'
    language = request.args.get('language', '')
    gender = request.args.get('gender', '')
    query_text = request.args.get('q', '')
    sort_by = request.args.get('sort', 'default')

    query = Doctor.query

    if accepting:
        query = query.filter_by(accepting_new_patients=True)
    if gender:
        query = query.filter_by(gender=gender)
    if language:
        query = query.filter(Doctor.languages.ilike(f'%{language}%'))
    if query_text:
        s = f"%{query_text}%"
        query = query.filter(
            db.or_(
                Doctor.first_name.ilike(s),
                Doctor.last_name.ilike(s),
                Doctor.clinic_name.ilike(s),
                Doctor.address.ilike(s),
            )
        )

    if sort_by == 'name':
        query = query.order_by(Doctor.last_name.asc())
    elif sort_by == 'experience':
        query = query.order_by(Doctor.years_of_experience.desc())
    else:
        query = query.order_by(Doctor.accepting_new_patients.desc())

    doctors = query.all()

    all_languages = set()
    for doc in Doctor.query.all():
        for lang in doc.languages_list:
            all_languages.add(lang)

    return render_template('search.html',
                           doctors=doctors,
                           total_results=len(doctors),
                           all_languages=sorted(all_languages),
                           filters={
                               'accepting': accepting,
                               'language': language,
                               'gender': gender,
                               'q': query_text,
                               'sort': sort_by,
                           })


@app.route('/doctor/<int:doctor_id>')
def doctor_profile(doctor_id):
    doctor = Doctor.query.get_or_404(doctor_id)
    reviews = Review.query.filter_by(doctor_id=doctor_id).order_by(Review.created_at.desc()).all()

    rating_dist = {5: 0, 4: 0, 3: 0, 2: 0, 1: 0}
    for review in reviews:
        rating_dist[review.rating] += 1

    return render_template('doctor_profile.html',
                           doctor=doctor,
                           reviews=reviews,
                           rating_distribution=rating_dist)


@app.route('/walkin-clinics')
def walkin_clinics():
    clinics = WalkinClinic.query.order_by(WalkinClinic.current_wait_minutes.asc()).all()
    return render_template('walkin_clinics.html', clinics=clinics)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm = request.form.get('confirm_password', '')
        first_name = request.form.get('first_name', '').strip()
        last_name = request.form.get('last_name', '').strip()

        if not email or not password or not first_name:
            flash('Please fill in all required fields.', 'error')
            return render_template('register.html')

        if password != confirm:
            flash('Passwords do not match.', 'error')
            return render_template('register.html')

        if len(password) < 6:
            flash('Password must be at least 6 characters.', 'error')
            return render_template('register.html')

        if User.query.filter_by(email=email).first():
            flash('Email already registered.', 'error')
            return render_template('register.html')

        user = User(email=email, first_name=first_name, last_name=last_name)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        session['user_id'] = user.id
        flash(f'Welcome, {first_name}!', 'success')
        return redirect(url_for('home'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            session['user_id'] = user.id
            flash(f'Welcome back, {user.first_name}!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid email or password.', 'error')

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Logged out successfully.', 'info')
    return redirect(url_for('home'))


@app.route('/seed')
def seed():
    seed_database()
    flash('Sample data added!', 'success')
    return redirect(url_for('home'))


# ==========================================
# API ROUTES
# ==========================================

@app.route('/api/doctors')
def api_doctors():
    doctors = Doctor.query.all()
    return jsonify({'success': True, 'data': [d.to_dict() for d in doctors]})


@app.route('/api/doctors/<int:doctor_id>')
def api_doctor(doctor_id):
    doctor = Doctor.query.get_or_404(doctor_id)
    data = doctor.to_dict()
    data['reviews'] = [r.to_dict() for r in doctor.reviews]
    return jsonify({'success': True, 'data': data})


@app.route('/api/reviews', methods=['POST'])
def api_add_review():
    data = request.json
    if not data:
        return jsonify({'success': False, 'error': 'No data'}), 400

    doctor_id = data.get('doctor_id')
    rating = data.get('rating')

    if not doctor_id or not rating:
        return jsonify({'success': False, 'error': 'Missing fields'}), 400

    user_id = session.get('user_id', 1)

    review = Review(
        doctor_id=int(doctor_id),
        user_id=user_id,
        rating=int(rating),
        title=data.get('title', ''),
        comment=data.get('comment', ''),
    )
    db.session.add(review)
    db.session.commit()

    return jsonify({'success': True, 'message': 'Review added!'})


@app.route('/api/walkin-clinics')
def api_clinics():
    clinics = WalkinClinic.query.all()
    return jsonify({'success': True, 'data': [c.to_dict() for c in clinics]})

# ==========================================
# ADMIN ROUTES
# ==========================================

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        user = get_current_user()
        if not user or not user.is_admin:
            flash('Admin access required.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated


@app.route('/admin')
@admin_required
def admin_dashboard():
    stats = {
        'total_doctors': Doctor.query.count(),
        'accepting_doctors': Doctor.query.filter_by(accepting_new_patients=True).count(),
        'total_users': User.query.count(),
        'total_reviews': Review.query.count(),
    }
    doctors = Doctor.query.order_by(Doctor.last_name).all()
    reviews = Review.query.order_by(Review.created_at.desc()).all()
    users = User.query.order_by(User.created_at.desc()).all()

    return render_template('admin.html',
                           stats=stats,
                           doctors=doctors,
                           reviews=reviews,
                           users=users)


@app.route('/admin/add-doctor', methods=['POST'])
@admin_required
def admin_add_doctor():
    doctor = Doctor(
        first_name=request.form.get('first_name'),
        last_name=request.form.get('last_name'),
        gender=request.form.get('gender'),
        phone=request.form.get('phone'),
        clinic_name=request.form.get('clinic_name'),
        address=request.form.get('address'),
        postal_code=request.form.get('postal_code'),
        cpso_number=request.form.get('cpso_number') or None,
        languages=request.form.get('languages', 'English'),
        specializations=request.form.get('specializations', 'Family Medicine'),
        education=request.form.get('education'),
        years_of_experience=request.form.get('years_of_experience', type=int),
        wait_time_weeks=request.form.get('wait_time_weeks', type=int),
        accepting_new_patients=request.form.get('accepting_new_patients') == 'true',
    )
    db.session.add(doctor)
    db.session.commit()
    flash(f'{doctor.full_name} added successfully!', 'success')
    return redirect(url_for('admin_dashboard'))


@app.route('/admin/edit/<int:doctor_id>', methods=['GET', 'POST'])
@admin_required
def admin_edit_doctor(doctor_id):
    doctor = Doctor.query.get_or_404(doctor_id)

    if request.method == 'POST':
        doctor.first_name = request.form.get('first_name')
        doctor.last_name = request.form.get('last_name')
        doctor.gender = request.form.get('gender')
        doctor.phone = request.form.get('phone')
        doctor.clinic_name = request.form.get('clinic_name')
        doctor.address = request.form.get('address')
        doctor.postal_code = request.form.get('postal_code')
        doctor.cpso_number = request.form.get('cpso_number') or doctor.cpso_number
        doctor.languages = request.form.get('languages', 'English')
        doctor.specializations = request.form.get('specializations', 'Family Medicine')
        doctor.education = request.form.get('education')
        doctor.years_of_experience = request.form.get('years_of_experience', type=int)
        doctor.wait_time_weeks = request.form.get('wait_time_weeks', type=int)
        doctor.accepting_new_patients = request.form.get('accepting_new_patients') == 'true'
        doctor.updated_at = datetime.utcnow()

        db.session.commit()
        flash(f'{doctor.full_name} updated successfully!', 'success')
        return redirect(url_for('admin_dashboard'))

    return render_template('admin_edit.html', doctor=doctor)


@app.route('/api/admin/toggle-status', methods=['POST'])
@admin_required
def api_toggle_status():
    data = request.json
    doctor = Doctor.query.get(data.get('doctor_id'))
    if not doctor:
        return jsonify({'success': False, 'error': 'Doctor not found'}), 404

    doctor.accepting_new_patients = data.get('accepting')
    doctor.updated_at = datetime.utcnow()
    db.session.commit()
    return jsonify({'success': True, 'message': 'Status updated!'})


@app.route('/api/admin/delete-doctor/<int:doctor_id>', methods=['DELETE'])
@admin_required
def api_delete_doctor(doctor_id):
    doctor = Doctor.query.get(doctor_id)
    if not doctor:
        return jsonify({'success': False, 'error': 'Doctor not found'}), 404

    db.session.delete(doctor)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Doctor deleted!'})


@app.route('/api/admin/delete-review/<int:review_id>', methods=['DELETE'])
@admin_required
def api_delete_review(review_id):
    review = Review.query.get(review_id)
    if not review:
        return jsonify({'success': False, 'error': 'Review not found'}), 404

    db.session.delete(review)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Review deleted!'})


@app.route('/create-admin')
def create_admin():
    existing = User.query.filter_by(email='admin@guelphdoctorfinder.ca').first()
    if existing:
        flash('Admin account already exists!', 'warning')
        return redirect(url_for('home'))

    admin = User(
        email='admin@guelphdoctorfinder.ca',
        first_name='Admin',
        last_name='Owner',
        is_admin=True,
    )
    admin.set_password('admin123')
    db.session.add(admin)
    db.session.commit()
    flash('Admin account created! Login with admin@guelphdoctorfinder.ca / admin123', 'success')
    return redirect(url_for('login'))


# ==========================================
# RUN APP (THIS MUST BE THE VERY LAST LINE)
# ==========================================
if __name__ == '__main__':
    app.run(debug=True, port=5000)
