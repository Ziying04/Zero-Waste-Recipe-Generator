document.addEventListener('DOMContentLoaded', function() {
    // Check if user is already authenticated
    if (document.body.dataset.authenticated === 'true') {
        window.location.href = '/';
        return;
    }
});

document.getElementById('login-form').addEventListener('submit', function (e) {
    e.preventDefault();
  
    const formData = new FormData(this);
    const errors = {};
  
    // Validate email
    const email = formData.get('email').trim();
    if (!email) {
      errors.email = 'Email is required';
    }
  
    // Validate password
    const password = formData.get('password').trim();
    if (!password) {
      errors.password = 'Password is required';
    }
  
    if (Object.keys(errors).length > 0) {
      // Show error messages
      document.getElementById('email-error').textContent = errors.email || '';
      document.getElementById('password-error').textContent = errors.password || '';
      document.getElementById('form-error').textContent = '';
    } else {
      // Perform actual login
      const submitBtn = document.getElementById('submit-btn');
      submitBtn.disabled = true;
      submitBtn.textContent = 'Logging in...';
  
      // Submit the form to Django backend
      fetch('/login/', {
        method: 'POST',
        body: formData,
        credentials: 'same-origin'
      })
      .then(response => {
        if (response.ok) {
          // Check if it's a redirect response
          if (response.redirected) {
            window.location.href = response.url;
          } else {
            // For successful login, redirect to home
            window.location.href = '/';
          }
        } else {
          return response.text().then(text => {
            // Parse the response to extract error message
            const parser = new DOMParser();
            const doc = parser.parseFromString(text, 'text/html');
            const errorElement = doc.querySelector('.error-message');
            const errorMessage = errorElement ? errorElement.textContent : 'Login failed. Please try again.';
            throw new Error(errorMessage);
          });
        }
      })
      .catch(error => {
        document.getElementById('form-error').textContent = error.message;
        submitBtn.disabled = false;
        submitBtn.textContent = 'Sign In';
      });
    }
  });
