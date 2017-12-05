DROP VIEW IF EXISTS vw_api_log;
CREATE VIEW vw_api_log AS
SELECT * 
FROM api_log 
ORDER BY time_stamp DESC 
LIMIT 10;