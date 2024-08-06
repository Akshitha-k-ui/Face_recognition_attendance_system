document.addEventListener("DOMContentLoaded", function() {
  var loginBtn = document.querySelector('.login-btn');
  var loginModal = document.getElementById('loginModal');
  var closeModal = document.querySelector('.close');

  loginBtn.addEventListener('click', function(event) {
    event.preventDefault();
    loginModal.style.display = "block";
  });

  closeModal.addEventListener('click', function() {
    loginModal.style.display = "none";
  });

  window.addEventListener('click', function(event) {
    if (event.target == loginModal) {
      loginModal.style.display = "none";
    }
  });

  // Toggle between login and register forms
  var loginForm = document.getElementById('loginForm');
  var registerForm = document.getElementById('registerForm');

  document.getElementById('login_switch').addEventListener('click', function() {
    loginForm.style.display = "block";
    registerForm.style.display = "none";
  });

  document.getElementById('register_switch').addEventListener('click', function() {
    loginForm.style.display = "none";
    registerForm.style.display = "block";
  });

  // Handle form submission and store user credentials (sample logic)
  document.getElementById('loginForm').addEventListener('submit', function(event) {
    event.preventDefault();
    var username = document.getElementById('login_username').value;
    var password = document.getElementById('login_password').value;
    // Here you can add your login logic (e.g., sending credentials to the server)
    console.log('Login - Username: ' + username + ', Password: ' + password);
  });

  document.getElementById('registerForm').addEventListener('submit', function(event) {
    event.preventDefault();
    var username = document.getElementById('register_username').value;
    var email = document.getElementById('register_email').value;
    var password = document.getElementById('register_password').value;
    // Here you can add your registration logic (e.g., sending data to the server)
    console.log('Register - Username: ' + username + ', Email: ' + email + ', Password: ' + password);
  });
});