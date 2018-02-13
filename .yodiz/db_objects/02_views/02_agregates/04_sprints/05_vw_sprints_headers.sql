DROP VIEW IF EXISTS vw_sprints_headers CASCADE;
CREATE VIEW vw_sprints_headers AS
SELECT  T1.sprint_id,
        T1.sprint_title,
        T2.full_name                            AS responsible,
        T2.email                                AS responsible_email,
        T1.start_date,
        T1.end_date,
        T1.end_date - T1.start_date +1          AS total_days,
        current_date - T1.start_date + 1        AS day_number, 
        T1.end_date - current_date              AS remaining_days
FROM vw_sprints AS T1
JOIN vw_users   AS T2 ON T2.user_id = T1.created_by_id
WHERE T1.is_active;