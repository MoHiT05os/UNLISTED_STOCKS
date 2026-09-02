/**
 * ============================================================
 * APP.JS — Main Application Initialization
 * Premium Financial Information Platform
 * ============================================================
 */

(function () {
  'use strict';

  /* ──────────────────────────────────────────────────────────
   *  1.  DARK MODE
   * ────────────────────────────────────────────────────────── */

  const THEME_KEY = 'unlisted_theme';

  const initDarkMode = () => {
    const html = document.documentElement;
    // Always default to light mode — clear any stale dark preference
    const saved = localStorage.getItem(THEME_KEY) === 'dark' ? null : localStorage.getItem(THEME_KEY);
    const theme = saved || 'light';
    html.setAttribute('data-theme', theme);

    // Bind toggle buttons (all of them on page)
    document.querySelectorAll('.theme-toggle, [data-theme-toggle]').forEach((btn) => {
      updateThemeIcon(btn, theme);

      btn.addEventListener('click', () => {
        const current = html.getAttribute('data-theme') || 'light';
        const next = current === 'dark' ? 'light' : 'dark';
        html.setAttribute('data-theme', next);
        localStorage.setItem(THEME_KEY, next);

        // Update all toggle icons
        document.querySelectorAll('.theme-toggle, [data-theme-toggle]').forEach((b) =>
          updateThemeIcon(b, next)
        );
      });
    });
  };

  const updateThemeIcon = (btn, theme) => {
    if (!btn) return;
    const sunIcon =
      '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>';
    const moonIcon =
      '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>';

    btn.innerHTML = theme === 'dark' ? sunIcon : moonIcon;
    btn.setAttribute('aria-label', theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode');
  };

  /* ──────────────────────────────────────────────────────────
   *  2.  SCROLL REVEAL (IntersectionObserver)
   * ────────────────────────────────────────────────────────── */

  const initScrollReveal = () => {
    const elements = document.querySelectorAll('.reveal');
    if (!elements.length) return;

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add('visible');
            observer.unobserve(entry.target); // animate once
          }
        });
      },
      {
        threshold: 0.1,
        rootMargin: '0px 0px -40px 0px'
      }
    );

    elements.forEach((el) => observer.observe(el));

    // Re-observe after dynamic content is added
    window._revealObserver = observer;
  };

  /** Re-observe new .reveal elements (call after dynamic rendering) */
  const observeNewReveals = () => {
    if (!window._revealObserver) return;
    document.querySelectorAll('.reveal:not(.visible)').forEach((el) => {
      window._revealObserver.observe(el);
    });
  };

  /* ──────────────────────────────────────────────────────────
   *  3.  HEADER SHRINK ON SCROLL
   * ────────────────────────────────────────────────────────── */

  const initHeaderShrink = () => {
    const header = document.querySelector('header, .header, .navbar');
    if (!header) return;

    let ticking = false;
    const onScroll = () => {
      if (!ticking) {
        requestAnimationFrame(() => {
          header.classList.toggle('scrolled', window.scrollY > 50);
          ticking = false;
        });
        ticking = true;
      }
    };

    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll(); // initial state
  };

  /* ──────────────────────────────────────────────────────────
   *  4.  MOBILE HAMBURGER MENU
   * ────────────────────────────────────────────────────────── */

  const initMobileMenu = () => {
    const toggleBtn = document.querySelector('.hamburger, .mobile-menu-btn, [data-mobile-toggle]');
    const nav = document.querySelector('.nav-links, .mobile-nav, .nav-menu');
    if (!toggleBtn || !nav) return;

    toggleBtn.addEventListener('click', () => {
      const isOpen = nav.classList.toggle('active');
      toggleBtn.classList.toggle('active', isOpen);
      toggleBtn.setAttribute('aria-expanded', String(isOpen));

      // Prevent body scroll when menu is open
      document.body.classList.toggle('menu-open', isOpen);
    });

    // Close when clicking a nav link
    nav.querySelectorAll('a').forEach((link) => {
      link.addEventListener('click', () => {
        nav.classList.remove('active');
        toggleBtn.classList.remove('active');
        toggleBtn.setAttribute('aria-expanded', 'false');
        document.body.classList.remove('menu-open');
      });
    });

    // Close on outside click
    document.addEventListener('click', (e) => {
      if (
        nav.classList.contains('active') &&
        !nav.contains(e.target) &&
        !toggleBtn.contains(e.target)
      ) {
        nav.classList.remove('active');
        toggleBtn.classList.remove('active');
        toggleBtn.setAttribute('aria-expanded', 'false');
        document.body.classList.remove('menu-open');
      }
    });
  };

  /* ──────────────────────────────────────────────────────────
   *  5.  SMOOTH SCROLL FOR ANCHOR LINKS
   * ────────────────────────────────────────────────────────── */

  const initSmoothScroll = () => {
    document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
      anchor.addEventListener('click', (e) => {
        const href = anchor.getAttribute('href');
        if (!href || href === '#' || href.length <= 1) return;

        const target = document.querySelector(href);
        if (target) {
          e.preventDefault();
          const headerOffset = document.querySelector('header, .header, .navbar')?.offsetHeight || 80;
          const elementPosition = target.getBoundingClientRect().top + window.scrollY;
          const offsetPosition = elementPosition - headerOffset - 20;

          window.scrollTo({
            top: offsetPosition,
            behavior: 'smooth'
          });
        }
      });
    });
  };

  /* ──────────────────────────────────────────────────────────
   *  6.  COUNTER ANIMATIONS (when stats section is visible)
   * ────────────────────────────────────────────────────────── */

  const initCounters = () => {
    const counters = document.querySelectorAll('.counter');
    if (!counters.length) return;

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            const el = entry.target;
            const target = parseFloat(el.dataset.target || el.textContent);
            const duration = parseInt(el.dataset.duration || '2000', 10);

            if (!isNaN(target) && window.Animations?.countUp) {
              window.Animations.countUp(el, target, duration);
            }

            observer.unobserve(el);
          }
        });
      },
      { threshold: 0.3 }
    );

    counters.forEach((c) => observer.observe(c));
  };

  /* ──────────────────────────────────────────────────────────
   *  7.  HERO TYPEWRITER
   * ────────────────────────────────────────────────────────── */

  const initTypewriter = () => {
    const el = document.querySelector('.typewriter-text');
    if (!el || !window.Animations?.typewriter) return;

    const words = [
      'NSE India',
      'Zepto',
      'OYO Rooms',
      'Ather Energy',
      'boAt Lifestyle',
      'PPFAS AMC',
      'CSK Cricket',
      'Cochin Airport',
      'Bira 91',
      'PharmEasy'
    ];

    window.Animations.typewriter(el, words, 100, 60, 1800);
  };

  /* ──────────────────────────────────────────────────────────
   *  8.  PARTICLES CANVAS
   * ────────────────────────────────────────────────────────── */

  const initParticlesCanvas = () => {
    const canvas = document.getElementById('hero-particles');
    if (!canvas || !window.Animations?.initParticles) return;
    window.Animations.initParticles('hero-particles');
  };

  /* ──────────────────────────────────────────────────────────
   *  9.  SEARCH OVERLAY
   * ────────────────────────────────────────────────────────── */

  const initSearch = () => {
    if (window.Search?.init) {
      window.Search.init();
    }
  };

  /* ──────────────────────────────────────────────────────────
   *  10.  RENDER SHARE CARDS FROM DATA
   * ────────────────────────────────────────────────────────── */

  const initSharesRendering = () => {
    const data = window.SHARES_DATA;
    if (!data || !window.Components) return;

    /* ── Hero stocks (top 5 hot) ────────────────────────── */
    const heroContainer = document.getElementById('hero-stocks');
    if (heroContainer) {
      const hotStocks = data.filter((s) => s.hot).slice(0, 5);
      heroContainer.innerHTML = hotStocks
        .map((stock) => {
          const isUp = stock.price >= (stock.prevPrice || stock.price);
          const chg = stock.prevPrice
            ? (((stock.price - stock.prevPrice) / stock.prevPrice) * 100).toFixed(2)
            : '0.00';
          const sign = isUp ? '+' : '';
          const cls = isUp ? 'up' : 'down';

          return `
          <div class="hero-stock-chip ${cls}">
            <span class="hero-stock-name">${stock.shortName || stock.name}</span>
            <span class="hero-stock-price">${window.Components.formatPrice(stock.price)}</span>
            <span class="hero-stock-change ${cls}">${sign}${chg}%</span>
          </div>`;
        })
        .join('');
    }

    /* ── Popular shares ─────────────────────────────────── */
    const popularContainer = document.getElementById('popular-shares');
    if (popularContainer) {
      const popularStocks = data.filter((s) => s.hot);
      window.Components.renderSharesGrid(popularContainer, popularStocks, 1, 8);
      observeNewReveals();
    }

    /* ── New arrivals ───────────────────────────────────── */
    const newContainer = document.getElementById('new-arrivals');
    if (newContainer) {
      const newStocks = data.filter((s) => s.isNew);
      window.Components.renderSharesGrid(newContainer, newStocks, 1, 8);
      observeNewReveals();
    }

    /* ── Full shares grid (shares listing page) ─────────── */
    const sharesGrid = document.getElementById('shares-grid');
    const paginationContainer = document.getElementById('shares-pagination');
    if (sharesGrid) {
      const PER_PAGE = 12;
      let currentPage = 1;

      // Check for sector filter in URL hash
      let filteredStocks = [...data];
      const hash = window.location.hash.replace('#', '');
      if (hash.startsWith('sector-')) {
        const sectorSlug = hash.replace('sector-', '');
        filteredStocks = data.filter((s) => s.sectorSlug === sectorSlug);
      }

      const renderPage = (page) => {
        currentPage = page;

        // Show skeletons briefly for perceived loading
        window.Components.renderSkeletonCards(sharesGrid, PER_PAGE);

        setTimeout(() => {
          window.Components.renderSharesGrid(sharesGrid, filteredStocks, page, PER_PAGE);

          if (paginationContainer) {
            window.Components.setupPagination(
              paginationContainer,
              filteredStocks.length,
              PER_PAGE,
              page,
              renderPage
            );
          }

          observeNewReveals();

          // Scroll grid into view on page change (not on first load)
          if (page > 1) {
            sharesGrid.scrollIntoView({ behavior: 'smooth', block: 'start' });
          }
        }, 300);
      };

      renderPage(1);
    }

    /* ── Sectors grid ───────────────────────────────────── */
    const sectorsGrid = document.getElementById('sectors-grid');
    if (sectorsGrid && window.SECTORS_DATA) {
      sectorsGrid.innerHTML = window.SECTORS_DATA
        .filter((s) => s.count > 0)
        .map((sector) => window.Components.renderSectorCard(sector))
        .join('');
      observeNewReveals();
    }
  };

  /* ──────────────────────────────────────────────────────────
   *  11.  LIVE CLOCK IN TICKER AREA
   * ────────────────────────────────────────────────────────── */

  const initLiveClock = () => {
    const clockEl = document.getElementById('live-clock');
    if (!clockEl) return;

    const updateClock = () => {
      const now = new Date();
      const options = {
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        hour12: true,
        timeZone: 'Asia/Kolkata'
      };
      clockEl.textContent = now.toLocaleTimeString('en-IN', options) + ' IST';
    };

    updateClock();
    setInterval(updateClock, 1000);
  };

  /* ──────────────────────────────────────────────────────────
   *  12.  WHATSAPP FAB
   * ────────────────────────────────────────────────────────── */

  const initWhatsAppFAB = () => {
    const fab = document.querySelector('.whatsapp-fab, .fab-whatsapp, [data-whatsapp-fab]');
    if (!fab) return;

    fab.addEventListener('click', (e) => {
      // If it's an anchor tag, let it navigate naturally
      if (fab.tagName === 'A' && fab.href) return;

      e.preventDefault();
      window.open(
        'https://wa.me/919354082477?text=Hi%2C%20I%20am%20interested%20in%20unlisted%20shares.',
        '_blank',
        'noopener,noreferrer'
      );
    });
  };

  /* ──────────────────────────────────────────────────────────
   *  SCROLL-TO-TOP BUTTON (bonus utility)
   * ────────────────────────────────────────────────────────── */

  const initScrollToTop = () => {
    const btn = document.querySelector('.scroll-top, [data-scroll-top]');
    if (!btn) return;

    const toggleVisibility = () => {
      btn.classList.toggle('visible', window.scrollY > 400);
    };

    window.addEventListener('scroll', toggleVisibility, { passive: true });
    toggleVisibility();

    btn.addEventListener('click', () => {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  };

  /* ──────────────────────────────────────────────────────────
   *  HASH CHANGE HANDLER (for SPA-like navigation)
   * ────────────────────────────────────────────────────────── */

  const initHashChangeHandler = () => {
    window.addEventListener('hashchange', () => {
      // Re-render shares grid if on shares page with sector filter
      const sharesGrid = document.getElementById('shares-grid');
      if (sharesGrid) {
        initSharesRendering();
      }
    });
  };

  /* ──────────────────────────────────────────────────────────
   *  BOOTSTRAP — DOMContentLoaded
   * ────────────────────────────────────────────────────────── */

  const init = () => {
    initDarkMode();          // 1
    initScrollReveal();      // 2
    initHeaderShrink();      // 3
    initMobileMenu();        // 4
    initSmoothScroll();      // 5
    initCounters();          // 6
    initTypewriter();        // 7
    initParticlesCanvas();   // 8
    initSearch();            // 9
    initSharesRendering();   // 10
    initLiveClock();         // 11
    initWhatsAppFAB();       // 12
    initScrollToTop();       // bonus
    initHashChangeHandler(); // bonus
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    // DOM already ready (script loaded with defer or at end of body)
    init();
  }

  /* ── Expose app utilities globally ──────────────────────── */
  window.App = {
    init,
    observeNewReveals
  };
})();

// Bento Grid GSAP Animation
document.addEventListener('DOMContentLoaded', () => {
    if (typeof gsap !== 'undefined') {
        gsap.fromTo('.bento-card', 
            { y: 60, opacity: 0, scale: 0.95 },
            { 
                y: 0, 
                opacity: 1, 
                scale: 1, 
                duration: 0.8, 
                stagger: 0.15, 
                ease: 'back.out(1.2)', 
                delay: 0.2
            }
        );
    }
});

/* ── Anti-Copy & Security ──────────────────────────────── */
document.addEventListener('contextmenu', e => e.preventDefault());
document.addEventListener('copy', e => {
  e.preventDefault();
  if (e.clipboardData) e.clipboardData.setData('text/plain', 'Content protected by MDB ARTHASPHERE');
});
document.addEventListener('keydown', e => {
  if (e.key === 'F12' ||
      (e.ctrlKey && e.shiftKey && ['I', 'J', 'C'].includes(e.key.toUpperCase())) ||
      (e.ctrlKey && ['U', 'C'].includes(e.key.toUpperCase())) ||
      (e.metaKey && ['C'].includes(e.key.toUpperCase()))) {
    e.preventDefault();
  }
});


/* ── Auth State Management (Nav Update) ────────────────── */
document.addEventListener('DOMContentLoaded', () => {
    const token = localStorage.getItem('auth_token');
    const userName = localStorage.getItem('user_name');
    
    if (token && userName) {
        // Find all Sign In buttons and replace them with Account dropdown/link
        const signinBtns = document.querySelectorAll('a[href="login.html"]');
        
        signinBtns.forEach(btn => {
            if (btn.classList.contains('hide-sm') || btn.classList.contains('btn-ghost')) {
                const isFooter = !btn.classList.contains('hide-sm');
                if (isFooter) {
                    btn.textContent = 'My Account';
                    btn.href = 'account.html';
                } else {
                    const accountHtml = `
                        <div class="account-dropdown" style="position: relative; display: inline-block;">
                            <a href="account.html" class="btn btn-ghost hide-sm" style="display: inline-flex; align-items: center; gap: 8px; text-decoration: none; padding: 6px 12px;">
                                <div style="width:24px; height:24px; background:var(--primary); color:#000; border-radius:50%; display:flex; align-items:center; justify-content:center; font-weight:bold; font-size:12px;">
                                    ${userName.charAt(0).toUpperCase()}
                                </div>
                                <span>${userName.split(' ')[0]}</span>
                            </a>
                        </div>
                    `;
                    btn.outerHTML = accountHtml;
                }
            }
        });
    }
});
