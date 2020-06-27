import pyrebase

from django.shortcuts import render, redirect
from django.contrib import auth

firebase_api = open('firebase_api.txt')

config = {
	'apiKey': "AIzaSyBC7ooZMf_K2R5OkSvHIHHi9-6b7ke02hA",
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

def home(request):
	return render(request, 'home.html')

def login(request):
	return render(request, 'login.html')


def post_sign(request):
	email = request.POST.get('email')
	password = request.POST.get('password')

	try:
		user = fireauth.sign_in_with_email_and_password(email, password)
	except Exception as e:
		message = "Invalid Credentials"
		print(e)
		return render(request, 'login.html', {'msg': message})

	print(user['idToken'])
	session_id = user['idToken']
	request.session['uid'] = str(session_id)
	return render(request, 'index.html', {"email": email})


def logout(request):
	auth.logout(request)
	return render(request, 'login.html')


def signup(request):
	return render(request, 'signup.html')
	if request.method == 'POST':
		try:
			name = request.POST.get('name')
			email = request.POST.get('email')
			password = request.POST.get('password')
			user = fireauth.create_user_with_email_and_password(email, password)
			uid = user['localId']
			data = {'name': name, 'status': 1}
			database.child("users").child(uid).child("details").set(data)
			return redirect('login')
		except Exception as e:
			message = "Unable to create account. Please Try again"
			print(e)
			# return render(request, 'login.html', {'msg': message})
			return redirect('login')
	else:
		return render(request, 'login.html')