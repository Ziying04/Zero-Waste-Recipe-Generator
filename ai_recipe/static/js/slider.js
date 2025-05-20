document.addEventListener('DOMContentLoaded', function () {
  const slider = document.getElementById('distance');
  const sliderLine = document.querySelector('.slider-line');
  const mileDisplay = document.getElementById('mile-display');
  const tooltip = document.getElementById('mile-tooltip');

  function updateSlider(value) {
    const max = slider.max || 50;
    const min = slider.min || 0;
    const percentage = ((value - min) / (max - min)) * 100;

    // Update line width and fixed display
    sliderLine.style.width = `${percentage}%`;
    mileDisplay.textContent = value;

    // Update tooltip
    tooltip.textContent = `${value} mi`;
    tooltip.style.left = `calc(${percentage}% - 20px)`; // Adjust tooltip to center over thumb
    tooltip.classList.remove('hidden');
  }

  if (slider && sliderLine && mileDisplay && tooltip) {
    updateSlider(slider.value);

    slider.addEventListener('input', function (e) {
      updateSlider(e.target.value);
    });

    slider.addEventListener('change', function () {
      tooltip.classList.add('hidden'); // Hide tooltip after interaction if desired
    });

    slider.addEventListener('blur', function () {
      tooltip.classList.add('hidden');
    });
  }
});
