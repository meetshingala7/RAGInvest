CREATE TABLE stock_information (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    full_name VARCHAR,
    stock_symbol VARCHAR,
    upstox_url VARCHAR,
    google_finance_url VARCHAR,
    company_summary VARCHAR,
    company_sector VARCHAR,
    shareholding_pattern JSON,
    market_cap VARCHAR,
    primary_exchange VARCHAR,
    dividend_yield VARCHAR,
    pe_ratio VARCHAR,
    avg_volume VARCHAR,
    year_range VARCHAR,
    day_range VARCHAR,
    previous_close VARCHAR,
    founded VARCHAR,
    headquarters VARCHAR,
    website VARCHAR,
    website_url VARCHAR,
    employees INTEGER,
    ceo VARCHAR,
    ceo_url VARCHAR,
    is_full_name BOOLEAN,
    is_current BOOLEAN,
    version_no INT
);

