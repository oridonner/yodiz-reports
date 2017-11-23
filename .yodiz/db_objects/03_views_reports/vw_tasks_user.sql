DROP VIEW IF EXISTS vw_tasks_user CASCADE;
CREATE VIEW vw_tasks_user AS
SELECT  T4.sprint_title,
        T2.full_name,
        COUNT(T1.task_id)       AS "#tasks",
        SUM(T1.effort_estimate) AS "#effort_estimate",
        SUM(T1.effort_logged)   AS "#effort_logged",
        SUM(T1.effort_remaining)   AS "#effort_remaining"
FROM vw_tasks       AS T1
JOIN vw_users       AS T2 ON T2.user_id = T1.task_owner_id
JOIN vw_userstories AS T3 ON T3.userstory_id = T1.userstory_id
JOIN vw_sprints     AS T4 ON T4.sprint_id = T3.sprint_id
GROUP BY 1,2
ORDER BY 1,4 DESC;