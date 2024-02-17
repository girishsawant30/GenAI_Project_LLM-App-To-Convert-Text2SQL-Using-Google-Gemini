from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import pyodbc
import sqlite3
import google.generativeai as genai

# Connection parameters
server = 'Karnika'
database = 'AdventureWorks2022'
username = 'pyodbc_conn'
password = os.getenv("PASSWORD")

# Create a connection string
connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'
print(connection_string)

#Configure API Key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-pro")
def get_gemini_response(question, prompt):
    config = {
        "max_output_tokens": 2048,
        "temperature": 0.5,
        "top_p": 1
    }
    response = model.generate_content([question, prompt])
    return response.text

## Function to retrieve query from the SQL database

def read_sql_query1(sql, db):
    connection = sqlite3.connect(db)
    cursor = connection.cursor()
    cursor.execute(sql)
    rows=cursor.fetchall()
    connection.commit()
    connection.close()
    for row in rows:
        print(row)
    return rows

def read_sql_query(sql, connection_string):
    try:
        #Establish the conn
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()

        #Execute the query
        cursor.execute(sql)
        rows = cursor.fetchall()
        for row in rows:
            print(row)
        return rows
    
    except Exception as e:
        st.error(f"Error: {e}")
        return None

    finally:
        # Close the connection
        if connection:
            connection.close()

## Define Your Prompt
prompt ="""You are an expert in converting English questions to SQL query!
The SQL database has the name AdventureWorks2017 and the table name is Employees 
under schema dbo and has the following columns - ID, FirstName, LastName, Gender, Salary
For example,\nExample 1 - How many count of records are present?, 
the SQL command will be something like this SELECT COUNT(*) FROM AdventureWorks2017.dbo.Employees;
Example 2 - Tell me person name with the highest salary?, 
the SQL command will be something like this SELECT TOP 1 FirstName, LastName FROM AdventureWorks2017.dbo.Employees order by Salary desc; 
also the sql code should not have ``` in beginning or end and sql word in output. Do not makeup answer, if you are unable to understand
the answer then just say that you do not know the answer. Do not give wrong answers validate once before giving them.
"""

## Streamlit App

st.set_page_config(page_title="I can Retrieve Any SQL query")
st.header("Gemini App To Retrieve SQL Data")

question=st.text_input("Input: ",key="input")

submit=st.button("Ask the question")

# if submit is clicked
if submit:
    response = get_gemini_response(question, prompt)
    st.subheader("Generated SQL Query:")
    
    # Display the generated SQL query in an expander
    with st.expander("Click to view"):
        st.write(response)

    # Execute the SQL query and display results
    result = read_sql_query(response, connection_string)
    
    st.subheader("The Response is:")
    for row in result:
        print(row)
        st.header(row)


