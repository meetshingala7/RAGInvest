CREATE TABLE Country (
    CountryId UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    Country_Name VARCHAR(255) UNIQUE NOT NULL,
    Alpha2_code CHAR(2),
    Alpha3_code CHAR(3),
    Continent VARCHAR(100),
    Region VARCHAR(255),
    Capital VARCHAR(255),
    Population BIGINT,
    Currency_code CHAR(3),
    Currency_Name VARCHAR(255),
    Time_Zones TEXT[],
	Latitude DECIMAL(9,6) NOT NULL,
	Longitude DECIMAL(9,6) NOT NULL
);

CREATE TABLE CountryLogs (
    Id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    CountryName VARCHAR NOT NULL,
    StatusCode VARCHAR,
    Cca2Code VARCHAR(2),
	error_message VARCHAR
);