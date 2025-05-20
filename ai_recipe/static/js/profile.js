document.addEventListener("DOMContentLoaded", () => {
  const modal = document.getElementById("edit-profile-modal");
  const editBtn = document.getElementById("edit-profile-btn");
  const closeBtn = modal.querySelector(".close");

  editBtn.addEventListener("click", () => {
    modal.style.display = "flex";
  });

  closeBtn.addEventListener("click", () => {
    modal.style.display = "none";
  });

  window.addEventListener("click", (event) => {
    if (event.target === modal) {
      modal.style.display = "none";
    }
  });

  const form = document.getElementById("edit-profile-form");
  form.addEventListener("submit", (event) => {
    event.preventDefault();
    // Add AJAX request to update profile details
    alert("Profile updated successfully!");
    modal.style.display = "none";
  });
});
