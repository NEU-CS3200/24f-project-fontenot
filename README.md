# Fall 2024 CS 3200 Project - Form Example

A student asked for an example of an input form in Streamlit that packages up and sends information to the API to ultimately get stored in the database.  This repo is meant to demo how you might go about doing that. 

## What to check out

- First, take a look at [api/backend/products/products_routes.py](api/backend/products/products_routes.py) and notice that there are routes for creating a new product with `POST /product` (starting at line 142) and for retrieving all the categories of products currently in use with `GET /categories` (starting at line 177).
- Now, take a look at [app/src/pages/22_Add_Product.py](app/src/pages/22_Add_Product.py) where I create the form.  I added a ton of comments in this file to explain what's happening. 
  - When creating the form for the user to add a new product to the database, I need them to choose a category rather than enter a category ID (that's inconvenient).  
  - So, I use the `GET /categories` route to get a list of categories (around line 20) that is used to populate a Streamlit `selectbox` widget. 
  - The creation of the form and the widgets on the form start at line 38. It uses 4 different input widgets: `text_input`, `text_area`, `number_input`, `selectbox`. 
  - Lines 53 - 61 do some basic input validation. 
  - Lines 68 - 73 package the data up into a Python dictionary, which can easily be converted to JSON. 
  - Lines 80 - 92 demo how to make the POST request and attach the values entered by the user (Line 85, in particular). 
- Take a look at the different input widget options provided by Streamlit.  You can find a quick overview in the [Streamlit docs](https://docs.streamlit.io/develop/api-reference/widgets). 

If you want to clone this repo and try it out, go for it.  I've changed the container names and ports slightly to minimize conflicts with your main project repo.  

To get to the form, click on the System Admin button on the front page of the app, then there should be a button for adding a new product.  


## Controlling the Containers

- `docker compose up -d` to start all the containers in the background
- `docker compose down` to shutdown and delete the containers
- `docker compose up db -d` only start the database container (replace db with the other services as needed)
- `docker compose stop` to "turn off" the containers but not delete them. 
 
