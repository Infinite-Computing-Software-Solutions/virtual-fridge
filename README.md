# Virutal-Fridge
### Infinite Computing Software Solutions

Share recipes from your virtual fridge and find out which ones you can make from your ingredients.


## Features
- **Login and Sign Up**
- **Dashboard**: Drop down bar on top with options: search, my favorites, share recipe, my fridge, popular recipes and recommended recipes
- **Search**: just a search bar with a select bar on the side where you can select if you're looking for desert Italian food Chinese etc.
- **Favorites**: A list of all favorited recipes
- **My Fridge**: A place where the user can input all their ingredients
- **Share Recipe**: A place where the user can share their own recipe, must have a youtube video link, and list of ingredients, also a text box to be filled with a minimum of 100 characters description (also must include 2 tags)
- **Popular Recipes**: Top 10 recipes
- **Recommended Recipes**: A list of 10 recipes which are made based on what you have the ingredients for and what type of dishes you like based on their tags(chinese dinner, dessert etc)


## Instructions
1. Run the following commands to install dependencies:
```
pip3 install -r requirements.txt
```
Or alternatively:
```
pip3 install django
pip3 install pyrebase
```

1. To run the web application server:
```
python3 manage.py runserver
```
Then go to http://127.0.0.1:8000/ to check it out in development mode.

## Technology
- HTML5
- CSS
- Django
- Python
- Firebase
