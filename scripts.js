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