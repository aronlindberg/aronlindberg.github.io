// Build Studio — Main JS

// Active nav link
(function () {
  const path = window.location.pathname;
  document.querySelectorAll('.nav__links a').forEach(a => {
    if (a.getAttribute('href') && path.endsWith(a.getAttribute('href').replace('../build-studio/', '').replace('.html', ''))) {
      a.classList.add('active');
    }
  });
  // Home active
  if (path.endsWith('/build-studio/') || path.endsWith('/build-studio/index.html')) {
    document.querySelectorAll('.nav__links a[href="index.html"]').forEach(a => a.classList.add('active'));
  }
})();

// Hamburger toggle
const hamburger = document.querySelector('.nav__hamburger');
const navLinks  = document.querySelector('.nav__links');
if (hamburger && navLinks) {
  hamburger.addEventListener('click', () => {
    navLinks.style.display = navLinks.style.display === 'flex' ? 'none' : 'flex';
    navLinks.style.flexDirection = 'column';
    navLinks.style.position = 'absolute';
    navLinks.style.top = '64px';
    navLinks.style.right = '20px';
    navLinks.style.background = '#1A2744';
    navLinks.style.padding = '8px';
    navLinks.style.borderRadius = '8px';
    navLinks.style.boxShadow = '0 8px 24px rgba(0,0,0,0.3)';
  });
}
