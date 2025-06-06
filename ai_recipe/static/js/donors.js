document.addEventListener('DOMContentLoaded', function() {
    console.log("donors.js loaded, initializing donor page scripts");
    
    // Initialize image preview for file upload
    initImagePreview();
    
    // Initialize tab functionality
    initTabs();
    
    // Initialize form validation
    initFormValidation();
    
    // Initialize delete confirmation
    initDeleteConfirmation();
    
    // Add animations
    initAnimations();
});

// Tab functionality - Show/hide content
function showTab(tabName) {
    const tabs = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');
    
    // Remove active class from all tabs and contents
    tabs.forEach(t => t.classList.remove('active'));
    tabContents.forEach(c => c.classList.remove('active'));
    
    // Add active class to selected tab and content
    if (tabName === 'donations') {
      document.getElementById('tab-donations').classList.add('active');
      document.getElementById('tab-content-donations').classList.add('active');
    } else if (tabName === 'add') {
      document.getElementById('tab-add').classList.add('active');
      document.getElementById('tab-content-add').classList.add('active');
    }
}

// Initialize tabs based on donation count
function initTabs() {
    // The tab initialization is now handled by the showTab function
    // We'll use the default tabs from the Django template context
    console.log("Tab initialization complete");
}

// Image preview functionality
function initImagePreview() {
    const fileInput = document.querySelector('.file-input');
    
    if (fileInput) {
        console.log("Found file input, attaching change handler");
        fileInput.addEventListener('change', function() {
            console.log("File input changed");
            const fileUpload = this.parentElement;
            
            if (this.files && this.files[0]) {
                console.log(`Selected file: ${this.files[0].name}`);
                const reader = new FileReader();
                
                reader.onload = function(e) {
                    // Remove existing preview if any
                    const existingPreview = fileUpload.querySelector('.file-preview');
                    if (existingPreview) {
                        existingPreview.remove();
                    }
                    
                    console.log("Creating preview element");
                    // Create preview element
                    const preview = document.createElement('div');
                    preview.className = 'file-preview';
                    preview.style.cssText = `
                        position: absolute;
                        top: 0;
                        left: 0;
                        width: 100%;
                        height: 100%;
                        z-index: 1;
                        background-image: url('${e.target.result}');
                        background-size: cover;
                        background-position: center;
                        border-radius: 1.5rem;
                    `;
                    
                    // Create overlay with file name
                    const overlay = document.createElement('div');
                    overlay.className = 'file-preview-overlay';
                    overlay.style.cssText = `
                        position: absolute;
                        bottom: 0;
                        left: 0;
                        width: 100%;
                        padding: 0.75rem;
                        background: rgba(0, 0, 0, 0.6);
                        color: white;
                        font-size: 0.875rem;
                        border-radius: 0 0 1.5rem 1.5rem;
                    `;
                    overlay.textContent = fileInput.files[0].name;
                    
                    preview.appendChild(overlay);
                    fileUpload.appendChild(preview);
                    
                    // Add file-has-preview class to the upload container
                    fileUpload.classList.add('file-has-preview');
                    console.log("Preview added successfully");
                };
                
                reader.onerror = function(error) {
                    console.error("Error reading file:", error);
                    alert("There was an error processing your image. Please try a different one.");
                };
                
                reader.readAsDataURL(this.files[0]);
            }
        });
    } else {
        console.warn("File input element not found!");
    }
}

// Form validation
function initFormValidation() {
    const form = document.getElementById('donation-form');
    if (form) {
        console.log("Found donation form, attaching submission handler");
        form.addEventListener('submit', function(e) {
            console.log("Form submission attempted");
            let isValid = true;
            const requiredFields = form.querySelectorAll('[required]');
            
            requiredFields.forEach(field => {
                if (field.type === 'file') {
                    if (!field.files || field.files.length === 0) {
                        isValid = false;
                        field.parentElement.style.borderColor = '#dc2626';
                        console.log(`File field ${field.name} is empty`);
                    }
                } else if (!field.value.trim()) {
                    isValid = false;
                    field.style.borderColor = '#dc2626';
                    console.log(`Field ${field.name} is empty`);
                }
            });
            
            if (!isValid) {
                e.preventDefault();
                alert('Please fill in all required fields');
            } else {
                console.log('Form validation passed');
            }
        });
    } else {
        console.warn("Form not found!");
    }
}

// Delete confirmation
function initDeleteConfirmation() {
    document.querySelectorAll('.delete-post-btn').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const postId = this.getAttribute('data-post-id');
            const postTitle = this.getAttribute('data-post-title');
            
            if (confirm(`Are you sure you want to delete "${postTitle}"? This action cannot be undone.`)) {
                deletePost(postId);
            }
        });
    });
}

// Function to delete a post via AJAX
function deletePost(postId) {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    
    fetch(`/community/delete_donation/${postId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken,
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Failed to delete donation');
        }
        return response.json();
    })
    .then(data => {
        const postCard = document.querySelector(`[data-post-id="${postId}"]`);
        if (postCard) {
            postCard.style.transition = "all 0.5s ease";
            postCard.style.transform = "translateY(20px)";
            postCard.style.opacity = "0";
            
            setTimeout(() => {
                postCard.remove();
                
                // Check if there are no more posts and show empty state if needed
                const remainingPosts = document.querySelectorAll('.post-card').length;
                if (remainingPosts === 0) {
                    window.location.reload(); // Reload to show empty state
                }
            }, 500);
        }
        
        // Show success message
        showToast(data.message || 'Donation deleted successfully!', 'success');
        
        // Update stats without full page reload if possible
        updateStats();
    })
    .catch(error => {
        console.error('Error:', error);
        showToast(error.message || 'An error occurred. Please try again.', 'error');
    });
}

// Function to update stats - could be enhanced to fetch via AJAX instead of reloading
function updateStats() {
    // For now, just reload after a short delay
    setTimeout(() => {
        window.location.reload();
    }, 1000);
}

// Helper function to get cookie for CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Toast notifications
function showToast(message, type = 'info') {
    // Create toast container if it doesn't exist
    let toastContainer = document.querySelector('.toast-container');
    if (!toastContainer) {
        toastContainer = document.createElement('div');
        toastContainer.className = 'toast-container';
        toastContainer.style.cssText = `
            position: fixed;
            bottom: 20px;
            right: 20px;
            z-index: 9999;
        `;
        document.body.appendChild(toastContainer);
    }
    
    // Create toast element
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.style.cssText = `
        background-color: ${type === 'success' ? '#dcfce7' : type === 'error' ? '#fee2e2' : '#e0f2fe'};
        color: ${type === 'success' ? '#166534' : type === 'error' ? '#991b1b' : '#0c4a6e'};
        border-left: 4px solid ${type === 'success' ? '#16a34a' : type === 'error' ? '#dc2626' : '#0ea5e9'};
        border-radius: 0.375rem;
        padding: 1rem 1.5rem;
        margin-bottom: 0.75rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        display: flex;
        align-items: center;
        max-width: 350px;
        animation: slideInRight 0.3s ease forwards;
    `;
    
    // Set icon based on type
    const icon = type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : 'info-circle';
    
    // Toast content
    toast.innerHTML = `
        <i class="fas fa-${icon}" style="margin-right: 0.75rem; font-size: 1.25rem;"></i>
        <span>${message}</span>
        <button class="toast-close" style="margin-left: auto; background: none; border: none; cursor: pointer; color: inherit; opacity: 0.7;">
            <i class="fas fa-times"></i>
        </button>
    `;
    
    // Add to container
    toastContainer.appendChild(toast);
    
    // Close button functionality
    const closeBtn = toast.querySelector('.toast-close');
    closeBtn.addEventListener('click', () => {
        toast.style.animation = 'slideOutRight 0.3s ease forwards';
        setTimeout(() => {
            toastContainer.removeChild(toast);
        }, 300);
    });
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        if (toast.parentNode === toastContainer) {
            toast.style.animation = 'slideOutRight 0.3s ease forwards';
            setTimeout(() => {
                if (toast.parentNode === toastContainer) {
                    toastContainer.removeChild(toast);
                }
            }, 300);
        }
    }, 5000);
}

// Initialize animations
function initAnimations() {
    // Animate the form title
    const formTitle = document.querySelector('.form-title');
    if (formTitle) {
        formTitle.style.opacity = '0';
        formTitle.style.transform = 'translateY(-30px)';
        setTimeout(() => {
            formTitle.style.transition = 'opacity 1s ease, transform 1s ease';
            formTitle.style.opacity = '1';
            formTitle.style.transform = 'translateY(0)';
        }, 100);
    }
    
    // Animate in the tabs
    const tabsNav = document.querySelector('.tabs-nav');
    if (tabsNav) {
        tabsNav.style.opacity = '0';
        tabsNav.style.transform = 'translateY(-20px)';
        setTimeout(() => {
            tabsNav.style.transition = 'opacity 1s ease, transform 1s ease';
            tabsNav.style.opacity = '1';
            tabsNav.style.transform = 'translateY(0)';
        }, 300);
    }
    
    // Add hover effect to post cards
    document.querySelectorAll('.post-card').forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-10px) scale(1.02)';
            this.style.boxShadow = '0 30px 60px rgba(0, 0, 0, 0.15)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
            this.style.boxShadow = '0 20px 50px rgba(0, 0, 0, 0.1)';
        });
    });
    
    // Add special effects to form elements
    document.querySelectorAll('.input, .select, .textarea').forEach(input => {
        input.addEventListener('focus', function() {
            this.style.transform = 'translateY(-2px)';
        });
        
        input.addEventListener('blur', function() {
            if (!this.value) {
                this.style.transform = 'translateY(0)';
            }
        });
    });
}

// Add keyframes for animations
const styleSheet = document.createElement('style');
styleSheet.textContent = `
    @keyframes slideInRight {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes slideOutRight {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(100%); opacity: 0; }
    }
`;
document.head.appendChild(styleSheet);
