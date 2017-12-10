DROP VIEW IF EXISTS vw_release_effort CASCADE;
CREATE VIEW vw_release_effort AS
        WITH effort AS
        (
                SELECT  T3.release_title,
                        SUM(T1."estimate_total")   AS total_effort_estimate, 
                        SUM(T1."logged_total")     AS total_effort_spent, 
                        SUM(T1."remainig_total")   AS total_effort_remaining
                FROM vw_sprint_userstories      AS T1
                JOIN vw_userstories             AS T2 ON T2.userstory_id = T1.userstory_id 
                JOIN vw_releases                AS T3 ON T3.release_id = T2.release_id
                WHERE T3.is_active
                GROUP BY 1
        )
        SELECT  release_title,
                total_effort_estimate, 
                total_effort_spent, 
                total_effort_remaining,
                round(total_effort_spent*100/total_effort_estimate) AS effort_completion_ratio
        FROM effort;