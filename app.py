from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import pyodbc
import sqlite3
import google.generativeai as genai

#Configure API Key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-pro")
def get_gemini_response(question, prompt):
    config = {
        "max_output_tokens": 2048,
        "temperature": 0.5,
        "top_p": 1
    }
    response = model.generate_content([prompt, question])
    return response.text

## Function to retrieve query from the database
