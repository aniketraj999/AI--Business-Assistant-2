import sqlite3
import random
from faker import Faker
from datetime import datetime, timedelta

fake = Faker()

conn = sqlite3.connect("company.db")
cursor = conn.cursor()
cursor.execute("DELETE FROM sales")

products = [
    ("Laptop","Electronics",65000),
    ("Mobile","Electronics",30000),
    ("Headphones","Electronics",2500),
    ("Chair","Furniture",4500),
    ("Table","Furniture",7000),
    ("Shoes","Fashion",3500),
    ("T-Shirt","Fashion",1200),
    ("Watch","Accessories",5000),
    ("Backpack","Accessories",2200),
    ("Book","Books",700)
]

regions = ["North","South","East","West"]

cities = {
    "North":["Delhi","Chandigarh","Lucknow"],
    "South":["Bangalore","Chennai","Hyderabad"],
    "East":["Kolkata","Patna","Bhubaneswar"],
    "West":["Mumbai","Pune","Ahmedabad"]
}

salespersons = [
    "Rahul Sharma",
    "Priya Singh",
    "Amit Kumar",
    "Neha Verma",
    "Rohit Mehta",
    "Karan Gupta",
    "Sneha Jain",
    "Arjun Kapoor"
]

payment_modes = [
    "Cash",
    "Credit Card",
    "Debit Card",
    "UPI",
    "Net Banking"
]

start_date = datetime(2025,1,1)

for order_id in range(1,10001):

    order_date = start_date + timedelta(days=random.randint(0,364))

    region = random.choice(regions)

    city = random.choice(cities[region])

    salesperson = random.choice(salespersons)

    customer = fake.name()

    product,category,price = random.choice(products)

    quantity = random.randint(1,8)

    discount = random.randint(0,30)

    revenue = quantity * price * (1-discount/100)

    cost = revenue * random.uniform(0.55,0.80)

    profit = revenue - cost

    rating = random.randint(1,5)

    payment = random.choice(payment_modes)

    cursor.execute("""
    INSERT INTO sales VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """,(
        order_id,
        order_date.strftime("%Y-%m-%d"),
        customer,
        region,
        city,
        salesperson,
        product,
        category,
        quantity,
        price,
        discount,
        round(revenue,2),
        round(cost,2),
        round(profit,2),
        payment,
        rating
    ))

conn.commit()
conn.close()

print("10000 Enterprise Sales Records Generated Successfully!")