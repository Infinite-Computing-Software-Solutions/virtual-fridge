var loginpage = document.getElementById("login-page");
var signuppage = document.getElementById("signup-page");
var loginform = document.getElementById("login-form");
var signupform = document.getElementById("signup-form");
signupform.style.display = "none";

function signupForm(){
    loginform.style.display="none";
    signupform.style.display = "block";
}
function loginForm(){
    signupform.style.display = "none";
    loginform.style.display="block";
    
}

firebase.auth().onAuthStateChanged(function(user) {
    if (user) {
      // User is signed in.
      document.getElementById("loginform").style.display="none";
      change();
      window.location.href="index.html";
    } else {
      // No user is signed in.
      document.getElementById("loginform").style.display="block";

    }
  });

/*function login(){
    var userEmail = document.getElementById("eimp").value;
    var userPass = document.getElementById("pimp").value;

  firebase.auth().signInWithEmailAndPassword(userEmail, userPass).catch(function(error) {
    // Handle Errors here.
    var errorCode = error.code;
    var errorMessage = error.message;

    window.alert("Error : " + errorMessage);

    // ...
  });

}*/
loginform.addEventListener('submit',(e) =>{
  e.preventDefault();
  var userEmail = document.getElementById("eimp").value;
    var userPass = document.getElementById("pimp").value;

  firebase.auth().signInWithEmailAndPassword(userEmail, userPass).catch(function(error) {
    // Handle Errors here.
    var errorCode = error.code;
    var errorMessage = error.message;

    window.alert("Error : " + errorMessage);

    // ...
  });
});

  function logout(){
    firebase.auth().signOut();
  }

signupform.addEventListener('submit',(e) =>{
  e.preventDefault();
  var email= document.getElementById("email").value;
  var pass =document.getElementById("password").value;
  var name =document.getElementById("name").value;
  var user = firebase.auth().currentUser;
  
  firebase.auth().createUserWithEmailAndPassword(email,pass).then(cred => {

  });
  firebase.auth().signInWithEmailAndPassword(email, pass).catch(function(error) {
    // Handle Errors here.
    var errorCode = error.code;
    var errorMessage = error.message;

    console.log("Error : " + errorMessage);

    // ...
  });
  
});

function change(){
  var user = firebase.auth().currentUser;
  var name = document.getElementById("name").value;

user.updateProfile({
  displayName: name,
  photoURL: "https://example.com/jane-q-user/profile.jpg"
}).then(function() {
  // Update successful.
}).catch(function(error) {
  // An error happened.
});
  }


// The app only has access as defined in the Security Rules
/*var db = firebase.database();
var ref = db.ref("/text");
ref.on("value", function(snapshot) {
  console.log(snapshot.val());
});
*/
var dbref = firebase.database().ref();
var somevalue = "hello"
dbref.child("text").set(somevalue);