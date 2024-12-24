CREATE TABLE Country (
    CountryId SERIAL PRIMARY KEY,                 -- Auto-incrementing primary key
    Country_Name VARCHAR(255) UNIQUE NOT NULL,          -- Country name
    Alpha2_code CHAR(2) UNIQUE,                -- ISO Alpha-2 code
    Alpha3_code CHAR(3) UNIQUE,                -- ISO Alpha-3 code
    Continent VARCHAR(100),             -- Continent
    Region VARCHAR(255),                -- Region
    Capital VARCHAR(255),               -- Capital city
    Population BIGINT,                  -- Population
    Currency_code CHAR(3),              -- ISO Currency code
    Currency_Name VARCHAR(255),         -- Full name of the currency
    Time_Zones TEXT[],                    -- List of time zones
	Latitude DECIMAL(9,6) NOT NULL,
	Longitude DECIMAL(9,6) NOT NULL
);

SELECT COUNT(*) FROM Country limit 5;