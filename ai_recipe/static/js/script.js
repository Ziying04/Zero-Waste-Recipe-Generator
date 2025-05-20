document.getElementById("generate-btn").addEventListener("click", async () => {
    const ingredients = document.getElementById("ingredients").value;
    const recipeOutput = document.getElementById("recipe-output");

    if (!ingredients.trim()) {
        recipeOutput.value = "Please enter some ingredients.";
        return;
    }

    recipeOutput.value = "Generating recipe...";

    try {
        const response = await fetch("/api/generate/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ ingredients: ingredients.split(",").map(i => i.trim()) }),
        });

        const data = await response.json();

        if (response.ok) {
            recipeOutput.value = data.recipe;
        } else {
            recipeOutput.value = data.error || "An error occurred while generating the recipe.";
        }
    } catch (error) {
        recipeOutput.value = "Failed to connect to the server.";
    }
});
