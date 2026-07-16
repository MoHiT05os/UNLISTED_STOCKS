/**
 * ============================================================
 * SEARCH — Full-screen overlay with fuzzy matching & keyboard nav
 * Premium Financial Information Platform
 * ============================================================
 */

(function () {
  'use strict';

  const RECENT_KEY = 'unlisted_recent_searches';
  const MAX_RECENT = 5;
  const MAX_RESULTS = 8;

  let overlay = null;
  let input = null;
  let resultsList = null;
  let recentSection = null;
  let activeIndex = -1;
  let currentResults = [];
  let isOpen = false;

  /* ── Helpers ────────────────────────────────────────────── */

  const getRecent = () => {
    try {
      return JSON.parse(localStorage.getItem(RECENT_KEY)) || [];
    } catch {
      return [];
    }
  };

  const saveRecent = (term) => {
    if (!term || term.trim().length === 0) return;
    let recent = getRecent();
    recent = recent.filter((r) => r.toLowerCase() !== term.toLowerCase());
    recent.unshift(term.trim());
    if (recent.length > MAX_RECENT) recent = recent.slice(0, MAX_RECENT);
    localStorage.setItem(RECENT_KEY, JSON.stringify(recent));
  };

  const clearRecent = () => {
    localStorage.removeItem(RECENT_KEY);
    renderRecent();
  };

  /* ── Fuzzy-ish match scoring ────────────────────────────── */

  const scoreMatch = (query, stock) => {
    const q = query.toLowerCase();
    const name = stock.name.toLowerCase();
    const shortName = (stock.shortName || '').toLowerCase();
    const sector = (stock.sector || '').toLowerCase();

    // Exact short-name match → highest
    if (shortName === q) return 100;
    // Short-name starts with
    if (shortName.startsWith(q)) return 90;
    // Name starts with
    if (name.startsWith(q)) return 80;
    // Short-name contains
    if (shortName.includes(q)) return 70;
    // Name contains
    if (name.includes(q)) return 60;
    // Sector contains
    if (sector.includes(q)) return 40;
    // Word-boundary match inside name
    const words = name.split(/\s+/);
    for (const w of words) {
      if (w.startsWith(q)) return 55;
    }

    return 0;
  };

  const search = (query) => {
    if (!window.SHARES_DATA) return [];
    if (!query || query.trim().length === 0) return [];

    const scored = window.SHARES_DATA
      .map((stock) => ({ stock, score: scoreMatch(query, stock) }))
      .filter((s) => s.score > 0)
      .sort((a, b) => b.score - a.score)
      .slice(0, MAX_RESULTS);

    return scored.map((s) => s.stock);
  };

  /* ── Price helpers ──────────────────────────────────────── */

  const formatPrice = (p) => {
    if (p == null) return '—';
    return '₹' + Number(p).toLocaleString('en-IN', { maximumFractionDigits: 2 });
  };

  const changePercent = (stock) => {
    if (!stock.prevPrice || stock.prevPrice === 0) return 0;
    return ((stock.price - stock.prevPrice) / stock.prevPrice) * 100;
  };

  /* ── Build overlay DOM ──────────────────────────────────── */

  const createOverlay = () => {
    if (document.getElementById('search-overlay')) {
      overlay = document.getElementById('search-overlay');
      // Populate inner structure if empty
      if (!overlay.querySelector('.search-inner')) {
        overlay.innerHTML = buildInnerHTML();
      }
    } else {
      overlay = document.createElement('div');
      overlay.id = 'search-overlay';
      overlay.className = 'search-overlay';
      overlay.innerHTML = buildInnerHTML();
      document.body.appendChild(overlay);
    }

    input = overlay.querySelector('.search-input');
    resultsList = overlay.querySelector('.search-results');
    recentSection = overlay.querySelector('.search-recent');

    bindOverlayEvents();
  };

  const buildInnerHTML = () => `
    <div class="search-inner">
      <div class="search-header">
        <div class="search-input-wrap">
          <svg class="search-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>
          </svg>
          <input type="text" class="search-input" placeholder="Search unlisted shares…" autocomplete="off" spellcheck="false" />
          <kbd class="search-kbd">ESC</kbd>
        </div>
      </div>
      <div class="search-body">
        <div class="search-recent"></div>
        <ul class="search-results" role="listbox"></ul>
        <div class="search-empty" style="display:none;">
          <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" opacity="0.4"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
          <p>No shares found. Try a different search term.</p>
        </div>
      </div>
      <div class="search-footer">
        <span><kbd>↑↓</kbd> Navigate</span>
        <span><kbd>↵</kbd> Open</span>
        <span><kbd>esc</kbd> Close</span>
      </div>
    </div>`;

  /* ── Render functions ───────────────────────────────────── */

  const renderRecent = () => {
    if (!recentSection) return;
    const recent = getRecent();

    if (recent.length === 0) {
      recentSection.innerHTML = '';
      return;
    }

    recentSection.innerHTML = `
      <div class="recent-header">
        <span class="recent-title">Recent Searches</span>
        <button class="recent-clear" type="button">Clear</button>
      </div>
      <div class="recent-tags">
        ${recent
          .map(
            (r) =>
              `<button class="recent-tag" type="button" data-query="${r.replace(/"/g, '&quot;')}">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="1 4 1 10 7 10"/><path d="M3.51 15a9 9 0 1 0 2.13-9.36L1 10"/></svg>
                ${r}
              </button>`
          )
          .join('')}
      </div>`;

    recentSection.querySelector('.recent-clear')?.addEventListener('click', clearRecent);

    recentSection.querySelectorAll('.recent-tag').forEach((tag) => {
      tag.addEventListener('click', () => {
        const q = tag.dataset.query;
        if (input) {
          input.value = q;
          handleInput();
        }
      });
    });
  };

  const renderResults = (results) => {
    currentResults = results;
    activeIndex = -1;
    const emptyEl = overlay.querySelector('.search-empty');

    if (input.value.trim().length === 0) {
      resultsList.innerHTML = '';
      if (emptyEl) emptyEl.style.display = 'none';
      if (recentSection) recentSection.style.display = '';
      return;
    }

    if (recentSection) recentSection.style.display = 'none';

    if (results.length === 0) {
      resultsList.innerHTML = '';
      if (emptyEl) emptyEl.style.display = 'flex';
      return;
    }

    if (emptyEl) emptyEl.style.display = 'none';

    resultsList.innerHTML = results
      .map((stock, i) => {
        const chg = changePercent(stock);
        const chgClass = chg >= 0 ? 'up' : 'down';
        const chgSign = chg >= 0 ? '+' : '';

        return `
        <li class="search-result" role="option" data-index="${i}" data-slug="${stock.slug}">
          <div class="result-logo" style="background:${stock.logoColor || '#6366f1'}">${stock.logoInitials || '??'}</div>
          <div class="result-info">
            <span class="result-name">${highlightMatch(stock.shortName || stock.name, input.value)}</span>
            <span class="result-sector">${stock.sector || ''}</span>
          </div>
          <div class="result-price">
            <span class="result-price-value">${formatPrice(stock.price)}</span>
            <span class="result-change ${chgClass}">${chgSign}${chg.toFixed(2)}%</span>
          </div>
        </li>`;
      })
      .join('');
  };

  const highlightMatch = (text, query) => {
    if (!query) return text;
    const idx = text.toLowerCase().indexOf(query.toLowerCase());
    if (idx === -1) return text;
    const before = text.substring(0, idx);
    const match = text.substring(idx, idx + query.length);
    const after = text.substring(idx + query.length);
    return `${before}<mark>${match}</mark>${after}`;
  };

  const updateActive = () => {
    const items = resultsList.querySelectorAll('.search-result');
    items.forEach((el, i) => {
      el.classList.toggle('active', i === activeIndex);
      if (i === activeIndex) {
        el.scrollIntoView({ block: 'nearest' });
      }
    });
  };

  /* ── Navigation ─────────────────────────────────────────── */

  const navigateToStock = (slug) => {
    if (!slug) return;
    saveRecent(input?.value || slug);
    closeSearch();
    // Navigate to the share detail page
    window.location.href = `shares.html#${slug}`;
  };

  /* ── Event handlers ─────────────────────────────────────── */

  const handleInput = () => {
    const query = input.value.trim();
    const results = search(query);
    renderResults(results);
  };

  const handleKeydown = (e) => {
    const total = currentResults.length;

    switch (e.key) {
      case 'ArrowDown':
        e.preventDefault();
        activeIndex = total > 0 ? (activeIndex + 1) % total : -1;
        updateActive();
        break;

      case 'ArrowUp':
        e.preventDefault();
        activeIndex = total > 0 ? (activeIndex - 1 + total) % total : -1;
        updateActive();
        break;

      case 'Enter':
        e.preventDefault();
        if (activeIndex >= 0 && activeIndex < total) {
          navigateToStock(currentResults[activeIndex].slug);
        } else if (total > 0) {
          navigateToStock(currentResults[0].slug);
        }
        break;

      case 'Escape':
        e.preventDefault();
        closeSearch();
        break;
    }
  };

  const bindOverlayEvents = () => {
    input?.addEventListener('input', handleInput);
    input?.addEventListener('keydown', handleKeydown);

    // Click on result
    resultsList?.addEventListener('click', (e) => {
      const li = e.target.closest('.search-result');
      if (li) {
        navigateToStock(li.dataset.slug);
      }
    });

    // Mouse hover sets active index
    resultsList?.addEventListener('mouseover', (e) => {
      const li = e.target.closest('.search-result');
      if (li) {
        activeIndex = parseInt(li.dataset.index, 10);
        updateActive();
      }
    });

    // Backdrop click closes
    overlay?.addEventListener('click', (e) => {
      if (e.target === overlay || e.target.classList.contains('search-overlay')) {
        closeSearch();
      }
    });
  };

  /* ── Open / Close ───────────────────────────────────────── */

  const openSearch = () => {
    if (!overlay) createOverlay();
    isOpen = true;
    overlay.classList.add('active');
    document.body.style.overflow = 'hidden';
    renderRecent();
    renderResults([]);

    // Clear and focus
    if (input) {
      input.value = '';
      // Micro-delay so focus works after class toggle
      requestAnimationFrame(() => input.focus());
    }
  };

  const closeSearch = () => {
    if (!overlay) return;
    isOpen = false;
    overlay.classList.remove('active');
    document.body.style.overflow = '';
    activeIndex = -1;
    currentResults = [];
  };

  const toggleSearch = () => {
    isOpen ? closeSearch() : openSearch();
  };

  /* ── Global keyboard shortcut: Ctrl+K / Cmd+K ──────────── */

  const initGlobalShortcut = () => {
    document.addEventListener('keydown', (e) => {
      const isMod = e.ctrlKey || e.metaKey;
      if (isMod && e.key === 'k') {
        e.preventDefault();
        toggleSearch();
        return;
      }

      // Also close on Escape if open
      if (e.key === 'Escape' && isOpen) {
        e.preventDefault();
        closeSearch();
      }
    });
  };

  /* ── Init  ──────────────────────────────────────────────── */

  const init = () => {
    createOverlay();
    initGlobalShortcut();

    // Bind any search trigger buttons on the page
    document.querySelectorAll('[data-search-trigger], .search-trigger, .nav-search-btn').forEach((btn) => {
      btn.addEventListener('click', (e) => {
        e.preventDefault();
        openSearch();
      });
    });
  };

  /* ── Expose globally ────────────────────────────────────── */
  window.Search = {
    init,
    open: openSearch,
    close: closeSearch,
    toggle: toggleSearch
  };
})();
