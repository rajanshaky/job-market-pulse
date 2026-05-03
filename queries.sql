create database job_market;
use job_market;
select * from job_listings;

update job_listings
set city = 'Not Specified'
where city = 'India';

SELECT 
    CASE 
        WHEN city = 'India' OR city = '' OR city IS NULL 
        THEN 'Not Specified'
        ELSE city
    END AS city
FROM job_listings;

set SQL_SAFE_UPDATES = 0;

select distinct(city) from job_listings ;