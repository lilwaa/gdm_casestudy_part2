"""
GDM Chatbot - Flask Application with Basic Authentication
CS 584 Case Study

This is a starter template. You'll extend it in future lectures.
"""

from flask import Flask, render_template, request, redirect, url_for, session, g
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this'  # Change in production!
DATABASE = 'database/gdm_chatbot.db' # This is your SQLite database file.


# ==================== DATABASE HELPER FUNCTIONS ====================

def get_db():
    """Get database connection"""
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row  # Access columns by name
    return db


@app.teardown_appcontext
def close_connection(exception):
    """Close database connection at end of request"""
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


# ==================== AUTHENTICATION ROUTES ====================

@app.route('/')
def index():
    """Landing page"""
    if 'user_id' in session:
        # User is logged in, redirect to their dashboard
        profile_type = session.get('profile_type')
        if profile_type == 'patient':
            return redirect(url_for('patient_dashboard'))
        elif profile_type == 'provider':
            return redirect(url_for('provider_dashboard'))
        else:
            return redirect(url_for('asha_dashboard'))
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        name = request.form.get('name')
        profile_type = request.form.get('profile_type')
        phone = request.form.get('phone')
        language = request.form.get('language', 'ml')
        
        # TODO: Add validation (email format, password strength, etc.)
        
        # Hash password before storing
        password_hash = generate_password_hash(password)
        
        db = get_db()
        try:
            cursor = db.execute(
                '''INSERT INTO users (email, password_hash, profile_type, name, phone, language_preference)
                   VALUES (?, ?, ?, ?, ?, ?)''',
                (email, password_hash, profile_type, name, phone, language)
            )
            db.commit()
            user_id = cursor.lastrowid
            
            # If patient, create patient record
            if profile_type == 'patient':
                # TODO: Get additional patient info from form
                # For now, create minimal patient record
                db.execute(
                    '''INSERT INTO patients (user_id, due_date, diagnosis_date, gestational_age_weeks)
                       VALUES (?, ?, ?, ?)''',
                    (user_id, '2026-06-01', '2026-01-15', 20)  # Placeholder values
                )
                db.commit()
            
            return redirect(url_for('login'))
            
        except sqlite3.IntegrityError:
            error = 'Email already registered'
            return render_template('register.html', error=error)
    
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        db = get_db()
        user = db.execute(
            'SELECT * FROM users WHERE email = ?',
            (email,)
        ).fetchone()
        
        if user and check_password_hash(user['password_hash'], password):
            # Login successful
            session['user_id'] = user['id']
            session['profile_type'] = user['profile_type']
            session['name'] = user['name']
            session['language'] = user['language_preference']
            
            # Update last login
            db.execute(
                'UPDATE users SET last_login = ? WHERE id = ?',
                (datetime.now(), user['id'])
            )
            db.commit()
            
            # Redirect based on profile type
            if user['profile_type'] == 'patient':
                return redirect(url_for('patient_dashboard'))
            elif user['profile_type'] == 'provider':
                return redirect(url_for('provider_dashboard'))
            else:
                return redirect(url_for('asha_dashboard'))
        else:
            error = 'Invalid email or password'
            return render_template('login.html', error=error)
    
    return render_template('login.html')


@app.route('/logout')
def logout():
    """User logout"""
    session.clear()
    return redirect(url_for('index'))


# ==================== PATIENT DASHBOARD ====================

@app.route('/patient/dashboard')
def patient_dashboard():
    """Patient dashboard - shows glucose data, chat, etc."""
    if 'user_id' not in session or session['profile_type'] != 'patient':
        return redirect(url_for('login'))
    
    db = get_db()
    
    # Get patient info
    patient = db.execute(
        '''SELECT p.*, u.name, u.email, u.language_preference
           FROM patients p
           JOIN users u ON p.user_id = u.id
           WHERE u.id = ?''',
        (session['user_id'],)
    ).fetchone()
    
    # Get recent glucose readings
    readings = db.execute(
        '''SELECT * FROM glucose_readings
           WHERE patient_id = ?
           ORDER BY timestamp DESC
           LIMIT 10''',
        (patient['id'],)
    ).fetchall()
    
    # TODO: Calculate statistics (average glucose, compliance, etc.)
    
    return render_template('patient_dashboard.html', 
                         patient=patient, 
                         readings=readings)


# ==================== PROVIDER DASHBOARD ====================

@app.route('/provider/dashboard')
def provider_dashboard():
    """Provider dashboard - shows all patients, alerts, etc."""
    if 'user_id' not in session or session['profile_type'] != 'provider':
        return redirect(url_for('login'))
    
    # TODO: Implement provider dashboard
    # Should show: list of assigned patients, recent alerts, etc.
    
    return render_template('provider_dashboard.html')


# ==================== ASHA DASHBOARD ====================

@app.route('/asha/dashboard')
def asha_dashboard():
    """ASHA worker dashboard - shows assigned patients in community"""
    if 'user_id' not in session or session['profile_type'] != 'asha':
        return redirect(url_for('login'))
    
    # TODO: Implement ASHA dashboard
    # Should show: list of patients in area, visit schedule, etc.
    
    return render_template('asha_dashboard.html')


# ==================== GLUCOSE LOGGING ====================

@app.route('/patient/log-glucose', methods=['GET', 'POST'])
def log_glucose():
    """Log a glucose reading"""
    if 'user_id' not in session or session['profile_type'] != 'patient':
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        db = get_db()
        
        # Get patient_id from user_id
        patient = db.execute(
            'SELECT id FROM patients WHERE user_id = ?',
            (session['user_id'],)
        ).fetchone()
        
        reading_value = float(request.form.get('reading_value'))
        reading_type = request.form.get('reading_type')
        meal_context = request.form.get('meal_context', '')
        carbs = request.form.get('carbs_estimated', None)
        notes = request.form.get('notes', '')
        
        # TODO: Add validation
        
        # Determine if reading is flagged
        target_fasting = 95.0
        target_postmeal = 120.0
        flagged_high = (reading_type == 'fasting' and reading_value > target_fasting) or \
                      (reading_type != 'fasting' and reading_value > target_postmeal)
        flagged_low = reading_value < 70.0
        
        db.execute(
            '''INSERT INTO glucose_readings 
               (patient_id, reading_value, reading_type, meal_context, 
                carbs_estimated, notes, flagged_high, flagged_low)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
            (patient['id'], reading_value, reading_type, meal_context, 
             carbs, notes, flagged_high, flagged_low)
        )
        db.commit()
        
        return redirect(url_for('patient_dashboard'))
    
    return render_template('log_glucose.html')


# ==================== RUN APPLICATION ====================

if __name__ == '__main__':
    app.run(debug=True)