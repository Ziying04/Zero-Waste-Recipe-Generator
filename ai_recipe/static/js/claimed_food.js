// Claimed Food Interactive Features
class ClaimedFoodUI {
    constructor() {
        this.init();
        this.setupEventListeners();
        this.animateCards();
        this.setupProgressBars();
        this.setupTooltips();
    }

    init() {
        // Add loading animation to cards
        this.addLoadingAnimation();
        
        // Setup intersection observer for animations
        this.setupIntersectionObserver();
        
        // Initialize particle background
        this.initParticleBackground();
        
        // Setup real-time status updates
        this.setupStatusUpdates();
    }

    addLoadingAnimation() {
        const cards = document.querySelectorAll('.card');
        cards.forEach((card, index) => {
            card.style.opacity = '0';
            card.style.transform = 'translateY(50px)';
            
            setTimeout(() => {
                card.style.transition = 'all 0.6s cubic-bezier(0.4, 0, 0.2, 1)';
                card.style.opacity = '1';
                card.style.transform = 'translateY(0)';
            }, index * 150);
        });
    }

    setupIntersectionObserver() {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate-in');
                    this.animateCounter(entry.target);
                }
            });
        }, {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        });

        // Observe stat cards
        document.querySelectorAll('.stat-card').forEach(card => {
            observer.observe(card);
        });

        // Observe main cards
        document.querySelectorAll('.card').forEach(card => {
            observer.observe(card);
        });
    }

    animateCounter(element) {
        const counter = element.querySelector('.stat-number');
        if (!counter) return;

        const target = parseInt(counter.textContent);
        const duration = 2000;
        const increment = target / (duration / 16);
        let current = 0;

        const timer = setInterval(() => {
            current += increment;
            if (current >= target) {
                current = target;
                clearInterval(timer);
            }
            counter.textContent = Math.floor(current);
        }, 16);
    }    setupEventListeners() {
        // Message button interactions
        document.querySelectorAll('.button.message').forEach(button => {
            button.addEventListener('click', this.handleMessageClick.bind(this));
        });

        // Mark as completed form submissions
        document.querySelectorAll('form[action*="mark_received"]').forEach(form => {
            form.addEventListener('submit', this.handleMarkCompletedForm.bind(this));
        });

        // Card hover effects
        document.querySelectorAll('.card').forEach(card => {
            card.addEventListener('mouseenter', this.handleCardHover.bind(this));
            card.addEventListener('mouseleave', this.handleCardLeave.bind(this));
        });

        // Add click sound effects
        this.setupSoundEffects();

        // Setup keyboard navigation
        this.setupKeyboardNavigation();
    }

    handleMarkCompletedForm(event) {
        event.preventDefault();
        const form = event.currentTarget;
        const button = form.querySelector('.button.success');
        const card = form.closest('.card');
        
        // Add ripple effect (we need to create a fake event for this)
        const fakeEvent = {
            clientX: button.getBoundingClientRect().left + button.offsetWidth / 2,
            clientY: button.getBoundingClientRect().top + button.offsetHeight / 2
        };
        this.addRippleEffect(button, fakeEvent);
        
        // Show confirmation
        this.showCompletionConfirmation(card, button, form);
    }

    handleMessageClick(event) {
        event.preventDefault();
        const button = event.currentTarget;
        
        // Add ripple effect
        this.addRippleEffect(button, event);
        
        // Animate button
        button.style.transform = 'scale(0.95)';
        setTimeout(() => {
            button.style.transform = 'scale(1)';
        }, 150);

        // Show message modal (placeholder)
        this.showMessageModal();
    }    handleCardHover(event) {
        const card = event.currentTarget;
        // Add subtle glow effect
        card.style.boxShadow = '0 25px 50px rgba(0, 0, 0, 0.15), 0 10px 24px rgba(0, 0, 0, 0.1), 0 0 20px rgba(102, 126, 234, 0.3)';
    }

    handleCardLeave(event) {
        const card = event.currentTarget;
        // Remove glow effect
        card.style.boxShadow = '';
    }showCompletionConfirmation(card, button, form = null) {
        // Create confirmation overlay
        const overlay = document.createElement('div');
        overlay.className = 'confirmation-overlay';
        overlay.innerHTML = `
            <div class="confirmation-modal">
                <div class="confirmation-icon">
                    <i class="fas fa-check-circle"></i>
                </div>
                <h3>Mark as Completed?</h3>
                <p>Confirm that you have received this food item.</p>
                <div class="confirmation-buttons">
                    <button class="button cancel">Cancel</button>
                    <button class="button success confirm">Yes, Completed</button>
                </div>
            </div>
        `;

        document.body.appendChild(overlay);

        // Add styles for the overlay
        this.addConfirmationStyles();

        // Animate in
        setTimeout(() => {
            overlay.classList.add('show');
        }, 10);

        // Handle button clicks
        overlay.querySelector('.cancel').addEventListener('click', () => {
            this.closeConfirmation(overlay);
        });

        overlay.querySelector('.confirm').addEventListener('click', () => {
            if (form) {
                // Submit the actual form
                form.submit();
            } else {
                // Fallback for direct button clicks
                this.markAsCompleted(card, button);
            }
            this.closeConfirmation(overlay);
        });

        // Close on outside click
        overlay.addEventListener('click', (e) => {
            if (e.target === overlay) {
                this.closeConfirmation(overlay);
            }
        });
    }

    closeConfirmation(overlay) {
        overlay.classList.remove('show');
        setTimeout(() => {
            overlay.remove();
        }, 300);
    }

    markAsCompleted(card, button) {
        // Update badge
        const badge = card.querySelector('.badge');
        badge.textContent = 'Completed';
        badge.className = 'badge completed';

        // Update progress bar
        const progressFill = card.querySelector('.progress-fill');
        if (progressFill) {
            progressFill.className = 'progress-fill completed';
        }

        // Remove the completion button
        button.style.transform = 'scale(0)';
        button.style.opacity = '0';
        setTimeout(() => {
            button.remove();
        }, 300);

        // Add completion animation
        this.addCompletionAnimation(card);

        // Show success message
        this.showSuccessToast('Food marked as completed! 🎉');
    }

    addCompletionAnimation(card) {
        // Add confetti effect
        this.createConfetti(card);

        // Pulse animation
        card.style.animation = 'pulse 0.6s ease-out';
        setTimeout(() => {
            card.style.animation = '';
        }, 600);
    }

    createConfetti(element) {
        const colors = ['#667eea', '#764ba2', '#10b981', '#fbbf24', '#ef4444'];
        const rect = element.getBoundingClientRect();
        
        for (let i = 0; i < 30; i++) {
            const confetti = document.createElement('div');
            confetti.className = 'confetti';
            confetti.style.cssText = `
                position: fixed;
                width: 10px;
                height: 10px;
                background: ${colors[Math.floor(Math.random() * colors.length)]};
                left: ${rect.left + rect.width / 2}px;
                top: ${rect.top + rect.height / 2}px;
                border-radius: 50%;
                pointer-events: none;
                z-index: 1000;
                animation: confetti-fall 3s ease-out forwards;
            `;
            
            confetti.style.setProperty('--random-x', Math.random() * 400 - 200);
            confetti.style.setProperty('--random-y', Math.random() * 400 + 200);
            confetti.style.setProperty('--random-rotation', Math.random() * 360);
            
            document.body.appendChild(confetti);
            
            setTimeout(() => {
                confetti.remove();
            }, 3000);
        }
    }

    showMessageModal() {
        const modal = document.createElement('div');
        modal.className = 'message-modal-overlay';
        modal.innerHTML = `
            <div class="message-modal">
                <div class="message-header">
                    <h3>Send Message</h3>
                    <button class="close-btn">&times;</button>
                </div>
                <div class="message-body">
                    <textarea placeholder="Type your message here..." rows="4"></textarea>
                    <div class="quick-messages">
                        <button class="quick-msg">Thank you!</button>
                        <button class="quick-msg">When can I pick up?</button>
                        <button class="quick-msg">Is this still available?</button>
                    </div>
                </div>
                <div class="message-footer">
                    <button class="button cancel">Cancel</button>
                    <button class="button primary">Send Message</button>
                </div>
            </div>
        `;

        document.body.appendChild(modal);
        this.addModalStyles();

        setTimeout(() => {
            modal.classList.add('show');
        }, 10);

        // Event listeners
        modal.querySelector('.close-btn').addEventListener('click', () => {
            this.closeModal(modal);
        });

        modal.querySelector('.cancel').addEventListener('click', () => {
            this.closeModal(modal);
        });

        modal.querySelector('.primary').addEventListener('click', () => {
            this.sendMessage(modal);
        });

        modal.querySelectorAll('.quick-msg').forEach(btn => {
            btn.addEventListener('click', () => {
                const textarea = modal.querySelector('textarea');
                textarea.value = btn.textContent;
                textarea.focus();
            });
        });
    }

    closeModal(modal) {
        modal.classList.remove('show');
        setTimeout(() => {
            modal.remove();
        }, 300);
    }

    sendMessage(modal) {
        const textarea = modal.querySelector('textarea');
        const message = textarea.value.trim();
        
        if (message) {
            this.showSuccessToast('Message sent successfully! 📨');
            this.closeModal(modal);
        } else {
            this.showErrorToast('Please enter a message');
        }
    }

    addRippleEffect(button, event) {
        const ripple = document.createElement('span');
        const rect = button.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);
        const x = event.clientX - rect.left - size / 2;
        const y = event.clientY - rect.top - size / 2;
        
        ripple.style.cssText = `
            position: absolute;
            width: ${size}px;
            height: ${size}px;
            left: ${x}px;
            top: ${y}px;
            background: rgba(255, 255, 255, 0.3);
            border-radius: 50%;
            transform: scale(0);
            animation: ripple 0.6s ease-out;
            pointer-events: none;
        `;
        
        button.style.position = 'relative';
        button.style.overflow = 'hidden';
        button.appendChild(ripple);
        
        setTimeout(() => {
            ripple.remove();
        }, 600);
    }

    setupProgressBars() {
        document.querySelectorAll('.card').forEach(card => {
            const badge = card.querySelector('.badge');
            if (!badge) return;

            // Create progress bar if it doesn't exist
            let progressContainer = card.querySelector('.progress-container');
            if (!progressContainer) {
                progressContainer = document.createElement('div');
                progressContainer.className = 'progress-container';
                progressContainer.innerHTML = `
                    <div class="progress-bar">
                        <div class="progress-fill"></div>
                    </div>
                `;
                
                const infoSection = card.querySelector('.info-item').parentElement;
                infoSection.appendChild(progressContainer);
            }

            const progressFill = progressContainer.querySelector('.progress-fill');
            const status = badge.textContent.toLowerCase();
            
            // Set appropriate class and animate
            setTimeout(() => {
                progressFill.classList.add(status);
            }, 500);
        });
    }

    showSuccessToast(message) {
        this.showToast(message, 'success', '#10b981');
    }

    showErrorToast(message) {
        this.showToast(message, 'error', '#ef4444');
    }

    showToast(message, type, color) {
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.innerHTML = `
            <div class="toast-content">
                <i class="fas ${type === 'success' ? 'fa-check-circle' : 'fa-exclamation-circle'}"></i>
                <span>${message}</span>
            </div>
        `;
        
        toast.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: ${color};
            color: white;
            padding: 1rem 1.5rem;
            border-radius: 12px;
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
            z-index: 1000;
            transform: translateX(100%);
            transition: transform 0.3s ease;
        `;
        
        document.body.appendChild(toast);
        
        setTimeout(() => {
            toast.style.transform = 'translateX(0)';
        }, 10);
        
        setTimeout(() => {
            toast.style.transform = 'translateX(100%)';
            setTimeout(() => {
                toast.remove();
            }, 300);
        }, 3000);
    }

    setupSoundEffects() {
        // Add subtle click sounds (optional)
        document.querySelectorAll('.button').forEach(button => {
            button.addEventListener('click', () => {
                // You can add Web Audio API sounds here
                this.playClickSound();
            });
        });
    }

    playClickSound() {
        // Create a subtle click sound using Web Audio API
        if (typeof AudioContext !== 'undefined' || typeof webkitAudioContext !== 'undefined') {
            const audioContext = new (AudioContext || webkitAudioContext)();
            const oscillator = audioContext.createOscillator();
            const gainNode = audioContext.createGain();
            
            oscillator.connect(gainNode);
            gainNode.connect(audioContext.destination);
            
            oscillator.frequency.setValueAtTime(800, audioContext.currentTime);
            oscillator.frequency.exponentialRampToValueAtTime(400, audioContext.currentTime + 0.1);
            
            gainNode.gain.setValueAtTime(0.1, audioContext.currentTime);
            gainNode.gain.exponentialRampToValueAtTime(0.001, audioContext.currentTime + 0.1);
            
            oscillator.start(audioContext.currentTime);
            oscillator.stop(audioContext.currentTime + 0.1);
        }
    }

    setupKeyboardNavigation() {
        const cards = document.querySelectorAll('.card');
        let currentIndex = 0;
        
        document.addEventListener('keydown', (e) => {
            if (e.key === 'ArrowDown') {
                e.preventDefault();
                currentIndex = Math.min(currentIndex + 1, cards.length - 1);
                this.focusCard(cards[currentIndex]);
            } else if (e.key === 'ArrowUp') {
                e.preventDefault();
                currentIndex = Math.max(currentIndex - 1, 0);
                this.focusCard(cards[currentIndex]);
            } else if (e.key === 'Enter' && document.activeElement.classList.contains('card')) {
                const button = document.activeElement.querySelector('.button');
                if (button) button.click();
            }
        });
    }

    focusCard(card) {
        card.focus();
        card.scrollIntoView({ behavior: 'smooth', block: 'center' });
        
        // Add focus highlight
        document.querySelectorAll('.card').forEach(c => c.classList.remove('keyboard-focus'));
        card.classList.add('keyboard-focus');
    }

    initParticleBackground() {
        // Create subtle floating particles
        const particleCount = 20;
        
        for (let i = 0; i < particleCount; i++) {
            setTimeout(() => {
                this.createParticle();
            }, i * 200);
        }
        
        // Continuously create new particles
        setInterval(() => {
            this.createParticle();
        }, 3000);
    }

    createParticle() {
        const particle = document.createElement('div');
        particle.className = 'floating-particle';
        particle.style.cssText = `
            position: fixed;
            width: 4px;
            height: 4px;
            background: rgba(255, 255, 255, 0.3);
            border-radius: 50%;
            pointer-events: none;
            z-index: 0;
            left: ${Math.random() * 100}vw;
            top: 100vh;
            animation: float-up ${10 + Math.random() * 10}s linear forwards;
        `;
        
        document.body.appendChild(particle);
        
        setTimeout(() => {
            particle.remove();
        }, 20000);
    }

    setupStatusUpdates() {
        // Simulate real-time status updates
        setInterval(() => {
            this.checkForStatusUpdates();
        }, 30000); // Check every 30 seconds
    }

    checkForStatusUpdates() {
        // This would typically make an AJAX call to check for updates
        // For now, we'll just add a subtle pulse to show the system is active
        const badges = document.querySelectorAll('.badge.pending');
        badges.forEach(badge => {
            badge.style.animation = 'pulse 0.5s ease-out';
            setTimeout(() => {
                badge.style.animation = '';
            }, 500);
        });
    }

    addConfirmationStyles() {
        if (!document.getElementById('confirmation-styles')) {
            const style = document.createElement('style');
            style.id = 'confirmation-styles';
            style.textContent = `
                .confirmation-overlay {
                    position: fixed;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    background: rgba(0, 0, 0, 0.5);
                    backdrop-filter: blur(10px);
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    z-index: 1000;
                    opacity: 0;
                    transition: opacity 0.3s ease;
                }
                
                .confirmation-overlay.show {
                    opacity: 1;
                }
                
                .confirmation-modal {
                    background: white;
                    padding: 2rem;
                    border-radius: 20px;
                    text-align: center;
                    max-width: 400px;
                    width: 90%;
                    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
                    transform: scale(0.9);
                    transition: transform 0.3s ease;
                }
                
                .confirmation-overlay.show .confirmation-modal {
                    transform: scale(1);
                }
                
                .confirmation-icon {
                    font-size: 3rem;
                    color: #10b981;
                    margin-bottom: 1rem;
                }
                
                .confirmation-buttons {
                    display: flex;
                    gap: 1rem;
                    margin-top: 1.5rem;
                }
                
                .confirmation-buttons .button {
                    flex: 1;
                }
            `;
            document.head.appendChild(style);
        }
    }

    addModalStyles() {
        if (!document.getElementById('modal-styles')) {
            const style = document.createElement('style');
            style.id = 'modal-styles';
            style.textContent = `
                .message-modal-overlay {
                    position: fixed;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    background: rgba(0, 0, 0, 0.5);
                    backdrop-filter: blur(10px);
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    z-index: 1000;
                    opacity: 0;
                    transition: opacity 0.3s ease;
                }
                
                .message-modal-overlay.show {
                    opacity: 1;
                }
                
                .message-modal {
                    background: white;
                    border-radius: 20px;
                    max-width: 500px;
                    width: 90%;
                    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
                    transform: scale(0.9);
                    transition: transform 0.3s ease;
                    overflow: hidden;
                }
                
                .message-modal-overlay.show .message-modal {
                    transform: scale(1);
                }
                
                .message-header {
                    padding: 1.5rem;
                    border-bottom: 1px solid #e5e7eb;
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                }
                
                .close-btn {
                    background: none;
                    border: none;
                    font-size: 1.5rem;
                    cursor: pointer;
                    color: #6b7280;
                }
                
                .message-body {
                    padding: 1.5rem;
                }
                
                .message-body textarea {
                    width: 100%;
                    border: 2px solid #e5e7eb;
                    border-radius: 12px;
                    padding: 1rem;
                    font-family: inherit;
                    resize: vertical;
                    margin-bottom: 1rem;
                }
                
                .quick-messages {
                    display: flex;
                    flex-wrap: wrap;
                    gap: 0.5rem;
                }
                
                .quick-msg {
                    background: #f3f4f6;
                    border: none;
                    padding: 0.5rem 1rem;
                    border-radius: 20px;
                    cursor: pointer;
                    font-size: 0.875rem;
                    transition: all 0.2s ease;
                }
                
                .quick-msg:hover {
                    background: #e5e7eb;
                }
                
                .message-footer {
                    padding: 1.5rem;
                    border-top: 1px solid #e5e7eb;
                    display: flex;
                    gap: 1rem;
                    justify-content: flex-end;
                }
                
                @keyframes ripple {
                    to {
                        transform: scale(2);
                        opacity: 0;
                    }
                }
                
                @keyframes float-up {
                    to {
                        transform: translateY(-100vh);
                        opacity: 0;
                    }
                }
                
                @keyframes confetti-fall {
                    to {
                        transform: translate(var(--random-x, 0), var(--random-y, 0)) rotate(var(--random-rotation, 0));
                        opacity: 0;
                    }
                }
                
                .keyboard-focus {
                    outline: 3px solid #667eea;
                    outline-offset: 2px;
                }
                
                .card {
                    tabindex: 0;
                }
            `;
            document.head.appendChild(style);
        }
    }

    animateCards() {
        // Add staggered animation to cards
        const cards = document.querySelectorAll('.card');
        cards.forEach((card, index) => {
            card.style.animationDelay = `${index * 0.1}s`;
        });
    }

    setupTooltips() {
        // Add tooltips to buttons and badges
        const elementsWithTooltips = [
            { selector: '.badge.pending', text: 'Waiting for pickup confirmation' },
            { selector: '.badge.completed', text: 'Food successfully transferred' },
            { selector: '.badge.claimed', text: 'Food has been claimed' },
            { selector: '.button.message', text: 'Send a message to the donor' },
            { selector: '.button.success', text: 'Mark as received' }
        ];

        elementsWithTooltips.forEach(({ selector, text }) => {
            document.querySelectorAll(selector).forEach(element => {
                element.setAttribute('title', text);
            });
        });
    }
}

// Initialize the UI when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new ClaimedFoodUI();
});

// Add resize handler for responsive behavior
window.addEventListener('resize', () => {
    // Recalculate layouts if needed
    const cards = document.querySelectorAll('.card');
    cards.forEach(card => {
        card.style.transition = 'none';
        setTimeout(() => {
            card.style.transition = '';
        }, 100);
    });
});