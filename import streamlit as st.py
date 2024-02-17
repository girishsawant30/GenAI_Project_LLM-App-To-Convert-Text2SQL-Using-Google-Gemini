import streamlit as st

# Example list
my_list = ['Item 1', 'Item 2', 'Item 3']

# Display the list using st.header
st.header('My List:')
for item in my_list:
    st.write(item)