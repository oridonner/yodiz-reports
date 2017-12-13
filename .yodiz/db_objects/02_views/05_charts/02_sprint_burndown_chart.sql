DROP VIEW IF EXISTS vw_sprint_burndown_chart CASCADE;
CREATE VIEW vw_sprint_burndown_chart AS
WITH remaining_1 AS
(
SELECT  sprint_id,
        sprint_date,
        is_work_day,
        sprint_day,
        remaining_days,
        CASE 
                WHEN remaining_effort IS NULL THEN lead(remaining_effort) OVER (ORDER BY sprint_id,sprint_date) 
                ELSE remaining_effort
        END AS remaining_effort,
        trend_line
FROM vw_sprint_burndown
),  remaining_2 AS
(
SELECT  sprint_id,
        sprint_date,
        is_work_day,
        sprint_day,
        remaining_days,
        CASE 
                WHEN remaining_effort IS NULL THEN lead(remaining_effort) OVER (ORDER BY sprint_id,sprint_date) 
                ELSE remaining_effort
        END AS remaining_effort,
        trend_line
FROM remaining_1
)
SELECT  sprint_id,
        sprint_date,
        is_work_day,
        sprint_day,
        remaining_days,
        CASE 
                WHEN remaining_effort IS NULL THEN lead(remaining_effort) OVER (ORDER BY sprint_id,sprint_date) 
                ELSE remaining_effort
        END AS remaining_effort,
        trend_line
FROM remaining_2;