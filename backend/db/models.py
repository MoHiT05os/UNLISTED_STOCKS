"""
SQLAlchemy database models for the stock data pipeline.
Tables: companies, stock_prices, ipos, ipo_gmp_history
"""
from datetime import datetime, date
from sqlalchemy import (
    Column, Integer, String, Float, Boolean, Date, DateTime,
    ForeignKey, Text, UniqueConstraint, Index, create_engine
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Company(Base):
    """Master list of all NSE/BSE listed companies."""
    __tablename__ = 'companies'

    id = Column(Integer, primary_key=True, autoincrement=True)
    symbol = Column(String(50), nullable=False)
    company_name = Column(String(255), nullable=False)
    isin = Column(String(12), nullable=True)
    sector = Column(String(100), nullable=True)
    industry = Column(String(100), nullable=True)
    exchange = Column(String(10), nullable=False)  # NSE, BSE, or BOTH
    series = Column(String(10), nullable=True)  # EQ, BE, SM, etc.
    listing_date = Column(Date, nullable=True)
    face_value = Column(Float, nullable=True)
    paid_up_value = Column(Float, nullable=True)

    # Dhan API mapping
    dhan_nse_security_id = Column(String(20), nullable=True)
    dhan_bse_security_id = Column(String(20), nullable=True)

    # Metadata
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    stock_price = relationship('StockPrice', back_populates='company', uselist=False)

    __table_args__ = (
        Index('idx_symbol', 'symbol'),
        Index('idx_isin', 'isin'),
        Index('idx_exchange', 'exchange'),
        Index('idx_company_name', 'company_name'),
    )

    def __repr__(self):
        return f'<Company {self.symbol} ({self.exchange})>'


class StockPrice(Base):
    """Latest stock price data (updated hourly)."""
    __tablename__ = 'stock_prices'

    id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(Integer, ForeignKey('companies.id'), unique=True, nullable=False)
    price = Column(Float, nullable=True)  # Last Traded Price
    open = Column(Float, nullable=True)
    high = Column(Float, nullable=True)
    low = Column(Float, nullable=True)
    prev_close = Column(Float, nullable=True)
    change = Column(Float, nullable=True)  # price - prev_close
    change_percent = Column(Float, nullable=True)
    volume = Column(Integer, nullable=True)
    market_cap = Column(Float, nullable=True)
    week_52_high = Column(Float, nullable=True)
    week_52_low = Column(Float, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    company = relationship('Company', back_populates='stock_price')

    __table_args__ = (
        Index('idx_price_company', 'company_id'),
        Index('idx_change_percent', 'change_percent'),
    )

    def __repr__(self):
        return f'<StockPrice company_id={self.company_id} price={self.price}>'


class IPO(Base):
    """IPO details — upcoming, current, and listed."""
    __tablename__ = 'ipos'

    id = Column(Integer, primary_key=True, autoincrement=True)
    company_name = Column(String(255), nullable=False)
    exchange = Column(String(10), nullable=True)
    ipo_type = Column(String(20), nullable=True)  # Mainboard, SME
    issue_price_lower = Column(Float, nullable=True)
    issue_price_upper = Column(Float, nullable=True)
    issue_size = Column(Float, nullable=True)  # in Crores
    lot_size = Column(Integer, nullable=True)
    open_date = Column(Date, nullable=True)
    close_date = Column(Date, nullable=True)
    listing_date = Column(Date, nullable=True)
    listing_price = Column(Float, nullable=True)
    listing_gain_percent = Column(Float, nullable=True)

    # GMP & Grey Market
    gmp = Column(Float, nullable=True)
    estimated_listing_price = Column(Float, nullable=True)
    kostak = Column(Float, nullable=True)
    subject_to_sauda = Column(Float, nullable=True)

    # Subscription
    subscription_retail = Column(Float, nullable=True)
    subscription_hni = Column(Float, nullable=True)
    subscription_qib = Column(Float, nullable=True)
    subscription_total = Column(Float, nullable=True)

    # Status
    status = Column(String(20), default='upcoming')  # upcoming, open, closed, listed

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    gmp_history = relationship('IPOGMPHistory', back_populates='ipo')

    def __repr__(self):
        return f'<IPO {self.company_name}>'


class IPOGMPHistory(Base):
    """Historical GMP records for charting."""
    __tablename__ = 'ipo_gmp_history'

    id = Column(Integer, primary_key=True, autoincrement=True)
    ipo_id = Column(Integer, ForeignKey('ipos.id'), nullable=False)
    date = Column(Date, nullable=False)
    gmp = Column(Float, nullable=True)
    kostak = Column(Float, nullable=True)
    subject_to_sauda = Column(Float, nullable=True)

    # Relationships
    ipo = relationship('IPO', back_populates='gmp_history')

    __table_args__ = (
        UniqueConstraint('ipo_id', 'date', name='uq_ipo_date'),
        Index('idx_gmp_ipo', 'ipo_id'),
    )

    def __repr__(self):
        return f'<IPOGMPHistory ipo_id={self.ipo_id} date={self.date} gmp={self.gmp}>'


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String(255), nullable=False)
    phone = Column(String(20), unique=True, nullable=False)
    pan_number = Column(String(20), unique=True, nullable=False)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<User {self.full_name} ({self.phone})>'
