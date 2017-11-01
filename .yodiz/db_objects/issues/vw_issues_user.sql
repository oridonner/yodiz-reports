-- Bugs per user
DROP VIEW IF EXISTS vw_issues_user;
CREATE VIEW vw_issues_user AS
    SELECT  T2.full_name,
            COUNT(T1.issue_id) AS issues
    FROM vw_issues T1
    JOIN vw_users  T2 ON T1.responsible_id = T2.user_id
    WHERE T1.is_open 
    GROUP BY T2.full_name
    ORDER BY 2 DESC;


    