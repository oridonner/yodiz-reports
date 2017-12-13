DROP VIEW IF EXISTS vw_sprint_issues CASCADE;
CREATE VIEW vw_sprint_issues AS
        -- WITH total AS 
        -- (
        SELECT  T2.sprint_title,
                T1.issue_id,
                T1.issue_title,
                T1.status,
                T2.is_active,
                T1.effort_estimate::NUMERIC                        AS effort_estimate,
                T1.effort_remaining::NUMERIC                       AS effort_remaining,
                T1.effort_logged::NUMERIC                          AS effort_spent,
                CASE 
                        WHEN effort_estimate = 0 THEN 0
                ELSE round(T1.effort_logged*100/T1.effort_estimate) 
        END                                                        AS effort_completion_ratio,  
                CASE WHEN T1.is_open THEN 0 ELSE 1 END::NUMERIC    AS is_done
        FROM vw_issues     T1
        JOIN vw_sprints    T2 ON T2.sprint_id=T1.sprint_id
        WHERE T2.is_active
        ORDER BY        sprint_title,
        8 DESC;
        -- )
        -- SELECT  sprint_title,
        --         issue_id,
        --         issue_title,
        --         effort_estimate,
        --         effort_remaining,
        --         effort_spent,
        --         is_done,
        --         effort_completion_ratio,
        --         case
        --              when is_done = 1 then 'Done'
        --              when effort_spent > 0 then 'In Progress'
        --              when effort_completion_ratio = 0 then 'Not Started'
        --              else 'err'
        --         end                     AS "status" 
        -- FROM total
        -- ORDER BY        sprint_title,
        --                 8 DESC;