import requests
import logging
from django.conf import settings
from urllib.parse import unquote as urlunquote
import re

def generate_recipe(ingredients):
    url = "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1"
    headers = {"Authorization": f"Bearer {settings.HUGGINGFACE_API_KEY}"}
    
    prompt = (
        f"Generate a recipe using ONLY the following ingredients: {', '.join(ingredients)}. "
        "Do not include any other ingredients. "
        "Be creative but stick to the list exactly. Return the recipe in the format: Title, Cooking Time, Ingredients, Instructions and sample image urls."
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
    


def parse_ai_recipe(recipe_text):
    title_match = re.search(r"Title\s*:\s*(.+)", recipe_text)
    time_match = re.search(r"Cooking Time\s*:\s*(\d+)", recipe_text)
    ingredients_match = re.search(r"Ingredients\s*:\s*(.+?)(?:Instructions|$)", recipe_text, re.DOTALL)
    steps_match = re.search(r"Instructions\s*:\s*(.+?)(?:Image|$)", recipe_text, re.DOTALL)
    image_match = re.search(r"(https?://[^\s]+(?:\.jpg|\.jpeg|\.png|\.webp))", recipe_text)

    ingredients_raw = ingredients_match.group(1).strip() if ingredients_match else ""
    steps_raw = steps_match.group(1).strip() if steps_match else ""

    # Split ingredients and steps into list items
    ingredients_list = [line.strip("-•* \n") for line in ingredients_raw.strip().splitlines() if line.strip()]
    steps_list = [line.strip("0123456789). \n") for line in steps_raw.strip().splitlines() if line.strip()]

    return {
        "name": title_match.group(1).strip() if title_match else "Untitled AI Recipe",
        "cooking_time": int(time_match.group(1)) if time_match else 30,
        "ingredients": ingredients_list,
        "steps": steps_list,
        "image_url": image_match.group(1).strip() if image_match else None
    }
