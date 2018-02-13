DROP VIEW IF EXISTS vw_tasks_headers CASCADE;
CREATE VIEW vw_tasks_headers AS
        SELECT  T2.release_id,
                T3.sprint_id,
                T3.sprint_title,
                T3.is_active AS sprint_is_active,
                T2.userstory_id,
                T1.task_id,
                T1.task_title,
                T1.created_on   AS task_created_on,
                T3.start_date   AS sprint_start_date
        FROM vw_tasks       AS T1
        JOIN vw_userstories AS T2 ON T2.userstory_id = T1.userstory_id
        JOIN vw_sprints     AS T3 ON T3.sprint_id = T2.sprint_id;