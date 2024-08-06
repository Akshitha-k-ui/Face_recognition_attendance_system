

$(document).ready(function() {
    $('#signupLink').click(function() {
        $('#loginForm').hide();
        $('#signupForm').show();
    });

    $('#loginLink').click(function() {
        $('#signupForm').hide();
        $('#loginForm').show();
    });

    // Handle login
    $('#loginFormElement').submit(function(event) {
        event.preventDefault(); // Prevent default form submission
        $.ajax({
            type: 'POST',
            url: '/login',
            data: $(this).serialize(),
            success: function(response) {
                alert(response.message);
                window.location.href = '/'; // Redirect to index page
            },
            error: function(xhr) {
                const response = JSON.parse(xhr.responseText);
                alert(response.message || 'Login failed!');
            }
        });
    });

    // Handle signup
    $('#signupFormElement').submit(function(event) {
        event.preventDefault(); // Prevent default form submission
        $.ajax({
            type: 'POST',
            url: '/signup',
            data: $(this).serialize(),
            success: function(response) {
                alert(response.message);
                window.location.href = '/'; // Redirect to index page
            },
            error: function(xhr) {
                const response = JSON.parse(xhr.responseText);
                alert(response.message || 'Signup failed!');
            }
        });
    });
});
