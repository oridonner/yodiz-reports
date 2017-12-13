DROP VIEW IF EXISTS vw_sprints_daily CASCADE;
CREATE VIEW vw_sprints_daily AS 
SELECT  T1.date                  ,
        T2.sprint_id             ,
        T2.sprint_title          ,
        SUM(T1.tasks_total)             AS tasks_total,
        SUM(T1.total_tasks_unplanned)   AS total_tasks_unplanned,
        SUM(T1.total_tasks_progress)    AS total_tasks_progress,
        SUM(T1.tasks_completed)         AS tasks_completed,
        SUM(T1.estimate_total)          AS estimate_total,
        SUM(T1.logged_total)            AS logged_total,
        SUM(T1.remaining_total)          AS remaining_total  
FROM userstories_daily  AS T1
JOIN vw_userstories     AS T2 ON T2.userstory_id = T1.userstory_id
GROUP BY 1,2,3
ORDER BY 2,1 ASC;