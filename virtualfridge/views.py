import pyrebase

from django.shortcuts import render, redirect
from django.contrib import auth
from django.core.files.storage import FileSystemStorage

firebase_api = open('firebase_api.txt')

config = {
	'apiKey': firebase_api.read(),
	'authDomain': "fridge-50aa2.firebaseapp.com",
	'databaseURL': "https://fridge-50aa2.firebaseio.com",
	'projectId': "fridge-50aa2",
	'storageBucket': "fridge-50aa2.appspot.com",
	'messagingSenderId': "826509812988",
	'appId': "1:826509812988:web:49ebd376df7915fb51e379",
	'measurementId': "G-SBHD2XQW2M"
}

firebase = pyrebase.initialize_app(config)
fireauth = firebase.auth()
database = firebase.database()
storage = firebase.storage()
token = ''

def home(request):
  maxnum = 8
  allrecipes = database.child('recipes').get().val()
  featuredrecipes = {}
  i = 0
  for k in allrecipes:
    # fname = allrecipes[k]['name']+allrecipes[k]['image']
    # storage.child("recipe_images/"+fname).download("/media/"+fname)
    featuredrecipes[k] = allrecipes[k]
    i += 1
    if i == maxnum:
      break
  
  return render(request, 'home.html', {'featuredrecipes': featuredrecipes})

def login(request):
	return render(request, 'login.html')


def recipe(request, name):
  recipe = database.child('recipes').child(name).get().val()
  return render(request, 'recipe.html', {'recipe': recipe})


def dashboard(request):
  ingredientslist = []
  with open('ingredientslist.txt') as my_file:
    for line in my_file:
      ingredientslist.append(line.replace('\n', ''))

  if request.method == 'POST': 
    try:
      email = request.POST['email']
      password = request.POST['password']
      user = fireauth.sign_in_with_email_and_password(email, password)
    except Exception as e:
      message = "Invalid Credentials"
      print(e)
      return render(request, 'login.html', {'msg': message})

    print("Login Successful!", user['idToken'][:10])
    session_id = user['idToken']
    request.session['sid'] = str(session_id)
    request.session['email'] = email
    uid = user['localId']
    request.session['uid'] = uid 
    request.session.modified = True
    ingredients =  database.child("users").child(uid).child('ingredients').get().val()
    if ingredients == None: # empty
      ingredients = {}

    return render(request, 'dashboard.html', {
      'email': email, 
      'ingredients': ingredients,
      'ingredientslist': ingredientslist
    })
  else:
    if (request.session.get('sid')):
      uid = request.session.get('uid')
      print("User", uid, "landed to their dashboard.")
      email = request.session.get('email')
      ingredients =  database.child("users").child(uid).child('ingredients').get().val()
      if ingredients == None: # empty
        ingredients = {}

      return render(request, 'dashboard.html', {
        'email': email, 
        'ingredients': ingredients,
        'ingredientslist': ingredientslist
      })
    else:
      return redirect('/login/')


def logout(request):
	auth.logout(request)
	return render(request, 'login.html')

def search(request):
  if request.method == 'POST':
    searchtext = request.POST['searchtext']
    recipeData = database.child("recipes").get().val()

    for rid, contents in recipeData.items():
      if searchtext.lower() in contents['name'].lower():
        print("Found similar recipe", contents)
        return render(request, 'recipe.html', {'recipe': contents})
  return redirect('home')


def signup(request):
  if request.method == 'POST':
    try:
      name = request.POST['name']
      username = request.POST['username']
      email = request.POST['email']
      password = request.POST['password']
      user = fireauth.create_user_with_email_and_password(email, password)
      uid = user['localId']
      # empty fridge initially
      data = {
        'uid': uid,
        'name': name, 
        'username': username,
				'fridge': {},
      }
      
      database.child("users").child(uid).set(data)
      return redirect('login')
    except Exception as e:
      message = "Unable to create account. Please Try again"
      print(e, message)
      return render(request, 'signup.html', {'msg': message})
  else:
    return render(request, 'signup.html')

def addrecipe(request): 
  if request.method == 'POST':
    rname = request.POST['recipename']
    rauthor = request.POST['recipeauthor']
    rdesc = request.POST['recipedescription']
    ringr = request.POST['recipeingredients']
    rinstr = request.POST['recipeinstructions']
    image_upload = request.FILES['recipeimage']
    fs = FileSystemStorage()
    fname = rname+image_upload.name
    fs.save(fname, image_upload)


    data = {
      'name': rname, 
      'author': rauthor,
      'description': rdesc,
      'ingredients': {},
      'instructions': rinstr,
      'image': fname
    }

    for ingr in ringr.split(","):
      name, quantity, unit = ingr.split(' ')
      name = name.replace('\n', ' ').replace('\r', ' ')
      data["ingredients"][name] =  {"quantity": quantity,"unit": unit}
    print(data)
    storage.child("recipe_images/"+fname).put("media/"+fname, request.session['sid'])
    database.child("recipes").child(rname).set(data)
    return render(request, 'dashboard.html')


def addingredient(request):
  # uid won't work on repl, since session is not saved as no cookies
  uid = request.session.get('uid') 
  if request.method == 'POST':
    iname = request.POST['name']
    iquantity = request.POST['quantity']
    iunit = request.POST['unit']

    data = {
      'name': iname, 
      'quantity': iquantity,
      'unit': iunit,
    }

    database.child("users").child(uid).child('ingredients').child(iname).set(data)
  return redirect('/dashboard/')

def deleteingredient(request, name):
  uid = request.session.get('uid')
  print("Ingredient",name,"is being deleted.")
  database.child("users").child(uid).child('ingredients').child(name).remove()

  return redirect('/dashboard/')

from django.template.defaulttags import register
...
@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

from collections import OrderedDict

def recipeslist(request):
	dic = OrderedDict()
	all_recipes = database.child("recipes").get()
	uid = request.session.get('uid')
	try:
		sortedrecipes = database.child('user').child(uid).child('sortedrecipe').get()
		for recipe in sortedrecipes.each():
			dic[recipe.val()] = database.child('recipes').child(recipe.val())
		return render(request, 'recipeslist.html', {"dic":dic})
	except:
		for recipe in all_recipes.each():
			dic[recipe.key()] = recipe.val()
		return render(request, 'recipeslist.html', {"dic":dic})


#sort recipelist
def extractRecipesUtil(recipes):
	r = {}
	for recipek,recipe in recipes.items():
		r[recipe['name']] = recipe['ingredients']
	return r

def searchrecipesUtil(fridgeingredients, recipes, sortmethod):
	maxmatch = []
	minmiss = []
	for recipek in recipes:
		matched = 0
		missing = 0
		for ingredientk in recipes[recipek]:
			if ingredientk in fridgeingredients:
				if int(recipes[recipek][ingredientk]["quantity"]) <= int(fridgeingredients[ingredientk]["quantity"]):
					matched += 1
				else:
					missing += 1
			else:
				missing += 1
		maxmatch.append([matched, recipek])
		minmiss.append([missing, recipek])
	maxmatch = sorted(maxmatch, reverse = 1)
	minmiss = sorted(minmiss)
	if sortmethod == 'maxmatch':
		return [r[1] for r in maxmatch]
	elif sortmethod == 'minmiss':
		return [r[1] for r in minmiss]

def sortrecipelistMain(request):
	uid = request.session.get('uid') 
	if request.method == 'POST':
		rsortmethod = request.POST['sort']
		extracted = extractRecipesUtil(database.child("recipes").get().val())
		fridgeingredients = database.child('users').child(uid).child('ingredients').get().val()
		sorteddata = searchrecipesUtil(fridgeingredients,extracted, rsortmethod)
		print(sorteddata)
		for i,recipe in enumerate(sorteddata):
			database.child('users').child(uid).child('sortedrecipes').child(i).set(recipe)
	
		return redirect('/recipeslist/')
print(1)