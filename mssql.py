import pyodbc
import os
from dotenv import load_dotenv
load_dotenv()

# Connection parameters
server = 'Karnika'
database = 'AdventureWorks2017'
username = 'pyodbc_conn'
password = os.getenv("PASSWORD")

# Create a connection string
connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'

# Establish a connection
try:
    connection = pyodbc.connect(connection_string)
    cursor = connection.cursor()

    # Execute SQL queries or commands here
    cursor.execute('SELECT TOP 5 * FROM dbo.Employees')
    rows = cursor.fetchall()
    for row in rows:
        print(row)

except Exception as e:
    print(f"Error: {e}")

finally:
    # Close the connection
    if connection:
        connection.close()

