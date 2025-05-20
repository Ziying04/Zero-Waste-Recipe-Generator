// Modal functionality
function openShareModal() {
    document.getElementById('shareModal').style.display = 'block';
}

function closeShareModal() {
    document.getElementById('shareModal').style.display = 'none';
}

// Filter posts by state
function filterPosts() {
    const state = document.getElementById('stateFilter').value;
    const posts = document.querySelectorAll('.post-card');
    
    posts.forEach(post => {
        if (!state || post.dataset.state === state) {
            post.style.display = 'block';
        } else {
            post.style.display = 'none';
        }
    });
}

// Sort posts
function sortPosts() {
    const sortBy = document.getElementById('sortBy').value;
    const postsContainer = document.querySelector('.posts-container');
    const posts = Array.from(document.querySelectorAll('.post-card'));
    
    posts.sort((a, b) => {
        const dateA = new Date(a.querySelector('.post-details span').textContent);
        const dateB = new Date(b.querySelector('.post-details span').textContent);
        
        return sortBy === 'recent' ? dateB - dateA : dateA - dateB;
    });
    
    posts.forEach(post => postsContainer.appendChild(post));
}

// Contact functionality
function contactUser(email) {
    window.location.href = `mailto:${email}`;
}

// Close modal when clicking outside
window.onclick = function(event) {
    const modal = document.getElementById('shareModal');
    if (event.target == modal) {
        modal.style.display = 'none';
    }
}

// Form submission handling
document.getElementById('shareForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);

    // Get CSRF token from the cookie
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
    const csrftoken = getCookie('csrftoken');

    try {
        const response = await fetch('/api/community/share', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': csrftoken
            }
        });

        if (response.ok) {
            closeShareModal();
            location.reload();
        } else {
            alert('Error sharing food post. Please try again.');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error sharing food post. Please try again.');
    }
});
