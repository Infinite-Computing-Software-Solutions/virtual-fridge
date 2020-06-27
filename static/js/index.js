// Your web app's Firebase configuration
var firebaseConfig = {
  apiKey: "<enter your api key>",
  authDomain: "<enter auth domain>",
  databaseURL: "<https://databse url>",
  projectId: "<enter project id>",
  storageBucket: "<val>",
  messagingSenderId: "<id>",
  appId: "<app id >",
  measurementId: "<mid>"
};
// Initialize Firebase
firebase.initializeApp(firebaseConfig);
var database = firebase.database();

// Your web app's Firebase configuration

  firebase.auth().onAuthStateChanged(function(user) {
    if (user) {
      // User is signed in.
      window.alert("hi"+" "+user.uid);
      var userid=user.uid;
      var nam = user.displayName;
      appt(userid, nam);
    } else {
      // No user is signed in.
      /*window.location.replace("http://127.0.0.1:5500/login.html");*/
      window.location.href = "login.html";

    }
  });

  function logout(){
    firebase.auth().signOut()
  .then(function() {
    // Sign-out successful.
  })
  .catch(function(error) {
    // An error happened
    window.alert("Error:"+error);
  });
  }

  var db = firebase.database();
  var ref = db.ref("/text");
  ref.on("value", function(snapshot) {
    console.log(snapshot.val());
  });


function appt(id,name){
var dbref = firebase.database().ref();
var somevalue = "hi";
dbref.child("text").set(id);
alert(id);
alert(name);
}


