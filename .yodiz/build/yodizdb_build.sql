
CREATE SCHEMA IF NOT EXISTS EXTR;
CREATE SCHEMA IF NOT EXISTS TRNS;
CREATE SCHEMA IF NOT EXISTS LOAD;
CREATE SCHEMA IF NOT EXISTS TEMP;
CREATE SCHEMA IF NOT EXISTS YODIZ;


CREATE EXTENSION IF NOT EXISTS tablefunc;
CREATE EXTENSION IF NOT EXISTS hstore;


-- CREATE OR REPLACE FUNCTION html_table(query text)
--   RETURNS SETOF text AS
-- $BODY$
-- declare
--     rec record;
--     header boolean := true;
-- begin
--     return next '<html><head><style>h1 {color: green;text-align: center;}label {color: darkgreen;}table {border-collapse: collapse;width: 100%;}th {text-align: left;padding: 8px;background-color:cornflowerblue;color:white;}.tdErr {color:red;}.tdOk {color:green;}</style></head><body><h1></h1><table>';
--     for rec in
--         execute format($q$
--             select row_to_json(q) json_row
--             from (%s) q
--             $q$, query)
--     loop
--         if header then
--             return query select
--                 format ('<tr><th>%s</th></tr>', string_agg(key, '</th><th>'))
--             from json_each(rec.json_row);
--             header := false;
--         end if;
--         return query select
--             format ('<tr><td>%s</td></tr>', string_agg(value, '</td><td>'))
--         from json_each_text(rec.json_row);
--     end loop;
--     return next '</table></body></html>';
-- end $BODY$
--   LANGUAGE plpgsql VOLATILE
--   COST 100
--   ROWS 1000;
-- ALTER FUNCTION html_table(text)
--   OWNER TO postgres;
DROP FUNCTION IF EXISTS last_month(timestamp without time zone);
CREATE FUNCTION last_month(timestamp without time zone) RETURNS timestamp without time zone AS $$
    select $1 - interval '1' month
$$ LANGUAGE SQL;
DROP FUNCTION IF EXISTS last_month_trunc(timestamp without time zone);
CREATE FUNCTION last_month_trunc(timestamp without time zone) RETURNS timestamp without time zone AS $$
    select date_trunc('month',last_month($1))
$$ LANGUAGE SQL;
DROP FUNCTION IF EXISTS days_trunc(timestamp without time zone);
CREATE FUNCTION days_trunc(timestamp without time zone) RETURNS interval AS $$
    select date_trunc('day',$1 - date_trunc('month',$1)) + interval '1' day
$$ LANGUAGE SQL;


DROP TABLE IF EXISTS Emails CASCADE;
CREATE TABLE Emails(
    user_id         int,
    email           text
);
INSERT INTO Emails VALUES (25, 'ofers@sqreamtech.com');
INSERT INTO Emails VALUES (11, 'ben@sqreamtech.com');
INSERT INTO Emails VALUES (36, 'gilm@sqreamtech.com');
INSERT INTO Emails VALUES (31, 'yuval@sqreamtech.com');
INSERT INTO Emails VALUES (4, 'eyal@sqreamtech.com');
INSERT INTO Emails VALUES (7, 'or@sqreamtech.com');
INSERT INTO Emails VALUES (19, 'shai@sqreamtech.com');
INSERT INTO Emails VALUES (3, 'galit@sqreamtech.com');
INSERT INTO Emails VALUES (17, 'sivan@sqreamtech.com');
INSERT INTO Emails VALUES (33, 'omert@sqreamtech.com');
INSERT INTO Emails VALUES (52, 'orid@sqreamtech.com');
INSERT INTO Emails VALUES (47, 'eyalc@sqreamtech.com');
INSERT INTO Emails VALUES (51, 'eliy@sqreamtech.com');
INSERT INTO Emails VALUES (18, 'eli@sqreamtech.com');
INSERT INTO Emails VALUES (28, 'yanai@sqreamtech.com');
INSERT INTO Emails VALUES (41, 'rotem@sqreamtech.com');
INSERT INTO Emails VALUES (45, 'erez@sqreamtech.com');
INSERT INTO Emails VALUES (14, 'razi@sqreamtech.com');
INSERT INTO Emails VALUES (53, 'jeremy@sqreamtech.com');

DROP TABLE IF EXISTS Issues CASCADE;
CREATE TABLE Issues(
    Guid              text,
    Id                int,
    Title             text,
    UserStoryId       int,   -- inserted by code, not from custom api
    CreatedById       int,
    UpdatedOn         timestamp without time zone,
    UpdatedById       int,
    CreatedOn         timestamp without time zone,
    ResponsibleId     int, 
    Status            text,
    Severity          text,
    ReleaseId         int,
    SprintId          int,
    EffortEstimate    real,
    EffortRemaining   real,
    EffortLogged      real
);

DROP TABLE IF EXISTS Releases CASCADE;
CREATE TABLE Releases(
    Guid              text,
    Id                int,
    Title             text,
    CreatedById       int,
    UpdatedOn         timestamp without time zone,
    CreatedOn         timestamp without time zone,
    Status            text,
    StartDate         timestamp without time zone,
    EndDate           timestamp without time zone    
);

DROP TABLE IF EXISTS Sprints CASCADE;
CREATE TABLE Sprints(
    Guid              text,
    Id                int,
    Title             text,
    CreatedById       int,
    UpdatedOn         timestamp without time zone,
    CreatedOn         timestamp without time zone,
    Status            text,
    StartDate         timestamp without time zone,
    EndDate           timestamp without time zone    
);

DROP TABLE IF EXISTS Tasks CASCADE;
CREATE TABLE Tasks(
    Guid              text,
    TaskId            int,
    UserStoryId       int,  --inserted by code, not custom api
    Title             text,
    CreatedById       int,
    UpdatedOn         timestamp without time zone,
    UpdatedById       int,
    CreatedOn         timestamp without time zone,
    Status            text,
    EffortEstimate    real,
    EffortRemaining   real,
    EffortLogged      real
);

DROP TABLE IF EXISTS Users;
CREATE TABLE Users(
    Guid              text,
    Id                int,
    FirstName         text,
    LastName          text,
    UpdatedOn         timestamp without time zone,
    CreatedOn         timestamp without time zone
);

DROP TABLE IF EXISTS UserStories;
CREATE TABLE UserStories(
    Guid              text,
    Id                int,
    Title             text,
    CreatedById       int,
    UpdatedOn         timestamp without time zone,
    UpdatedById       int,
    CreatedOn         timestamp without time zone,
    ResponsibleId     int, 
    Status            text,
    ReleaseId         int,
    SprintId          int,
    EffortEstimate    real,
    EffortRemaining   real,
    EffortLogged      real
);

DROP VIEW IF EXISTS vw_users CASCADE;
CREATE VIEW vw_users AS
        SELECT  t1.Id                              AS user_id,
                t1.FirstName                       AS first_name,
                t1.LastName                        AS last_name,
                t1.FirstName || ' ' || LastName    AS full_name,
                t2.email                           AS email,
                t1.UpdatedOn                       AS updated_on,
                t1.CreatedOn                       AS created_on
        FROM Users              AS t1
        LEFT JOIN Emails        AS t2 ON t2.user_id = t1.Id;


--Added fields: IsOpen boolean, SeverityVal int  
DROP VIEW IF EXISTS vw_issues CASCADE;
CREATE VIEW vw_issues as
    SELECT  Guid            ,
            Id              AS issue_id,
            Title           ,
            UserStoryId     AS userstory_id,
            CreatedById     AS created_by_id,
            UpdatedOn       AS updated_on,
            UpdatedById     AS updated_by_id,
            CreatedOn       AS created_on,
            ResponsibleId   AS responsible_id,
            Status          ,
            Severity        ,
            ReleaseId       ,
            SprintId        AS sprint_id,
            EffortEstimate  AS effort_estimate,
            EffortRemaining AS effort_remaining,
            EffortLogged    AS effort_logged,  
            CASE 
                WHEN status IN ('Ignored','Closed','Duplicate','Rejected','Custom status') THEN False
                WHEN severity IN ('Not in Use') THEN False
                ELSE True
            END AS is_open,
            CASE
                WHEN Severity = 'Blocker' THEN 1
                WHEN Severity = 'Critical' THEN 2
                WHEN Severity = 'Major' THEN 3
                WHEN Severity = 'Normal' THEN 4
                WHEN Severity = 'Minor' THEN 5
                ELSE 99
            END AS severity_val,
            CASE    
                WHEN Status IN ('Blocked') THEN 'Blocked'
                WHEN Status IN ('New','Next') THEN 'Open'
                WHEN Status IN ('Waiting for testing','Testing','Developing') THEN 'InProgress'
                WHEN Status IN ('QA approved') THEN 'Approved'
            END AS open_issue_category
    FROM Issues;

DROP VIEW IF EXISTS vw_releases;
CREATE VIEW vw_releases AS
WITH Status AS 
(
    SELECT  Id,
            Title,
            CASE 
                WHEN StartDate > current_date                       THEN 'Planned'
                WHEN current_date BETWEEN StartDate AND EndDate     THEN 'Active'
                WHEN current_date > EndDate                         THEN 'Closed'
            END AS Status,
            CreatedById,
            UpdatedOn,
            CreatedOn,
            StartDate,
            EndDate
    FROM Releases
)
SELECT  *,
        CASE 
            WHEN Status = 'Active'     THEN True
            ELSE False
        END AS IsActive
FROM Status;


DROP VIEW IF EXISTS vw_tasks CASCADE;
CREATE VIEW vw_tasks AS
SELECT  T1.guid,
        T1.taskid       AS task_id,
        T1.userstoryid  AS userstory_id,
        T1.title,
        T1.createdbyid  AS created_by,
        T1.updatedon    AS updated_on,
        T1.updatedbyid  AS updated_by,
        T1.createdon    AS created_on,
        CASE
            WHEN T1.status ~~ '%10%'::text THEN 'new'::text
            WHEN T1.status ~~ '%20%'::text THEN 'in progress'::text
            WHEN T1.status ~~ '%30%'::text THEN 'done'::text
            WHEN T1.status ~~ '%40%'::text THEN 'blocked'::text
            ELSE 'unknown'::text
        END AS status,
        T1.effortestimate   AS effort_estimate,
        T1.effortremaining  AS effort_remaining,
        T1.effortlogged     AS effort_logged
   FROM tasks AS T1;

DROP VIEW IF EXISTS vw_sprints CASCADE;
CREATE VIEW vw_sprints AS
    WITH status AS 
    (
        SELECT  Id                          AS sprint_id,
                Title                       AS sprint_title,
                CASE 
                    WHEN StartDate > current_date                       THEN 'Planned'
                    WHEN current_date BETWEEN StartDate AND EndDate     THEN 'Active'
                    WHEN current_date > EndDate                         THEN 'Closed'
                END                         AS status,
                CreatedById                 AS created_by_id,
                CAST(UpdatedOn AS DATE)     AS updated_on,
                CAST(CreatedOn AS DATE)     AS created_on,
                CAST(StartDate AS DATE)     AS start_date,
                CAST(EndDate AS DATE)       AS end_date
        FROM Sprints
    )
    SELECT  t1.sprint_id                                AS sprint_id,
            t1.sprint_title                             AS sprint_title,
            t1.status                                   AS status,
            t1.created_by_id                            AS created_by_id,
            t2.full_name                                AS created_by,
            t1.updated_on                               AS updated_on,
            t1.created_on                               AS created_on,
            t1.start_date                               AS start_date,
            t1.end_date                                 AS end_date,
            CASE 
                WHEN Status = 'Active'     THEN True
                ELSE False
            END                                         AS is_active
    FROM status     AS t1
    JOIN vw_users   AS t2 on t2.user_id = t1.created_by_id;


DROP VIEW IF EXISTS vw_userstories CASCADE;
CREATE VIEW vw_userstories AS
    SELECT  T1.Id                                       AS userstory_id,
            T1.Title                                    AS userstory_title,
            T1.ReleaseId                                AS release_id,
            T2.sprint_id                                AS sprint_id,
            T2.sprint_title                             AS sprint_title,            
            T1.CreatedById                              AS created_by,
            T1.UpdatedOn                                AS updated_on,
            T1.UpdatedById                              AS updated_by,
            T1.CreatedOn                                AS created_on,
            T1.ResponsibleId                            AS responsible,
            T1.Status                                   AS status,
            CASE 
                WHEN T2.Status = 'Active'     THEN True
                ELSE False
            END                                         AS is_active,
            T1.EffortEstimate                           AS effort_estimate,
            T1.EffortRemaining                          AS effort_remaining,
            T1.EffortLogged                             AS effort_logged
    FROM UserStories    T1
    JOIN vw_sprints     T2 ON T2.sprint_id = T1.SprintId; 

-- open mtd , close mtd , open lmtd , close lmtd
DROP VIEW IF EXISTS vw_issues_mtd;
CREATE VIEW vw_issues_mtd AS
SELECT  mtd_category ,
        opened_current_month,
        closed_current_month,
        opened_last_month,
        closed_last_month
FROM crosstab 
('
    WITH 
    categories AS (
        SELECT  issue_id,
                status,
                updated_on,
                created_on,
                CASE 
                    WHEN created_on BETWEEN last_month_trunc(current_date) AND last_month(current_date)                         THEN ''opened_last_month''
                    WHEN status=''Closed'' AND updated_on BETWEEN last_month_trunc(current_date) AND last_month(current_date)    THEN ''closed_last_month''
                    WHEN created_on>=date_trunc(''month'',current_date)                                                         THEN ''opened_current_month''
                    WHEN status=''Closed'' AND updated_on>=date_trunc(''month'',current_date)                                   THEN ''closed_current_month''
                END AS mtd_category
        FROM vw_issues
    )
    SELECT  ''MTD Report'',
            mtd_category,
            COUNT(issue_id)::INT AS Ids
    FROM categories
    WHERE categories IS NOT NULL
    GROUP BY 1,2
    ORDER BY 1,2
') AS final_results(
                        mtd_category            TEXT, 
                        closed_last_month       INT, 
                        opened_last_month       INT, 
                        opened_current_month    INT, 
                        closed_current_month    INT
                    );

-- Open issues severity pivoted by OpenIssueCategory
DROP VIEW IF EXISTS vw_open_issues_severity;
CREATE VIEW vw_open_issues_severity AS
    SELECT  severity , 
            open , 
            in_progress , 
            approved , 
            blocked 
    FROM crosstab
    ('
        SELECT  severity, 
                open_issue_category, 
                COUNT(issue_id)::int AS ct
        FROM vw_issues
        WHERE is_open
        GROUP BY 1,2 
        ORDER BY 1,2
    ') 
    AS final_results(   
                        severity    TEXT, 
                        approved    INT, 
                        blocked     INT,
                        in_progress INT, 
                        open        INT
                    );

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


DROP VIEW IF EXISTS vw_sprints_headers CASCADE;
CREATE VIEW vw_sprints_headers AS
SELECT  T1.sprint_id,
        T1.sprint_title,
        T2.full_name                            AS responsible,
        T2.email                                AS responsible_email,
        T1.start_date,
        T1.end_date,
        T1.end_date - T1.start_date +1          AS total_days,
        current_date - T1.start_date + 1        AS day_number 
FROM vw_sprints AS T1
JOIN vw_users   AS T2 ON T2.user_id = T1.created_by_id
WHERE T1.is_active;

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

