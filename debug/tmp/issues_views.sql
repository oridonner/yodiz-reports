--Added fields: IsOpen boolean, SeverityVal int  
DROP VIEW IF EXISTS vw_issues CASCADE;
CREATE VIEW vw_issues as
    SELECT  *,
            CASE 
                WHEN status IN ('Ignored','Closed','Duplicate','Rejected','Custom status') THEN False
                WHEN severity IN ('Not in Use') THEN False
                ELSE True
            END AS IsOpen,
            CASE
                WHEN Severity = 'Blocker' THEN 1
                WHEN Severity = 'Critical' THEN 2
                WHEN Severity = 'Major' THEN 3
                WHEN Severity = 'Normal' THEN 4
                WHEN Severity = 'Minor' THEN 5
                ELSE 99
            END AS SeverityVal,
            CASE    
                WHEN Status IN ('Blocked') THEN 'Blocked'
                WHEN Status IN ('New','Next') THEN 'Open'
                WHEN Status IN ('Waiting for testing','Testing','Developing') THEN 'InProgress'
                WHEN Status IN ('QA approved') THEN 'Approved'
            END AS OpenIssueCategory
    FROM Issues;


-- Open issues severity pivoted by OpenIssueCategory
DROP VIEW IF EXISTS vw_open_issues_severity;
CREATE VIEW vw_open_issues_severity AS
SELECT Severity , Open , InProgress , Approved , Blocked 
FROM crosstab('select Severity, OpenIssueCategory, count(id)::int as ct from vw_issues where isopen group by 1,2 order by 1,2') 
AS final_results(Severity TEXT, Approved INT, Blocked INT,InProgress INT, Open INT);

-- Bugs per user
DROP VIEW IF EXISTS vw_open_issues_per_user;
CREATE VIEW vw_open_issues_per_user AS
SELECT  T2.FirstName || ' ' || T2.LastName AS UserName,
        COUNT(T1.Id) AS Issues
        FROM vw_open_issues T1
JOIN Users  T2 ON T1.ResponsibleId = T2.Id
WHERE T1.IsOpen 
GROUP BY T2.FirstName || ' ' || T2.LastName
ORDER BY 2 DESC;

-- Total bugs closed vs. opened  MTD PMTD
DROP VIEW IF EXISTS vw_mtd_vs_pmtd_issues;
CREATE VIEW vw_mtd_vs_pmtd_issues AS
-- open mtd , close mtd , open lmtd , close lmtd
SELECT  MtdCategory ,
        closed_last_month,
        opened_current_month,
        opened_last_month
FROM crosstab 
('
    WITH 
    categories AS (
        SELECT  Id,
                Status,
                UpdatedOn,
                CreatedOn,
                CASE 
                    WHEN CreatedOn BETWEEN last_month_trunc(current_date) AND last_month(current_date)                          THEN ''opened_last_month''
                    WHEN Status=''Closed'' AND UpdatedOn BETWEEN last_month_trunc(current_date) AND last_month(current_date)    THEN ''closed_last_month''
                    WHEN CreatedOn>=date_trunc(''month'',current_date)                                                          THEN ''opened_current_month''
                    WHEN Status=''Closed'' AND UpdatedOn>=date_trunc(''month'',current_date)                                    THEN ''closed_current_month''
                END AS MtdCategory
        FROM vw_issues
    )
    SELECT  ''MTD Report'',
            MtdCategory,
            COUNT(Id)::INT AS Ids
    FROM categories
    WHERE categories IS NOT NULL
    GROUP BY 1,2
    ORDER BY 1,2
') AS final_results(
                        MtdCategory             TEXT, 
                        closed_last_month       INT, 
                        opened_last_month       INT, 
                        opened_current_month    INT, 
                        closed_current_month    INT
                    );