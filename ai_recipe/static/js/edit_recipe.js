document.addEventListener('DOMContentLoaded', function() {
    const recipe = document.querySelector('.recipe-edit');
    const editableFields = document.querySelectorAll('.editable-field');
    const saveButton = document.querySelector('.save-button');

    // Make fields editable on page load
    editableFields.forEach(field => {
        field.contentEditable = true;
    });

    saveButton.addEventListener('click', async () => {
        const recipeId = recipe.dataset.recipeId;
        const updatedData = {};
        
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
                alert('Recipe updated successfully!');
                window.location.href = '/api/sharing/';
            } else {
                throw new Error(data.error || 'Failed to update recipe');
            }
        } catch (error) {
            alert(error.message);
            console.error('Error:', error);
        }
    });
});
