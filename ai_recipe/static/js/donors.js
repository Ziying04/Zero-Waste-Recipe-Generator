document.addEventListener('DOMContentLoaded', function() {
    // Initialize tab functionality
    initTabs();
    
    // Initialize form animations
    initFormAnimations();
    
    // Initialize post card animations
    animatePostCards();
    
    // Initialize image preview for file upload
    initImagePreview();
    
    // Initialize delete confirmation
    initDeleteConfirmation();
});

// Tab functionality
function initTabs() {
    const tabs = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');
    
    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            // Get the target content id from the tab's data attribute
            const targetId = tab.getAttribute('data-target');
            
            // Remove active class from all tabs and contents
            tabs.forEach(t => t.classList.remove('active'));
            tabContents.forEach(c => c.classList.remove('active'));
            
            // Add active class to current tab and its content
            tab.classList.add('active');
            document.getElementById(targetId).classList.add('active');
        });
    });
}

// Form animations
function initFormAnimations() {
    const formGroups = document.querySelectorAll('.form-group');
    
    formGroups.forEach((group, index) => {
        // Add staggered animation to form groups
        group.style.animation = `slideInUp 0.4s ease forwards ${index * 0.1}s`;
        group.style.opacity = '0';
        
        // Add focus effects
        const input = group.querySelector('input, select, textarea');
        const label = group.querySelector('.label');
        
        if (input && label) {
            input.addEventListener('focus', () => {
                label.style.color = '#16a34a';
            });
            
            input.addEventListener('blur', () => {
                label.style.color = '';
            });
        }
    });
    
    // Add animation to submit button
    const submitBtn = document.querySelector('.donation-form .button');
    if (submitBtn) {
        submitBtn.style.animation = `slideInUp 0.5s ease forwards ${formGroups.length * 0.1}s`;
        submitBtn.style.opacity = '0';
    }
}

// Post card animations
function animatePostCards() {
    const cards = document.querySelectorAll('.post-card');
    
    cards.forEach((card, index) => {
        // Add staggered animation to cards
        card.style.animation = `slideInUp 0.5s ease forwards ${index * 0.1}s`;
        card.style.opacity = '0';
        
        // Add hover effect
        card.addEventListener('mouseenter', () => {
            const badge = card.querySelector('.status-badge');
            if (badge) {
                badge.classList.add('pulse-animation');
            }
        });
        
        card.addEventListener('mouseleave', () => {
            const badge = card.querySelector('.status-badge');
            if (badge) {
                badge.classList.remove('pulse-animation');
            }
        });
    });
}

// Image preview functionality
function initImagePreview() {
    const fileInput = document.querySelector('.file-input');
    
    if (fileInput) {
        fileInput.addEventListener('change', function() {
            const fileUpload = this.parentElement;
            
            if (this.files && this.files[0]) {
                const reader = new FileReader();
                
                reader.onload = function(e) {
                    // Remove existing preview if any
                    const existingPreview = fileUpload.querySelector('.file-preview');
                    if (existingPreview) {
                        existingPreview.remove();
                    }
                    
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
                        border-radius: 0.75rem;
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
                        background: rgba(0, 0, 0, 0.5);
                        color: white;
                        font-size: 0.875rem;
                        border-radius: 0 0 0.75rem 0.75rem;
                    `;
                    overlay.textContent = fileInput.files[0].name;
                    
                    preview.appendChild(overlay);
                    fileUpload.appendChild(preview);
                    
                    // Add file-has-preview class to the upload container
                    fileUpload.classList.add('file-has-preview');
                }
                
                reader.readAsDataURL(this.files[0]);
            }
        });
    }
}

// Delete confirmation
function initDeleteConfirmation() {
    const deleteButtons = document.querySelectorAll('.delete-post-btn');
    
    deleteButtons.forEach(button => {
        button.addEventListener('click', (e) => {
            e.preventDefault();
            const postId = button.getAttribute('data-post-id');
            const postTitle = button.getAttribute('data-post-title');
            
            // Create and show the custom confirmation dialog
            showDeleteConfirmation(postId, postTitle);
        });
    });
}

function showDeleteConfirmation(postId, postTitle) {
    // Create modal overlay
    const overlay = document.createElement('div');
    overlay.className = 'modal-overlay';
    overlay.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0, 0, 0, 0.5);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 1000;
        animation: fadeIn 0.3s ease forwards;
    `;
    
    // Create modal content
    const modal = document.createElement('div');
    modal.className = 'modal-content';
    modal.style.cssText = `
        background: white;
        border-radius: 1rem;
        padding: 2rem;
        max-width: 500px;
        width: 90%;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
        animation: slideInUp 0.4s ease forwards;
    `;
    
    // Create modal header
    const header = document.createElement('div');
    header.className = 'modal-header';
    header.innerHTML = `
        <h3 style="font-size: 1.5rem; font-weight: 600; color: #1f2937; margin-bottom: 1rem;">
            <i class="fas fa-trash-alt" style="color: #dc2626; margin-right: 0.5rem;"></i>
            Delete Donation
        </h3>
    `;
    
    // Create modal body
    const body = document.createElement('div');
    body.className = 'modal-body';
    body.innerHTML = `
        <p style="color: #4b5563; margin-bottom: 1.5rem;">
            Are you sure you want to delete "${postTitle}"? This action cannot be undone.
        </p>
    `;
    
    // Create modal footer with action buttons
    const footer = document.createElement('div');
    footer.className = 'modal-footer';
    footer.style.cssText = `
        display: flex;
        justify-content: flex-end;
        gap: 1rem;
        margin-top: 1.5rem;
    `;
    
    // Cancel button
    const cancelButton = document.createElement('button');
    cancelButton.className = 'button cancel';
    cancelButton.textContent = 'Cancel';
    cancelButton.style.cssText = `
        padding: 0.75rem 1.5rem;
        border-radius: 0.75rem;
        font-weight: 500;
        background: #f3f4f6;
        color: #4b5563;
        border: none;
        cursor: pointer;
        transition: all 0.3s ease;
    `;
    cancelButton.addEventListener('mouseenter', () => {
        cancelButton.style.backgroundColor = '#e5e7eb';
    });
    cancelButton.addEventListener('mouseleave', () => {
        cancelButton.style.backgroundColor = '#f3f4f6';
    });
    cancelButton.addEventListener('click', () => {
        document.body.removeChild(overlay);
    });
    
    // Delete button
    const deleteButton = document.createElement('button');
    deleteButton.className = 'button danger';
    deleteButton.innerHTML = '<i class="fas fa-trash-alt" style="margin-right: 0.5rem;"></i> Delete';
    deleteButton.style.cssText = `
        padding: 0.75rem 1.5rem;
        border-radius: 0.75rem;
        font-weight: 500;
        background: #dc2626;
        color: white;
        border: none;
        cursor: pointer;
        transition: all 0.3s ease;
    `;
    deleteButton.addEventListener('mouseenter', () => {
        deleteButton.style.backgroundColor = '#b91c1c';
        deleteButton.style.transform = 'translateY(-2px)';
        deleteButton.style.boxShadow = '0 4px 8px rgba(220, 38, 38, 0.3)';
    });
    deleteButton.addEventListener('mouseleave', () => {
        deleteButton.style.backgroundColor = '#dc2626';
        deleteButton.style.transform = 'translateY(0)';
        deleteButton.style.boxShadow = 'none';
    });
    deleteButton.addEventListener('click', () => {
        deletePost(postId);
        document.body.removeChild(overlay);
    });
    
    // Assemble the modal
    footer.appendChild(cancelButton);
    footer.appendChild(deleteButton);
    modal.appendChild(header);
    modal.appendChild(body);
    modal.appendChild(footer);
    overlay.appendChild(modal);
    
    // Add the modal to the document
    document.body.appendChild(overlay);
    
    // Add click event to close when clicking outside the modal
    overlay.addEventListener('click', (e) => {
        if (e.target === overlay) {
            document.body.removeChild(overlay);
        }
    });
}

// Function to delete a post
function deletePost(postId) {
    // Create form data
    const formData = new FormData();
    formData.append('post_id', postId);
    
    // Get CSRF token from a cookie
    const csrfToken = getCookie('csrftoken');
    
    // Send delete request
    fetch(`/community/delete_donation/${postId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken
        },
        body: formData
    })
    .then(response => {
        if (response.ok) {
            return response.json().then(data => {
                // Remove the post card from the DOM
                const postCard = document.querySelector(`.post-card[data-post-id="${postId}"]`);
                if (postCard) {
                    postCard.style.animation = 'slideOutDown 0.3s ease forwards';
                    setTimeout(() => {
                        postCard.remove();
                        
                        // Check if there are no more posts
                        const remainingPosts = document.querySelectorAll('.post-card');
                        if (remainingPosts.length === 0) {
                            // Add empty state if no more posts
                            const postsContainer = document.querySelector('.posts-feed');
                            const emptyState = document.createElement('div');
                            emptyState.className = 'empty-state';
                            emptyState.innerHTML = `
                                <div class="empty-state-icon">
                                    <i class="fas fa-box-open"></i>
                                </div>
                                <h3 class="empty-state-title">No Donations Yet</h3>
                                <p class="empty-state-text">You haven't shared any food items. Add your first donation to help reduce food waste.</p>
                                <button class="button primary" onclick="document.querySelector('[data-target=tab-content-add]').click()">
                                    <i class="fas fa-plus"></i> Add Your First Donation
                                </button>
                            `;
                            postsContainer.appendChild(emptyState);
                        }
                    }, 300);
                }
                showToast(data.message || 'Donation deleted successfully!', 'success');
            });
        } else {
            return response.json().then(data => {
                showToast(data.message || 'Failed to delete donation. Please try again.', 'error');
            }).catch(() => {
                showToast('Failed to delete donation. Please try again.', 'error');
            });
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showToast('An error occurred. Please try again.', 'error');
    });
}

// Helper function to get cookie by name (for CSRF token)
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

// Toast notification function
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
    const icon = type === 'success' ? 'fas fa-check-circle' : type === 'error' ? 'fas fa-exclamation-circle' : 'fas fa-info-circle';
    
    // Toast content
    toast.innerHTML = `
        <i class="${icon}" style="margin-right: 0.75rem; font-size: 1.25rem;"></i>
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

// Additional animations
document.addEventListener('DOMContentLoaded', function() {
    // Add animation classes to back button
    const backButton = document.querySelector('.back-button');
    if (backButton) {
        backButton.style.animation = 'slideInUp 0.3s ease forwards';
        backButton.style.opacity = '0';
    }
    
    // Add animation to page title
    const pageTitle = document.querySelector('h1');
    if (pageTitle) {
        pageTitle.style.animation = 'slideInUp 0.4s ease forwards 0.1s';
        pageTitle.style.opacity = '0';
    }
    
    // Add animation to tabs
    const tabsContainer = document.querySelector('.tabs-container');
    if (tabsContainer) {
        tabsContainer.style.animation = 'slideInUp 0.4s ease forwards 0.2s';
        tabsContainer.style.opacity = '0';
    }
});

// Additional CSS animations
const additionalStyles = document.createElement('style');
additionalStyles.textContent = `
    @keyframes slideInRight {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOutRight {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
    
    @keyframes slideOutDown {
        from {
            transform: translateY(0);
            opacity: 1;
        }
        to {
            transform: translateY(30px);
            opacity: 0;
        }
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
`;
document.head.appendChild(additionalStyles);

// Function to actually delete a post
function deletePost(postId) {
    // In a real implementation, you would send an AJAX request to delete the post
    console.log(`Deleting post with ID: ${postId}`);
    
    // For now, we'll just remove the post card from the DOM with animation
    const postCard = document.querySelector(`.post-card[data-post-id="${postId}"]`);
    if (postCard) {
        postCard.style.animation = 'slideOutDown 0.3s ease forwards';
        setTimeout(() => {
            postCard.remove();
            showToast('Donation deleted successfully!', 'success');
        }, 300);
    }
}
