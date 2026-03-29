(function () {
  'use strict';

  function prefersReducedMotion() {
    return window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  }

  function smoothScrollToTop() {
    window.scrollTo({ top: 0, behavior: prefersReducedMotion() ? 'auto' : 'smooth' });
  }

  function ensureSkipLink() {
    if (document.getElementById('skip-to-content')) {
      return;
    }

    var target = document.querySelector('main, #main-content, section, #hero, .page-hero, .vsyc-page-hero');
    if (!target) {
      return;
    }

    if (!target.id) {
      target.id = 'main-content';
    }

    if (!target.hasAttribute('tabindex')) {
      target.setAttribute('tabindex', '-1');
    }

    var skip = document.createElement('a');
    skip.id = 'skip-to-content';
    skip.className = 'skip-link';
    skip.href = '#' + target.id;
    skip.textContent = 'Skip to content';
    document.body.insertBefore(skip, document.body.firstChild);

    skip.addEventListener('click', function () {
      window.setTimeout(function () {
        target.focus({ preventScroll: true });
      }, 0);
    });
  }

  function normalizeExternalLinks() {
    var links = document.querySelectorAll('a[target="_blank"]');
    links.forEach(function (link) {
      var rel = (link.getAttribute('rel') || '').toLowerCase();
      var parts = rel.split(/\s+/).filter(Boolean);
      if (parts.indexOf('noopener') === -1) {
        parts.push('noopener');
      }
      if (parts.indexOf('noreferrer') === -1) {
        parts.push('noreferrer');
      }
      link.setAttribute('rel', parts.join(' '));
    });
  }

  function optimizeImages() {
    var images = document.querySelectorAll('img');
    images.forEach(function (img) {
      if (!img.hasAttribute('decoding')) {
        img.setAttribute('decoding', 'async');
      }

      var inHero = !!img.closest('#hero, .page-hero, .vsyc-page-hero');
      if (!inHero && !img.hasAttribute('loading')) {
        img.setAttribute('loading', 'lazy');
      }
    });
  }

  function initMobileEnhancements() {
    if (document.getElementById('mobile-enhancements-style')) {
      return;
    }

    var style = document.createElement('style');
    style.id = 'mobile-enhancements-style';
    style.textContent = ".mobile-quick-actions { display: none; }"
      + ".skip-link { position: fixed; left: 10px; top: -44px; z-index: 1200; background: #111827; color: #ffffff; padding: 10px 12px; border-radius: 6px; font-size: 0.78rem; font-weight: 700; letter-spacing: 0.03em; text-decoration: none; transition: top 0.2s ease; }"
      + ".skip-link:focus { top: 10px; outline: 2px solid #ffffff; outline-offset: 2px; }"
      + "@media (max-width: 768px) {"
      + ".mobile-menu { position: fixed !important; top: 64px; left: 0; right: 0; max-height: calc(100vh - 64px); overflow-y: auto; z-index: 900; }"
      + ".mobile-menu.open { display: flex !important; }"
      + ".mobile-nav-locked { overflow: hidden; touch-action: none; }"
      + ".mobile-quick-actions { position: fixed; right: calc(14px + env(safe-area-inset-right, 0px)); bottom: calc(14px + env(safe-area-inset-bottom, 0px)); display: flex; flex-direction: column; gap: 10px; z-index: 1000; }"
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
    menuButton.setAttribute('aria-expanded', 'false');
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

    function syncMenuState() {
      var menu = document.getElementById('mobile-menu');
      var hamburger = document.getElementById('hamburger');
      var isOpen = !!(menu && menu.classList.contains('open') && isMobileView());

      document.body.classList.toggle('mobile-nav-locked', isOpen);
      if (hamburger) {
        hamburger.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
      }
      menuButton.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
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
      smoothScrollToTop();
    });

    menuButton.addEventListener('click', function () {
      if (!isMobileView()) {
        return;
      }

      var menu = document.getElementById('mobile-menu');
      var hamburger = document.getElementById('hamburger');

      if (!menu) {
        smoothScrollToTop();
        return;
      }

      menu.classList.toggle('open');
      syncMenuState();
    });

    window.addEventListener('scroll', toggleTopVisibility, { passive: true });
    window.addEventListener('resize', function () {
      toggleTopVisibility();
      syncMenuState();
    });

    var hamburgerButton = document.getElementById('hamburger');
    if (hamburgerButton) {
      hamburgerButton.addEventListener('click', function () {
        window.setTimeout(syncMenuState, 0);
      });
    }

    document.addEventListener('click', function (event) {
      if (event.target && event.target.closest('.mobile-menu a')) {
        window.setTimeout(syncMenuState, 0);
      }
    });

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
        syncMenuState();
      }
    });

    document.addEventListener('keydown', function (event) {
      if (event.key !== 'Escape') {
        return;
      }

      var menu = document.getElementById('mobile-menu');
      if (menu && menu.classList.contains('open')) {
        menu.classList.remove('open');
        syncMenuState();
      }
    });

    ensureSkipLink();
    normalizeExternalLinks();
    optimizeImages();
    toggleTopVisibility();
    syncMenuState();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initMobileEnhancements);
  } else {
    initMobileEnhancements();
  }
})();
