import sys
import os
import pandas as pd

# Insert backend directory to path
sys.path.append(os.path.abspath('backend'))

from db.database import init_db, SessionLocal
from db.models import User, Company, StockPrice

def main():
    print("1. Initializing Supabase Tables...")
    try:
        init_db()
        print("Tables initialized on Supabase Postgres successfully!")
    except Exception as e:
        print(f"Error initializing tables on Supabase: {e}")
        return

    db = SessionLocal()
    try:
        # Create Demo User if not exists
        print("\n2. Checking Demo Account...")
        demo_phone = '9999999999'
        existing_user = db.query(User).filter(User.phone == demo_phone).first()
        if not existing_user:
            demo = User(
                full_name='Demo Investor',
                phone=demo_phone,
                pan_number='ABCDE1234F',
                is_verified=True
            )
            db.add(demo)
            db.commit()
            print("Demo account created on Supabase!")
        else:
            print("Demo account already exists on Supabase.")

        # Read Excel Data
        excel_path = 'Details of stocks.xlsx'
        if not os.path.exists(excel_path):
            print(f"Error: {excel_path} not found.")
            return

        print("\n3. Loading Shares from Excel...")
        df = pd.read_excel(excel_path, sheet_name='All unlisted shares')
        df.columns = [c.strip() for c in df.columns]
        
        print(f"Loaded {len(df)} rows. Processing...")
        
        # Clear existing companies to prevent duplicates on migration run
        db.query(StockPrice).delete()
        db.query(Company).delete()
        db.commit()

        companies_added = 0
        
        for index, row in df.iterrows():
            symbol = str(row.get('Symbol', '')).strip()
            price = row.get('Price', None)
            prev_close = row.get('Previous Close', None)
            
            if not symbol or symbol.lower() == 'nan' or price is None or str(price).lower() == 'nan':
                continue
                
            try:
                price = float(price)
                prev_close = float(prev_close) if prev_close is not None and str(prev_close).lower() != 'nan' else price
            except:
                continue

            # Create Company record
            comp = Company(
                symbol=symbol[:50],
                company_name=symbol[:255],
                exchange='UNLISTED',
                is_active=True
            )
            db.add(comp)
            db.flush() # Populate ID
            
            # Create Stock Price record
            chg = price - prev_close
            chg_pct = (chg / prev_close * 100) if prev_close != 0 else 0
            
            sp = StockPrice(
                company_id=comp.id,
                price=price,
                prev_close=prev_close,
                change=chg,
                change_percent=chg_pct,
                volume=0,
                market_cap=0
            )
            db.add(sp)
            companies_added += 1

        db.commit()
        print(f"Successfully migrated {companies_added} unlisted stocks from Excel to Supabase Postgres!")

    except Exception as e:
        db.rollback()
        print(f"Error during migration: {e}")
    finally:
        db.close()

if __name__ == '__main__':
    main()
