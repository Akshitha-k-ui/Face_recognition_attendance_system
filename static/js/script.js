// Get the modal
var modal = document.getElementById("loginModal");

// Get the button that opens the modal
var loginButton = document.getElementById("loginButton");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// When the user clicks on the button, open the modal
loginButton.onclick = function() {
  modal.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
  modal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}


// Get the signup link
var signupLink = document.getElementById("signupLink");
var loginLink = document.getElementById("loginLink");

// Get the login form and signup form
var loginForm = document.getElementById("loginForm");
var signupForm = document.getElementById("signupForm");

// Hide the signup form initially
signupForm.style.display = "none";

// When the signup link is clicked, show the signup form and hide the login form
signupLink.onclick = function() {
  loginForm.style.display = "none";
  signupForm.style.display = "block";
}


loginLinkLink.onclick = function() {
  loginForm.style.display = "block";
  signupForm.style.display = "none";
}



