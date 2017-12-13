--All sprints related to active release - including finished ones
DROP VIEW IF EXISTS vw_sprint_effort CASCADE;
CREATE VIEW vw_sprint_effort AS
        WITH effort AS
        (
                SELECT  sprint_id,
                        sprint_title, 
                        SUM("estimate_total")   AS total_effort_estimate, 
                        SUM("logged_total")     AS total_effort_spent, 
                        SUM("remaining_total")   AS total_effort_remaining
                FROM vw_sprint_userstories 
                GROUP BY 1,2
        )
        SELECT  sprint_id,
                sprint_title,
                total_effort_estimate, 
                total_effort_spent, 
                total_effort_remaining,
                CASE 
                        WHEN total_effort_estimate = 0 THEN 0
                        ELSE round(total_effort_spent*100/total_effort_estimate) 
                END AS effort_completion_ratio
        FROM effort;