import logging
logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout = 'wide')

SideBarLinks()

st.title('Add Product Page')

st.write('\n\n')

# Create a Streamlit form widget
with st.form("add_product_form"):
    
    # Create the various input widgets needed for 
    # each piece of information you're eliciting from the user
    product_name = st.text_input("Product Name")
    product_description = st.text_area("Product Description")
    product_price = st.number_input("Product Price", min_value=0.0, step=0.01)
    product_category = st.text_input("Product Category")
    
    # Add the submit button (which every form needs)
    submit_button = st.form_submit_button("Add Product")
    
    if submit_button:
        
        # Package the data up that the user entered into 
        # a dictionary (which is just like JSON in this case)
        product_data = {
            "product_name": product_name,
            "product_description": product_description,
            "product_price": product_price,
            "product_category": product_category
        }
        
        # printing out the data - will show up in the Docker Desktop logs tab
        # for the web-app container 
        logger.info(f"Product form submitted with data: {product_data}")
        
        # Now, we try to make a POST request to the proper end point
        try:
            # using the requests library to POST to /p/product.  Passing
            # product_data to the endpoint through the json parameter.
            # This particular end point is located in the products_routes.py
            # file found in api/backend/products folder. 
            response = requests.post('http://api:4000/p/product', json=product_data)
            if response.status_code == 200:
                st.success("Product added successfully!")
            else:
                st.error(f"Error adding product: {response.text}")
        except requests.exceptions.RequestException as e:
            st.error(f"Error connecting to server: {str(e)}")
