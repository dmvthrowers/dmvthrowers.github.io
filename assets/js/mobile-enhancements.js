/*
  mobile-enhancements.js — shared progressive-enhancement layer for every page.

  Loaded with `defer` so HTML parses first; initMobileEnhancements() then runs
  on DOMContentLoaded (or immediately if the document is already past that).

  Responsibilities, in order of run:
    1. Inject mobile-only CSS (skip link, fixed mobile-menu position, quick-action FAB styles).
    2. Build floating "TOP" + "MENU" quick-action buttons for narrow viewports.
    3. Wire hamburger + mobile-menu + quick-menu so their state stays in sync
       (aria-expanded, body scroll lock, outside-click / Escape closes).
    4. Call ensureSkipLink() (no-op if the page already has a static skip link).
    5. Call normalizeExternalLinks() to force rel="noopener noreferrer" on target=_blank.
    6. Call optimizeImages() to set decoding=async + loading=lazy on non-hero images.

  Idempotency: the style block has id="mobile-enhancements-style" and initialization
  bails if it's already present. Safe to include on every page without double-binding.
*/
(function () {
  'use strict';

  // Honors OS-level "reduce motion" preference for programmatic scrolls/animations.
  function prefersReducedMotion() {
    return window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  }

  function smoothScrollToTop() {
    window.scrollTo({ top: 0, behavior: prefersReducedMotion() ? 'auto' : 'smooth' });
  }

  // Injects a "Skip to content" link as the first body element if the page doesn't already
  // have one. Static pages ship theirs as class="skip-link" (no id), so check both.
  function ensureSkipLink() {
    if (document.getElementById('skip-to-content') || document.querySelector('.skip-link')) {
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

  // Safety net for a[target="_blank"]: appends "noopener noreferrer" to any link missing them.
  // HTML authors already add these manually; this catches accidental omissions.
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

  // Adds decoding="async" + loading="lazy" to images that don't already set them.
  // Hero images are excluded from lazy-loading so LCP isn't delayed.
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

  // Main entry point. Builds the mobile UX layer (styles + quick-action FAB + listeners),
  // then kicks off the non-mobile-specific helpers. Guarded by the style-tag id check
  // so running twice is a no-op.
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

    // Single source of truth for menu state across the hamburger, the FAB menu button,
    // and body's scroll-lock class. Called on toggle, scroll, resize, outside-click, Escape.
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

    // Shows the floating "TOP" button after the user has scrolled past ~one viewport
    // on narrow screens. Hidden on desktop where a floating button would be noise.
    function toggleTopVisibility() {
      window.requestAnimationFrame(function () {
        if (!isMobileView()) {
          topButton.classList.remove('visible');
          return;
        }
        if (window.scrollY > 320) {
          topButton.classList.add('visible');
        } else {
          topButton.classList.remove('visible');
        }
      });
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

  // Defer attribute means the script runs after HTML parse; if for any reason the document
  // is still loading (older browsers, sync injection), wait for DOMContentLoaded.
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initMobileEnhancements);
  } else {
    initMobileEnhancements();
  }
})();
