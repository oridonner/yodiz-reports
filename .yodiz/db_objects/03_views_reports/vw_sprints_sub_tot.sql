DROP VIEW IF EXISTS vw_sprints_sub_tot CASCADE;
CREATE VIEW vw_sprints_sub_tot AS
        WITH total AS 
        (
        SELECT  T1.sprint_id,
                T1.sprint_title,
                T1.userstory_title ,
                L1.total_tasks_usersoty + L2.total_issues_userstory                     AS tasks_total,
                COALESCE(L1.total_tasks_blocked,0)                                      AS total_tasks_blocked,
                COALESCE(L1.total_tasks_progress,0)                                     AS total_tasks_progress,
                COALESCE(L2.total_issues_done,0)  + COALESCE(L1.total_tasks_done,0)     AS tasks_completed,
                CASE    WHEN 
                                L1.total_tasks_usersoty + L2.total_issues_userstory = 0 THEN 0
                        ELSE
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
                                        )   
                END                                                                     AS task_comp_ratio,
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
        FROM vw_userstories     T1
        -- tasks totals
        LEFT JOIN LATERAL (     
                                SELECT  COUNT(P1.task_id)::NUMERIC                                              AS total_tasks_usersoty,
                                        SUM(P1.effort_estimate)::NUMERIC                                        AS total_tasks_estimate,
                                        SUM(P1.effort_remaining)::NUMERIC                                       AS total_tasks_remaining,
                                        SUM(P1.effort_logged)::NUMERIC                                          AS total_tasks_logged,
                                        SUM (CASE WHEN P1.status = 'done' THEN 1 ELSE 0 END)::NUMERIC           AS total_tasks_done,
                                        SUM (CASE WHEN P1.status = 'blocked' THEN 1 ELSE 0 END )::NUMERIC       AS total_tasks_blocked,
                                        SUM (CASE WHEN P1.status = 'in progress' THEN 1 ELSE 0 END)::NUMERIC    AS total_tasks_progress
                                FROM vw_tasks AS P1
                                WHERE P1.userstory_id   = T1.userstory_id
                        ) AS L1 ON TRUE
        -- isuues totals
        LEFT JOIN LATERAL (     
                                SELECT  COUNT(P1.issue_id)::NUMERIC                             AS total_issues_userstory,
                                        SUM(P1.effort_estimate)::NUMERIC                        AS total_issues_estimate,
                                        SUM(P1.effort_remaining)::NUMERIC                       AS total_issues_remaining,
                                        SUM(P1.effort_logged)::NUMERIC                          AS total_issues_logged,
                                        SUM(CASE WHEN P1.is_open THEN 0 ELSE 1 END)::NUMERIC    AS total_issues_done
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
                remainig_total,
                total_tasks_blocked,
                total_tasks_progress,
                case
                     when task_comp_ratio = 100 then 'Done'
                     when total_tasks_progress > 0 or tasks_completed > 0 then 'In Progress'
                     when task_comp_ratio > 0  and task_comp_ratio < 100 and total_tasks_blocked > 0 then 'Blocked'
                     when total_tasks_progress = 0 and tasks_completed = 0 then 'Not Started'
                     else 'err'
                end as userstory_status
        FROM total
        ORDER BY        sprint_title,
                        task_comp_ratio DESC;