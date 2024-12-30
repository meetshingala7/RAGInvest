CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE users (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    email_id VARCHAR(255),
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    first_name VARCHAR(255) NOT NULL,
    middle_name VARCHAR(255),
    last_name VARCHAR(255) NOT NULL,
    country_id UUID,
    valid_from TIMESTAMP DEFAULT NOW(),
    is_valid BOOLEAN DEFAULT TRUE,
    valid_to TIMESTAMP DEFAULT '9999-12-31 23:59:59'
    FOREIGN KEY (country_id) REFERENCES Country(CountryId)
);

CREATE OR REPLACE FUNCTION update_valid_to() 
RETURNS TRIGGER AS $$
BEGIN
    UPDATE users
    SET is_valid = FALSE,
	    valid_to = NOW()
    WHERE username = NEW.username AND is_valid = TRUE;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER handle_validity
BEFORE INSERT ON users
FOR EACH ROW
EXECUTE FUNCTION update_valid_to();

INSERT INTO users(email_id, username, password, first_name, middle_name, last_name)
VALUES ('meetshingala2024@gmail.com', 'meet.shingala', 'meet1234', 'Meet', 'Chetankumar', 'Shingala');

SELECT * FROM users limit 5;