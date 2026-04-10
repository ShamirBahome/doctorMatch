# Database setup and seeding with doctor data

import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('doctors.db')
c = conn.cursor()

# Create table
c.execute('''CREATE TABLE IF NOT EXISTS doctors (
             id INTEGER PRIMARY KEY,
             name TEXT NOT NULL,
             specialty TEXT NOT NULL,
             experience INTEGER NOT NULL,
             details TEXT
         )''')

# Example doctor data
 doctors = [
    (1, 'Dr. John Smith', 'Cardiology', 10, 'Experienced cardiologist'),
    (2, 'Dr. Jane Doe', 'Dermatology', 8, 'Skilled dermatologist'),
    (3, 'Dr. Alice Brown', 'Pediatrics', 5, 'Child specialist')
 ]

# Insert data
c.executemany('INSERT INTO doctors VALUES (?, ?, ?, ?, ?)', doctors)

# Commit the transaction and close the connection
conn.commit()
conn.close()