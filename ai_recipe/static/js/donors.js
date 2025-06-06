document.addEventListener('DOMContentLoaded', function() {
    console.log("donors.js loaded, initializing donor page scripts");
    
    // Initialize image preview for file upload
    initImagePreview();
});

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
