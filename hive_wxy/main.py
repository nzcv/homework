import csv

import mysql.connector

# MySQL connection configuration
config = {
    'user': 'root',
    'password': '1234',
    'host': 'localhost',
    'database': 'test'
}

# Connect to MySQL
conn = mysql.connector.connect(**config)
cursor = conn.cursor()

# Create table if not exists
create_table_query = """
CREATE TABLE IF NOT EXISTS sales_prediction (
    product_id INT,
    price FLOAT,
    discount FLOAT,
    season VARCHAR(20),
    promotion VARCHAR(5),
    quantity_sold_last_quarter INT,
    stock_quantity INT,
    rating FLOAT,
    reviews_count INT,
    category VARCHAR(50),
    sales_forecast INT
)
"""
cursor.execute(create_table_query)

# Read CSV file and insert data into MySQL
csv_file_path = './sales_prediction_data.csv'
with open(csv_file_path, mode='r') as file:
    csv_reader = csv.reader(file)
    next(csv_reader)  # Skip header row
    for row in csv_reader:
        insert_query = """
        INSERT INTO sales_prediction (
            product_id, price, discount, season, promotion, quantity_sold_last_quarter, 
            stock_quantity, rating, reviews_count, category, sales_forecast
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, row)

# Commit the transaction
conn.commit()

# Close the connection
cursor.close()
conn.close()