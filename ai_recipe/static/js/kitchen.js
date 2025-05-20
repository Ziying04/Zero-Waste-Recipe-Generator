document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('recipe-search');
    const recipeCards = document.querySelectorAll('.col-12.col-md-6.col-lg-4');

    searchInput.addEventListener('input', function(e) {
        const searchTerm = e.target.value.toLowerCase().trim();

        recipeCards.forEach(card => {
            const recipeName = card.querySelector('.recipe-card-title a').textContent.toLowerCase();
            const isVisible = recipeName.includes(searchTerm);
            card.style.display = isVisible ? '' : 'none';
        });

        // Show "no results" message if no matches
        const noResults = document.querySelector('.no-results');
        const hasVisibleCards = Array.from(recipeCards).some(card => card.style.display !== 'none');
        
        if (!hasVisibleCards && !noResults) {
            const message = document.createElement('div');
            message.className = 'col-12 no-results';
            message.innerHTML = '<p class="text-center text-muted">No recipes found matching your search.</p>';
            document.getElementById('recipe-grid').appendChild(message);
        } else if (hasVisibleCards && noResults) {
            noResults.remove();
        }
    });

    document.querySelectorAll(".save-btn").forEach((button) => {
        button.addEventListener("click", async function () {
            const recipeId = this.dataset.recipeId;
            const url = `/api/recipe/${recipeId}/save/`;

            try {
                const response = await fetch(url, {
                    method: "POST",
                    headers: {
                        "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value,
                        "Content-Type": "application/json",
                    },
                });

                if (response.ok) {
                    const data = await response.json();
                    const icon = this.querySelector("i");
                    const countSpan = this.querySelector(".save-count");

                    this.dataset.saved = data.saved;
                    icon.style.color = data.saved ? "#ffd700" : "#000";
                    alert(data.message || "Recipe saved successfully!");
                    countSpan.textContent = data.count;
                } else {
                    const errorData = await response.json();
                    console.error("Error Response:", errorData);
                    alert(errorData.error || "An error occurred. Please try again.");
                }
            } catch (error) {
                console.error("Error:", error);
                alert("An error occurred. Please try again.");
            }
        });
    });

    document.querySelectorAll(".like-btn").forEach((button) => {
        button.addEventListener("click", async function () {
            const recipeId = this.dataset.recipeId;
            const url = `/api/recipe/${recipeId}/like/`;
            const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

            try {
                const response = await fetch(url, {
                    method: "POST",
                    headers: {
                        "X-CSRFToken": csrfToken,
                        "Content-Type": "application/json",
                    },
                    credentials: 'include'
                });

                if (response.ok) {
                    const data = await response.json();
                    const icon = this.querySelector("i");
                    const countSpan = this.querySelector(".like-count");
                    
                    this.dataset.liked = data.liked;
                    icon.style.color = data.liked ? "#ff4b4b" : "#000";
                    countSpan.textContent = data.count;
                    
                    // Show success message
                    const message = data.liked ? "Recipe added to likes" : "Recipe removed from likes";
                    alert(message);
                } else {
                    const errorData = await response.json();
                    if (response.status === 401) {
                        alert("Please login to like recipes");
                        window.location.href = '/api/login/';
                    } else {
                        alert(errorData.error || "An error occurred while updating like");
                    }
                }
            } catch (error) {
                console.error("Error:", error);
                alert("An error occurred. Please try again.");
            }
        });
    });
});
