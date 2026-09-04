"""
╔══════════════════════════════════════════════════════════════════╗
║   MDB ARTHASPHERE — Excel → Supabase Uploader                   ║
║   Upload / Update all unlisted stock prices from Excel           ║
║   Run: python upload_excel.py                                    ║
║   Run dry-run: python upload_excel.py --dry-run                 ║
╚══════════════════════════════════════════════════════════════════╝
"""

import sys
import os
import math
import argparse
from datetime import datetime

# ── Dependency check ───────────────────────────────────────────────
def check_deps():
    missing = []
    for pkg, imp in [('pandas', 'pandas'), ('openpyxl', 'openpyxl'),
                     ('psycopg2', 'psycopg2'), ('tabulate', 'tabulate')]:
        try:
            __import__(imp)
        except ImportError:
            missing.append(pkg)
    if missing:
        print(f"\n[!] Missing packages: {', '.join(missing)}")
        print(f"    Run: pip install {' '.join(missing)}\n")
        sys.exit(1)

check_deps()

import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
from tabulate import tabulate

# ── Config ─────────────────────────────────────────────────────────
DATABASE_URL = (
    "postgresql://postgres.zgctcrizcunvnioxjkyb:ELkb2B4-FGpS6Z3"
    "@aws-0-ap-southeast-2.pooler.supabase.com:5432/postgres"
)
EXCEL_FILE   = "Details of stocks.xlsx"
SHEET_NAME   = "All unlisted shares"
BATCH_SIZE   = 100   # rows per DB insert batch

# ── Colors for terminal output ──────────────────────────────────────
GREEN  = "\033[92m"
YELLOW = "\033[93m"
RED    = "\033[91m"
CYAN   = "\033[96m"
BOLD   = "\033[1m"
DIM    = "\033[2m"
RESET  = "\033[0m"

def ok(msg):   print(f"  {GREEN}✔{RESET}  {msg}")
def warn(msg): print(f"  {YELLOW}⚠{RESET}  {msg}")
def err(msg):  print(f"  {RED}✘{RESET}  {msg}")
def info(msg): print(f"  {CYAN}→{RESET}  {msg}")
def section(title):
    print(f"\n{BOLD}{CYAN}{'─'*54}{RESET}")
    print(f"{BOLD}{CYAN}  {title}{RESET}")
    print(f"{BOLD}{CYAN}{'─'*54}{RESET}")

def safe_float(val, default=None):
    try:
        f = float(val)
        return default if math.isnan(f) else round(f, 4)
    except (TypeError, ValueError):
        return default

def progress_bar(done, total, width=40):
    pct  = done / total if total else 0
    fill = int(pct * width)
    bar  = '█' * fill + '░' * (width - fill)
    return f"[{bar}] {done}/{total} ({pct*100:.1f}%)"

# ── Step 1: Read & validate Excel ──────────────────────────────────
def read_excel():
    section("STEP 1 — Reading Excel File")
    if not os.path.exists(EXCEL_FILE):
        err(f"Excel file not found: {EXCEL_FILE}")
        err("Make sure 'Details of stocks.xlsx' is in the same folder as this script.")
        sys.exit(1)

    info(f"Reading: {EXCEL_FILE} → Sheet: '{SHEET_NAME}'")
    df = pd.read_excel(EXCEL_FILE, sheet_name=SHEET_NAME)
    df.columns = [str(c).strip() for c in df.columns]
    ok(f"Loaded {len(df)} rows, {len(df.columns)} columns")

    # Show available columns
    info(f"Columns found: {', '.join(df.columns.tolist())}")

    # Drop empty symbol rows
    before = len(df)
    df = df.dropna(subset=['Symbol'])
    df = df[df['Symbol'].astype(str).str.strip().str.len() > 0]
    dropped = before - len(df)
    if dropped:
        warn(f"Dropped {dropped} rows with missing Symbol")
    ok(f"{len(df)} valid stock rows ready for upload")

    return df

# ── Step 2: Parse rows into records ────────────────────────────────
def parse_records(df):
    section("STEP 2 — Parsing & Validating Data")
    records = []
    skipped = []
    errors  = []

    for idx, row in df.iterrows():
        sym  = str(row['Symbol']).strip()
        name = str(row.get('Company Name', row.get('Name', sym))).strip()
        if name == 'nan': name = sym

        price = safe_float(row.get('Price') or row.get('LTP') or row.get('Last Price'))
        if price is None or price <= 0:
            skipped.append({'symbol': sym, 'reason': 'No valid price'})
            continue

        prev  = safe_float(row.get('Previous Close') or row.get('Prev Close'), price)
        chg   = safe_float(row.get('Chg') or row.get('Change'), round(price - prev, 2))
        chgp  = safe_float(row.get('Chg%') or row.get('Change%'),
                           round((chg / prev * 100) if prev else 0, 2))
        high  = safe_float(row.get('52W High') or row.get('High'))
        low   = safe_float(row.get('52W Low')  or row.get('Low'))
        vol   = safe_float(row.get('Volume'))
        mcap  = safe_float(row.get('Market Cap') or row.get('Mkt Cap'))

        records.append({
            'symbol':         sym,
            'company_name':   name[:255],
            'price':          price,
            'prev_close':     prev,
            'change':         chg,
            'change_percent': chgp,
            'week_52_high':   high,
            'week_52_low':    low,
            'volume':         int(vol) if vol is not None else None,
            'market_cap':     mcap,
            'exchange':       'UNLISTED',
            'is_active':      True,
            'updated_at':     datetime.utcnow(),
        })

    ok(f"Parsed:  {len(records)} valid records")
    if skipped:
        warn(f"Skipped: {len(skipped)} rows (no price data)")
        for s in skipped[:5]:
            print(f"     {DIM}{s['symbol']}: {s['reason']}{RESET}")
        if len(skipped) > 5:
            print(f"     {DIM}... and {len(skipped)-5} more{RESET}")

    return records

# ── Step 3: Preview (dry-run) ───────────────────────────────────────
def preview(records):
    section("PREVIEW — First 10 Records (Dry Run)")
    sample = records[:10]
    rows = [[r['symbol'][:20], f"₹{r['price']:,.2f}",
             f"{r['change_percent']:+.2f}%" if r['change_percent'] is not None else '-',
             r['exchange']] for r in sample]
    print(tabulate(rows, headers=['Symbol', 'Price', 'Change%', 'Exchange'],
                   tablefmt='rounded_outline'))
    print(f"\n  {DIM}... and {len(records)-10} more records{RESET}")
    print(f"\n  {YELLOW}Dry run complete. No data was written to the database.{RESET}")
    print(f"  Remove --dry-run flag to actually upload.\n")

# ── Step 4: Upload to Supabase ──────────────────────────────────────
def upload_to_supabase(records, dry_run=False):
    section("STEP 3 — Connecting to Supabase")
    info("Host: aws-0-ap-southeast-2.pooler.supabase.com:5432")
    info("Database: postgres (Supabase project zgctcrizcunvnioxjkyb)")

    try:
        conn = psycopg2.connect(DATABASE_URL, connect_timeout=15)
        conn.autocommit = False
        cur  = conn.cursor()
        ok("Connected to Supabase Postgres")
    except Exception as e:
        err(f"Connection failed: {e}")
        err("Check your internet connection or Supabase credentials.")
        sys.exit(1)

    section("STEP 4 — Uploading to Supabase")

    updated  = 0
    inserted = 0
    failed   = 0
    batches  = [records[i:i+BATCH_SIZE] for i in range(0, len(records), BATCH_SIZE)]

    for b_idx, batch in enumerate(batches):
        print(f"\r  {progress_bar(b_idx * BATCH_SIZE, len(records))}  ", end='', flush=True)

        for rec in batch:
            try:
                # Check if company already exists
                cur.execute("SELECT id FROM companies WHERE symbol = %s LIMIT 1",
                            (rec['symbol'],))
                row = cur.fetchone()

                if row:
                    # Update existing company
                    cur.execute("""
                        UPDATE companies
                           SET company_name = %s,
                               is_active    = %s,
                               updated_at   = %s
                         WHERE symbol = %s
                    """, (rec['company_name'], rec['is_active'],
                          rec['updated_at'], rec['symbol']))
                    company_id = row[0]
                    updated += 1
                else:
                    # Insert new company
                    cur.execute("""
                        INSERT INTO companies
                               (symbol, company_name, exchange, is_active, updated_at)
                        VALUES (%s, %s, %s, %s, %s)
                        RETURNING id
                    """, (rec['symbol'], rec['company_name'],
                          rec['exchange'], rec['is_active'], rec['updated_at']))
                    company_id = cur.fetchone()[0]
                    inserted += 1

                # Upsert stock price
                cur.execute("""
                    INSERT INTO stock_prices
                           (company_id, price, prev_close, change, change_percent,
                            week_52_high, week_52_low, volume, market_cap, updated_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (company_id) DO UPDATE SET
                        price          = EXCLUDED.price,
                        prev_close     = EXCLUDED.prev_close,
                        change         = EXCLUDED.change,
                        change_percent = EXCLUDED.change_percent,
                        week_52_high   = EXCLUDED.week_52_high,
                        week_52_low    = EXCLUDED.week_52_low,
                        volume         = EXCLUDED.volume,
                        market_cap     = EXCLUDED.market_cap,
                        updated_at     = EXCLUDED.updated_at
                """, (company_id, rec['price'], rec['prev_close'],
                      rec['change'], rec['change_percent'],
                      rec['week_52_high'], rec['week_52_low'],
                      rec['volume'], rec['market_cap'], rec['updated_at']))

            except Exception as e:
                failed += 1
                errors_log = str(e)[:80]

        conn.commit()

    print(f"\r  {progress_bar(len(records), len(records))}  ")
    cur.close()
    conn.close()
    return inserted, updated, failed

# ── Step 5: Summary Report ──────────────────────────────────────────
def print_summary(records, inserted, updated, failed, start_time):
    section("UPLOAD COMPLETE — Summary Report")
    elapsed = (datetime.utcnow() - start_time).total_seconds()

    rows = [
        ["Total rows in Excel",       len(records)],
        ["New companies inserted",    f"{GREEN}{inserted}{RESET}"],
        ["Existing prices updated",   f"{GREEN}{updated}{RESET}"],
        ["Failed / errors",           f"{RED}{failed}{RESET}" if failed else f"{GREEN}0{RESET}"],
        ["Time taken",                f"{elapsed:.1f}s"],
        ["Upload timestamp (UTC)",    datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')],
    ]
    print(tabulate(rows, headers=['Metric', 'Value'], tablefmt='rounded_outline'))

    if failed == 0:
        print(f"\n  {GREEN}{BOLD}✔ All prices updated successfully in Supabase!{RESET}")
    else:
        print(f"\n  {YELLOW}⚠ Completed with {failed} error(s). Check above output.{RESET}")

    print(f"\n  {DIM}View your data: https://supabase.com/dashboard/project/zgctcrizcunvnioxjkyb/editor{RESET}")
    print(f"  {DIM}Screener will now show updated prices: http://localhost:8080/screener.html{RESET}\n")

# ── Main ────────────────────────────────────────────────────────────
def main():
    global EXCEL_FILE, SHEET_NAME
    
    parser = argparse.ArgumentParser(
        description='Upload unlisted stock prices from Excel to Supabase')
    parser.add_argument('--dry-run', action='store_true',
                        help='Preview what would be uploaded without writing to DB')
    parser.add_argument('--file', default=EXCEL_FILE,
                        help=f'Excel file path (default: {EXCEL_FILE})')
    parser.add_argument('--sheet', default=SHEET_NAME,
                        help=f'Sheet name (default: {SHEET_NAME})')
    args = parser.parse_args()

    EXCEL_FILE  = args.file
    SHEET_NAME  = args.sheet

    print(f"\n{BOLD}{CYAN}╔══════════════════════════════════════════════════╗{RESET}")
    print(f"{BOLD}{CYAN}║    MDB ARTHASPHERE — Excel → Supabase Uploader   ║{RESET}")
    print(f"{BOLD}{CYAN}║    {datetime.now().strftime('%d %b %Y  %I:%M %p'):<44}║{RESET}")
    print(f"{BOLD}{CYAN}╚══════════════════════════════════════════════════╝{RESET}")

    start_time = datetime.utcnow()

    df      = read_excel()
    records = parse_records(df)

    if not records:
        err("No valid records found. Nothing to upload.")
        sys.exit(1)

    if args.dry_run:
        preview(records)
        sys.exit(0)

    # Confirm before uploading
    print(f"\n  {YELLOW}About to upload {len(records)} stock records to Supabase.{RESET}")
    ans = input(f"  {BOLD}Proceed? [Y/n]: {RESET}").strip().lower()
    if ans not in ('', 'y', 'yes'):
        print("  Cancelled.\n")
        sys.exit(0)

    inserted, updated, failed = upload_to_supabase(records)
    print_summary(records, inserted, updated, failed, start_time)

if __name__ == '__main__':
    main()
