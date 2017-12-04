INSERT INTO vw_userstories_daily (
                                    userstory_id         ,
                                    userstory_title      ,
                                    status               ,
                                    tasks_total          ,
                                    total_tasks_unplanned,
                                    total_tasks_progress ,
                                    tasks_completed      ,
                                    task_comp_ratio      ,
                                    estimate_total       ,
                                    logged_total         ,
                                    remainig_total       
                                )
SELECT      userstory_id         ,
            userstory_title      ,
            status               ,
            tasks_total          ,
            total_tasks_unplanned,
            total_tasks_progress ,
            tasks_completed      ,
            task_comp_ratio      ,
            estimate_total       ,
            logged_total         ,
            remainig_total       
FROM vw_sprint_userstories;
