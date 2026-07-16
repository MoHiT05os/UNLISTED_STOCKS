/**
 * ============================================================
 * SHARES DATA — Unlisted / Pre-IPO Indian Stocks
 * Premium Financial Information Platform
 * ============================================================
 */

(function () {
  'use strict';

  /* ── Helper: slug generator ─────────────────────────────── */
  const toSlug = (str) =>
    str
      .toLowerCase()
      .replace(/[^a-z0-9]+/g, '-')
      .replace(/(^-|-$)/g, '');

  /* ── Helper: generate realistic sparkline data ──────────── */
  const spark = (base, volatility, trend) => {
    const pts = [];
    let v = base;
    for (let i = 0; i < 12; i++) {
      v += (Math.random() - 0.45) * volatility + trend;
      pts.push(Math.round(v * 100) / 100);
    }
    return pts;
  };

  /* ──────────────────────────────────────────────────────────
   *  SHARES DATA  (25+ unlisted / pre-IPO Indian stocks)
   * ────────────────────────────────────────────────────────── */
  const SHARES_DATA = [
    {
      name: 'MSEI (Metropolitan Stock Exchange) Unlisted Shares',
      shortName: 'MSEI',
      sector: 'Financial Services',
      sectorSlug: 'financial-services',
      price: 5.75,
      prevPrice: 5.50,
      lotSize: 5000,
      logoInitials: 'MS',
      logoColor: '#6366f1',
      slug: 'msei-metropolitan-stock-exchange-unlisted-shares',
      hot: false,
      isNew: false,
      sparkData: [5.2, 5.3, 5.1, 5.4, 5.6, 5.5, 5.7, 5.65, 5.8, 5.75, 5.9, 5.75],
      asOf: '2026-07-14'
    },
    {
      name: 'NSE India Limited Unlisted Shares',
      shortName: 'NSE India',
      sector: 'Financial Services',
      sectorSlug: 'financial-services',
      price: 2095,
      prevPrice: 1980,
      lotSize: 250,
      logoInitials: 'NI',
      logoColor: '#2563eb',
      slug: 'nse-india-limited-unlisted-shares',
      hot: true,
      isNew: false,
      sparkData: [1920, 1945, 1960, 1980, 1995, 2010, 2030, 2055, 2040, 2070, 2085, 2095],
      asOf: '2026-07-14'
    },
    {
      name: 'HPX India Unlisted Shares',
      shortName: 'HPX India',
      sector: 'Energy',
      sectorSlug: 'energy',
      price: 24.5,
      prevPrice: 23.0,
      lotSize: 2000,
      logoInitials: 'HX',
      logoColor: '#0891b2',
      slug: 'hpx-india-unlisted-shares',
      hot: false,
      isNew: true,
      sparkData: [21.5, 22.0, 22.3, 22.8, 23.0, 23.2, 23.8, 24.0, 23.5, 24.2, 24.4, 24.5],
      asOf: '2026-07-14'
    },
    {
      name: 'Onix Renewable Limited Unlisted Shares',
      shortName: 'Onix Renewable',
      sector: 'Renewable Energy',
      sectorSlug: 'renewable-energy',
      price: 54,
      prevPrice: 50,
      lotSize: 1000,
      logoInitials: 'OR',
      logoColor: '#16a34a',
      slug: 'onix-renewable-limited-unlisted-shares',
      hot: false,
      isNew: true,
      sparkData: [48, 49, 50, 49.5, 51, 52, 51.5, 53, 52, 53.5, 54, 54],
      asOf: '2026-07-14'
    },
    {
      name: 'GFCL EV Unlisted Shares',
      shortName: 'GFCL EV',
      sector: 'Electric Vehicles',
      sectorSlug: 'electric-vehicles',
      price: 41,
      prevPrice: 38.5,
      lotSize: 1000,
      logoInitials: 'GE',
      logoColor: '#7c3aed',
      slug: 'gfcl-ev-unlisted-shares',
      hot: false,
      isNew: false,
      sparkData: [36, 37, 37.5, 38, 38.5, 39, 39.5, 40, 39.8, 40.5, 41, 41],
      asOf: '2026-07-14'
    },
    {
      name: 'GH2 Solar Unlisted Shares',
      shortName: 'GH2 Solar',
      sector: 'Renewable Energy',
      sectorSlug: 'renewable-energy',
      price: 242,
      prevPrice: 230,
      lotSize: 500,
      logoInitials: 'GS',
      logoColor: '#ea580c',
      slug: 'gh2-solar-unlisted-shares',
      hot: true,
      isNew: false,
      sparkData: [220, 222, 225, 228, 230, 232, 235, 238, 236, 240, 241, 242],
      asOf: '2026-07-14'
    },
    {
      name: 'Zepto Unlisted Shares',
      shortName: 'Zepto',
      sector: 'E-Commerce',
      sectorSlug: 'e-commerce',
      price: 39,
      prevPrice: 35,
      lotSize: 2000,
      logoInitials: 'ZP',
      logoColor: '#dc2626',
      slug: 'zepto-unlisted-shares',
      hot: true,
      isNew: false,
      sparkData: [32, 33, 34, 34.5, 35, 36, 36.5, 37, 37.5, 38, 38.5, 39],
      asOf: '2026-07-14'
    },
    {
      name: 'OYO Rooms Unlisted Shares',
      shortName: 'OYO',
      sector: 'Hospitality',
      sectorSlug: 'hospitality',
      price: 25,
      prevPrice: 23,
      lotSize: 2000,
      logoInitials: 'OY',
      logoColor: '#e11d48',
      slug: 'oyo-rooms-unlisted-shares',
      hot: true,
      isNew: false,
      sparkData: [21, 21.5, 22, 22.5, 23, 23, 23.5, 24, 24, 24.5, 25, 25],
      asOf: '2026-07-14'
    },
    {
      name: 'Hinduja Leyland Finance Unlisted Shares',
      shortName: 'Hinduja Leyland Finance',
      sector: 'Financial Services',
      sectorSlug: 'financial-services',
      price: 238,
      prevPrice: 225,
      lotSize: 500,
      logoInitials: 'HL',
      logoColor: '#0d9488',
      slug: 'hinduja-leyland-finance-unlisted-shares',
      hot: false,
      isNew: false,
      sparkData: [218, 220, 222, 224, 225, 227, 230, 232, 234, 235, 237, 238],
      asOf: '2026-07-14'
    },
    {
      name: 'Cochin International Airport Unlisted Shares',
      shortName: 'Cochin Airport',
      sector: 'Infrastructure',
      sectorSlug: 'infrastructure',
      price: 464,
      prevPrice: 440,
      lotSize: 250,
      logoInitials: 'CA',
      logoColor: '#1d4ed8',
      slug: 'cochin-international-airport-unlisted-shares',
      hot: true,
      isNew: false,
      sparkData: [430, 435, 438, 440, 442, 445, 450, 455, 452, 458, 462, 464],
      asOf: '2026-07-14'
    },
    {
      name: 'ORBIS Financial Corporation Unlisted Shares',
      shortName: 'ORBIS Financial',
      sector: 'Financial Services',
      sectorSlug: 'financial-services',
      price: 385,
      prevPrice: 370,
      lotSize: 500,
      logoInitials: 'OF',
      logoColor: '#4f46e5',
      slug: 'orbis-financial-corporation-unlisted-shares',
      hot: false,
      isNew: false,
      sparkData: [360, 362, 365, 368, 370, 372, 375, 378, 380, 382, 384, 385],
      asOf: '2026-07-14'
    },
    {
      name: 'Chennai Super Kings (CSK) Unlisted Shares',
      shortName: 'CSK',
      sector: 'Sports & Entertainment',
      sectorSlug: 'sports-entertainment',
      price: 256,
      prevPrice: 240,
      lotSize: 500,
      logoInitials: 'CK',
      logoColor: '#eab308',
      slug: 'chennai-super-kings-csk-unlisted-shares',
      hot: true,
      isNew: false,
      sparkData: [230, 232, 235, 238, 240, 242, 245, 248, 250, 252, 255, 256],
      asOf: '2026-07-14'
    },
    {
      name: 'PPFAS Asset Management Unlisted Shares',
      shortName: 'PPFAS',
      sector: 'Asset Management',
      sectorSlug: 'asset-management',
      price: 18250,
      prevPrice: 17500,
      lotSize: 10,
      logoInitials: 'PP',
      logoColor: '#059669',
      slug: 'ppfas-asset-management-unlisted-shares',
      hot: true,
      isNew: false,
      sparkData: [16800, 17000, 17200, 17300, 17500, 17600, 17800, 17900, 18000, 18100, 18200, 18250],
      asOf: '2026-07-14'
    },
    {
      name: 'Motilal Oswal Home Finance Unlisted Shares',
      shortName: 'Motilal Oswal Home Finance',
      sector: 'Financial Services',
      sectorSlug: 'financial-services',
      price: 11.95,
      prevPrice: 11.20,
      lotSize: 5000,
      logoInitials: 'MO',
      logoColor: '#b45309',
      slug: 'motilal-oswal-home-finance-unlisted-shares',
      hot: false,
      isNew: false,
      sparkData: [10.5, 10.7, 10.9, 11.0, 11.2, 11.1, 11.3, 11.5, 11.4, 11.7, 11.8, 11.95],
      asOf: '2026-07-14'
    },
    {
      name: 'Polymatech Electronics Unlisted Shares',
      shortName: 'Polymatech',
      sector: 'Electronics',
      sectorSlug: 'electronics',
      price: 53,
      prevPrice: 50,
      lotSize: 1000,
      logoInitials: 'PE',
      logoColor: '#9333ea',
      slug: 'polymatech-electronics-unlisted-shares',
      hot: false,
      isNew: false,
      sparkData: [47, 48, 49, 49.5, 50, 50.5, 51, 51.5, 52, 52.5, 53, 53],
      asOf: '2026-07-14'
    },
    {
      name: 'NCDEX Unlisted Shares',
      shortName: 'NCDEX',
      sector: 'Financial Services',
      sectorSlug: 'financial-services',
      price: 428,
      prevPrice: 410,
      lotSize: 250,
      logoInitials: 'NC',
      logoColor: '#0369a1',
      slug: 'ncdex-unlisted-shares',
      hot: false,
      isNew: false,
      sparkData: [400, 402, 405, 408, 410, 412, 415, 418, 420, 423, 426, 428],
      asOf: '2026-07-14'
    },
    {
      name: 'Kineco Limited Unlisted Shares',
      shortName: 'Kineco',
      sector: 'Manufacturing',
      sectorSlug: 'manufacturing',
      price: 3250,
      prevPrice: 3100,
      lotSize: 50,
      logoInitials: 'KN',
      logoColor: '#475569',
      slug: 'kineco-limited-unlisted-shares',
      hot: false,
      isNew: false,
      sparkData: [3000, 3020, 3050, 3080, 3100, 3120, 3150, 3170, 3190, 3210, 3230, 3250],
      asOf: '2026-07-14'
    },
    {
      name: 'Apollo Green Energy Unlisted Shares',
      shortName: 'Apollo Green Energy',
      sector: 'Renewable Energy',
      sectorSlug: 'renewable-energy',
      price: 92,
      prevPrice: 85,
      lotSize: 500,
      logoInitials: 'AG',
      logoColor: '#15803d',
      slug: 'apollo-green-energy-unlisted-shares',
      hot: false,
      isNew: true,
      sparkData: [80, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92],
      asOf: '2026-07-14'
    },
    {
      name: 'Mohan Meakin Limited Unlisted Shares',
      shortName: 'Mohan Meakin',
      sector: 'FMCG',
      sectorSlug: 'fmcg',
      price: 2425,
      prevPrice: 2350,
      lotSize: 50,
      logoInitials: 'MM',
      logoColor: '#92400e',
      slug: 'mohan-meakin-limited-unlisted-shares',
      hot: false,
      isNew: false,
      sparkData: [2280, 2300, 2310, 2330, 2350, 2360, 2370, 2380, 2390, 2400, 2415, 2425],
      asOf: '2026-07-14'
    },
    {
      name: 'PharmEasy Unlisted Shares',
      shortName: 'PharmEasy',
      sector: 'Healthcare',
      sectorSlug: 'healthcare',
      price: 8.5,
      prevPrice: 9.0,
      lotSize: 5000,
      logoInitials: 'PH',
      logoColor: '#be123c',
      slug: 'pharmeasy-unlisted-shares',
      hot: false,
      isNew: false,
      sparkData: [10.5, 10.2, 9.8, 9.5, 9.2, 9.0, 8.8, 8.7, 8.6, 8.5, 8.5, 8.5],
      asOf: '2026-07-14'
    },
    {
      name: 'SBI Mutual Fund Unlisted Shares',
      shortName: 'SBI Mutual Fund',
      sector: 'Asset Management',
      sectorSlug: 'asset-management',
      price: 575,
      prevPrice: 550,
      lotSize: 250,
      logoInitials: 'SM',
      logoColor: '#1e40af',
      slug: 'sbi-mutual-fund-unlisted-shares',
      hot: true,
      isNew: false,
      sparkData: [530, 535, 540, 545, 550, 552, 555, 560, 565, 568, 572, 575],
      asOf: '2026-07-14'
    },
    {
      name: 'boAt Lifestyle Unlisted Shares',
      shortName: 'boAt',
      sector: 'Consumer Electronics',
      sectorSlug: 'consumer-electronics',
      price: 1850,
      prevPrice: 1780,
      lotSize: 100,
      logoInitials: 'BT',
      logoColor: '#dc2626',
      slug: 'boat-lifestyle-unlisted-shares',
      hot: true,
      isNew: false,
      sparkData: [1720, 1735, 1750, 1765, 1780, 1790, 1800, 1810, 1820, 1835, 1845, 1850],
      asOf: '2026-07-14'
    },
    {
      name: 'Swiggy ESOP Unlisted Shares',
      shortName: 'Swiggy ESOP',
      sector: 'Food Delivery',
      sectorSlug: 'food-delivery',
      price: 395,
      prevPrice: 380,
      lotSize: 500,
      logoInitials: 'SW',
      logoColor: '#f97316',
      slug: 'swiggy-esop-unlisted-shares',
      hot: false,
      isNew: false,
      sparkData: [365, 368, 372, 375, 380, 382, 385, 388, 390, 392, 394, 395],
      asOf: '2026-07-14'
    },
    {
      name: 'Bira 91 Unlisted Shares',
      shortName: 'Bira91',
      sector: 'FMCG',
      sectorSlug: 'fmcg',
      price: 450,
      prevPrice: 430,
      lotSize: 250,
      logoInitials: 'B9',
      logoColor: '#d97706',
      slug: 'bira-91-unlisted-shares',
      hot: false,
      isNew: true,
      sparkData: [415, 418, 420, 425, 430, 432, 435, 438, 440, 445, 448, 450],
      asOf: '2026-07-14'
    },
    {
      name: 'Ather Energy Unlisted Shares',
      shortName: 'Ather Energy',
      sector: 'Electric Vehicles',
      sectorSlug: 'electric-vehicles',
      price: 620,
      prevPrice: 590,
      lotSize: 200,
      logoInitials: 'AE',
      logoColor: '#10b981',
      slug: 'ather-energy-unlisted-shares',
      hot: true,
      isNew: false,
      sparkData: [570, 575, 580, 585, 590, 595, 600, 605, 608, 612, 617, 620],
      asOf: '2026-07-14'
    },
    {
      name: 'HDB Financial Services Unlisted Shares',
      shortName: 'HDB Financial',
      sector: 'Financial Services',
      sectorSlug: 'financial-services',
      price: 1450,
      prevPrice: 1390,
      lotSize: 100,
      logoInitials: 'HF',
      logoColor: '#1e3a5f',
      slug: 'hdb-financial-services-unlisted-shares',
      hot: true,
      isNew: false,
      sparkData: [1350, 1360, 1375, 1380, 1390, 1400, 1410, 1420, 1430, 1440, 1445, 1450],
      asOf: '2026-07-14'
    },
    {
      name: 'Studds Accessories Unlisted Shares',
      shortName: 'Studds',
      sector: 'Auto Ancillaries',
      sectorSlug: 'auto-ancillaries',
      price: 875,
      prevPrice: 850,
      lotSize: 200,
      logoInitials: 'SA',
      logoColor: '#374151',
      slug: 'studds-accessories-unlisted-shares',
      hot: false,
      isNew: false,
      sparkData: [830, 835, 840, 842, 850, 855, 858, 862, 865, 868, 872, 875],
      asOf: '2026-07-14'
    },
    {
      name: 'Vikram Solar Unlisted Shares',
      shortName: 'Vikram Solar',
      sector: 'Renewable Energy',
      sectorSlug: 'renewable-energy',
      price: 340,
      prevPrice: 320,
      lotSize: 500,
      logoInitials: 'VS',
      logoColor: '#f59e0b',
      slug: 'vikram-solar-unlisted-shares',
      hot: false,
      isNew: true,
      sparkData: [305, 308, 312, 315, 320, 322, 325, 328, 332, 335, 338, 340],
      asOf: '2026-07-14'
    }
  ];

  /* ──────────────────────────────────────────────────────────
   *  SECTORS DATA
   * ────────────────────────────────────────────────────────── */

  /** Count stocks per sector slug */
  const sectorCounts = {};
  SHARES_DATA.forEach((s) => {
    sectorCounts[s.sectorSlug] = (sectorCounts[s.sectorSlug] || 0) + 1;
  });

  const SECTORS_DATA = [
    {
      name: 'Financial Services',
      slug: 'financial-services',
      count: sectorCounts['financial-services'] || 0,
      icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M3 21h18"/><path d="M3 10h18"/><path d="M5 6l7-3 7 3"/><path d="M4 10v11"/><path d="M20 10v11"/><path d="M8 14v3"/><path d="M12 14v3"/><path d="M16 14v3"/></svg>'
    },
    {
      name: 'Renewable Energy',
      slug: 'renewable-energy',
      count: sectorCounts['renewable-energy'] || 0,
      icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2"/><path d="M12 20v2"/><path d="m4.93 4.93 1.41 1.41"/><path d="m17.66 17.66 1.41 1.41"/><path d="M2 12h2"/><path d="M20 12h2"/><path d="m6.34 17.66-1.41 1.41"/><path d="m19.07 4.93-1.41 1.41"/></svg>'
    },
    {
      name: 'Electric Vehicles',
      slug: 'electric-vehicles',
      count: sectorCounts['electric-vehicles'] || 0,
      icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M7 17m-2 0a2 2 0 1 0 4 0 2 2 0 1 0-4 0"/><path d="M17 17m-2 0a2 2 0 1 0 4 0 2 2 0 1 0-4 0"/><path d="M5 17H3v-6l2-5h9l4 5h1a2 2 0 0 1 2 2v4h-2"/><path d="M9 17h6"/><path d="M14 7l-3 5"/></svg>'
    },
    {
      name: 'E-Commerce',
      slug: 'e-commerce',
      count: sectorCounts['e-commerce'] || 0,
      icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="9" cy="21" r="1"/><circle cx="20" cy="21" r="1"/><path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"/></svg>'
    },
    {
      name: 'Hospitality',
      slug: 'hospitality',
      count: sectorCounts['hospitality'] || 0,
      icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M3 21h18"/><path d="M5 21V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2v16"/><path d="M9 7h1"/><path d="M14 7h1"/><path d="M9 11h1"/><path d="M14 11h1"/><path d="M9 15h1"/><path d="M14 15h1"/></svg>'
    },
    {
      name: 'Infrastructure',
      slug: 'infrastructure',
      count: sectorCounts['infrastructure'] || 0,
      icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M2 20h20"/><path d="m5 20-.5-3h15l-.5 3"/><path d="M12 2c-2.5 2-4 4.5-4 7a4 4 0 0 0 8 0c0-2.5-1.5-5-4-7Z"/></svg>'
    },
    {
      name: 'Sports & Entertainment',
      slug: 'sports-entertainment',
      count: sectorCounts['sports-entertainment'] || 0,
      icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20"/><path d="M2 12h20"/></svg>'
    },
    {
      name: 'Asset Management',
      slug: 'asset-management',
      count: sectorCounts['asset-management'] || 0,
      icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M22 12h-4l-3 9L9 3l-3 9H2"/></svg>'
    },
    {
      name: 'Healthcare',
      slug: 'healthcare',
      count: sectorCounts['healthcare'] || 0,
      icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M8 2v4"/><path d="M16 2v4"/><path d="M12 10v6"/><path d="M9 13h6"/><rect x="4" y="4" width="16" height="16" rx="2"/></svg>'
    },
    {
      name: 'Consumer Electronics',
      slug: 'consumer-electronics',
      count: sectorCounts['consumer-electronics'] || 0,
      icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="3" width="20" height="14" rx="2" ry="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/></svg>'
    },
    {
      name: 'Food Delivery',
      slug: 'food-delivery',
      count: sectorCounts['food-delivery'] || 0,
      icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M17 8C8 10 5.9 16.17 3.82 21.34l1.89.66.95-2.3c.48.17.98.3 1.34.3C19 20 22 3 22 3c-1 2-8 2.25-13 3.25S2 11.5 2 13.5s1.75 3.75 1.75 3.75"/></svg>'
    },
    {
      name: 'FMCG',
      slug: 'fmcg',
      count: sectorCounts['fmcg'] || 0,
      icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M6 2 3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4Z"/><path d="M3 6h18"/><path d="M16 10a4 4 0 0 1-8 0"/></svg>'
    },
    {
      name: 'Manufacturing',
      slug: 'manufacturing',
      count: sectorCounts['manufacturing'] || 0,
      icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M2 20a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V8l-7 5V8l-7 5V4a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2Z"/></svg>'
    },
    {
      name: 'Electronics',
      slug: 'electronics',
      count: sectorCounts['electronics'] || 0,
      icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="4" width="16" height="16" rx="2"/><rect x="9" y="9" width="6" height="6"/><path d="M15 2v2"/><path d="M15 20v2"/><path d="M2 15h2"/><path d="M2 9h2"/><path d="M20 15h2"/><path d="M20 9h2"/><path d="M9 2v2"/><path d="M9 20v2"/></svg>'
    },
    {
      name: 'Energy',
      slug: 'energy',
      count: sectorCounts['energy'] || 0,
      icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>'
    },
    {
      name: 'Auto Ancillaries',
      slug: 'auto-ancillaries',
      count: sectorCounts['auto-ancillaries'] || 0,
      icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06A1.65 1.65 0 0 0 9 4.68a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>'
    }
  ];

  /* ── Expose globally ────────────────────────────────────── */
  window.SHARES_DATA = SHARES_DATA;
  window.SECTORS_DATA = SECTORS_DATA;
})();
