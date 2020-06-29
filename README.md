# Virutal-Fridge
### Infinite Computing Software Solutions
Share recipes from your virtual fridge dashboard, manage your ingredients virtually and find out which ones you can make from your ingredients.


## Instructions
1. Run the following commands to install dependencies:
  ```
  pip3 install -r requirements.txt
  ```

2. To run the web application server:
  ```
  python3 manage.py runserver
  ```
Then go to http://127.0.0.1:8000/ to check it out in development mode.


## Features
- **Login and Sign Up**: Secure OAuth2.0 Firebase authentication system
- **Dashboard**: Drop down bar on top with options: search, my favorites, share recipe, my fridge, popular recipes and recommended recipes
- **Search**: just a search bar with a select bar on the side where you can select if you're looking for desert Italian food Chinese etc.
- **My Virtual Fridge**: A place where the user can input all their ingredients
- **Publish a Recipe**: A place where the user can share their own recipe, and a list of ingredients, also a text box to be filled with a minimum of 100 characters description (also must include 2 tags)
- **Featured Recipes**: Top 10 recipes
- **My Recipes**: A list of recipes which are made based on what you have the ingredients for

## Technology
- HTML5
- CSS
- Django
- Python
- Firebase
