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
      // Simulate login
      document.getElementById('submit-btn').disabled = true;
      document.getElementById('submit-btn').textContent = 'Logging in...';
  
      // Simulate an API call (replace with your own login logic)
      setTimeout(() => {
        // Simulate a failed login
        const loginSuccessful = false; // Change this to `true` to simulate success
  
        if (!loginSuccessful) {
          document.getElementById('form-error').textContent = 'Invalid email or password. Please try again.';
          document.getElementById('submit-btn').disabled = false;
          document.getElementById('submit-btn').textContent = 'Log In';
        } else {
          window.location.href = '/dashboard'; // Redirect to the dashboard
        }
      }, 1500);
    }
  });
  