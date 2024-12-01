import logging
logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout = 'wide')

SideBarLinks()

st.title('Add Product Page')

st.write('\n\n')

# Fetch categories from API
# This has to be outside the form so the list of categories is 
# populated when form is displayed. 
try:
    # Access /p/categories with a GET request
    categories_response = requests.get('http://api:4000/p/categories')
    
    # 200 means the request was successful
    if categories_response.status_code == 200:
        # pull the data from the response object as json
        categories_data = categories_response.json()
        # create a list of categories from the json. The initial [""] is so 
        # there isn't a default category selected in the product category select widget
        category_options = [""] + [category['value'] for category in categories_data]
    else:
        # means we got back some HTTP code besides 200
        st.error("Failed to fetch categories")
        category_options = []
except requests.exceptions.RequestException as e:
    st.error(f"Error connecting to categories API: {str(e)}")
    category_options = []

# Create a Streamlit form widget
with st.form("add_product_form"):
    
    # Create the various input widgets needed for 
    # each piece of information you're eliciting from the user
    product_name = st.text_input("Product Name")
    product_description = st.text_area("Product Description")
    product_price = st.number_input("Product Price", min_value=0.0, step=0.01)
    # Notice here, we are using a selectbox widget.  The options for the 
    # select are provided with the 'options' parameter.
    product_category = st.selectbox("Product Category", options=category_options, index=0)
    
    # Add the submit button (which every form needs)
    submit_button = st.form_submit_button("Add Product")
    
    # Validate all fields are filled when form is submitted
    if submit_button:
        if not product_name:
            st.error("Please enter a product name")
        elif not product_description:
            st.error("Please enter a product description")
        elif product_price <= 0:
            st.error("Please enter a valid product price")
        elif not product_category:
            st.error("Please select a product category")
        else:
            # We only get into this else clause if all the input fields have something 
            # in them. 
            #
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
