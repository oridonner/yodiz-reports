DROP VIEW IF EXISTS vw_sprints_headers CASCADE;
CREATE VIEW vw_sprints_headers AS
SELECT  sprint_id,
        sprint_title,
        start_date,
        end_date,
        end_date - start_date +1 AS total_days,
        current_date - start_date + 1 AS day_number 
FROM vw_sprints 
WHERE is_active;