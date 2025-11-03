// Dashboard 10 - Interactive Features

document.addEventListener('DOMContentLoaded', function() {
    console.log('Dashboard 10 loaded');

    // Add hover effects
    const cards = document.querySelectorAll('[data-name*="Frame"]');
    cards.forEach(card => {
        card.classList.add('hover-lift');
    });

    // Handle "View all" clicks
    const viewAllLinks = document.querySelectorAll('[data-name*="View all"]');
    viewAllLinks.forEach(link => {
        link.style.cursor = 'pointer';
        link.addEventListener('click', function(e) {
            console.log('View all clicked:', this.textContent);
            // Add your navigation logic here
        });
    });

    // Add fade-in animation
    const animatedElements = document.querySelectorAll('[data-name*="Frame"]');
    animatedElements.forEach((el, index) => {
        el.style.opacity = '0';
        setTimeout(() => {
            el.classList.add('animate-fade-in');
            el.style.opacity = '1';
        }, index * 50);
    });

    // Notification dot pulse
    const notificationDots = document.querySelectorAll('[data-name*="Ellipse 1949"]');
    notificationDots.forEach(dot => {
        dot.style.animation = 'pulse 2s infinite';
    });
});

// Add CSS for pulse animation
const style = document.createElement('style');
style.textContent = `
    @keyframes pulse {
        0%, 100% {
            opacity: 1;
        }
        50% {
            opacity: 0.5;
        }
    }
`;
document.head.appendChild(style);
