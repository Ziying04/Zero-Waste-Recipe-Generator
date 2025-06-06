// Enhanced Notification System

// Toggle the notification dropdown
function toggleNotificationDropdown() {
    const dropdown = document.getElementById('notificationDropdown');
    
    if (dropdown.classList.contains('show')) {
        dropdown.classList.remove('show');
    } else {
        dropdown.classList.add('show');
        fetchNotifications();
    }
}

// Close dropdown when clicking outside
document.addEventListener('click', function(event) {
    const dropdown = document.getElementById('notificationDropdown');
    const notificationBtn = document.getElementById('notificationToggle');
    
    if (dropdown && dropdown.classList.contains('show') && 
        !dropdown.contains(event.target) && 
        event.target !== notificationBtn && 
        !notificationBtn.contains(event.target)) {
        dropdown.classList.remove('show');
    }
});

// Fetch notifications from API
async function fetchNotifications() {
    try {
        const response = await fetch('/notification/api/get-notifications/', {
            method: 'GET',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'Content-Type': 'application/json'
            },
            credentials: 'same-origin'
        });
        
        if (!response.ok) {
            throw new Error('Failed to fetch notifications');
        }
        
        const data = await response.json();
        renderNotifications(data.notifications || [], data.unread_count || 0);
        
    } catch (error) {
        console.error('Error fetching notifications:', error);
        renderErrorState();
    }
}

// Render notifications in dropdown
function renderNotifications(notifications, unreadCount) {
    const dropdown = document.getElementById('notificationDropdown');
    
    // Create header
    let content = `
        <div class="notification-dropdown-header">
            <h4><i class="fas fa-bell mr-2"></i>Notifications</h4>
            ${unreadCount > 0 ? 
                `<a href="#" class="mark-all-read" onclick="markAllAsRead(event)">Mark all read</a>` : 
                ''
            }
        </div>
    `;
    
    // No notifications state
    if (notifications.length === 0) {
        content += `
            <div class="empty-notifications">
                <i class="fas fa-bell-slash"></i>
                <h5>No notifications</h5>
                <p>You're all caught up!</p>
            </div>
        `;
    } else {
        // List notifications
        content += '<ul class="notification-list">';
        
        notifications.forEach(notification => {
            const readClass = notification.is_read ? '' : 'unread';
            const icon = getNotificationIcon(notification.type);
            
            content += `
                <li class="notification-item ${readClass}" data-id="${notification.id}">
                    <div class="notification-content">
                        <div class="notification-icon ${notification.type}">
                            <i class="${icon}"></i>
                        </div>
                        <div class="notification-text">
                            <p>${notification.content}</p>
                            <small>${notification.created_at}</small>
                        </div>
                    </div>
                    <div class="notification-actions">
                        ${notification.link ? 
                            `<a href="${notification.link}" class="btn btn-sm btn-primary">View</a>` : 
                            ''
                        }
                        ${!notification.is_read ? 
                            `<button onclick="markAsRead(${notification.id}, event)" class="btn btn-sm btn-outline-secondary">Mark read</button>` : 
                            ''
                        }
                    </div>
                </li>
            `;
        });
        
        content += '</ul>';
    }
    
    // Add view all link - Replace Django template tag with direct URL
    content += `<a href="/notification/" class="view-all">View All Notifications <i class="fas fa-arrow-right ml-1"></i></a>`;
    
    dropdown.innerHTML = content;
}

// Return appropriate icon based on notification type
function getNotificationIcon(type) {
    switch(type) {
        case 'like':
            return 'fas fa-heart';
        case 'expiry':
            return 'fas fa-exclamation-triangle';
        case 'admin_warning':
            return 'fas fa-shield-alt';
        default:
            return 'fas fa-bell';
    }
}

// Mark a notification as read
async function markAsRead(notificationId, event) {
    event.preventDefault();
    event.stopPropagation();
    
    try {
        const csrf = document.querySelector('[name=csrfmiddlewaretoken]')?.value;
        
        const response = await fetch(`/notification/mark-as-read/${notificationId}/`, {
            method: 'POST',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'Content-Type': 'application/json',
                'X-CSRFToken': csrf
            },
            credentials: 'same-origin'
        });
        
        if (response.ok) {
            // Update UI
            const notificationItem = document.querySelector(`.notification-item[data-id="${notificationId}"]`);
            if (notificationItem) {
                notificationItem.classList.remove('unread');
                
                // Remove mark as read button
                const markReadBtn = notificationItem.querySelector('button');
                if (markReadBtn) {
                    markReadBtn.remove();
                }
            }
            
            // Update badge count
            const badge = document.querySelector('.notification-badge');
            if (badge) {
                const currentCount = parseInt(badge.textContent);
                if (currentCount > 1) {
                    badge.textContent = currentCount - 1;
                } else {
                    badge.style.display = 'none';
                }
            }
        }
    } catch (error) {
        console.error('Error marking notification as read:', error);
    }
}

// Mark all notifications as read
async function markAllAsRead(event) {
    event.preventDefault();
    
    try {
        const csrf = document.querySelector('[name=csrfmiddlewaretoken]')?.value;
        
        const response = await fetch('/notification/mark-all-as-read/', {
            method: 'POST',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'Content-Type': 'application/json',
                'X-CSRFToken': csrf
            },
            credentials: 'same-origin'
        });
        
        if (response.ok) {
            // Refresh notifications
            fetchNotifications();
            
            // Hide badge
            const badge = document.querySelector('.notification-badge');
            if (badge) {
                badge.style.display = 'none';
            }
        }
    } catch (error) {
        console.error('Error marking all notifications as read:', error);
    }
}

// Render error state
function renderErrorState() {
    const dropdown = document.getElementById('notificationDropdown');
    
    dropdown.innerHTML = `
        <div class="notification-dropdown-header">
            <h4><i class="fas fa-exclamation-circle mr-2"></i>Error</h4>
        </div>
        <div class="empty-notifications">
            <i class="fas fa-exclamation-triangle"></i>
            <h5>Something went wrong</h5>
            <p>Could not load notifications</p>
            <button onclick="fetchNotifications()" class="btn btn-sm btn-primary mt-3">Try Again</button>
        </div>
    `;
}
