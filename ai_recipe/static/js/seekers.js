/**
 * Seekers page JavaScript - Enhanced version
 */
document.addEventListener('DOMContentLoaded', function() {
    // Initialize card animations with staggered delay
    const cards = document.querySelectorAll('.food-card');
    cards.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.05}s`;
    });
    
    // Set up slider functionality
    setupSlider();
    
    // Handle map resizing properly
    const map = document.getElementById('map');
    if (map && window.map) {
        window.addEventListener('resize', function() {
            if (document.getElementById('map-container').style.display !== 'none') {
                setTimeout(() => window.map.invalidateSize(), 100);
            }
        });
    }
    
    // Make sure category select fits properly
    adjustSelectWidth();
    window.addEventListener('resize', adjustSelectWidth);
    
    // Initialize any existing location data
    initializeLocationData();
});

// Function to ensure the category select has appropriate width
function adjustSelectWidth() {
    const categorySelect = document.querySelector('.category-select select');
    const searchBar = document.querySelector('.search-bar');
    
    if (categorySelect && searchBar) {
        if (window.innerWidth <= 640) {
            categorySelect.style.width = '100%';
        } else {
            // Reset to default on larger screens
            categorySelect.style.width = '';
        }
    }
}

// Function to initialize existing location data
function initializeLocationData() {
    const userLat = document.getElementById('user_lat').value;
    const userLon = document.getElementById('user_lon').value;
    
    if (userLat && userLon) {
        // Add a visual indicator that location is being used
        const locationBtn = document.querySelector('.location-button');
        if (locationBtn) {
            locationBtn.innerHTML = '<i class="fa-solid fa-location-dot mr-2"></i> Location Set';
            locationBtn.classList.add('location-active');
        }
    }
}

// Function to set up slider functionality
function setupSlider() {
    const slider = document.getElementById('distance');
    const sliderLine = document.querySelector('.slider-line');
    const mileDisplay = document.getElementById('mile-display');
    
    if (slider && sliderLine && mileDisplay) {
        // Update slider on load
        updateSliderUI(slider.value, slider.min, slider.max);
        
        // Update on changes
        slider.addEventListener('input', function() {
            updateSliderUI(this.value, this.min, this.max);
        });
    }
}

// Update slider UI components
function updateSliderUI(value, min, max) {
    const slider = document.getElementById('distance');
    const sliderLine = document.querySelector('.slider-line');
    const mileDisplay = document.getElementById('mile-display');
    
    if (slider && sliderLine && mileDisplay) {
        const percentage = ((value - min) / (max - min)) * 100;
        sliderLine.style.width = `${percentage}%`;
        mileDisplay.textContent = value;
    }
}

// Show map container
function showMap() {
    const mapContainer = document.getElementById('map-container');
    const mapLoading = document.getElementById('map-loading');
    
    if (mapContainer) {
        mapContainer.classList.remove('hidden');
        
        // Initialize map if not already done
        if (!window.map) {
            // Show loading indicator
            if (mapLoading) mapLoading.style.display = 'flex';
            
            // Default to a central location if none provided
            const userLat = parseFloat(document.getElementById('user_lat').value) || 3.1390;
            const userLon = parseFloat(document.getElementById('user_lon').value) || 101.6869;
            
            window.map = L.map('map').setView([userLat, userLon], 12);
            
            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: '© OpenStreetMap contributors'
            }).addTo(window.map);
            
            // Add marker if coordinates exist
            if (document.getElementById('user_lat').value && document.getElementById('user_lon').value) {
                window.marker = L.marker([userLat, userLon]).addTo(window.map);
            }
            
            window.map.on('click', function(e) {
                if (window.marker) {
                    window.map.removeLayer(window.marker);
                }
                window.marker = L.marker(e.latlng).addTo(window.map);
                document.getElementById("user_lat").value = e.latlng.lat;
                document.getElementById("user_lon").value = e.latlng.lng;
                
                // Update location button style
                const locationBtn = document.querySelector('.location-button');
                if (locationBtn) {
                    locationBtn.innerHTML = '<i class="fa-solid fa-location-dot mr-2"></i> Location Set';
                    locationBtn.classList.add('location-active');
                }
            });
            
            // Hide loading indicator when map tiles are loaded
            window.map.whenReady(function() {
                if (mapLoading) mapLoading.style.display = 'none';
            });
        }
        
        // Force map to recalculate size when displayed
        setTimeout(function() {
            if (window.map) window.map.invalidateSize();
        }, 100);
    }
    
    // Smooth scroll to map
    mapContainer.scrollIntoView({behavior: "smooth"});
}

// Hide map container
function hideMap() {
    const mapContainer = document.getElementById('map-container');
    if (mapContainer) {
        mapContainer.classList.add('hidden');
    }
}

// Clear search input
function clearSearch(button) {
    const input = button.parentElement.querySelector('input');
    if (input) {
        input.value = '';
        // Submit the form to refresh results
        document.getElementById('filterForm').submit();
    }
}
