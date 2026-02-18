
// --- Embedded Script from frontend/index.html ---
// Enhanced Navbar Scroll Effect
window.addEventListener('scroll', function () {
    const navbar = document.querySelector('.navbar');
    if (window.scrollY > 50) {
        navbar.classList.add('scrolled');
    } else {
        navbar.classList.remove('scrolled');
    }
});

// Mobile Menu Toggle
// Note: This might duplicate script.js logic, but keeping strictly from index.html
const hamburger = document.querySelector('.hamburger');
const navMenu = document.querySelector('.nav-menu');

if (hamburger && navMenu) {
    hamburger.addEventListener('click', function () {
        hamburger.classList.toggle('active');
        navMenu.classList.toggle('active');
    });

    // Close mobile menu when clicking on a link
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', function () {
            hamburger.classList.remove('active');
            navMenu.classList.remove('active');
        });
    });

    // Close mobile menu when clicking outside
    document.addEventListener('click', function (event) {
        if (!hamburger.contains(event.target) && !navMenu.contains(event.target)) {
            hamburger.classList.remove('active');
            navMenu.classList.remove('active');
        }
    });
}

// Add icons to navigation links
document.addEventListener('DOMContentLoaded', function () {
    const navLinks = document.querySelectorAll('.nav-link');
    const navIcons = {
        'index.html': 'fas fa-home',
        '/': 'fas fa-home',
        'about.html': 'fas fa-info-circle',
        '/about/': 'fas fa-info-circle',
        'contact.html': 'fas fa-envelope',
        '/contact/': 'fas fa-envelope',
        'help.html': 'fas fa-question-circle',
        '/help/': 'fas fa-question-circle',
        'login.html': 'fas fa-sign-in-alt',
        '/accounts/login/': 'fas fa-sign-in-alt'
    };

    navLinks.forEach(link => {
        const href = link.getAttribute('href');
        // Match partial hrefs or mapped values
        const iconClass = navIcons[href] ||
            (href.includes('index') ? navIcons['index.html'] : null) ||
            (href.includes('about') ? navIcons['about.html'] : null) ||
            (href.includes('contact') ? navIcons['contact.html'] : null) ||
            (href.includes('help') ? navIcons['help.html'] : null) ||
            (href.includes('login') ? navIcons['login.html'] : null);

        if (iconClass && !link.querySelector('i')) {
            const icon = document.createElement('i');
            icon.className = iconClass;
            link.insertBefore(icon, link.firstChild);
        }
    });
});
