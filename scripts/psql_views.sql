-- Enable extension
CREATE extension tablefunc;

--Added fields: IsOpen boolean, SeverityVal int  
DROP VIEW IF EXISTS vw_issues;
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
AS final_results(Severity TEXT, Open INT, InProgress INT, Approved INT, Blocked INT);

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
WITH 
calendar as
(
select  last_month_trunc(current_date) AS LastMonthStart,
        date_trunc('month',current_date) AS CurrentMonthStart
),
opened_last_month AS(
    SELECT  COUNT(Id) AS opened_last_month,
            last_month_trunc(current_date) AS LastMonthStart,
            date_trunc('month',current_date) AS CurrentMonthStart
    FROM vw_issues 
    WHERE CreatedOn>=last_month_trunc(current_date) and CreatedOn<last_month(current_date)
    GROUP BY 2,3   
),
closed_last_month AS(
    SELECT  COUNT(Id) AS closed_last_month,
            last_month_trunc(current_date) AS LastMonthStart,
            date_trunc('month',current_date) AS CurrentMonthStart
    FROM vw_issues 
    WHERE Status='Closed' AND UpdatedOn>=last_month_trunc(current_date) and UpdatedOn<last_month(current_date)
    GROUP BY 2,3
),
opened_current_month AS(
    SELECT  COUNT(Id) AS opened_current_month,
            last_month_trunc(current_date) AS LastMonthStart,
            date_trunc('month',current_date) AS CurrentMonthStart
    FROM vw_issues 
    WHERE CreatedOn>=date_trunc('month',current_date)
    GROUP BY 2,3
),
closed_current_month AS (
    SELECT  COUNT(Id) AS closed_current_month,
            last_month_trunc(current_date) AS LastMonthStart,
            date_trunc('month',current_date) AS CurrentMonthStart
    FROM vw_issues 
    WHERE Status='Closed' AND UpdatedOn>=date_trunc('month',current_date)
    GROUP By 2,3
)
SELECT  T1.opened_last_month,
        T2.closed_last_month,
        T3.opened_current_month,
        T4.closed_current_month
FROM calendar T
LEFT JOIN opened_last_month T1 ON T1.LastMonthStart=T.LastMonthStart
LEFT JOIN closed_last_month T2 ON T2.LastMonthStart=T.LastMonthStart
LEFT JOIN opened_current_month T3 ON T3.LastMonthStart = T.LastMonthStart
LEFT JOIN closed_current_month T4 ON T4.LastMonthStart = T.LastMonthStart;



-- DROP VIEW IF EXISTS vw_severity_status;
-- create view vw_severity_status as
--     select severity ,     
--     sum(case when OpenIssueCategory ='Blocked' then 1 else 0 end) as blocked,
--     sum(case when OpenIssueCategory = 'Open' then 1 else 0 end) as open_bugs,
--     sum(case when OpenIssueCategory = 'InProgress' then 1 else 0 end) as in_progress,
--     sum(case when OpenIssueCategory = 'Approved' then 1 else 0 end) as qa_approved,
--     count(1) as total
--     from vw_open_issues a
--     WHERE 1=1
--     and a.IsOpen 
--     group by a.severity,a.SeverityVal  
--     order by a.SeverityVal
--     ;


-- -- Bugs OPENED since the beginning of CURRENT month
-- DROP VIEW IF EXISTS vw_issues_opened_current_month;
-- CREATE VIEW vw_issues_opened_current_month AS
-- SELECT  Id,
--         CreatedOn,
--         date_trunc('month',CreatedOn) AS CurrentMonthStart
-- FROM vw_issues 
-- WHERE CreatedOn>=date_trunc('month',current_date);
-- -- Total bugs OPENED since the beginning of CURRENT month
-- DROP VIEW IF EXISTS vw_total_issues_opened_current_month;
-- CREATE VIEW vw_total_issues_opened_current_month AS
-- SELECT  COUNT(Id) Issues,
--         date_trunc('month',CreatedOn) AS CurrentMonthStart
-- FROM vw_issues 
-- WHERE CreatedOn>=date_trunc('month',current_date)
-- GROUP BY 2;


-- -- Bugs OPENED since the beginning of LAST month
-- DROP VIEW IF EXISTS vw_issues_opened_last_month;
-- CREATE VIEW vw_issues_opened_last_month AS
-- SELECT  Id,
--         CreatedOn,
--         last_month_trunc(current_date) AS LastMonthStart,
--         last_month(current_date) AS DayLastMonth,
--         date_trunc('month',current_date) AS CurrentMonthStart
-- FROM vw_issues 
-- WHERE CreatedOn>=last_month_trunc(current_date) and CreatedOn<last_month(current_date);
-- -- Total bugs OPENED since the beginning of LAST month
-- DROP VIEW IF EXISTS vw_total_issues_opened_last_month;
-- CREATE VIEW vw_total_issues_opened_last_month AS
-- SELECT  COUNT(Id) Issues,
--         last_month_trunc(current_date) AS LastMonthStart
-- FROM vw_issues 
-- WHERE CreatedOn>=last_month_trunc(current_date) and CreatedOn<last_month(current_date)
-- GROUP BY 2;


-- -- Bugs CLOSED since the beginning of CURRENT month
-- DROP VIEW IF EXISTS vw_issues_closed_current_month;
-- CREATE VIEW vw_issues_closed_current_month AS
-- SELECT  Id,
--         UpdatedOn,
--         Status,
--         date_trunc('month',UpdatedOn) AS CurrentMonthStart
-- FROM vw_issues 
-- WHERE Status='Closed' AND UpdatedOn>=date_trunc('month',current_date);
-- -- Total bugs CLOSED since the beginning of CURRENT month
-- DROP VIEW IF EXISTS vw_total_issues_closed_current_month;
-- CREATE VIEW vw_total_issues_closed_current_month AS
-- SELECT  COUNT(Id) Issues,
--         date_trunc('month',UpdatedOn) AS CurrentMonthStart
-- FROM vw_issues 
-- WHERE Status='Closed' AND UpdatedOn>=date_trunc('month',current_date)
-- GROUP By 2;

-- -- Bugs CLOSED since the beginning of LAST month
-- DROP VIEW IF EXISTS vw_issues_closed_last_month;
-- CREATE VIEW vw_issues_closed_last_month AS
-- SELECT  Id,
--         UpdatedOn,
--         Status,
--         last_month_trunc(current_date) AS LastMonthStart,
--         last_month(current_date) AS DayLastMonth,
--         date_trunc('month',current_date) AS CurrentMonthStart
-- FROM vw_issues 
-- WHERE Status='Closed' AND UpdatedOn>=last_month_trunc(current_date) and UpdatedOn<last_month(current_date);
-- -- Total bugs CLOSED since the beginning of LAST month
-- DROP VIEW IF EXISTS vw_total_issues_closed_last_month;
-- CREATE VIEW vw_total_issues_closed_last_month AS
-- SELECT  COUNT(Id) Issues,
--         last_month_trunc(current_date) AS LastMonthStart
-- FROM vw_issues 
-- WHERE Status='Closed' AND UpdatedOn>=last_month_trunc(current_date) and UpdatedOn<last_month(current_date)
-- GROUP BY 2;
