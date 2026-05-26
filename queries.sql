use aqi_db;

DROP TABLE IF EXISTS aqi_data;

CREATE TABLE aqi_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    city VARCHAR(100),
    aqi INT,
    dominant_pollutant VARCHAR(20),
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

select * from aqi_data;