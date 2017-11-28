DROP VIEW IF EXISTS vw_capacity CASCADE;
CREATE VIEW vw_capacity AS
        SELECT  T4.sprint_title,
                T2.full_name,
                COUNT(T1.task_id)                               AS tot_assigned_tasks,
                SUM(T1.effort_estimate)                         AS sum_effort_estimate,
                SUM(T1.effort_logged)                           AS sum_effort_logged,
                SUM(T1.effort_remaining)                        AS sum_effort_remaining,
                T5.remaining_days                               AS days_remaining,
                T5.remaining_days * 8.5 * T2.focus_factor       AS estimated_remaining_capacity
        FROM vw_tasks           AS T1
        LEFT JOIN vw_users      AS T2 ON T2.user_id = T1.task_owner_id
        JOIN vw_userstories     AS T3 ON T3.userstory_id = T1.userstory_id
        JOIN vw_sprints         AS T4 ON T4.sprint_id = T3.sprint_id
        JOIN vw_sprints_headers AS T5 ON T5.sprint_id = T4.sprint_id
        GROUP BY 1,2,7,8;     

