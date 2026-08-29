import re

path = r'C:\Users\TheRealMohitYadav\Videos\UNLISTED_STOCKS\screener.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update slider default values to show all data initially
replacements = {
    'ebitda-range': ('5000', '0'),
    'ebitda-margin': ('30', '0'),
    'ebit-margin': ('25', '0'),
    'rev-growth': ('30', '0'),
    'ebitda-growth': ('20', '0'),
    'ebit-growth': ('20', '0'),
    'arr-growth': ('50', '0'),
    'ev-ebitda': ('40', '100'),
    'price-range': ('25000', '50000'),
    'risk-score': ('7', '10')
}

for r_id, (old_val, new_val) in replacements.items():
    content = re.sub(rf'(<input type="range"[^>]+id="{r_id}"[^>]*value=")({old_val})(")', rf'\g<1>{new_val}\g<3>', content)
    content = re.sub(rf'(<input type="range"[^>]+value=")({old_val})("[^>]*id="{r_id}")', rf'\g<1>{new_val}\g<3>', content)

# 2. Add filter trigger to slider inputs
content = content.replace(
    "document.getElementById(cfg.el).textContent = cfg.fmt(el.value);",
    "document.getElementById(cfg.el).textContent = cfg.fmt(el.value);\n      applyFilters();"
)

# 3. Add filter trigger to checkboxes
content = content.replace(
    'function resetFilters() {',
    '''
  document.querySelectorAll('.filter-sidebar input[type=checkbox]').forEach(cb => {
    cb.addEventListener('change', applyFilters);
  });

  function resetFilters() {'''
)

# 4. Implement applyFilters logic
filter_logic = '''
  function applyFilters() {
    let data = [...(window._allShares || [])];

    // Read range slider values
    const minEbitda = parseFloat(document.getElementById('ebitda-range').value) || 0;
    const minEbitdaMgn = parseFloat(document.getElementById('ebitda-margin').value) || 0;
    const minRevGrowth = parseFloat(document.getElementById('rev-growth').value) || 0;
    const maxEv = parseFloat(document.getElementById('ev-ebitda').value) || 100;
    const maxPrice = parseFloat(document.getElementById('price-range').value) || 50000;
    const maxRisk = parseFloat(document.getElementById('risk-score').value) || 10;

    // Filter array
    data = data.filter(s => {
      // Sliders
      if ((s.ebitda || 0) < minEbitda) return false;
      if ((s.ebitdaMargin || 0) < minEbitdaMgn) return false;
      if ((s.annualRevenueGrowth || 0) < minRevGrowth) return false;
      if ((s.evEbitda || 0) > maxEv) return false;
      if ((s.price || 0) > maxPrice) return false;
      if ((s.financialRiskScore || 0) > maxRisk) return false;
      return true;
    });

    renderScreenerTable(data);
  }
'''
content = content.replace('function applySort() {', filter_logic + '\n  function applySort() {')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Screener updated with filter logic.')
