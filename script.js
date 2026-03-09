// ===== DOM Ready =====
document.addEventListener('DOMContentLoaded', () => {
  initNavbar();
  initMobileMenu();
  initScrollReveal();
  initContactForm();
  initSmoothScroll();
  initLanguageSwitcher();
});

// ===== Sticky Navbar =====
function initNavbar() {
  const navbar = document.getElementById('navbar');
  let lastScroll = 0;

  window.addEventListener('scroll', () => {
    const currentScroll = window.scrollY;

    if (currentScroll > 50) {
      navbar.classList.add('scrolled');
    } else {
      navbar.classList.remove('scrolled');
    }

    lastScroll = currentScroll;
  }, { passive: true });
}

// ===== Mobile Menu =====
function initMobileMenu() {
  const toggle = document.getElementById('menuToggle');
  const navLinks = document.getElementById('navLinks');
  const overlay = document.getElementById('overlay');

  function closeMenu() {
    toggle.classList.remove('active');
    navLinks.classList.remove('active');
    overlay.classList.remove('active');
    document.body.style.overflow = '';
  }

  function openMenu() {
    toggle.classList.add('active');
    navLinks.classList.add('active');
    overlay.classList.add('active');
    document.body.style.overflow = 'hidden';
  }

  toggle.addEventListener('click', () => {
    if (navLinks.classList.contains('active')) {
      closeMenu();
    } else {
      openMenu();
    }
  });

  overlay.addEventListener('click', closeMenu);

  // Close menu when clicking a link
  navLinks.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', closeMenu);
  });
}

// ===== Scroll Reveal Animation =====
function initScrollReveal() {
  const reveals = document.querySelectorAll('.reveal');

  const observerOptions = {
    root: null,
    rootMargin: '0px 0px -80px 0px',
    threshold: 0.1
  };

  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry, index) => {
      if (entry.isIntersecting) {
        // Stagger animation for grid items
        const delay = entry.target.dataset.delay || 0;
        setTimeout(() => {
          entry.target.classList.add('visible');
        }, delay);
        observer.unobserve(entry.target);
      }
    });
  }, observerOptions);

  // Add staggered delays for grid children
  document.querySelectorAll('.services-grid .reveal, .insurance-grid .reveal, .steps-grid .reveal, .credit-grid .reveal, .testimonials-grid .reveal').forEach((el, i) => {
    el.dataset.delay = (i % 4) * 120;
  });

  reveals.forEach(el => observer.observe(el));
}

// ===== Contact Form =====
function initContactForm() {
  const form = document.getElementById('contactForm');

  form.addEventListener('submit', (e) => {
    e.preventDefault();

    const name = document.getElementById('name').value.trim();
    const phone = document.getElementById('phone').value.trim();
    const interest = document.getElementById('interest').value;
    const message = document.getElementById('message').value.trim();

    // Obtain language from the document context
    const lang = document.documentElement.lang || 'ro';

    if (!name || !phone || !interest) {
      showNotification(lang === 'en' ? 'Please fill in all required fields.' : 'Te rugăm să completezi toate câmpurile obligatorii.', 'error');
      return;
    }

    // Build WhatsApp message
    const interestLabels = {
      'ro': {
        'rca': 'Asigurare RCA',
        'casco': 'Asigurare CASCO',
        'locuinta': 'Asigurare locuință',
        'calatorie': 'Asigurare călătorie',
        'sanatate': 'Asigurare sănătate',
        'viata': 'Asigurare viață',
        'bunuri': 'Asigurare bunuri',
        'rc': 'Răspundere civilă',
        'ipotecar': 'Credit ipotecar',
        'refinantare': 'Refinanțare',
        'nevoi': 'Credit nevoi personale',
        'imobiliar': 'Consultanță imobiliară'
      },
      'en': {
        'rca': 'RCA Insurance',
        'casco': 'CASCO Insurance',
        'locuinta': 'Home Insurance',
        'calatorie': 'Travel Insurance',
        'sanatate': 'Health Insurance',
        'viata': 'Life Insurance',
        'bunuri': 'Goods Insurance',
        'rc': 'Civil liability',
        'ipotecar': 'Mortgage Loan',
        'refinantare': 'Refinancing',
        'nevoi': 'Personal Loan',
        'imobiliar': 'Real Estate Consulting'
      }
    };

    let whatsappMsg = lang === 'en' ? `Hello, my name is ${name}.\n` : `Bună ziua, mă numesc ${name}.\n`;
    whatsappMsg += (lang === 'en' ? 'Phone: ' : 'Telefon: ') + `${phone}\n`;
    whatsappMsg += (lang === 'en' ? 'I am interested in: ' : 'Sunt interesat de: ') + `${(interestLabels[lang] && interestLabels[lang][interest]) || interest}\n`;
    if (message) {
      whatsappMsg += (lang === 'en' ? '\nMessage: ' : '\nMesaj: ') + `${message}`;
    }

    const whatsappUrl = `https://wa.me/40766658583?text=${encodeURIComponent(whatsappMsg)}`;
    window.open(whatsappUrl, '_blank');

    showNotification(lang === 'en' ? 'Message prepared! Opening WhatsApp...' : 'Mesajul a fost pregătit! Se deschide WhatsApp...', 'success');
    form.reset();
  });
}

// ===== Notification Toast =====
function showNotification(message, type = 'success') {
  // Remove existing toast
  const existing = document.querySelector('.toast-notification');
  if (existing) existing.remove();

  const toast = document.createElement('div');
  toast.className = `toast-notification toast-${type}`;
  toast.innerHTML = `
    <span class="toast-icon">${type === 'success' ? '✅' : '⚠️'}</span>
    <span class="toast-message">${message}</span>
  `;

  // Style the toast
  Object.assign(toast.style, {
    position: 'fixed',
    bottom: '30px',
    right: '30px',
    padding: '16px 24px',
    background: type === 'success'
      ? 'rgba(37, 211, 102, 0.15)'
      : 'rgba(244, 63, 94, 0.15)',
    backdropFilter: 'blur(20px)',
    WebkitBackdropFilter: 'blur(20px)',
    border: `1px solid ${type === 'success'
      ? 'rgba(37, 211, 102, 0.3)'
      : 'rgba(244, 63, 94, 0.3)'}`,
    borderRadius: '14px',
    color: '#f1f5f9',
    fontFamily: "'Inter', sans-serif",
    fontSize: '0.9rem',
    display: 'flex',
    alignItems: 'center',
    gap: '10px',
    zIndex: '10000',
    animation: 'fadeInUp 0.4s ease',
    boxShadow: '0 8px 32px rgba(0, 0, 0, 0.3)',
    maxWidth: '400px'
  });

  document.body.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateY(20px)';
    toast.style.transition = 'all 0.4s ease';
    setTimeout(() => toast.remove(), 400);
  }, 4000);
}

// ===== Smooth Scroll =====
function initSmoothScroll() {
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      const targetId = this.getAttribute('href');
      if (targetId === '#') return;

      e.preventDefault();
      const target = document.querySelector(targetId);
      if (target) {
        const navbarHeight = document.getElementById('navbar').offsetHeight;
        const targetPos = target.getBoundingClientRect().top + window.scrollY - navbarHeight - 20;
        window.scrollTo({
          top: targetPos,
          behavior: 'smooth'
        });
      }
    });
  });
}

// ===== Counter Animation for Stats =====
function animateCounters() {
  const counters = document.querySelectorAll('.stat-number');
  counters.forEach(counter => {
    const text = counter.textContent;
    // Only animate pure numbers
    if (/^\d+$/.test(text)) {
      const target = parseInt(text);
      let current = 0;
      const increment = target / 40;
      const timer = setInterval(() => {
        current += increment;
        if (current >= target) {
          counter.textContent = target;
          clearInterval(timer);
        } else {
          counter.textContent = Math.floor(current);
        }
      }, 30);
    }
  });
}

// Trigger counter animation when profile card is visible
const profileCard = document.querySelector('.profile-card');
if (profileCard) {
  const counterObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        animateCounters();
        counterObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.5 });

  counterObserver.observe(profileCard);
}

// ===== Language Switcher =====
function initLanguageSwitcher() {
  const langSwitch = document.getElementById('langSwitch');
  if (!langSwitch || typeof translations === 'undefined') return;

  const spans = langSwitch.querySelectorAll('span[data-lang]');
  let currentLang = localStorage.getItem('site_lang') || 'ro';

  // Set initial language
  setLanguage(currentLang);

  spans.forEach(span => {
    span.addEventListener('click', () => {
      const lang = span.getAttribute('data-lang');
      if (lang === currentLang) return;

      currentLang = lang;
      localStorage.setItem('site_lang', currentLang);
      setLanguage(currentLang);
    });
  });

  function setLanguage(lang) {
    // Update active class on switch
    spans.forEach(s => {
      if (s.getAttribute('data-lang') === lang) {
        s.classList.add('active');
      } else {
        s.classList.remove('active');
      }
    });

    // Update all elements with data-i18n
    const elements = document.querySelectorAll('[data-i18n]');
    elements.forEach(el => {
      const key = el.getAttribute('data-i18n');
      if (translations[key] && translations[key][lang]) {
        if (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA') {
          el.placeholder = translations[key][lang];
        } else if (el.tagName === 'OPTION') {
          el.textContent = translations[key][lang];
        } else {
          el.innerHTML = translations[key][lang];
        }
      }
    });

    // Update HTML lang attribute
    document.documentElement.lang = lang;
  }
}