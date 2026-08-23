import sqlite3

# Connect to database
conn = sqlite3.connect("company.db")
cursor = conn.cursor()

# Delete old table if it exists
cursor.execute("DROP TABLE IF EXISTS sales")

# Create new enterprise sales table
cursor.execute("""
CREATE TABLE sales(
    order_id INTEGER PRIMARY KEY,
    order_date TEXT,
    customer_name TEXT,
    region TEXT,
    city TEXT,
    salesperson TEXT,
    product TEXT,
    category TEXT,
    quantity INTEGER,
    unit_price REAL,
    discount REAL,
    revenue REAL,
    cost REAL,
    profit REAL,
    payment_mode TEXT,
    customer_rating INTEGER
)
""")

conn.commit()
conn.close()

print("Enterprise Sales Database Created Successfully!")
