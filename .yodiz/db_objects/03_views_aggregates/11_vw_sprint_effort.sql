DROP VIEW IF EXISTS vw_sprint_effort CASCADE;
CREATE VIEW vw_sprint_effort AS
        WITH effort AS
        (
                SELECT  sprint_title, 
                        SUM("estimate_total")   AS total_effort_estimate, 
                        SUM("logged_total")     AS total_effort_spent, 
                        SUM("remainig_total")   AS total_effort_remaining
                FROM vw_sprint_userstories 
                GROUP BY 1
        )
        SELECT  sprint_title,
                total_effort_estimate, 
                total_effort_spent, 
                total_effort_remaining,
                round(total_effort_spent*100/total_effort_estimate) AS effort_completion_ratio
        FROM effort;