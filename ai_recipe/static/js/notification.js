// Enhanced Professional Notification System

// Notification dropdown toggle with smooth animations
function toggleNotificationDropdown() {
    const dropdown = document.getElementById('notificationDropdown');
    const button = document.querySelector('.notification-button');
    
    if (dropdown.classList.contains('show')) {
        // Hide dropdown
        dropdown.style.transform = 'translateY(-10px)';
        dropdown.style.opacity = '0';
        setTimeout(() => {
            dropdown.classList.remove('show');
        }, 200);
        button.classList.remove('active');
    } else {
        // Show dropdown
        dropdown.classList.add('show');
        button.classList.add('active');
        
        // Fetch latest notifications when opening
        fetchNotifications();
        
        // Add staggered animation to notification items
        setTimeout(() => {
            animateNotificationItems();
        }, 100);
    }
}

// Enhanced click outside to close with better detection
document.addEventListener('click', function(event) {
    const dropdown = document.getElementById('notificationDropdown');
    const notificationBtn = document.querySelector('.notification-button');
    
    if (dropdown && dropdown.classList.contains('show') && 
        !dropdown.contains(event.target) && 
        !notificationBtn.contains(event.target)) {
        
        // Smooth close animation
        dropdown.style.transform = 'translateY(-10px)';
        dropdown.style.opacity = '0';
        setTimeout(() => {
            dropdown.classList.remove('show');
            notificationBtn.classList.remove('active');
        }, 200);
    }
});

// Enhanced notification fetching with error handling
async function fetchNotifications() {
    try {
        const response = await fetch('/notification/api/get-notifications/', {
            method: 'GET',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'Content-Type': 'application/json',
            },
            credentials: 'same-origin'
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        renderNotifications(data.notifications || []);
        
    } catch (error) {
        console.error('Error fetching notifications:', error);
        renderNotificationError();
    }
}

// Professional notification rendering with enhanced UI
function renderNotifications(notifications) {
    const dropdown = document.getElementById('notificationDropdown');
    
    // Create header
    const header = `
        <div class="notification-dropdown-header">
            <h4><i class="fas fa-bell mr-2"></i>Notifications</h4>
            ${notifications.some(n => !n.is_read) ? 
                '<a href="#" class="mark-all-read" onclick="markAllAsRead(event)">Mark all read</a>' : 
                '<span class="mark-all-read" style="opacity: 0.6;">All caught up!</span>'
            }
        </div>
    `;
    
    let content = '';
    
    if (notifications.length === 0) {
        content = `
            <div class="empty-notifications">
                <i class="fas fa-bell-slash"></i>
                <h5>All caught up!</h5>
                <p>You have no new notifications</p>
            </div>
        `;
    } else {
        content += '<div class="notification-list-container"><ul class="notification-list">';
        
        notifications.forEach((notification, index) => {
            const icon = getNotificationIcon(notification.notification_type || notification.type);
            const readClass = notification.is_read ? '' : 'unread';
            const timeAgo = formatTimeAgo(notification.created_at);
            
            content += `
                <li class="notification-item ${readClass}" data-notification-id="${notification.id}" style="animation-delay: ${index * 0.1}s">
                    <div class="notification-icon ${notification.notification_type || notification.type || 'default'}">
                        ${icon}
                    </div>
                    <div class="notification-content">
                        <p>${notification.content}</p>
                        <small><i class="fas fa-clock"></i> ${timeAgo}</small>
                        <div class="notification-actions">
                            ${notification.link ? 
                                `<a href="${notification.link}" class="notification-action-btn primary">View</a>` : 
                                ''
                            }
                            ${!notification.is_read ? 
                                `<button onclick="markAsRead(${notification.id}, event)" class="notification-action-btn">Mark read</button>` : 
                                ''
                            }
                        </div>
                    </div>
                </li>
            `;
        });
        
        content += '</ul></div>';
    }
    
    // Add view all footer
    const footer = `
        <a href="/notification/" class="view-all">
            View All Notifications <i class="fas fa-arrow-right"></i>
        </a>
    `;
    
    dropdown.innerHTML = header + content + footer;
}

// Enhanced notification icons with better styling
function getNotificationIcon(type) {
    const icons = {
        'like': '<i class="fas fa-heart"></i>',
        'expiry': '<i class="fas fa-exclamation-triangle"></i>',
        'admin_warning': '<i class="fas fa-shield-alt"></i>',
        'admin': '<i class="fas fa-shield-alt"></i>',
        'claim': '<i class="fas fa-hand-holding-heart"></i>',
        'donation': '<i class="fas fa-gift"></i>',
        'recipe': '<i class="fas fa-utensils"></i>',
        'system': '<i class="fas fa-cog"></i>',
        'default': '<i class="fas fa-bell"></i>'
    };
    
    return icons[type] || icons['default'];
}

// Professional time formatting
function formatTimeAgo(dateString) {
    const now = new Date();
    const notificationDate = new Date(dateString);
    const diffInSeconds = Math.floor((now - notificationDate) / 1000);
    
    if (diffInSeconds < 60) {
        return 'Just now';
    } else if (diffInSeconds < 3600) {
        const minutes = Math.floor(diffInSeconds / 60);
        return `${minutes} ${minutes === 1 ? 'minute' : 'minutes'} ago`;
    } else if (diffInSeconds < 86400) {
        const hours = Math.floor(diffInSeconds / 3600);
        return `${hours} ${hours === 1 ? 'hour' : 'hours'} ago`;
    } else if (diffInSeconds < 604800) {
        const days = Math.floor(diffInSeconds / 86400);
        return `${days} ${days === 1 ? 'day' : 'days'} ago`;
    } else {
        return notificationDate.toLocaleDateString();
    }
}

// Animate notification items with staggered effect
function animateNotificationItems() {
    const items = document.querySelectorAll('.notification-item');
    items.forEach((item, index) => {
        item.style.opacity = '0';
        item.style.transform = 'translateX(-20px)';
        
        setTimeout(() => {
            item.style.transition = 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)';
            item.style.opacity = '1';
            item.style.transform = 'translateX(0)';
        }, index * 50);
    });
}

// Enhanced mark as read with visual feedback
async function markAsRead(notificationId, event) {
    event.preventDefault();
    event.stopPropagation();
    
    const notificationItem = event.target.closest('.notification-item');
    const button = event.target;
    
    // Add loading state
    button.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
    button.disabled = true;
    
    try {
        const response = await fetch(`/notification/mark-as-read/${notificationId}/`, {
            method: 'POST',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': getCsrfToken(),
                'Content-Type': 'application/json',
            },
            credentials: 'same-origin'
        });
        
        if (!response.ok) {
            throw new Error('Failed to mark as read');
        }
        
        const data = await response.json();
        
        if (data.status === 'success') {
            // Smooth transition to read state
            notificationItem.style.transition = 'all 0.4s ease';
            notificationItem.classList.remove('unread');
            
            // Remove the unread indicator
            const unreadDot = notificationItem.querySelector('::before');
            if (unreadDot) {
                unreadDot.style.opacity = '0';
            }
            
            // Remove the mark as read button
            button.style.transform = 'scale(0)';
            setTimeout(() => {
                button.remove();
            }, 200);
            
            // Update badge count
            updateNotificationCount(-1);
            
            // Show success feedback
            showNotificationToast('Marked as read', 'success');
        }
    } catch (error) {
        console.error('Error marking notification as read:', error);
        button.innerHTML = 'Mark read';
        button.disabled = false;
        showNotificationToast('Failed to mark as read', 'error');
    }
}

// Mark all notifications as read
async function markAllAsRead(event) {
    event.preventDefault();
    
    const button = event.target;
    const originalText = button.innerHTML;
    button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Marking...';
    button.style.pointerEvents = 'none';
    
    try {
        const response = await fetch('/notification/mark-all-as-read/', {
            method: 'POST',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': getCsrfToken(),
                'Content-Type': 'application/json',
            },
            credentials: 'same-origin'
        });
        
        if (!response.ok) {
            throw new Error('Failed to mark all as read');
        }
        
        const data = await response.json();
        
        if (data.status === 'success') {
            // Refresh notifications
            fetchNotifications();
            
            // Reset notification count
            const countBadge = document.querySelector('.notification-count');
            if (countBadge) {
                countBadge.style.animation = 'fadeOut 0.3s ease';
                setTimeout(() => {
                    countBadge.style.display = 'none';
                }, 300);
            }
            
            showNotificationToast('All notifications marked as read', 'success');
        }
    } catch (error) {
        console.error('Error marking all as read:', error);
        button.innerHTML = originalText;
        button.style.pointerEvents = 'auto';
        showNotificationToast('Failed to mark all as read', 'error');
    }
}

// Update notification count badge
function updateNotificationCount(change) {
    const countBadge = document.querySelector('.notification-count');
    if (countBadge) {
        const currentCount = parseInt(countBadge.textContent) || 0;
        const newCount = Math.max(0, currentCount + change);
        
        if (newCount === 0) {
            countBadge.style.animation = 'fadeOut 0.3s ease';
            setTimeout(() => {
                countBadge.style.display = 'none';
            }, 300);
        } else {
            countBadge.textContent = newCount;
            countBadge.style.animation = 'countBounce 0.5s ease';
        }
    }
}

// Professional toast notifications
function showNotificationToast(message, type = 'info') {
    const toast = document.createElement('div');
    const colors = {
        success: 'linear-gradient(135deg, #10b981 0%, #059669 100%)',
        error: 'linear-gradient(135deg, #ef4444 0%, #dc2626 100%)',
        info: 'linear-gradient(135deg, #3b82f6 0%, #2563eb 100%)'
    };
    
    const icons = {
        success: 'fas fa-check-circle',
        error: 'fas fa-exclamation-circle',
        info: 'fas fa-info-circle'
    };
    
    toast.innerHTML = `
        <div style="
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 10000;
            background: ${colors[type]};
            color: white;
            padding: 12px 20px;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 0.875rem;
            font-weight: 500;
            transform: translateX(100%);
            transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        ">
            <i class="${icons[type]}"></i>
            ${message}
        </div>
    `;
    
    document.body.appendChild(toast);
    
    // Animate in
    setTimeout(() => {
        toast.firstElementChild.style.transform = 'translateX(0)';
    }, 100);
    
    // Auto remove
    setTimeout(() => {
        toast.firstElementChild.style.transform = 'translateX(100%)';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

// Get CSRF token
function getCsrfToken() {
    const token = document.querySelector('[name=csrfmiddlewaretoken]');
    return token ? token.value : '';
}

// Error state rendering
function renderNotificationError() {
    const dropdown = document.getElementById('notificationDropdown');
    dropdown.innerHTML = `
        <div class="notification-dropdown-header">
            <h4><i class="fas fa-exclamation-triangle mr-2"></i>Error</h4>
        </div>
        <div class="empty-notifications">
            <i class="fas fa-exclamation-triangle"></i>
            <h5>Unable to load notifications</h5>
            <p>Please check your connection and try again</p>
            <button onclick="fetchNotifications()" class="notification-action-btn primary" style="margin-top: 1rem;">
                <i class="fas fa-redo"></i> Retry
            </button>
        </div>
    `;
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    // Preload notifications if dropdown exists
    const dropdown = document.getElementById('notificationDropdown');
    if (dropdown) {
        // Add loading state initially
        dropdown.innerHTML = `
            <div class="notification-dropdown-header">
                <h4><i class="fas fa-bell mr-2"></i>Notifications</h4>
            </div>
            <div class="empty-notifications">
                <i class="fas fa-spinner fa-spin"></i>
                <h5>Loading...</h5>
            </div>
        `;
    }
});

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes fadeOut {
        from { opacity: 1; transform: scale(1); }
        to { opacity: 0; transform: scale(0.8); }
    }
    
    @keyframes countBounce {
        0% { transform: scale(1); }
        50% { transform: scale(1.2); }
        100% { transform: scale(1); }
    }
    
    .notification-button.active {
        background: linear-gradient(135deg, var(--primary-green) 0%, var(--primary-dark) 100%);
        border-color: var(--primary-green);
        box-shadow: 0 0 0 3px rgba(22, 163, 74, 0.1);
    }
    
    .notification-button.active i {
        color: white;
    }
`;
document.head.appendChild(style);
