-- Bugs per user
DROP VIEW IF EXISTS vw_issues_user;
CREATE VIEW vw_issues_user AS
    SELECT  T2.FirstName || ' ' || T2.LastName AS UserName,
            COUNT(T1.Id) AS Issues
            FROM vw_issues T1
    JOIN Users  T2 ON T1.ResponsibleId = T2.Id
    WHERE T1.IsOpen 
    GROUP BY T2.FirstName || ' ' || T2.LastName
    ORDER BY 2 DESC;


    