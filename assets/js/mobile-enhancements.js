(function () {
  'use strict';

  function initMobileEnhancements() {
    if (document.getElementById('mobile-enhancements-style')) {
      return;
    }

    var style = document.createElement('style');
    style.id = 'mobile-enhancements-style';
    style.textContent = ".mobile-quick-actions { display: none; }"
      + "@media (max-width: 768px) {"
      + ".mobile-menu { position: fixed !important; top: 64px; left: 0; right: 0; max-height: calc(100vh - 64px); overflow-y: auto; z-index: 900; }"
      + ".mobile-menu.open { display: flex !important; }"
      + ".mobile-quick-actions { position: fixed; right: 14px; bottom: 14px; display: flex; flex-direction: column; gap: 10px; z-index: 1000; }"
      + ".mobile-quick-btn { min-width: 58px; height: 42px; border: none; border-radius: 999px; font-size: 0.64rem; font-weight: 800; letter-spacing: 0.12em; cursor: pointer; box-shadow: 0 6px 18px rgba(0,0,0,0.25); }"
      + ".mobile-top-btn { background: #C8102E; color: #ffffff; opacity: 0; pointer-events: none; transform: translateY(8px); transition: opacity 0.2s ease, transform 0.2s ease; }"
      + ".mobile-top-btn.visible { opacity: 1; pointer-events: auto; transform: translateY(0); }"
      + ".mobile-menu-btn { background: #1a2744; color: #ffffff; }"
      + "}";

    document.head.appendChild(style);

    var quickActions = document.createElement('div');
    quickActions.className = 'mobile-quick-actions';
    quickActions.setAttribute('aria-label', 'Mobile quick actions');

    var topButton = document.createElement('button');
    topButton.type = 'button';
    topButton.className = 'mobile-quick-btn mobile-top-btn';
    topButton.setAttribute('aria-label', 'Back to top');
    topButton.textContent = 'TOP';

    var menuButton = document.createElement('button');
    menuButton.type = 'button';
    menuButton.className = 'mobile-quick-btn mobile-menu-btn';
    menuButton.setAttribute('aria-label', 'Open mobile menu');
    menuButton.textContent = 'MENU';

    quickActions.appendChild(topButton);
    quickActions.appendChild(menuButton);
    document.body.appendChild(quickActions);

    var hasMobileMenu = !!document.getElementById('mobile-menu');
    if (!hasMobileMenu) {
      menuButton.style.display = 'none';
    }

    function isMobileView() {
      return window.matchMedia('(max-width: 768px)').matches;
    }

    function toggleTopVisibility() {
      if (!isMobileView()) {
        topButton.classList.remove('visible');
        return;
      }
      if (window.scrollY > 320) {
        topButton.classList.add('visible');
      } else {
        topButton.classList.remove('visible');
      }
    }

    topButton.addEventListener('click', function () {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });

    menuButton.addEventListener('click', function () {
      if (!isMobileView()) {
        return;
      }

      var menu = document.getElementById('mobile-menu');
      var hamburger = document.getElementById('hamburger');

      if (!menu) {
        window.scrollTo({ top: 0, behavior: 'smooth' });
        return;
      }

      menu.classList.toggle('open');
      if (hamburger) {
        hamburger.setAttribute('aria-expanded', menu.classList.contains('open') ? 'true' : 'false');
      }
    });

    window.addEventListener('scroll', toggleTopVisibility, { passive: true });
    window.addEventListener('resize', toggleTopVisibility);

    document.addEventListener('click', function (event) {
      if (!isMobileView()) {
        return;
      }

      var menu = document.getElementById('mobile-menu');
      if (!menu || !menu.classList.contains('open')) {
        return;
      }

      var hamburger = document.getElementById('hamburger');
      var clickedInsideMenu = menu.contains(event.target);
      var clickedHamburger = hamburger ? hamburger.contains(event.target) : false;
      var clickedQuickMenu = menuButton.contains(event.target);

      if (!clickedInsideMenu && !clickedHamburger && !clickedQuickMenu) {
        menu.classList.remove('open');
        if (hamburger) {
          hamburger.setAttribute('aria-expanded', 'false');
        }
      }
    });

    toggleTopVisibility();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initMobileEnhancements);
  } else {
    initMobileEnhancements();
  }
})();
