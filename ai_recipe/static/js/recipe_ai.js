// Handle form switching
document.getElementById("use-text").addEventListener("click", () => {
  document.getElementById("generate-btn").dataset.target = "recipe-form";
});

document.getElementById("use-inventory").addEventListener("click", () => {
  document.getElementById("generate-btn").dataset.target = "ingredient-form";
});


// Handle form submission
document.getElementById("generate-btn").addEventListener("click", function () {
  const formId = this.dataset.target;
  const form = document.getElementById(formId);
  const btn = this;
  const spinner = btn.querySelector(".spinner");

  btn.disabled = true;
  if (spinner) spinner.style.display = "inline-block";

  fetch(form.action, {
    method: "POST",
    body: new FormData(form),
    headers: {
      "X-CSRFToken": form.querySelector("[name=csrfmiddlewaretoken]").value,
    },
  })
    .then((res) => res.text())
    .then((data) => {
      document.getElementById("output-section").classList.remove("hidden");
      document.getElementById("recipe-output").value = data;
    })
    .catch((err) => {
      console.error("Error:", err);
      alert("Something went wrong. Try again.");
    })
    .finally(() => {
      btn.disabled = false;
      if (spinner) spinner.style.display = "none";
    });
});

  function copyRecipe() {
    const recipeText = document.getElementById("recipe-output");
    recipeText.select();
    document.execCommand("copy");
    const copyBtn = document.querySelector(".copy-btn");
    copyBtn.innerHTML = '<i class="fas fa-check"></i> Copied!';
    setTimeout(() => {
      copyBtn.innerHTML = '<i class="fas fa-copy"></i> Copy';
    }, 2000);
  }

  function autoResizeTextarea(textarea) {
    textarea.style.height = "auto"; // Reset height
    textarea.style.height = textarea.scrollHeight + "px"; // Set to scroll height
  }

  document.querySelectorAll('.tab').forEach(tab => {
  tab.addEventListener('click', function () {
    // Remove active class from all tabs
    document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
    this.classList.add('active');

    const selected = this.getAttribute('data-tab');
    if(selected === 'input'){
      document.getElementById('recipe-form').classList.remove('hidden');
      document.getElementById('available-ingredient').classList.add('hidden');
    }else{
      document.getElementById('recipe-form').classList.add('hidden');
      document.getElementById('available-ingredient').classList.remove('hidden');

    }

  });
});

function toggleSelect(checkbox) {
    const card = checkbox.closest('.ingredient-card');
    if (checkbox.checked) {
      card.classList.add('selected');
    } else {
      card.classList.remove('selected');
    }
  }

  // Handle page load state (keep selected cards green if reloaded with checked boxes)
  window.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.select-checkbox').forEach(checkbox => {
      if (checkbox.checked) {
        checkbox.closest('.ingredient-card').classList.add('selected');
      }
    });
  });