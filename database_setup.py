import sqlite3

# Connect to SQLite database (it will create a file called ids_system.db)
conn = sqlite3.connect('ids_system.db')

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

# Create table for service requests
cursor.execute('''
CREATE TABLE IF NOT EXISTS service_requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    org_name TEXT NOT NULL,
    cust_name TEXT NOT NULL,
    role TEXT NOT NULL,
    service_needed TEXT NOT NULL,
    problem_desc TEXT NOT NULL,
    status TEXT DEFAULT 'Pending'
)
''')

# Commit changes and close connection
conn.commit()
conn.close()

print("Database and table created successfully!")
