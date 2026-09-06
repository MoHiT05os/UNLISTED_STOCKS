"""
╔══════════════════════════════════════════════════════════════════╗
║   MDB ARTHASPHERE — Live IPO GMP Auto-Scraper                    ║
║   Automatically pulls live GMP data and updates the website.     ║
║                                                                  ║
║   Prerequisites:                                                 ║
║   pip install playwright                                         ║
║   playwright install chromium                                    ║
║                                                                  ║
║   Run: python scrape_gmp.py                                      ║
╚══════════════════════════════════════════════════════════════════╝
"""

import asyncio
import json
import os
import re
from datetime import datetime

try:
    from playwright.async_api import async_playwright
except ImportError:
    print("[!] Missing playwright. Run: pip install playwright && playwright install chromium")
    import sys
    sys.exit(1)

# ── Config ─────────────────────────────────────────────────────────
TARGET_URL = 'https://www.investorgain.com/report/ipo-gmp-live/331/'
OUTPUT_FILE = 'js/gmp-data.js'

async def scrape_gmp_data():
    print(f"--- Starting Live Auto-Scraper ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')}) ---")
    print(f"[*] Launching headless browser...")
    
    async with async_playwright() as p:
        # Launch Chromium headless
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        
        print(f"[*] Navigating to {TARGET_URL}...")
        # Go to the URL and wait for network to be idle (so the JS table loads)
        await page.goto(TARGET_URL, wait_until='networkidle')
        
        # Wait specifically for the table body to contain tr elements
        try:
            await page.wait_for_selector('table tbody tr', timeout=10000)
        except Exception as e:
            print("[!] Timeout waiting for table to load.")
            await browser.close()
            return
        
        print(f"[*] Table found. Extracting data...")
        
        # Evaluate JavaScript directly in the page to extract the table rows
        scraped_data = await page.evaluate('''() => {
            const rows = document.querySelectorAll('table tbody tr');
            const data = [];
            
            rows.forEach((row, index) => {
                const cells = row.querySelectorAll('td, th');
                if (cells.length < 10) return; // Skip invalid rows
                
                try {
                    // Extracting the columns based on InvestorGain standard format
                    // 0: IPO, 1: Price, 2: GMP, 3: Est Listing, 4: IPO Size, 5: Lot, 6: Open, 7: Close, 8: BoA, 9: Listing, 10: GMP Update
                    
                    const nameCell = cells[0].innerText.trim();
                    const nameMatch = nameCell.match(/(.*?)(?:SME)?$/i);
                    let name = nameMatch ? nameMatch[1].trim() : nameCell;
                    const type = nameCell.toLowerCase().includes('sme') ? 'SME' : 'Mainboard';
                    
                    // Cleanup name
                    name = name.replace(' IPO', '').trim();
                    const id = name.toLowerCase().replace(/[^a-z0-9]+/g, '-');
                    
                    const price = cells[1].innerText.trim();
                    const gmpText = cells[2].innerText.trim();
                    const estListText = cells[3].innerText.trim();
                    
                    // Parse GMP (handle "--" or missing)
                    let gmp = 0;
                    const gmpMatch = gmpText.match(/[-]?\\d+/);
                    if (gmpMatch) gmp = parseInt(gmpMatch[0]);
                    
                    // Parse Est Listing & Gain
                    let estListing = 0;
                    let gainPct = 0;
                    const estMatch = estListText.match(/(\\d+)/);
                    if (estMatch) estListing = parseInt(estMatch[1]);
                    
                    const pctMatch = estListText.match(/\\(([-]?\\d+\\.?\\d*)%\\)/);
                    if (pctMatch) gainPct = parseFloat(pctMatch[1]);
                    
                    const lotSize = cells[5].innerText.trim();
                    const openDate = cells[6].innerText.trim();
                    const closeDate = cells[7].innerText.trim();
                    const listingDate = cells[9].innerText.trim();
                    
                    // Determine Status based on dates
                    let status = "Upcoming";
                    const today = new Date();
                    // Basic status logic (can be refined)
                    
                    data.push({
                        id: id,
                        name: name,
                        type: type,
                        priceBand: price,
                        price: parseInt(price.split('-').pop()) || 0,
                        gmp: gmp,
                        estListing: estListing,
                        gainPct: gainPct,
                        subTotal: "--",
                        subRetail: "--",
                        openDate: openDate,
                        closeDate: closeDate,
                        listingDate: listingDate,
                        lotSize: lotSize,
                        status: status,
                        subjectToSauda: 0,
                        kostak: 0
                    });
                } catch(e) {
                    console.error("Error parsing row", e);
                }
            });
            return data;
        }''')
        
        await browser.close()
        
        if not scraped_data:
            print("[!] No data extracted. Format may have changed.")
            return
            
        print(f"[*] Successfully scraped {len(scraped_data)} IPOs!")
        
        # Write to JS file
        js_content = f"(function () {{\n  'use strict';\n\n  // Auto-scraped Live IPO GMP Data ({datetime.now().strftime('%Y-%m-%d %H:%M')})\n  window.GMP_DATA = {json.dumps(scraped_data, indent=4)};\n}})();\n"
        
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            f.write(js_content)
            
        print(f"[*] Successfully updated {OUTPUT_FILE}")
        print(f"--- Scraping Complete ---")

if __name__ == '__main__':
    asyncio.run(scrape_gmp_data())
