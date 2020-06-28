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
    featuredrecipes[k] = allrecipes[k]
    i += 1
    if i == maxnum:
      break
  print(featuredrecipes)
  return render(request, 'home.html', {'featuredrecipes': featuredrecipes})

def login(request):
	return render(request, 'login.html')


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
      return render(request, 'dashboard.html', {'email': email})
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
        return render(request, 'home.html', {'recipe': contents}) # opens recipe page directly (home)
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

#to be fixed
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
			data["ingredients"][ingr.split()[0]] =  {"quantity": ingr.split()[1],"unit": ingr.split()[2]}

		# storage.child("recipe_images").put(image_upload)
		storage.child("recipe_images/"+fname).put("media/"+fname, request.session['sid'])
		database.child("recipes").push(data)
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

def recipeslist(request):
	
	dic = {}
	all_recipes = database.child("recipes").get()
	for recipe in all_recipes.each():
		dic[recipe.key()] = recipe.val()
	return render(request, 'recipeslist.html', {"dic":dic})
