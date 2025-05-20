document.addEventListener('DOMContentLoaded', function() {
    // Get current page URL
    const currentLocation = window.location.pathname;
    
    // Get all nav links
    const navLinks = document.querySelectorAll('.nav-link');
    
    // Set active class based on current URL
    navLinks.forEach(link => {
        const href = link.getAttribute('href');
        if (href === currentLocation || 
            (href === '/' && currentLocation === '/') ||
            (href !== '/' && currentLocation.startsWith(href))) {
            link.classList.add('active');
        }
    });
    
    // Smooth scroll to top when clicking brand
    document.querySelector('.navbar-brand').addEventListener('click', function(e) {
        if (window.location.pathname === '/') {
            e.preventDefault();
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        }
    });
});

function toggleProfileDropdown() {
    const isAuthenticated = document.querySelector('.profile-button')?.dataset.authenticated === 'true';
    
    if (!isAuthenticated) {
        window.location.href = '/api/login/';
        return;
    }
    
    const dropdown = document.getElementById('profileDropdown');
    dropdown.classList.toggle('show');
}

// Close dropdown when clicking outside
document.addEventListener('click', function(event) {
    const dropdown = document.getElementById('profileDropdown');
    const profileButton = document.querySelector('.profile-button');
    
    if (!profileButton?.contains(event.target) && dropdown?.classList.contains('show')) {
        dropdown.classList.remove('show');
    }
});

function toggleNotificationDropdown() {
  document.getElementById("notificationDropdown").classList.toggle("show");
}

document.addEventListener("click", function (event) {
  const dropdown = document.getElementById("notificationDropdown");
  if (!event.target.closest(".notification-button")) {
    dropdown.classList.remove("show");
  }
});

