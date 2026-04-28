document.addEventListener('DOMContentLoaded', function() {
    // Check if user is already authenticated
    if (document.body.dataset.authenticated === 'true') {
        window.location.href = '/';
        return;
    }
    
    // Password strength indicator
    const passwordInput = document.getElementById("password");
    const strengthIndicator = document.getElementById("password-strength");
    
    if (passwordInput && strengthIndicator) {
        passwordInput.addEventListener('input', function() {
            updatePasswordStrength(this.value);
        });
    }
});

function updatePasswordStrength(password) {
    const strengthIndicator = document.getElementById("password-strength");
    const strengthText = document.getElementById("strength-text");
    const strengthBar = document.getElementById("strength-bar");
    
    if (!strengthIndicator) return;
    
    const strength = calculatePasswordStrength(password);
    
    // Update strength bar
    strengthBar.className = `strength-bar ${strength.class}`;
    strengthBar.style.width = strength.percentage + '%';
    
    // Update strength text
    strengthText.textContent = strength.text;
    strengthText.className = `strength-text ${strength.class}`;
    
    // Show/hide indicator
    strengthIndicator.style.display = password.length > 0 ? 'block' : 'none';
}

function calculatePasswordStrength(password) {
    let score = 0;
    const checks = {
        length: password.length >= 8,
        lowercase: /[a-z]/.test(password),
        uppercase: /[A-Z]/.test(password),
        numbers: /\d/.test(password),
        special: /[!@#$%^&*(),.?":{}|<>]/.test(password),
        longLength: password.length >= 12
    };
    
    // Calculate score
    if (checks.length) score += 1;
    if (checks.lowercase) score += 1;
    if (checks.uppercase) score += 1;
    if (checks.numbers) score += 1;
    if (checks.special) score += 1;
    if (checks.longLength) score += 1;
    
    // Determine strength level
    if (score < 3) {
        return { class: 'weak', text: 'Weak', percentage: 25 };
    } else if (score < 4) {
        return { class: 'fair', text: 'Fair', percentage: 50 };
    } else if (score < 5) {
        return { class: 'good', text: 'Good', percentage: 75 };
    } else {
        return { class: 'strong', text: 'Strong', percentage: 100 };
    }
}

function validatePasswordStrength(password) {
    const requirements = [];
    
    if (password.length < 8) {
        requirements.push("At least 8 characters");
    }
    if (!/[a-z]/.test(password)) {
        requirements.push("One lowercase letter");
    }
    if (!/[A-Z]/.test(password)) {
        requirements.push("One uppercase letter");
    }
    if (!/\d/.test(password)) {
        requirements.push("One number");
    }
    if (!/[!@#$%^&*(),.?":{}|<>]/.test(password)) {
        requirements.push("One special character (!@#$%^&*(),.?\":{}|<>)");
    }
    
    return requirements;
}

document.getElementById("signupForm").addEventListener("submit", async function (e) {
    e.preventDefault();
  
    const name = document.getElementById("name").value.trim();
    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value;
    const confirmPassword = document.getElementById("confirmPassword").value;
  
    let hasError = false;
  
    const showError = (id, message) => {
      document.getElementById(`error-${id}`).innerText = message;
      hasError = true;
    };
  
    // Reset all errors
    ["name", "email", "password", "confirmPassword", "form"].forEach(id => {
      document.getElementById(`error-${id}`).innerText = "";
    });
  
    // Validate name
    if (!name) {
        showError("name", "Name is required");
    } else if (name.length < 2) {
        showError("name", "Name must be at least 2 characters");
    }
    
    // Validate email
    if (!email) {
        showError("email", "Email is required");
    } else if (!/\S+@\S+\.\S+/.test(email)) {
        showError("email", "Please enter a valid email address");
    }
  
    // Enhanced password validation
    if (!password) {
        showError("password", "Password is required");
    } else {
        const passwordRequirements = validatePasswordStrength(password);
        if (passwordRequirements.length > 0) {
            showError("password", "Password must include: " + passwordRequirements.join(", "));
        }
    }
  
    // Confirm password validation
    if (!confirmPassword) {
        showError("confirmPassword", "Please confirm your password");
    } else if (password !== confirmPassword) {
        showError("confirmPassword", "Passwords do not match");
    }
    
    // Additional security checks
    if (password && password.length > 0) {
        // Check for common weak passwords
        const commonPasswords = ['password', '123456', 'password123', 'admin', 'qwerty', 'letmein'];
        if (commonPasswords.includes(password.toLowerCase())) {
            showError("password", "This password is too common. Please choose a stronger password.");
        }
        
        // Check if password contains email
        if (email && password.toLowerCase().includes(email.split('@')[0].toLowerCase())) {
            showError("password", "Password should not contain your email address.");
        }
        
        // Check if password contains name
        if (name && password.toLowerCase().includes(name.toLowerCase())) {
            showError("password", "Password should not contain your name.");
        }
    }
  
    if (hasError) return;
  
    // Make the actual signup request
    try {
      document.getElementById("submitBtn").innerText = "Creating Account...";
      document.getElementById("submitBtn").disabled = true;
      
      const formData = new FormData();
      formData.append('name', name);
      formData.append('email', email);
      formData.append('password', password);
      formData.append('csrfmiddlewaretoken', document.querySelector("[name=csrfmiddlewaretoken]").value);

      const response = await fetch("/signup/", {
        method: "POST",
        body: formData,
        headers: {
            "Accept": "application/json"  
        },
        credentials: 'same-origin'
      });

      if (response.ok) {
        // Success: Hide the signup form and show a success card
        document.getElementById("signupCard").classList.add("hidden");
        document.getElementById("successCard").classList.remove("hidden");
        document.getElementById("userEmail").innerText = email;
      } else {
        // Handle errors from the backend
        if (response.status === 400) {
          const errorData = await response.json();
          document.getElementById("error-form").innerText = errorData.error;
        } else {
          document.getElementById("error-form").innerText = "An error occurred during sign up.";
        }
      }
      
    } catch (err) {
      console.error('Signup error:', err);
      document.getElementById("error-form").innerText = "An error occurred during sign up.";
    } finally {
      document.getElementById("submitBtn").innerText = "Create Account";
      document.getElementById("submitBtn").disabled = false;
    }
  });
