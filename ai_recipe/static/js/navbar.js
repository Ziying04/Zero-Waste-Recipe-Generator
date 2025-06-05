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
    
    // Mobile menu toggle
    const mobileToggle = document.getElementById('mobileToggle');
    const navMenu = document.getElementById('navMenu');
    
    if (mobileToggle) {
        mobileToggle.addEventListener('click', function() {
            this.classList.toggle('active');
            navMenu.classList.toggle('active');
        });
    }

    // Dropdown functionality
    const dropdowns = document.querySelectorAll('.dropdown');
    
    dropdowns.forEach(dropdown => {
        const trigger = dropdown.querySelector('.dropdown-toggle');
        const menu = dropdown.querySelector('.dropdown-menu');
        
        if (trigger && menu) {
            // Mouse events for desktop
            dropdown.addEventListener('mouseenter', () => {
                dropdown.classList.add('active');
            });
            
            dropdown.addEventListener('mouseleave', () => {
                dropdown.classList.remove('active');
            });
            
            // Click events for mobile
            trigger.addEventListener('click', (e) => {
                e.preventDefault();
                dropdown.classList.toggle('active');
                
                // Close other dropdowns
                dropdowns.forEach(otherDropdown => {
                    if (otherDropdown !== dropdown) {
                        otherDropdown.classList.remove('active');
                    }
                });
            });
        }
    });

    // Profile dropdown
    const profileTrigger = document.getElementById('profileTrigger');
    const profileDropdown = document.getElementById('profileDropdown');
    const profileSection = document.querySelector('.profile-section');
    
    if (profileTrigger && profileSection) {
        profileTrigger.addEventListener('click', function(e) {
            e.stopPropagation();
            profileSection.classList.toggle('active');
        });
        
        // Close on click outside
        document.addEventListener('click', function(e) {
            if (!profileSection.contains(e.target)) {
                profileSection.classList.remove('active');
            }
        });
    }

    // Search overlay
    const searchToggle = document.getElementById('searchToggle');
    const searchOverlay = document.getElementById('searchOverlay');
    const searchClose = document.getElementById('searchClose');
    const searchInput = document.querySelector('.search-input');
    
    if (searchToggle && searchOverlay) {
        searchToggle.addEventListener('click', function() {
            searchOverlay.classList.add('active');
            if (searchInput) {
                setTimeout(() => searchInput.focus(), 100);
            }
        });
    }
    
    if (searchClose) {
        searchClose.addEventListener('click', function() {
            searchOverlay.classList.remove('active');
        });
    }
    
    if (searchOverlay) {
        searchOverlay.addEventListener('click', function(e) {
            if (e.target === searchOverlay) {
                searchOverlay.classList.remove('active');
            }
        });
        
        // Close on Escape key
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape' && searchOverlay.classList.contains('active')) {
                searchOverlay.classList.remove('active');
            }
        });
    }

    // Theme toggle
    const themeToggle = document.getElementById('themeToggle');
    const themeIcon = themeToggle?.querySelector('i');
    
    if (themeToggle) {
        // Check for saved theme preference
        const savedTheme = localStorage.getItem('theme');
        const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        
        const currentTheme = savedTheme || (prefersDark ? 'dark' : 'light');
        document.documentElement.setAttribute('data-theme', currentTheme);
        
        updateThemeIcon(currentTheme);
        
        themeToggle.addEventListener('click', function() {
            const currentTheme = document.documentElement.getAttribute('data-theme');
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            
            document.documentElement.setAttribute('data-theme', newTheme);
            localStorage.setItem('theme', newTheme);
            
            updateThemeIcon(newTheme);
        });
        
        function updateThemeIcon(theme) {
            if (themeIcon) {
                themeIcon.className = theme === 'dark' ? 'fas fa-moon' : 'fas fa-sun';
            }
        }
    }

    // Search functionality
    const searchForm = document.querySelector('.search-box');
    if (searchForm && searchInput) {
        searchForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const query = searchInput.value.trim();
            if (query) {
                // Redirect to search results (adjust URL as needed)
                window.location.href = `/search/?q=${encodeURIComponent(query)}`;
            }
        });
    }

    // Close dropdowns when clicking outside
    document.addEventListener('click', function(e) {
        dropdowns.forEach(dropdown => {
            if (!dropdown.contains(e.target)) {
                dropdown.classList.remove('active');
            }
        });
    });

    // Navbar scroll effect
    let lastScrollY = window.scrollY;
    const navbar = document.querySelector('.navbar');
    
    if (navbar) {
        window.addEventListener('scroll', function() {
            const currentScrollY = window.scrollY;
            
            if (currentScrollY > 100) {
                navbar.classList.add('scrolled');
                
                if (currentScrollY > lastScrollY) {
                    // Scrolling down
                    navbar.style.transform = 'translateY(-100%)';
                } else {
                    // Scrolling up
                    navbar.style.transform = 'translateY(0)';
                }
            } else {
                navbar.classList.remove('scrolled');
                navbar.style.transform = 'translateY(0)';
            }
            
            lastScrollY = currentScrollY;
        });
    }

    // Add smooth transitions for all interactive elements
    const interactiveElements = document.querySelectorAll('.nav-link, .dropdown-item, .profile-item, .auth-btn, .nav-btn');
    
    interactiveElements.forEach(element => {
        element.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-1px)';
        });
        
        element.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });

    // Admin Dashboard Button Enhancement
    const adminBtn = document.querySelector('.admin-btn');
    if (adminBtn) {
        adminBtn.addEventListener('click', function(e) {
            // Add click animation
            this.style.transform = 'scale(0.95)';
            setTimeout(() => {
                this.style.transform = '';
            }, 150);
        });
    }

    // Enhanced Profile Section for Admin
    const profileSection = document.querySelector('.profile-section');
    const adminItems = document.querySelectorAll('.admin-item');
    
    // Check if user is admin and add admin class
    if (adminItems.length > 0 && profileSection) {
        profileSection.classList.add('admin');
    }

    // Admin item hover effects
    adminItems.forEach(item => {
        item.addEventListener('mouseenter', function() {
            this.style.transform = 'translateX(4px)';
        });
        
        item.addEventListener('mouseleave', function() {
            this.style.transform = 'translateX(0)';
        });
    });

    // Admin mode indicator
    function showAdminModeIndicator() {
        const adminBtn = document.querySelector('.admin-btn');
        if (adminBtn && window.location.pathname.includes('/admin')) {
            adminBtn.classList.add('active-admin');
            adminBtn.title = 'Currently in Admin Mode - Click to return to User Mode';
        }
    }

    // Call admin mode indicator
    showAdminModeIndicator();
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

// Admin Mode Toggle Function
function toggleAdminMode() {
    const currentPath = window.location.pathname;
    
    if (currentPath.includes('/admin')) {
        // Currently in admin mode, switch to user mode
        window.location.href = '/';
    } else {
        // Currently in user mode, switch to admin mode
        window.location.href = '/admin-dashboard/';
    }
}

// Enhanced Admin Dashboard Access
function accessAdminDashboard() {
    // Add loading state to admin button
    const adminBtn = document.querySelector('.admin-btn');
    if (adminBtn) {
        const originalHTML = adminBtn.innerHTML;
        adminBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
        
        // Restore original content after navigation
        setTimeout(() => {
            adminBtn.innerHTML = originalHTML;
        }, 1000);
    }
}

// Add click handler for admin dashboard button
document.addEventListener('click', function(e) {
    if (e.target.closest('.admin-btn')) {
        accessAdminDashboard();
    }
});

