document.addEventListener('DOMContentLoaded', function() {
    // Initialize checkboxes for ingredients
    const ingredientsList = document.querySelectorAll('.ingredient-item');
    ingredientsList.forEach(item => {
        item.addEventListener('click', function() {
            this.classList.toggle('checked');
        });
    });

    // Step progress tracking
    const stepItems = document.querySelectorAll('.step-item');
    stepItems.forEach(step => {
        step.addEventListener('click', function() {
            this.classList.toggle('completed');
        });
    });

    // Timer functionality
    let currentTimer = null;
    let remainingTime = 0;
    let isPaused = false;

    const timerDisplay = document.getElementById('timer-display');
    const startTimerBtn = document.getElementById('start-timer');
    const pauseTimerBtn = document.getElementById('pause-timer');
    const resetTimerBtn = document.getElementById('reset-timer');

    if (startTimerBtn) {
        startTimerBtn.addEventListener('click', function() {
            const cookingTime = parseInt(this.dataset.time);
            if (isPaused) {
                currentTimer = startTimer(remainingTime / 60);
                isPaused = false;
                this.innerHTML = '<i class="fas fa-play"></i> Start';
            } else {
                if (currentTimer) {
                    clearInterval(currentTimer);
                }
                currentTimer = startTimer(cookingTime);
            }
            pauseTimerBtn.disabled = false;
            this.disabled = true;
        });
    }

    if (pauseTimerBtn) {
        pauseTimerBtn.addEventListener('click', function() {
            if (currentTimer) {
                clearInterval(currentTimer);
                currentTimer = null;
                isPaused = true;
                startTimerBtn.disabled = false;
                startTimerBtn.innerHTML = '<i class="fas fa-play"></i> Resume';
                this.disabled = true;
            }
        });
    }

    if (resetTimerBtn) {
        resetTimerBtn.addEventListener('click', function() {
            if (currentTimer) {
                clearInterval(currentTimer);
            }
            timerDisplay.textContent = "00:00";
            startTimerBtn.disabled = false;
            pauseTimerBtn.disabled = true;
            startTimerBtn.innerHTML = '<i class="fas fa-play"></i> Start';
            isPaused = false;
            remainingTime = 0;
        });
    }

    function startTimer(duration) {
        remainingTime = duration * 60;

        return setInterval(() => {
            const minutes = parseInt(remainingTime / 60, 10);
            const seconds = parseInt(remainingTime % 60, 10);

            timerDisplay.textContent = `${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;

            if (--remainingTime < 0) {
                clearInterval(currentTimer);
                timerDisplay.textContent = "Time's up!";
                startTimerBtn.disabled = false;
                pauseTimerBtn.disabled = true;
                new Audio('/static/sounds/timer-done.mp3').play();
            }
        }, 1000);
    }
});
