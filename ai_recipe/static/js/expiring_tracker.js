let ingredients = []
let currentTab = "all"


function toggleForm() {
  const form = document.getElementById("form")
  const noData = document.getElementById("no-data")
  form.classList.toggle("hidden")
  noData.classList.toggle("hidden")
}

const ingredientsByCategory = {
  "Vegetables": ["Carrot", "Spinach", "Broccoli", "Onion", "Cabbage", "Potato"],
  "Fruits": ["Apple", "Banana", "Mango", "Strawberry", "Orange"],
  "Dairy": ["Milk", "Cheese", "Butter", "Yogurt"],
  "Meat": ["Chicken", "Beef", "Pork", "Lamb"],
  "Seafood": ["Salmon", "Shrimp", "Tuna", "Crab"],
  "Grains & Pasta": ["Rice", "Spaghetti", "Bread", "Oats"],
  "Bakery": ["Baguette", "Croissant", "Muffin"],
  "Frozen Foods": ["Frozen Peas", "Frozen Pizza", "Ice Cream"],
  "Beverages": ["Milk", "Juice", "Coffee", "Tea"],
  "Snacks": ["Chips", "Chocolate", "Cookies"]
};

const form = document.getElementById('ingredient-form');
const categorySelect = document.getElementById('category');
const nameSelect = document.getElementById('name');
const customCategoryInput = document.getElementById('custom-category');
const customNameInput = document.getElementById('custom-name');

// When Category changes
categorySelect.addEventListener('change', function() {
  const selectedCategory = this.value;

  // Reset Ingredient dropdown
  nameSelect.innerHTML = '<option value="">Select Ingredient</option>';
  customCategoryInput.classList.add('hidden');

  if (selectedCategory === 'Others') {
    // Show custom category input
    toggleCustomCategoryInput(true);
    nameSelect.innerHTML = '<option value="">Others</option>';
    toggleCustomNameInput(true);
    inputIngredient();
  } else {
    toggleCustomNameInput(false);
    // Populate ingredient list based on selected category
    const ingredients = ingredientsByCategory[selectedCategory] || [];
    ingredients.forEach(ingredient => {
      const option = document.createElement('option');
      option.value = ingredient;
      option.textContent = ingredient;
      nameSelect.appendChild(option);
    });
  }
});

// When Ingredient changes
  nameSelect.addEventListener('change', function() {
    const selectedIngredient = this.value;

    if (selectedIngredient === 'Others') {
      toggleCustomNameInput(true);
    } else {
      toggleCustomNameInput(false);
    }
  });


function toggleCustomNameInput(show) {
  if (show) {
    customNameInput.classList.remove('hidden');
  } else {
    customNameInput.classList.add('hidden');
  }
}

function toggleCustomCategoryInput(show) {
  if (show) {
    customCategoryInput.classList.remove('hidden');
  } else {
    customCategoryInput.classList.add('hidden');
  }
}

function inputIngredient(){
  const option = document.createElement('option');
    option.value = "Others";
    option.textContent = "Others";
    nameSelect.appendChild(option);
}

// If user selects Category, but still want "Others" in Ingredient options
categorySelect.addEventListener('change', function() {
  if (this.value !== "Others") {
    inputIngredient();
  }
});

form.addEventListener('submit', function(event) {
  if (categorySelect.value === 'Others') {
    // Swap: remove name from select, add name to custom input
    categorySelect.removeAttribute('name');
    customCategoryInput.setAttribute('name', 'category');
  }

  if(nameSelect.value === 'Others') {
    // Swap: remove name from select, add name to custom input
    nameSelect.removeAttribute('name');
    customNameInput.setAttribute('name', 'name');
  }
});


document.querySelectorAll('.tab').forEach(tab => {
  tab.addEventListener('click', function () {
    // Remove active class from all tabs
    document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
    this.classList.add('active');

    const selected = this.getAttribute('data-tab');
    const cards = document.querySelectorAll('.ingredient');

    cards.forEach(card => {
      const status = card.getAttribute('data-status');

      if (
        selected === 'all' ||
        (selected === 'expiring' && status === 'expiring soon') ||
        (selected === 'expired' && status === 'expired') ||
        (selected === 'fresh' && status === 'fresh')
      ) {
        card.style.display = 'block';
      } else {
        card.style.display = 'none';
      }
    });
  });
});


document.addEventListener("DOMContentLoaded", function () {
  const deleteForms = document.querySelectorAll(".delete-form");

  deleteForms.forEach(form => {
    form.addEventListener("submit", function (e) {
      e.preventDefault(); // Stop form from submitting right away

      Swal.fire({
        title: "Are you sure?",
        text: "This will delete the ingredient.",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#d33",
        cancelButtonColor: "#3085d6",
        confirmButtonText: "Yes, delete it",
      }).then((result) => {
        if (result.isConfirmed) {
          form.submit(); 
        }
      });
    });
  });
});



