import mysql.connector
import pandas as pd
from mysql.connector import Error

#Read CSV file using pandas
try:
    print("Reading CSV file...")
    datafile = pd.read_csv('Annual_expense.csv')
    print("CSV file read successfully.")
    #print(datafile.head())
except Exception as e:
    print(f"Error reading CSV: {e}")

try:
# Establish a connection to MySQL
    mydb = mysql.connector.connect(
    host="localhost",         # MySQL server address (use 'localhost' for local server)
    user="root",              # Your MySQL username
    password="Password7",  # Your MySQL password
    database="expense_db"   # Name of the database you want to connect to (optional)
    )
    print("Connection attempt complete.")

   
    # Create a cursor object to interact with the database 
    
    if mydb.is_connected():
        mycursor = mydb.cursor()
        print("Successfully connected to the database")
    
    # Insert data into MySQL
        for i, row in datafile.iterrows():
            # Define SQL INSERT query
            query = """INSERT INTO expenses (date, category, amount, description, payment_mode, cashback)
                       VALUES (%s, %s, %s, %s, %s, %s)"""
            # Prepare data tuple from DataFrame row
            data = (row['date'], row['category'], row['amount'], row['description'], row['payment_mode'], row['cashback'])
            
            # Execute query
            mycursor.execute(query, data)
        
        # Commit changes to the database
        mydb.commit()
        print(f"{mycursor.rowcount} records inserted successfully")
    else:
        print("not connected!")
   # Create a cursor object to interact with the database
except mysql.connector.Error as e:
    print(f"MySQL Error: {e}")
except Error as e:
    print(f'Error: {e}')

finally:
    #closing the connection
    print("closed")
    if mydb.is_connected():
        mycursor.close()
        mydb.close()
        print("MySql connection is closed!")