INSERT INTO userstories_daily (
                                    userstory_id         ,
                                    date,
                                    userstory_title      ,
                                    status               ,
                                    tasks_total          ,
                                    total_tasks_unplanned,
                                    total_tasks_progress ,
                                    tasks_completed      ,
                                    task_comp_ratio      ,
                                    estimate_total       ,
                                    logged_total         ,
                                    remaining_total       
                                )
SELECT      T1.userstory_id         ,
            current_date,
            T1.userstory_title      ,
            T1.status               ,
            T1.tasks_total          ,
            T1.total_tasks_unplanned,
            T1.total_tasks_progress ,
            T1.tasks_completed      ,
            T1.task_comp_ratio      ,
            T1.estimate_total       ,
            T1.logged_total         ,
            T1.remaining_total       
FROM vw_sprint_userstories  AS T1
JOIN vw_sprints             AS T2 ON T2.sprint_id = T1.sprint_id
WHERE T2.is_active;