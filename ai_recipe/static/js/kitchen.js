document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('recipe-search');
    const recipeCards = document.querySelectorAll('.col-12.col-md-6.col-lg-4');
    
    // Enhanced search with debounce
    let searchTimeout;
    
    searchInput.addEventListener('input', function(e) {
        clearTimeout(searchTimeout);
        
        searchTimeout = setTimeout(() => {
            const searchTerm = e.target.value.toLowerCase().trim();
            let foundCount = 0;

            recipeCards.forEach(card => {
                const recipeName = card.querySelector('.recipe-card-title a').textContent.toLowerCase();
                // Get cooking time if available
                const cookingTimeEl = card.querySelector('.recipe-card-time');
                const cookingTime = cookingTimeEl ? cookingTimeEl.textContent.toLowerCase() : '';
                
                const isVisible = recipeName.includes(searchTerm) || cookingTime.includes(searchTerm);
                card.style.display = isVisible ? '' : 'none';
                
                if (isVisible) foundCount++;
            });

            // Show "no results" message if no matches
            let noResults = document.querySelector('.no-results');
            
            if (foundCount === 0 && !noResults) {
                if (searchTerm.length > 0) {
                    const message = document.createElement('div');
                    message.className = 'col-12 no-results text-center mt-4';
                    message.innerHTML = `
                        <div class="alert alert-info">
                            <i class="fas fa-search me-2"></i>
                            No recipes found matching "${searchTerm}".
                        </div>
                    `;
                    document.getElementById('recipe-grid').appendChild(message);
                }
            } else if (foundCount > 0 && noResults) {
                noResults.remove();
            }
            
            // Animate the cards that are visible
            recipeCards.forEach(card => {
                if (card.style.display !== 'none') {
                    card.classList.add('animated');
                    setTimeout(() => {
                        card.classList.remove('animated');
                    }, 500);
                }
            });
        }, 300); // Debounce delay
    });

    // Enhanced save button functionality with visual feedback
    document.querySelectorAll(".save-btn").forEach((button) => {
        // Set initial button state
        if (button.dataset.saved === "true") {
            button.querySelector("i").style.color = "#ffd700";
        }
        
        button.addEventListener("click", async function() {
            // Visual feedback before API call
            this.classList.add("saving");
            
            const recipeId = this.dataset.recipeId;
            const url = `/api/recipe/${recipeId}/save/`;

            try {
                const response = await fetch(url, {
                    method: "POST",
                    headers: {
                        "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value,
                        "Content-Type": "application/json",
                    },
                });

                if (response.ok) {
                    const data = await response.json();
                    const icon = this.querySelector("i");
                    const countSpan = this.querySelector(".save-count");

                    this.dataset.saved = data.saved;
                    
                    if (data.saved) {
                        icon.style.color = "#ffd700";
                        // Show success animation
                        icon.classList.add("saved-animation");
                        setTimeout(() => icon.classList.remove("saved-animation"), 1000);
                    } else {
                        icon.style.color = "";
                    }
                    
                    // Update the count with animation
                    countSpan.classList.add("count-animation");
                    countSpan.textContent = data.count;
                    setTimeout(() => countSpan.classList.remove("count-animation"), 1000);
                    
                    // Show toast notification instead of alert
                    showToast(data.message || "Recipe saved successfully!");
                } else {
                    const errorData = await response.json();
                    console.error("Error Response:", errorData);
                    showToast(errorData.error || "An error occurred. Please try again.", "error");
                }
            } catch (error) {
                console.error("Error:", error);
                showToast("An error occurred. Please try again.", "error");
            } finally {
                this.classList.remove("saving");
            }
        });
    });

    // Enhanced like button functionality
    document.querySelectorAll(".like-btn").forEach((button) => {
        // Set initial button state
        if (button.dataset.liked === "true") {
            button.querySelector("i").style.color = "#ff4b4b";
        }
        
        button.addEventListener("click", async function() {
            // Visual feedback before API call
            this.classList.add("liking");
            
            const recipeId = this.dataset.recipeId;
            const url = `/api/recipe/${recipeId}/like/`;
            const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

            try {
                const response = await fetch(url, {
                    method: "POST",
                    headers: {
                        "X-CSRFToken": csrfToken,
                        "Content-Type": "application/json",
                    },
                    credentials: 'include'
                });

                if (response.ok) {
                    const data = await response.json();
                    const icon = this.querySelector("i");
                    const countSpan = this.querySelector(".like-count");
                    
                    this.dataset.liked = data.liked;
                    
                    if (data.liked) {
                        icon.style.color = "#ff4b4b";
                        // Show heart animation
                        icon.classList.add("heart-animation");
                        setTimeout(() => icon.classList.remove("heart-animation"), 1000);
                    } else {
                        icon.style.color = "";
                    }
                    
                    // Update count with animation
                    countSpan.classList.add("count-animation");
                    countSpan.textContent = data.count;
                    setTimeout(() => countSpan.classList.remove("count-animation"), 1000);
                    
                    // Show toast notification
                    showToast(data.liked ? "Recipe added to likes" : "Recipe removed from likes");
                } else {
                    const errorData = await response.json();
                    if (response.status === 401) {
                        showToast("Please login to like recipes", "warning");
                        setTimeout(() => {
                            window.location.href = '/api/login/';
                        }, 1500);
                    } else {
                        showToast(errorData.error || "An error occurred while updating like", "error");
                    }
                }
            } catch (error) {
                console.error("Error:", error);
                showToast("An error occurred. Please try again.", "error");
            } finally {
                this.classList.remove("liking");
            }
        });
    });
    
    // Toast notification function
    function showToast(message, type = "success") {
        // Check if we should use SweetAlert2 or create our own toast
        if (typeof Swal !== 'undefined') {
            Swal.fire({
                text: message,
                icon: type,
                toast: true,
                position: 'top-end',
                showConfirmButton: false,
                timer: 3000,
                timerProgressBar: true
            });
        } else {
            // Create our own toast if SweetAlert is not available
            const toast = document.createElement('div');
            toast.className = `toast toast-${type}`;
            toast.innerHTML = `
                <div class="toast-message">${message}</div>
            `;
            document.body.appendChild(toast);
            
            setTimeout(() => {
                toast.classList.add('show');
            }, 10);
            
            setTimeout(() => {
                toast.classList.remove('show');
                setTimeout(() => toast.remove(), 300);
            }, 3000);
        }
    }
});
