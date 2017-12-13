DROP VIEW IF EXISTS vw_userstories_daily CASCADE;
CREATE VIEW vw_userstories_daily AS 
SELECT  T1.date                  ,
        T2.sprint_id             ,
        T2.sprint_title          ,
        T1.userstory_id          ,
        T1.userstory_title       ,
        T1.status                ,
        T1.tasks_total           ,
        T1.total_tasks_unplanned ,
        T1.total_tasks_progress  ,
        T1.tasks_completed       ,
        T1.task_comp_ratio       ,
        T1.estimate_total        ,
        T1.logged_total          ,
        T1.remaining_total      
FROM userstories_daily  AS T1
JOIN vw_userstories     AS T2 ON T2.userstory_id = T1.userstory_id
ORDER BY 1 ASC;