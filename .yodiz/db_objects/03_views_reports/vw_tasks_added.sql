DROP VIEW IF EXISTS vw_tasks_added CASCADE;
CREATE VIEW vw_tasks_added AS
SELECT  T1.task_id,
        T1.created_on   AS task_created_on,
        T3.sprint_id,
        T3.sprint_title,
        T3.start_date   AS sprint_start_date
FROM vw_tasks       AS T1
JOIN vw_userstories AS T2 ON T2.userstory_id = T1.userstory_id
JOIN vw_sprints     AS T3 ON T3.sprint_id = T2.sprint_id
WHERE T1.created_on>T3.start_date;