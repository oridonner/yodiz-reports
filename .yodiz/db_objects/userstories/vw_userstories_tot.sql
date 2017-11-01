DROP VIEW IF EXISTS vw_userstories_tot CASCADE;
CREATE VIEW vw_userstories_tot AS
        WITH total AS 
        (
        SELECT  T1.sprint_id,
                T1.sprint_title,
                T1.userstory_title ,
                L1.total_tasks_usersoty + L2.total_issues_userstory                     AS tasks_total,
                COALESCE(L2.total_issues_done,0)  + COALESCE(L1.total_tasks_done,0)     AS tasks_completed,
                ROUND   (
                                (
                                        COALESCE(L2.total_issues_done,0)  
                                        + 
                                        COALESCE(L1.total_tasks_done,0)
                                )  
                                * 100 / 
                                (
                                        L1.total_tasks_usersoty 
                                        + 
                                        L2.total_issues_userstory
                                )
                        )                                                               AS task_comp_ratio,
                ROUND   (
                                COALESCE(L1.total_tasks_estimate,0) 
                                + 
                                COALESCE(L2.total_issues_estimate,0)
                                ,1
                        )                                                                AS estimate_total,        
                ROUND   (
                                COALESCE(L1.total_tasks_logged,0) 
                                + 
                                COALESCE(L2.total_issues_logged,0)
                                ,1
                        )                                                               AS logged_total,
                ROUND   (
                                COALESCE(L1.total_tasks_remaining,0)
                                + 
                                COALESCE(L2.total_issues_remaining,0)
                                ,1
                        )                                                               AS remainig_total
        FROM vw_userstories    T1
        -- tasks totals
        LEFT JOIN LATERAL (     
                                SELECT  COUNT(P1.task_id)::NUMERIC                      AS total_tasks_usersoty,
                                        SUM(P1.effort_estimate)::NUMERIC                AS total_tasks_estimate,
                                        SUM(P1.effort_remaining)::NUMERIC               AS total_tasks_remaining,
                                        SUM(P1.effort_logged)::NUMERIC                  AS total_tasks_logged,
                                        SUM(
                                                CASE    WHEN P1.status = 'done' THEN 1
                                                        ELSE 0
                                                END
                                )::NUMERIC                                              AS total_tasks_done
                                FROM vw_tasks AS P1     
                                WHERE P1.userstory_id   = T1.userstory_id
                        ) AS L1 ON TRUE
        -- isuues totals
        LEFT JOIN LATERAL (     
                                SELECT  COUNT(P1.issue_id)::NUMERIC                     AS total_issues_userstory,
                                        SUM(P1.effort_estimate)::NUMERIC                AS total_issues_estimate,
                                        SUM(P1.effort_remaining)::NUMERIC               AS total_issues_remaining,
                                        SUM(P1.effort_logged)::NUMERIC                  AS total_issues_logged,
                                        SUM(
                                                CASE    WHEN P1.is_open THEN 0
                                                        ELSE 1
                                                END
                                )::NUMERIC                                              AS total_issues_done
                                FROM vw_issues AS P1     
                                WHERE P1.userstory_id   = T1.userstory_id
                        ) AS L2 ON TRUE
        WHERE T1.is_active
        )
        SELECT  sprint_title,
                userstory_title,
                tasks_total,
                tasks_completed,
                task_comp_ratio || '%' AS task_comp_ratio_per,
                estimate_total,
                logged_total,
                remainig_total
        FROM total
        ORDER BY        sprint_title,
                        task_comp_ratio DESC;

