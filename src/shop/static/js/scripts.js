// Create animated particles
function createParticles() {
    const container = document.getElementById('particles-container');
    const particleCount = 30;
    
    for (let i = 0; i < particleCount; i++) {
        const particle = document.createElement('div');
        particle.classList.add('particle');
        
        // Random starting position
        const startX = Math.random() * window.innerWidth;
        const startY = Math.random() * window.innerHeight;
        
        // Random ending position
        const endX = (Math.random() - 0.5) * window.innerWidth;
        const endY = (Math.random() - 0.5) * window.innerHeight;
        
        particle.style.left = `${startX}px`;
        particle.style.top = `${startY}px`;
        particle.style.setProperty('--end-x', `${endX}px`);
        particle.style.setProperty('--end-y', `${endY}px`);
        
        // Random size
        const size = Math.random() * 5 + 2;
        particle.style.width = `${size}px`;
        particle.style.height = `${size}px`;
        
        // Random animation duration
        const duration = Math.random() * 10 + 5;
        particle.style.animationDuration = `${duration}s`;
        
        // Random delay
        const delay = Math.random() * 5;
        particle.style.animationDelay = `${delay}s`;
        
        container.appendChild(particle);
    }
}

// Change navbar background on scroll
window.addEventListener('scroll', function() {
    const navbar = document.querySelector('.navbar');
    if (window.scrollY > 50) {
        navbar.style.background = 'rgba(15, 12, 41, 0.9) !important';
        navbar.style.boxShadow = '0 5px 15px rgba(0, 0, 0, 0.1)';
    } else {
        navbar.style.background = 'transparent !important';
        navbar.style.boxShadow = 'none';
    }
});

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    createParticles();
});