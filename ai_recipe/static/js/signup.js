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
  
    if (!name) showError("name", "Name is required");
    if (!email) showError("email", "Email is required");
    else if (!/\S+@\S+\.\S+/.test(email)) showError("email", "Email is invalid");
  
    if (!password) showError("password", "Password is required");
    else if (password.length < 8) showError("password", "Password must be at least 8 characters");
  
    if (password !== confirmPassword) showError("confirmPassword", "Passwords do not match");
  
    if (hasError) return;
  
    // Simulate async API call
    try {
      document.getElementById("submitBtn").innerText = "Creating Account...";
      await new Promise((res) => setTimeout(res, 1000)); // fake delay

      // Make an AJAX POST request to the Django backend
      const response = await fetch("{% url 'signup' %}", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value, // Include CSRF token
        },
        body: JSON.stringify({
          name: name,
          email: email,
          password: password,
        })
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
        }
        
      }
      
    } catch (err) {
      document.getElementById("error-form").innerText = "An error occurred during sign up.";
    } finally {
      document.getElementById("submitBtn").innerText = "Sign Up";
    }
  });
  