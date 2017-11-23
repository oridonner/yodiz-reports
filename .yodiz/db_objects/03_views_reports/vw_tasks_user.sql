DROP VIEW IF EXISTS vw_tasks_user CASCADE;
CREATE VIEW vw_tasks_user AS
select 
        aa.* ,  
        case when aa.estimated_remaining_capacity < aa."#effort_remaining" then 'RISK' else 'OK' end as "capacity_allocation"
from (
        SELECT  T4.sprint_title,
                T2.full_name,
                COUNT(T1.task_id)       AS "#tasks",
                SUM(T1.effort_estimate) AS "#effort_estimate",
                SUM(T1.effort_logged)   AS "#effort_logged",
                SUM(T1.effort_remaining)   AS "#effort_remaining",
                ((T5.total_days - T5.day_number) * (8.5 * T2.focus_factor)) as "estimated_remaining_capacity"
        FROM vw_tasks              AS T1
        Left JOIN vw_users              AS T2 ON T2.user_id = T1.task_owner_id
        JOIN vw_userstories        AS T3 ON T3.userstory_id = T1.userstory_id
        JOIN vw_sprints            AS T4 ON T4.sprint_id = T3.sprint_id
        JOIN vw_sprints_headers    AS T5 ON T5.sprint_id = T4.sprint_id
        GROUP BY 1,2,7        
) aa
ORDER BY 8 Desc, 1,4 DESC ;
