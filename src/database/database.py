import psycopg2
import os
import ast
from dotenv import load_dotenv

load_dotenv()

connection = psycopg2.connect(**ast.literal_eval(os.getenv("DB_CONNECT")))
cursor = connection.cursor()
cursor.execute("SELECT * from cars;")
    
# Fetch all rows from database
record = cursor.fetchall()

print("Data from Database:- ", record)