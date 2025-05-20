document.addEventListener('DOMContentLoaded', () => {
    const ingredientInput = document.getElementById('ingredient-input');
    const addButton = document.querySelector('.btn-add');
    const ingredientBadges = document.getElementById('ingredient-badges');
  
    addButton.addEventListener('click', () => {
      const ingredient = ingredientInput.value.trim();
      if (ingredient) {
        const badge = document.createElement('span');
        badge.classList.add('badge');
        badge.innerHTML = `${ingredient} <button class="remove-badge">×</button>`;
        ingredientBadges.appendChild(badge);
        ingredientInput.value = ''; // Clear input after adding
  
        // Remove badge functionality
        badge.querySelector('.remove-badge').addEventListener('click', () => {
          badge.remove();
        });
      }
    });
  });
  