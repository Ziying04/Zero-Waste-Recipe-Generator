// Notification dropdown toggle
function toggleNotificationDropdown() {
    const dropdown = document.getElementById('notificationDropdown');
    dropdown.classList.toggle('show');
    
    if (dropdown.classList.contains('show')) {
        // Fetch latest notifications when opening dropdown
        fetchNotifications();
    }
}

// Close notification dropdown when clicking outside
document.addEventListener('click', function(event) {
    const dropdown = document.getElementById('notificationDropdown');
    const notificationBtn = document.querySelector('.notification-button');
    
    if (dropdown && dropdown.classList.contains('show') && 
        !dropdown.contains(event.target) && 
        !notificationBtn.contains(event.target)) {
        dropdown.classList.remove('show');
    }
});

// Fetch notifications via AJAX
function fetchNotifications() {
    fetch('/notification/api/get-notifications/')
        .then(response => response.json())
        .then(data => {
            renderNotifications(data.notifications);
        })
        .catch(error => console.error('Error fetching notifications:', error));
}

// Render notifications in dropdown
function renderNotifications(notifications) {
    const dropdown = document.getElementById('notificationDropdown');
    let content = '<h4>Notifications</h4>';
    
    if (notifications.length === 0) {
        content += '<div class="empty-notifications">No notifications</div>';
    } else {
        content += '<ul class="notification-list">';
        notifications.forEach(notification => {
            const icon = getNotificationIcon(notification.type);
            const readClass = notification.is_read ? '' : 'unread';
            
            content += `
                <li class="notification-item ${readClass}">
                    <div class="notification-icon">${icon}</div>
                    <div class="notification-content">
                        <p>${notification.content}</p>
                        <small>${notification.created_at}</small>
                    </div>
                    ${notification.link ? `<a href="${notification.link}">View</a>` : ''}
                    ${!notification.is_read ? 
                      `<button onclick="markAsRead(${notification.id}, event)">Mark as read</button>` : ''}
                </li>
            `;
        });
        content += '</ul>';
        content += '<a href="/notification/" class="view-all">View All</a>';
    }
    
    dropdown.innerHTML = content;
}

// Get icon based on notification type
function getNotificationIcon(type) {
    switch(type) {
        case 'like':
            return '<i class="fas fa-heart"></i>';
        case 'expiry':
            return '<i class="fas fa-exclamation-triangle"></i>';
        case 'admin_warning':
            return '<i class="fas fa-shield-alt"></i>';
        default:
            return '<i class="fas fa-bell"></i>';
    }
}

// Mark notification as read
function markAsRead(notificationId, event) {
    event.preventDefault();
    event.stopPropagation();
    
    fetch(`/notification/mark-as-read/${notificationId}/`, {
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            // Refresh notifications
            fetchNotifications();
            
            // Update badge count
            const countBadge = document.querySelector('.notification-count');
            if (countBadge) {
                const currentCount = parseInt(countBadge.textContent);
                if (currentCount > 1) {
                    countBadge.textContent = currentCount - 1;
                } else {
                    countBadge.style.display = 'none';
                }
            }
        }
    })
    .catch(error => console.error('Error marking notification as read:', error));
}
