document.addEventListener('DOMContentLoaded', function() {
    const recipes = document.querySelectorAll('.shared-recipe');

    recipes.forEach(recipe => {
        const editBtn = recipe.querySelector('.edit-button');
        const saveBtn = recipe.querySelector('.save-button');
        const cancelBtn = recipe.querySelector('.cancel-button');
        const editableFields = recipe.querySelectorAll('.editable-field');
        
        let originalValues = {};

        editBtn?.addEventListener('click', () => {
            // Store original values and enable editing
            editableFields.forEach(field => {
                originalValues[field.dataset.field] = field.textContent.trim();
                field.contentEditable = true;
                field.classList.add('editing');
            });

            // Toggle button visibility
            editBtn.style.display = 'none';
            saveBtn.style.display = 'inline-block';
            cancelBtn.style.display = 'inline-block';
        });

        saveBtn?.addEventListener('click', async () => {
            const recipeId = recipe.dataset.recipeId;
            const updatedData = {};
            
            // Collect updated values
            editableFields.forEach(field => {
                updatedData[field.dataset.field] = field.textContent.trim();
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

                const data = await response.json();

                if (response.ok) {
                    // Disable editing and update UI
                    editableFields.forEach(field => {
                        field.contentEditable = false;
                        field.classList.remove('editing');
                    });
                    
                    // Toggle button visibility
                    saveBtn.style.display = 'none';
                    cancelBtn.style.display = 'none';
                    editBtn.style.display = 'inline-block';
                    
                    alert('Recipe updated successfully!');
                } else {
                    throw new Error(data.error || 'Failed to update recipe');
                }
            } catch (error) {
                alert(error.message);
                console.error('Error:', error);
            }
        });

        cancelBtn?.addEventListener('click', () => {
            // Restore original values and disable editing
            editableFields.forEach(field => {
                field.textContent = originalValues[field.dataset.field];
                field.contentEditable = false;
                field.classList.remove('editing');
            });

            // Toggle button visibility
            saveBtn.style.display = 'none';
            cancelBtn.style.display = 'none';
            editBtn.style.display = 'inline-block';
        });
    });
});
