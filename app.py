from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import pyodbc
import sqlite3
import google.generativeai as genai

# Connection parameters
server = 'KARNIKA\SQLEXPRESS01'
database = 'AdventureWorks2017'
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
prompt1 ="""You are an expert in converting English questions to SQL query!
The SQL database has the name AdventureWorks2017 and the table name is Employees 
under schema dbo and has the following columns - ID, FirstName, LastName, Gender, Salary
For example,\nExample 1 - How many count of records are present?, 
the SQL command will be something like this SELECT COUNT(*) FROM AdventureWorks2017.dbo.Employees;
Example 2 - Tell me person name with the highest salary?, 
the SQL command will be something like this SELECT TOP 1 FirstName, LastName FROM AdventureWorks2017.dbo.Employees order by Salary desc; 
also the sql code should not have ``` in beginning or end and sql word in output. Do not makeup answer, if you are unable to understand
the answer then just say that you do not know the answer. Do not give wrong answers validate once before giving them.
"""

#(To get complex answers like inner join)
prompt ="""You are an expert in converting English questions to SQL query!
The SQL database has the name AdventureWorks2017 and there are two tables named Person & PersonPhone
under schema Person and has the following columns in 
Person table - BusinessEntityID, Title, FirstName, LastName, Demographics, EmailPromotion etc
and 
PersonPhone table - BusinessEntityID, PhoneNumber, where BusinessEntityID is primarykey of Person table & PersonPhone has BusinessEntityID as foreign key
I need your help to write basic to complex queries For example,\nExample 1 - How many count of records are present?, 
the SQL command will be something like this SELECT COUNT(*) FROM AdventureWorks2017.dbo.Employees;
Example 2 - Tell me person name with the highest salary?, 
the SQL command will be something like this SELECT TOP 1 FirstName, LastName FROM AdventureWorks2017.dbo.Employees order by Salary desc; 
also the sql code should not have ``` in beginning or end and sql word in output. Do not makeup answer, if you are unable to understand
the answer then just say that you do not know the answer. Do not give wrong answers validate once before giving them.
"""

## Streamlit App

st.set_page_config(page_title="I can Retrieve Any SQL query")
st.header("Gemini App To Retrieve SQL Data")

question=st.text_input("Input your question: ",key="input")

submit=st.button("Ask the question")

# if submit is clicked
if submit:
    response = get_gemini_response(question, prompt1)
    st.subheader("Generated SQL Query:")
    
    # Display the generated SQL query in an expander
    with st.expander("Click to view"):
        st.write(response)

    # Execute the SQL query and display results
    result = read_sql_query(response, connection_string)
    
    if result is not None:
        st.subheader("The Response is:")
        for row in result:
            # Remove the trailing comma from the tuple and convert it to a string
            row_str = str(row).replace(",", "")
            print(row_str)
            st.header(row_str)
    else:
        st.error("No results found for the query.")

#provide me phonenumber of person FirstName = 'ken' in person.person table by joining it with the  person.personphone table
#provide me count of persons in persons.persons table with the FirstName = 'ken' and lastname as 'Sánchez'
#please provide count of people by persontype in the table person.person, where persontype is a column in this table