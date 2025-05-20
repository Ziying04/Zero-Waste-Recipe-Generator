let map;
let marker;

function showMap() {
    document.getElementById("map").style.display = "block";

    if (!map) {
        map = L.map('map').setView([3.1390, 101.6869], 12);

        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '© OpenStreetMap contributors'
        }).addTo(map);

        map.on('click', function(e) {
            if (marker) {
                map.removeLayer(marker);
            }
            marker = L.marker(e.latlng).addTo(map);
            document.getElementById("user_lat").value = e.latlng.lat;
            document.getElementById("user_lon").value = e.latlng.lng;
            document.getElementById("filterForm").submit();
        });
    }
}

document.addEventListener('DOMContentLoaded', function () {
  const slider = document.getElementById('distance');
  const sliderLine = document.querySelector('.slider-line');
  const mileDisplay = document.getElementById('mile-display');
  const tooltip = document.getElementById('mile-tooltip');

  function updateSlider(value) {
    const max = slider.max || 50;
    const min = slider.min || 0;
    const percentage = ((value - min) / (max - min)) * 100;

    sliderLine.style.width = `${percentage}%`;
    mileDisplay.textContent = value;
    tooltip.textContent = `${value} mi`;
    tooltip.style.left = `calc(${percentage}% - 20px)`;
    tooltip.style.display = 'block';
  }

  if (slider && sliderLine && mileDisplay && tooltip) {
    updateSlider(slider.value);

    slider.addEventListener('input', function (e) {
      updateSlider(e.target.value);
    });

    slider.addEventListener('blur', function () {
      tooltip.style.display = 'none';
    });
  }
});


