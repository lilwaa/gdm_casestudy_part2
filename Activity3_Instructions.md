
# Activity 3: Database Schema Implementation

> **Activity Goal:** Design and implement SQLite database schema that supports American Diabetes Association (ADA) monitoring requirements and all persona needs.

---

## Clinical Requirements (ADA Guidelines)

**Required Daily Monitoring:**
- Fasting glucose (upon waking)
- Post-meal glucose (2 hours after breakfast, lunch, dinner)
- **Minimum: 4 readings per day**

**Additional Tracking:**
- Diet logs with carbohydrate estimates
- Physical activity
- Weight (weekly)
- Medication/insulin doses
- Symptoms

---

## Step 1: Review Starter Schema

We've provided 3 core tables to get you started. **Your task:** Add fields and create 2+ additional tables.

### Table 1: `users` (Authentication)

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    profile_type TEXT NOT NULL CHECK(profile_type IN ('patient', 'provider', 'asha')),
    name TEXT NOT NULL,
    phone TEXT,
    language_preference TEXT DEFAULT 'ml' CHECK(language_preference IN ('en', 'ml', 'hi')),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_login DATETIME
);
```

**What's here:**
- Basic authentication (email/password)
- Profile types (patient, provider, ASHA worker)
- Language support (English, Malayalam, Hindi)

**Question for you:** What other user fields are needed? 
whether they are technically flent, have a smartphone
---

### Table 2: `patients` (GDM-Specific Data)

```sql
CREATE TABLE patients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL UNIQUE,
    due_date DATE NOT NULL,
    diagnosis_date DATE NOT NULL,
    gestational_age_weeks INTEGER NOT NULL,
    kerala_region TEXT,
    pre_pregnancy_weight_kg REAL,
    height_cm REAL,
    family_history_diabetes BOOLEAN DEFAULT 0,
    insulin_prescribed BOOLEAN DEFAULT 0,
    target_fasting_glucose REAL DEFAULT 95.0,
    target_postmeal_glucose REAL DEFAULT 120.0,
    assigned_provider_id INTEGER,
    assigned_asha_id INTEGER,
    
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (assigned_provider_id) REFERENCES providers(id),
    FOREIGN KEY (assigned_asha_id) REFERENCES providers(id)
);
```

**What's here:**
- Link to user account
- Clinical data (diagnosis, due date, gestational age)
- Glucose targets
- Provider assignments

**YOUR TURN:** What fields from your personas are missing?

- **Urban Priya** needs: whether they live with family, how many times they have been pregnant before, employment status, who cooks
- **Rural Lakshmi** needs: whether they live with family, how many times they have been pregnant before, employment status, who cooks

Add them below:

```sql
INSERT INTO patients(live_with, times_pregnant, employment, cooks_meals)
-- ex. STRING, INT, STRING, BOOL
```

---

### Table 3: `glucose_readings` (Per ADA: 4+ readings/day)

```sql
CREATE TABLE glucose_readings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER NOT NULL,
    reading_value REAL NOT NULL,
    timestamp DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    reading_type TEXT NOT NULL CHECK(reading_type IN (
        'fasting', 
        'post_breakfast', 
        'post_lunch', 
        'post_dinner', 
        'bedtime'
    )),
    meal_context TEXT,
    carbs_estimated REAL,
    notes TEXT,
    flagged_high BOOLEAN DEFAULT 0,
    flagged_low BOOLEAN DEFAULT 0,
    
    FOREIGN KEY (patient_id) REFERENCES patients(id)
);
```

**What's here:**
- All glucose readings with timestamps
- Reading types (fasting, post-meal, bedtime)
- Meal context and carbs
- Automatic flags for high/low readings

**YOUR TURN:** What additional fields would help your personas?

```sql
-- TODO: Add your fields here
```

---

## Step 2: Design Additional Tables

Based on your personas and user stories, you need to create at least 2 more tables. Here are suggestions:

### Table 4: Create This One! (Choose One)

**Option A: `chat_messages`** (For chatbot conversations)
```sql
CREATE TABLE chat_messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER NOT NULL,
    message_text TEXT NOT NULL,
    is_from_bot BOOLEAN NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    -- TODO: What else should we track?
    
    FOREIGN KEY (patient_id) REFERENCES patients(id)
);
```

**Option B: `diet_logs`** (For meal tracking)
```sql
CREATE TABLE diet_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    meal_type TEXT CHECK(meal_type IN ('breakfast', 'lunch', 'dinner', 'snack')),
    -- TODO: What fields describe a meal?
    -- Example: food_items TEXT, total_carbs REAL
    
    FOREIGN KEY (patient_id) REFERENCES patients(id)
);
```

**YOUR TURN:** Design this table fully. Add all fields needed.

---

### Table 5: Create This One! (Choose One)

**Option A: `providers`** (Healthcare workers)
```sql
CREATE TABLE providers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL UNIQUE,
    provider_type TEXT NOT NULL CHECK(provider_type IN ('obgyn', 'endocrinologist', 'asha')),
    -- TODO: Add fields for facility, license, service area
    
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

**Option B: `appointments`** (Track clinic visits)
```sql
CREATE TABLE appointments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER NOT NULL,
    provider_id INTEGER NOT NULL,
    appointment_date DATETIME NOT NULL,
    -- TODO: Add fields for status, notes, type
    
    FOREIGN KEY (patient_id) REFERENCES patients(id),
    FOREIGN KEY (provider_id) REFERENCES providers(id)
);
```

**YOUR TURN:** Design this table fully.

---

## Step 3: Implement in SQLite

Now let's create the actual database!

### Create `schema.sql`

In your repo, create `database/schema.sql` with:

```sql
-- GDM Chatbot Database Schema
-- Created: [Your Date]

-- Table 1: Users (Authentication)
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    profile_type TEXT NOT NULL CHECK(profile_type IN ('patient', 'provider', 'asha')),
    name TEXT NOT NULL,
    phone TEXT,
    language_preference TEXT DEFAULT 'ml' CHECK(language_preference IN ('en', 'ml', 'hi')),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_login DATETIME
);

-- Table 2: Patients (GDM-Specific)
CREATE TABLE patients (
    -- COPY FROM ABOVE AND ADD YOUR FIELDS
);

-- Table 3: Glucose Readings
CREATE TABLE glucose_readings (
    -- COPY FROM ABOVE AND ADD YOUR FIELDS
);

-- Table 4: [Your Choice]
CREATE TABLE __________ (
    -- YOUR DESIGN HERE
);

-- Table 5: [Your Choice]
CREATE TABLE __________ (
    -- YOUR DESIGN HERE
);
```

### Initialize Database

```bash
# In your terminal
cd database
sqlite3 gdm_chatbot.db < schema.sql
```

### Verify It Worked

```bash
sqlite3 gdm_chatbot.db

# In SQLite shell:
.tables
# Should show: users, patients, glucose_readings, ...

.schema users
# Should show your users table structure
```

---

## Step 4: Add Sample Data

Create `database/sample_data.sql`:

```sql
-- Sample Users
INSERT INTO users (email, password_hash, profile_type, name, language_preference)
VALUES 
    ('priya@example.com', 'hashed_password_1', 'patient', 'Priya M.', 'en'),
    ('lakshmi@example.com', 'hashed_password_2', 'patient', 'Lakshmi R.', 'ml'),
    ('dr.sarah@hospital.gov.in', 'hashed_password_3', 'provider', 'Dr. Sarah Thomas', 'en');

-- Sample Patients
INSERT INTO patients (user_id, due_date, diagnosis_date, gestational_age_weeks, kerala_region)
VALUES
    (1, '2026-06-15', '2026-01-10', 24, 'Ernakulam'),
    (2, '2026-07-20', '2025-12-20', 28, 'Wayanad');

-- Sample Glucose Readings
INSERT INTO glucose_readings (patient_id, reading_value, reading_type, timestamp)
VALUES
    (1, 92.0, 'fasting', '2026-01-29 07:00:00'),
    (1, 118.0, 'post_breakfast', '2026-01-29 10:00:00'),
    (2, 105.0, 'fasting', '2026-01-29 08:00:00');

-- TODO: Add sample data for your tables
```

Load it:
```bash
sqlite3 gdm_chatbot.db < sample_data.sql
```

---

## Step 5: Test Queries

Make sure your schema supports these queries:

```sql
-- Can we find all patients assigned to a provider?
SELECT p.name, pt.due_date 
FROM patients pt
JOIN users p ON pt.user_id = p.id
WHERE pt.assigned_provider_id = 1;

-- Can we get all glucose readings for a patient in the last 7 days?
SELECT reading_value, reading_type, timestamp
FROM glucose_readings
WHERE patient_id = 1 
AND timestamp >= datetime('now', '-7 days')
ORDER BY timestamp DESC;

-- Can we identify patients with high readings?
SELECT DISTINCT u.name, u.phone
FROM users u
JOIN patients pt ON pt.user_id = u.id
JOIN glucose_readings gr ON gr.patient_id = pt.id
WHERE gr.flagged_high = 1
AND gr.timestamp >= datetime('now', '-24 hours');
```

**YOUR TURN:** Write 2 more queries that your personas need:

```sql
-- Query 1: _______________________________
-- TODO: Write query

-- Query 2: _______________________________
-- TODO: Write query
```

---

## Step 6: Connect to Flask

In your Flask app, connect to the database:

```python
# app.py
import sqlite3
from flask import Flask, g

app = Flask(__name__)
DATABASE = 'database/gdm_chatbot.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row  # Access columns by name
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Example: Get all patients
@app.route('/patients')
def get_patients():
    db = get_db()
    patients = db.execute('SELECT * FROM patients').fetchall()
    return {'patients': [dict(p) for p in patients]}
```

---

## Checklist: Is Your Schema Complete?

Before finishing, verify:

**Supports ADA Requirements:**
- [ ] Can store 4+ glucose readings per day
- [ ] Tracks fasting and post-meal separately
- [ ] Records timestamps for all readings
- [ ] Links readings to patients

**Supports Persona Needs:**

**Urban Priya:**
- [ ] Can set notification preferences
- [ ] Stores meal context for tracking
- [ ] Links to provider for data sharing

**Rural Lakshmi:**
- [ ] Language preference stored
- [ ] Links to ASHA worker for support
- [ ] Simple data entry supported

**Dr. Sarah:**
- [ ] Can query patients by provider
- [ ] Can identify high-risk readings
- [ ] Tracks patient compliance

**Technical:**
- [ ] All tables have primary keys
- [ ] Foreign keys properly reference other tables
- [ ] CHECK constraints prevent invalid data
- [ ] Sample data loads without errors
- [ ] Test queries work

---

## Deliverables

By end of activity:

1. `database/schema.sql` - Complete schema with all tables
2. `database/sample_data.sql` - Sample data for testing
3. `database/gdm_chatbot.db` - Initialized database file
4. Screenshots or output showing:
   - `.tables` command results
   - Sample query results

**Add these files to your repo and push to GitHub!**

---

## Next Steps

In next week's lecture, we'll build on this simple Flask app and implement some features to make it a minimum viable product (MVP).

Your schema is the foundation for everything we build!