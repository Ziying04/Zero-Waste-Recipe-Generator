document.addEventListener('DOMContentLoaded', function() {
    // Add hover effect to sections
    const sections = document.querySelectorAll('.section');
    sections.forEach(section => {
        section.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
        });
        
        section.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });

    // Load stats if available
    const loadStats = async () => {
        try {
            const response = await fetch('/api/diary/stats/');
            if (response.ok) {
                const stats = await response.json();
                updateStats(stats);
            }
        } catch (error) {
            console.error('Error loading stats:', error);
        }
    };

    const updateStats = (stats) => {
        if (stats.likes) {
            document.getElementById('likes-count').textContent = stats.likes;
        }
        if (stats.saved) {
            document.getElementById('saved-count').textContent = stats.saved;
        }
        if (stats.recipes) {
            document.getElementById('recipes-count').textContent = stats.recipes;
        }
    };

    loadStats();

    initializeEditControls();
});

function initializeEditControls() {
    document.querySelectorAll('.shared-recipe').forEach(recipe => {
        const editBtn = recipe.querySelector('.edit-button');
        const saveBtn = recipe.querySelector('.save-button');
        const cancelBtn = recipe.querySelector('.cancel-button');
        const editableFields = recipe.querySelectorAll('.editable-field');
        
        let originalValues = {};

        editBtn?.addEventListener('click', () => {
            recipe.classList.add('editing');
            editableFields.forEach(field => {
                originalValues[field.dataset.field] = field.textContent;
                field.contentEditable = true;
            });
            saveBtn.style.display = 'inline-block';
            cancelBtn.style.display = 'inline-block';
            editBtn.style.display = 'none';
        });

        saveBtn?.addEventListener('click', async () => {
            const recipeId = recipe.dataset.recipeId;
            const updatedData = {};
            editableFields.forEach(field => {
                updatedData[field.dataset.field] = field.textContent;
            });

            try {
                const response = await fetch(`/api/recipe/${recipeId}/update/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                    },
                    body: JSON.stringify(updatedData)
                });

                if (response.ok) {
                    recipe.classList.remove('editing');
                    editableFields.forEach(field => field.contentEditable = false);
                    saveBtn.style.display = 'none';
                    cancelBtn.style.display = 'none';
                    editBtn.style.display = 'inline-block';
                    alert('Recipe updated successfully!');
                } else {
                    throw new Error('Failed to update recipe');
                }
            } catch (error) {
                alert('Error updating recipe');
                console.error(error);
            }
        });

        cancelBtn?.addEventListener('click', () => {
            recipe.classList.remove('editing');
            editableFields.forEach(field => {
                field.textContent = originalValues[field.dataset.field];
                field.contentEditable = false;
            });
            saveBtn.style.display = 'none';
            cancelBtn.style.display = 'none';
            editBtn.style.display = 'inline-block';
        });
    });
}

