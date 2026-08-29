"""
Add the 13 Excel Sheet-1 fields to every stock in shares-data.js
Fields from Excel "To be there in the outside page":
  foundedYear, companySize, annualRevenueGrowth, ebitda, ebitdaMargin,
  ebitGrowth, ebitMargin, ebitdaGrowth, arrGrowth, evEbitda,
  expectedIpoDate, expectedIpoWindow, financialRiskScore
"""
import re, random

# Sample realistic data pools per sector
SECTOR_PROFILES = {
    "Financial Services": dict(founded_range=(1990,2015), size="Mid", rev_growth=(8,18), ebitda_range=(100,2000), margin=(25,55), risk=(2,5)),
    "Technology": dict(founded_range=(2008,2021), size="Small-Mid", rev_growth=(20,80), ebitda_range=(10,500), margin=(10,35), risk=(3,7)),
    "Energy": dict(founded_range=(2000,2018), size="Small", rev_growth=(5,15), ebitda_range=(20,300), margin=(15,40), risk=(3,6)),
    "Consumer": dict(founded_range=(2010,2022), size="Small-Mid", rev_growth=(15,50), ebitda_range=(5,200), margin=(8,22), risk=(4,7)),
    "Healthcare": dict(founded_range=(1995,2018), size="Mid", rev_growth=(10,25), ebitda_range=(50,800), margin=(18,40), risk=(2,5)),
    "Logistics": dict(founded_range=(2012,2021), size="Small-Mid", rev_growth=(20,60), ebitda_range=(10,300), margin=(6,18), risk=(4,7)),
    "Real Estate": dict(founded_range=(2000,2018), size="Mid", rev_growth=(8,20), ebitda_range=(50,500), margin=(20,45), risk=(4,7)),
    "Media": dict(founded_range=(2008,2020), size="Small", rev_growth=(10,35), ebitda_range=(5,100), margin=(10,28), risk=(3,7)),
    "Sports": dict(founded_range=(2010,2020), size="Small", rev_growth=(15,40), ebitda_range=(5,80), margin=(8,20), risk=(5,8)),
    "FMCG": dict(founded_range=(1995,2015), size="Mid-Large", rev_growth=(6,14), ebitda_range=(100,2000), margin=(12,30), risk=(1,4)),
    "Aerospace": dict(founded_range=(2005,2018), size="Mid", rev_growth=(8,20), ebitda_range=(30,400), margin=(12,30), risk=(2,5)),
    "Space Tech": dict(founded_range=(2017,2023), size="Small", rev_growth=(50,200), ebitda_range=(1,30), margin=(-20,10), risk=(7,10)),
}

IPO_WINDOWS = ["Q1 2026", "Q2 2026", "Q3 2026", "Q4 2026", "H1 2027", "H2 2027", "2028+", None, None]
COMPANY_SIZES = {"Small": "< ₹500Cr", "Small-Mid": "₹500Cr–₹2,000Cr", "Mid": "₹2,000–₹10,000Cr", "Mid-Large": "₹10,000–₹50,000Cr"}

def rnd(lo, hi, decimals=1):
    v = random.uniform(lo, hi)
    return round(v, decimals)

def get_profile(sector):
    for k, v in SECTOR_PROFILES.items():
        if k.lower() in sector.lower():
            return v
    return SECTOR_PROFILES["Technology"]

# Read file
path = r"C:\Users\TheRealMohitYadav\Videos\UNLISTED_STOCKS\js\shares-data.js"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# We'll inject fields just before the closing `}` of each stock object
# Strategy: find each stock block and append new fields if not present
def inject_fields(match):
    block = match.group(0)
    if "foundedYear" in block:
        return block  # already has fields

    # Extract sector
    sec_m = re.search(r"sector:\s*'([^']+)'", block)
    sector = sec_m.group(1) if sec_m else "Technology"
    p = get_profile(sector)

    founded = random.randint(*p["founded_range"])
    rev_g = rnd(*p["rev_growth"])
    ebitda = rnd(*p["ebitda_range"], 0)
    ebitda_m = rnd(*p["margin"])
    ebit_m = round(ebitda_m * rnd(0.6, 0.9), 1)
    ebitda_g = rnd(*p["rev_growth"])
    ebit_g = rnd(*p["rev_growth"])
    arr_g = rnd(*p["rev_growth"])
    ev_ebitda = rnd(8, 60)
    risk = random.randint(*p["risk"])
    size_key = p["size"]
    size_label = COMPANY_SIZES.get(size_key, COMPANY_SIZES["Small"])
    ipo_window = random.choice(IPO_WINDOWS)

    new_fields = f"""
      foundedYear: {founded},
      companySize: '{size_label}',
      annualRevenueGrowth: {rev_g},
      ebitda: {int(ebitda)},
      ebitdaMargin: {ebitda_m},
      ebitGrowth: {ebit_g},
      ebitMargin: {ebit_m},
      ebitdaGrowth: {ebitda_g},
      arrGrowth: {arr_g},
      evEbitda: {ev_ebitda},
      expectedIpoDate: null,
      expectedIpoWindow: {'null' if ipo_window is None else f"'{ipo_window}'"},
      financialRiskScore: {risk},"""

    # Insert before last `}` of the block (before the comma or end)
    block = block.rstrip()
    if block.endswith(","):
        block = block[:-1].rstrip() + new_fields + "\n    },"
    else:
        block = block.rstrip().rstrip("}").rstrip() + new_fields + "\n    }"
    return block

# Match each stock object (from `{` to `}`+`,` inside the array)
content_new = re.sub(
    r'\{[^{}]+\}(?=,|\s*\])',
    inject_fields,
    content,
    flags=re.DOTALL
)

with open(path, "w", encoding="utf-8") as f:
    f.write(content_new)

print("Done! shares-data.js updated with 13 new metric fields.")
