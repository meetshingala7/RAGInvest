UPDATE
	country
SET
	country_name = 'Myanmar'
WHERE
	country_name ILIKE 'Myanmar [%';

UPDATE
	country
SET
	country_name = 'Congo'
WHERE
	country_name ILIKE 'Congo [R%';
SELECT * FROM country WHERE country_name ILIKE 'Congo [%';
UPDATE
	country
SET
	country_name = 'Cocos (Keeling) Islands'
WHERE
	country_name ILIKE 'Cocos [%';

UPDATE
	country
SET
	country_name = 'Palestine'
WHERE
	country_name ILIKE 'Palestinian%';

UPDATE
	country
SET
	country_name = 'Falkland Islands'
WHERE
	country_name ILIKE 'Falkland Islands [%';


UPDATE
	country
SET
	country_name = 'MACEDONIA'
WHERE
	country_name ILIKE 'Macedonia%';

DELETE FROM 
    country 
WHERE 
    country_name IN ('Congo [DRC]', 'Gaza Strip', 'Netherlands Antilles', 'U.S. Virgin Islands');

SELECT COUNT(*) FROM country WHERE country_name IN ('Congo [DRC]', 'Gaza Strip', 'Netherlands Antilles', 'U.S. Virgin Islands');


