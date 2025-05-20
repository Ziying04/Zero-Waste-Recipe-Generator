import requests
import logging
from django.conf import settings

def generate_recipe(ingredients):
    url = "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1"
    headers = {"Authorization": f"Bearer {settings.HUGGINGFACE_API_KEY}"}
    
    prompt = (
        f"Generate a recipe using ONLY the following ingredients: {', '.join(ingredients)}. "
        "Do not include any other ingredients. "
        "Be creative but stick to the list exactly. Return the recipe in the format: Title, Ingredients, and Instructions."
    )
    
    response = requests.post(url, headers=headers, json={"inputs": prompt})
    
    if response.status_code == 200:
        output = response.json()[0]["generated_text"]

        if output.startswith(prompt):
            cleaned_output = output[len(prompt):].lstrip()  # Remove the prompt and leading whitespace
        else:
            cleaned_output = output

        return cleaned_output
    else:
        return f"Error: {response.status_code}, {response.text}"
