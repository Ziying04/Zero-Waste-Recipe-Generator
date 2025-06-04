document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('recipe-search');
    const recipeCards = document.querySelectorAll('.col-12.col-md-6.col-lg-4');
    
    // Enhanced search with debounce and animations
    let searchTimeout;
    
    searchInput.addEventListener('input', function(e) {
        clearTimeout(searchTimeout);
        
        searchTimeout = setTimeout(() => {
            const searchTerm = e.target.value.toLowerCase().trim();
            let foundCount = 0;

            recipeCards.forEach((card, index) => {
                const recipeName = card.querySelector('.recipe-card-title a').textContent.toLowerCase();
                const cookingTimeEl = card.querySelector('.recipe-card-time');
                const cookingTime = cookingTimeEl ? cookingTimeEl.textContent.toLowerCase() : '';
                
                const isVisible = recipeName.includes(searchTerm) || cookingTime.includes(searchTerm);
                
                // Staggered animation for smooth transitions
                setTimeout(() => {
                    if (isVisible) {
                        card.style.display = '';
                        card.style.opacity = '0';
                        card.style.transform = 'translateY(20px)';
                        
                        setTimeout(() => {
                            card.style.transition = 'all 0.4s cubic-bezier(0.4, 0, 0.2, 1)';
                            card.style.opacity = '1';
                            card.style.transform = 'translateY(0)';
                        }, 50);
                        
                        foundCount++;
                    } else {
                        card.style.transition = 'all 0.3s ease';
                        card.style.opacity = '0';
                        card.style.transform = 'translateY(-20px)';
                        setTimeout(() => {
                            card.style.display = 'none';
                        }, 300);
                    }
                }, index * 50);
            });

            // Handle no results message
            setTimeout(() => {
                let noResults = document.querySelector('.no-results');
                
                if (foundCount === 0 && searchTerm.length > 0 && !noResults) {
                    const message = document.createElement('div');
                    message.className = 'col-12 no-results text-center mt-4';
                    message.innerHTML = `
                        <div class="empty-state" style="animation: fadeInUp 0.5s ease;">
                            <i class="fas fa-search fa-3x mb-3"></i>
                            <h5 class="text-muted">No recipes found</h5>
                            <p class="text-muted">Try searching with different keywords like "${searchTerm}"</p>
                        </div>
                    `;
                    document.getElementById('recipe-grid').appendChild(message);
                } else if (foundCount > 0 && noResults) {
                    noResults.style.animation = 'fadeOut 0.3s ease';
                    setTimeout(() => noResults.remove(), 300);
                }
            }, recipeCards.length * 50 + 200);
        }, 300);
    });

    // Professional save button functionality
    document.querySelectorAll(".save-btn").forEach((button) => {
        // Set initial state with smooth transition
        if (button.dataset.saved === "true") {
            button.classList.add('saved-state');
        }
        
        button.addEventListener("click", async function(e) {
            e.preventDefault();
            
            // Prevent double clicks
            if (this.classList.contains('saving')) return;
            
            // Add loading state
            this.classList.add("saving");
            const originalContent = this.innerHTML;
            this.innerHTML = '<i class="fas fa-spinner fa-spin"></i> <span class="save-count">' + 
                           this.querySelector('.save-count').textContent + '</span>';
            
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
                    const countSpan = this.querySelector(".save-count");

                    // Update state with smooth animation
                    this.dataset.saved = data.saved;
                    
                    if (data.saved) {
                        this.classList.add('saved-state');
                        this.innerHTML = '<i class="fas fa-bookmark"></i> <span class="save-count">' + data.count + '</span>';
                        
                        // Success animation
                        this.style.transform = 'scale(1.05)';
                        setTimeout(() => {
                            this.style.transform = '';
                        }, 200);
                    } else {
                        this.classList.remove('saved-state');
                        this.innerHTML = '<i class="far fa-bookmark"></i> <span class="save-count">' + data.count + '</span>';
                    }
                    
                    // Animate count change
                    countSpan.style.animation = 'countBounce 0.5s ease';
                    
                    // Show professional toast
                    showProfessionalToast(data.message || "Recipe saved successfully!", "success");
                } else {
                    const errorData = await response.json();
                    this.innerHTML = originalContent;
                    showProfessionalToast(errorData.error || "An error occurred. Please try again.", "error");
                }
            } catch (error) {
                console.error("Error:", error);
                this.innerHTML = originalContent;
                showProfessionalToast("Network error. Please check your connection.", "error");
            } finally {
                this.classList.remove("saving");
            }
        });
    });

    // Professional like button functionality
    document.querySelectorAll(".like-btn").forEach((button) => {
        // Set initial state
        if (button.dataset.liked === "true") {
            button.classList.add('liked-state');
        }
        
        button.addEventListener("click", async function(e) {
            e.preventDefault();
            
            // Prevent double clicks
            if (this.classList.contains('liking')) return;
            
            // Add loading state
            this.classList.add("liking");
            const originalContent = this.innerHTML;
            this.innerHTML = '<i class="fas fa-spinner fa-spin"></i> <span class="like-count">' + 
                           this.querySelector('.like-count').textContent + '</span>';
            
            const recipeId = this.dataset.recipeId;
            const url = `/api/recipe/${recipeId}/like/`;

            try {
                const response = await fetch(url, {
                    method: "POST",
                    headers: {
                        "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value,
                        "Content-Type": "application/json",
                    },
                    credentials: 'include'
                });

                if (response.ok) {
                    const data = await response.json();
                    const countSpan = this.querySelector(".like-count");
                    
                    // Update state with animation
                    this.dataset.liked = data.liked;
                    
                    if (data.liked) {
                        this.classList.add('liked-state');
                        this.innerHTML = '<i class="fas fa-heart"></i> <span class="like-count">' + data.count + '</span>';
                        
                        // Heart animation
                        this.style.transform = 'scale(1.1)';
                        setTimeout(() => {
                            this.style.transform = '';
                        }, 300);
                    } else {
                        this.classList.remove('liked-state');
                        this.innerHTML = '<i class="far fa-heart"></i> <span class="like-count">' + data.count + '</span>';
                    }
                    
                    // Animate count
                    countSpan.style.animation = 'countBounce 0.5s ease';
                    
                    showProfessionalToast(data.liked ? "Added to favorites!" : "Removed from favorites", data.liked ? "success" : "info");
                } else {
                    const errorData = await response.json();
                    this.innerHTML = originalContent;
                    
                    if (response.status === 401) {
                        showProfessionalToast("Please login to like recipes", "warning", () => {
                            window.location.href = '/api/login/';
                        });
                    } else {
                        showProfessionalToast(errorData.error || "An error occurred", "error");
                    }
                }
            } catch (error) {
                console.error("Error:", error);
                this.innerHTML = originalContent;
                showProfessionalToast("Network error. Please try again.", "error");
            } finally {
                this.classList.remove("liking");
            }
        });
    });
    
    // Professional toast notification system
    function showProfessionalToast(message, type = "success", callback = null) {
        // Create toast container if it doesn't exist
        let toastContainer = document.querySelector('.toast-container');
        if (!toastContainer) {
            toastContainer = document.createElement('div');
            toastContainer.className = 'toast-container';
            toastContainer.style.cssText = `
                position: fixed;
                top: 20px;
                right: 20px;
                z-index: 9999;
                pointer-events: none;
            `;
            document.body.appendChild(toastContainer);
        }
        
        // Create toast element
        const toast = document.createElement('div');
        const icons = {
            success: 'fas fa-check-circle',
            error: 'fas fa-exclamation-circle',
            warning: 'fas fa-exclamation-triangle',
            info: 'fas fa-info-circle'
        };
        
        const colors = {
            success: 'linear-gradient(135deg, #10b981 0%, #059669 100%)',
            error: 'linear-gradient(135deg, #ef4444 0%, #dc2626 100%)',
            warning: 'linear-gradient(135deg, #f59e0b 0%, #d97706 100%)',
            info: 'linear-gradient(135deg, #3b82f6 0%, #2563eb 100%)'
        };
        
        toast.innerHTML = `
            <div style="
                background: ${colors[type]};
                color: white;
                padding: 16px 24px;
                border-radius: 12px;
                box-shadow: 0 10px 25px rgba(0,0,0,0.15);
                display: flex;
                align-items: center;
                gap: 12px;
                margin-bottom: 12px;
                transform: translateX(100%);
                transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
                pointer-events: auto;
                cursor: pointer;
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255,255,255,0.1);
            ">
                <i class="${icons[type]}" style="font-size: 1.2rem;"></i>
                <span style="font-weight: 600; font-size: 0.95rem;">${message}</span>
            </div>
        `;
        
        toastContainer.appendChild(toast);
        
        // Animate in
        setTimeout(() => {
            toast.firstElementChild.style.transform = 'translateX(0)';
        }, 50);
        
        // Click to dismiss
        toast.addEventListener('click', () => {
            toast.firstElementChild.style.transform = 'translateX(100%)';
            setTimeout(() => toast.remove(), 400);
            if (callback) callback();
        });
        
        // Auto dismiss
        setTimeout(() => {
            if (toast.parentNode) {
                toast.firstElementChild.style.transform = 'translateX(100%)';
                setTimeout(() => toast.remove(), 400);
                if (callback) callback();
            }
        }, 4000);
    }
    
    // Add smooth scroll behavior for better UX
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
});

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes fadeOut {
        from {
            opacity: 1;
            transform: translateY(0);
        }
        to {
            opacity: 0;
            transform: translateY(-30px);
        }
    }
    
    .recipe-card {
        animation: fadeInUp 0.6s ease forwards;
    }
    
    .search-input:focus {
        animation: searchFocus 0.3s ease;
    }
    
    @keyframes searchFocus {
        0% { transform: scale(1); }
        50% { transform: scale(1.02); }
        100% { transform: scale(1); }
    }
`;
document.head.appendChild(style);
