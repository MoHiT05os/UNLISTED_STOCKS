/**
 * ============================================================
 * COMPONENTS — Card Renderers · Pagination · Grid Builder
 * Premium Financial Information Platform
 * ============================================================
 */

(function () {
  'use strict';

  /* ── Price & change helpers ─────────────────────────────── */

  const formatPrice = (price) => {
    if (price == null || isNaN(price)) return '—';
    return '₹' + Number(price).toLocaleString('en-IN', { maximumFractionDigits: 2 });
  };

  const calcChange = (current, prev) => {
    if (!prev || prev === 0 || current == null) return { pct: 0, abs: 0 };
    const abs = current - prev;
    const pct = (abs / prev) * 100;
    return { pct, abs };
  };

  const changeHTML = (current, prev) => {
    const { pct, abs } = calcChange(current, prev);
    const isUp = pct >= 0;
    const sign = isUp ? '+' : '';
    const cls = isUp ? 'change-up' : 'change-down';
    const arrow = isUp
      ? '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="18 15 12 9 6 15"/></svg>'
      : '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="6 9 12 15 18 9"/></svg>';

    return `<span class="price-change ${cls}">${arrow} ${sign}${pct.toFixed(2)}%</span>`;
  };

  /* ── Sparkline via Animations module ────────────────────── */

  const getSparkline = (stock) => {
    if (!stock.sparkData || stock.sparkData.length < 2) return '';
    const isUp = stock.price >= (stock.prevPrice || stock.price);
    const color = isUp ? '#10b981' : '#ef4444';
    if (window.Animations?.generateSparkline) {
      return window.Animations.generateSparkline(stock.sparkData, 120, 40, color);
    }
    return '';
  };

  /* ──────────────────────────────────────────────────────────
   *  renderShareCard — glassmorphism share card
   * ────────────────────────────────────────────────────────── */

  const renderShareCard = (stock) => {
    if (!stock) return '';

    const name = stock.shortName || stock.name || 'Unknown';
    const fullName = stock.name || name;
    const sector = stock.sector || 'General';
    const price = formatPrice(stock.price);
    const logoColor = stock.logoColor || '#6366f1';
    const logoInitials = stock.logoInitials || name.substring(0, 2).toUpperCase();
    const slug = stock.slug || '';
    const sparkSVG = getSparkline(stock);

    const badges = [];
    if (stock.hot) {
      badges.push('<span class="badge badge-hot">🔥 Hot</span>');
    }
    if (stock.isNew) {
      badges.push('<span class="badge badge-new">✨ New</span>');
    }

    const change = changeHTML(stock.price, stock.prevPrice);

    return `
    <div class="share-card reveal" data-slug="${slug}">
      <div class="card-top">
        <div class="logo-circle" style="background:${logoColor}">
          <span>${logoInitials}</span>
        </div>
        <div class="card-info">
          <h3 class="card-name" title="${fullName}">${name}</h3>
          <span class="card-sector">${sector}</span>
        </div>
        ${badges.length ? `<div class="card-badges">${badges.join('')}</div>` : ''}
      </div>

      <div class="card-sparkline">
        ${sparkSVG}
      </div>

      <div class="card-price">
        <div class="price-row">
          <span class="price-value">${price}</span>
          ${change}
        </div>
        <span class="tag-indicative">Indicative Price</span>
      </div>

      <div class="card-actions">
        <a href="https://wa.me/919999999999?text=Hi%2C%20I%20am%20interested%20in%20${encodeURIComponent(fullName)}" 
           class="btn btn-primary" target="_blank" rel="noopener noreferrer">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
          Enquire
        </a>
        <a href="stock.html?symbol=${slug}" class="btn btn-ghost">
          Details
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>
        </a>
      </div>
    </div>`;
  };

  /* ──────────────────────────────────────────────────────────
   *  renderSectorCard
   * ────────────────────────────────────────────────────────── */

  const renderSectorCard = (sector) => {
    if (!sector) return '';

    const name = sector.name || 'Unknown';
    const slug = sector.slug || '';
    const count = sector.count || 0;
    const icon = sector.icon || '';

    return `
    <a href="shares.html#sector-${slug}" class="sector-card reveal">
      <div class="sector-icon">${icon}</div>
      <h3 class="sector-name">${name}</h3>
      <span class="sector-count">${count} ${count === 1 ? 'Share' : 'Shares'}</span>
      <svg class="sector-arrow" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>
    </a>`;
  };

  /* ──────────────────────────────────────────────────────────
   *  renderVideoCard
   * ────────────────────────────────────────────────────────── */

  const renderVideoCard = (video) => {
    if (!video) return '';

    const title = video.title || 'Untitled Video';
    const thumbnail = video.thumbnail || '';
    const url = video.url || '#';
    const duration = video.duration || '';
    const views = video.views || '';

    return `
    <a href="${url}" class="video-card reveal" target="_blank" rel="noopener noreferrer">
      <div class="video-thumb">
        ${thumbnail
          ? `<img src="${thumbnail}" alt="${title}" loading="lazy" />`
          : `<div class="video-thumb-placeholder">
              <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><polygon points="5 3 19 12 5 21 5 3"/></svg>
            </div>`
        }
        ${duration ? `<span class="video-duration">${duration}</span>` : ''}
        <div class="video-play-btn">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor"><polygon points="5 3 19 12 5 21 5 3"/></svg>
        </div>
      </div>
      <div class="video-info">
        <h4 class="video-title">${title}</h4>
        ${views ? `<span class="video-views">${views} views</span>` : ''}
      </div>
    </a>`;
  };

  /* ──────────────────────────────────────────────────────────
   *  renderBlogCard
   * ────────────────────────────────────────────────────────── */

  const renderBlogCard = (post) => {
    if (!post) return '';

    const title = post.title || 'Untitled';
    const excerpt = post.excerpt || '';
    const date = post.date || '';
    const category = post.category || '';
    const url = post.url || '#';
    const image = post.image || '';
    const readTime = post.readTime || '';

    return `
    <a href="${url}" class="blog-card reveal">
      ${image
        ? `<div class="blog-image"><img src="${image}" alt="${title}" loading="lazy" /></div>`
        : ''
      }
      <div class="blog-body">
        ${category ? `<span class="blog-category">${category}</span>` : ''}
        <h4 class="blog-title">${title}</h4>
        ${excerpt ? `<p class="blog-excerpt">${excerpt}</p>` : ''}
        <div class="blog-meta">
          ${date ? `<span class="blog-date">${date}</span>` : ''}
          ${readTime ? `<span class="blog-read">${readTime}</span>` : ''}
        </div>
      </div>
    </a>`;
  };

  /* ──────────────────────────────────────────────────────────
   *  renderSharesGrid — paginated grid of share cards
   * ────────────────────────────────────────────────────────── */

  const renderSharesGrid = (container, stocks, page = 1, perPage = 12) => {
    if (!container) return;
    if (!stocks || stocks.length === 0) {
      container.innerHTML = `
        <div class="empty-state">
          <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1" opacity="0.3">
            <rect x="2" y="7" width="20" height="14" rx="2" ry="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/>
          </svg>
          <p>No shares found.</p>
        </div>`;
      return;
    }

    const start = (page - 1) * perPage;
    const end = start + perPage;
    const pageStocks = stocks.slice(start, end);

    container.innerHTML = pageStocks.map((s) => renderShareCard(s)).join('');
  };

  /* ──────────────────────────────────────────────────────────
   *  setupPagination
   * ────────────────────────────────────────────────────────── */

  const setupPagination = (container, totalItems, perPage, currentPage, onPageChange) => {
    if (!container) return;

    const totalPages = Math.ceil(totalItems / perPage);
    if (totalPages <= 1) {
      container.innerHTML = '';
      return;
    }

    const pages = [];
    const range = 2; // pages around current to show

    // Always show first page
    pages.push(1);

    const rangeStart = Math.max(2, currentPage - range);
    const rangeEnd = Math.min(totalPages - 1, currentPage + range);

    if (rangeStart > 2) pages.push('...');
    for (let i = rangeStart; i <= rangeEnd; i++) pages.push(i);
    if (rangeEnd < totalPages - 1) pages.push('...');

    // Always show last page if > 1
    if (totalPages > 1) pages.push(totalPages);

    const prevDisabled = currentPage <= 1 ? 'disabled' : '';
    const nextDisabled = currentPage >= totalPages ? 'disabled' : '';

    container.innerHTML = `
      <div class="pagination">
        <button class="page-btn page-prev" ${prevDisabled} aria-label="Previous page">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="15 18 9 12 15 6"/></svg>
        </button>
        ${pages
          .map((p) => {
            if (p === '...') {
              return '<span class="page-ellipsis">…</span>';
            }
            const active = p === currentPage ? 'active' : '';
            return `<button class="page-btn page-num ${active}" data-page="${p}">${p}</button>`;
          })
          .join('')}
        <button class="page-btn page-next" ${nextDisabled} aria-label="Next page">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 18 15 12 9 6"/></svg>
        </button>
      </div>`;

    // Bind click handlers
    container.querySelectorAll('.page-num').forEach((btn) => {
      btn.addEventListener('click', () => {
        const page = parseInt(btn.dataset.page, 10);
        if (page && typeof onPageChange === 'function') {
          onPageChange(page);
        }
      });
    });

    container.querySelector('.page-prev')?.addEventListener('click', () => {
      if (currentPage > 1 && typeof onPageChange === 'function') {
        onPageChange(currentPage - 1);
      }
    });

    container.querySelector('.page-next')?.addEventListener('click', () => {
      if (currentPage < totalPages && typeof onPageChange === 'function') {
        onPageChange(currentPage + 1);
      }
    });
  };

  /* ──────────────────────────────────────────────────────────
   *  renderSkeletonCards — shimmer loading placeholders
   * ────────────────────────────────────────────────────────── */

  const renderSkeletonCards = (container, count = 6) => {
    if (!container) return;

    const skeleton = `
      <div class="share-card skeleton">
        <div class="card-top">
          <div class="skeleton-circle"></div>
          <div class="card-info">
            <div class="skeleton-line skeleton-line--lg"></div>
            <div class="skeleton-line skeleton-line--sm"></div>
          </div>
        </div>
        <div class="card-sparkline">
          <div class="skeleton-sparkline"></div>
        </div>
        <div class="card-price">
          <div class="skeleton-line skeleton-line--md"></div>
          <div class="skeleton-line skeleton-line--xs"></div>
        </div>
        <div class="card-actions">
          <div class="skeleton-btn"></div>
          <div class="skeleton-btn"></div>
        </div>
      </div>`;

    container.innerHTML = Array(count).fill(skeleton).join('');
  };

  /* ── Expose globally ────────────────────────────────────── */
  window.Components = {
    renderShareCard,
    renderSectorCard,
    renderVideoCard,
    renderBlogCard,
    renderSharesGrid,
    setupPagination,
    renderSkeletonCards,
    formatPrice,
    calcChange
  };
})();
