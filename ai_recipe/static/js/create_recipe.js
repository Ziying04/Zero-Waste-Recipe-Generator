document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('recipe-form');
    const imageUrlInput = document.getElementById('image_url');
    const imagePreview = document.getElementById('image-preview');
    
    // Form validation
    form.addEventListener('submit', function(event) {
        if (!form.checkValidity()) {
            event.preventDefault();
            event.stopPropagation();
            
            // Add visual feedback for invalid fields
            const invalidFields = form.querySelectorAll(':invalid');
            invalidFields.forEach(field => {
                field.classList.add('is-invalid');
            });
            
            // Scroll to the first invalid field
            if (invalidFields.length) {
                invalidFields[0].scrollIntoView({ behavior: 'smooth', block: 'center' });
            }
        }
        
        form.classList.add('was-validated');
    });
    
    // Remove invalid styling when field is edited
    form.querySelectorAll('input, textarea').forEach(field => {
        field.addEventListener('input', function() {
            if (field.checkValidity()) {
                field.classList.remove('is-invalid');
            }
        });
    });
    
    // Image URL preview
    imageUrlInput.addEventListener('input', debounce(function() {
        const url = imageUrlInput.value.trim();
        
        if (url) {
            // Show loading state
            imagePreview.innerHTML = '<div class="text-center"><i class="fas fa-spinner fa-spin"></i> Loading image preview...</div>';
            
            // Create an image element to test the URL
            const img = new Image();
            img.onload = function() {
                // Valid image
                imagePreview.innerHTML = '';
                imagePreview.classList.add('active');
                
                const previewImg = document.createElement('img');
                previewImg.src = url;
                previewImg.className = 'img-fluid rounded';
                imagePreview.appendChild(previewImg);
                
                const caption = document.createElement('div');
                caption.className = 'text-center text-success mt-2';
                caption.innerHTML = '<i class="fas fa-check-circle"></i> Image preview loaded successfully';
                imagePreview.appendChild(caption);
            };
            
            img.onerror = function() {
                // Invalid image
                imagePreview.innerHTML = '';
                imagePreview.classList.add('active');
                
                const errorMessage = document.createElement('div');
                errorMessage.className = 'alert alert-warning';
                errorMessage.innerHTML = '<i class="fas fa-exclamation-triangle"></i> Unable to load image from this URL. Please check the URL or try another.';
                imagePreview.appendChild(errorMessage);
            };
            
            img.src = url;
        } else {
            // Clear preview if URL is empty
            imagePreview.innerHTML = '';
            imagePreview.classList.remove('active');
        }
    }, 500));
    
    // Helper function to debounce input events
    function debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
});
