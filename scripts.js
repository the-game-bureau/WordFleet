// START: Navigation Active Link Script
// Purpose: Dynamically adds the 'active' class to the navigation link matching the current page's filename,
// applying CSS styles (black background, white text; bold on mobile) to highlight the active page.
// Used in: index.html, pandp.html, rules.html, codes.html, future.html to style the nav bar.
document.addEventListener('DOMContentLoaded', function() {
  const navLinks = document.querySelectorAll('.nav-link');
  const currentPage = window.location.pathname.split('/').pop() || 'index.html';
  navLinks.forEach(link => {
    const linkPage = link.getAttribute('href');
    if (linkPage === currentPage) {
      link.classList.add('active');
    } else {
      link.classList.remove('active');
    }
  });
});
// END: Navigation Active Link Script

// START: Mobile Hamburger Navigation Script
// Purpose: Handles mobile navigation hamburger menu functionality including:
// - Toggle hamburger animation (3 lines to X)
// - Show/hide mobile menu overlay
// - Prevent body scroll when menu is open
// - Auto-close menu when clicking links, outside menu, or pressing ESC
// Used in: All pages to provide mobile navigation experience
document.addEventListener('DOMContentLoaded', function() {
  const navToggle = document.getElementById('navToggle');
  const mobileMenu = document.getElementById('mobileMenu');
  const body = document.body;

  // Only run if hamburger menu elements exist (prevents errors on pages without mobile nav)
  if (navToggle && mobileMenu) {
    
    // Toggle mobile menu when hamburger is clicked
    navToggle.addEventListener('click', function() {
      navToggle.classList.toggle('active');
      mobileMenu.classList.toggle('active');
      
      // Prevent body scroll when menu is open
      if (mobileMenu.classList.contains('active')) {
        body.style.overflow = 'hidden';
      } else {
        body.style.overflow = '';
      }
    });

    // Close mobile menu when clicking on any navigation link
    const mobileNavLinks = mobileMenu.querySelectorAll('.nav-link');
    mobileNavLinks.forEach(link => {
      link.addEventListener('click', function() {
        navToggle.classList.remove('active');
        mobileMenu.classList.remove('active');
        body.style.overflow = '';
      });
    });

    // Close menu when clicking outside the navigation area
    document.addEventListener('click', function(event) {
      const isClickInsideNav = navToggle.contains(event.target) || mobileMenu.contains(event.target);
      
      if (!isClickInsideNav && mobileMenu.classList.contains('active')) {
        navToggle.classList.remove('active');
        mobileMenu.classList.remove('active');
        body.style.overflow = '';
      }
    });

    // Close menu when pressing Escape key (accessibility feature)
    document.addEventListener('keydown', function(event) {
      if (event.key === 'Escape' && mobileMenu.classList.contains('active')) {
        navToggle.classList.remove('active');
        mobileMenu.classList.remove('active');
        body.style.overflow = '';
      }
    });
  }
});
// END: Mobile Hamburger Navigation Script