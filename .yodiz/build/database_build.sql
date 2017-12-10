
DROP VIEW IF EXISTS vw_api_log;
CREATE VIEW vw_api_log AS
SELECT * 
FROM api_log 
ORDER BY time_stamp DESC 
LIMIT 10;

DROP DATABASE IF EXISTS yodizdev;
CREATE DATABASE yodizdev;
\c yodizdev

CREATE SCHEMA IF NOT EXISTS EXTR;
CREATE SCHEMA IF NOT EXISTS TRNS;
CREATE SCHEMA IF NOT EXISTS LOAD;
CREATE SCHEMA IF NOT EXISTS TEMP;
CREATE SCHEMA IF NOT EXISTS YODIZ;


CREATE EXTENSION IF NOT EXISTS tablefunc;
CREATE EXTENSION IF NOT EXISTS hstore;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

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
CREATE OR REPLACE FUNCTION public.table_count(table_name text) 
RETURNS SETOF RECORD
LANGUAGE plpgsql
AS $BODY$
BEGIN
    RETURN QUERY EXECUTE 'select count(*) from ' || table_name;
END
$BODY$;


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
INSERT INTO Emails VALUES (12, 'arnon@sqreamtech.com');
INSERT INTO Emails VALUES (46, 'guy@sqreamtech.com');
INSERT INTO Emails VALUES (38, 'dotan@sqreamtech.com');
INSERT INTO Emails VALUES (54, 'bennyvz@sqreamtech.com');
INSERT INTO Emails VALUES (29, 'amihaig@sqreamtech.com');
INSERT INTO Emails VALUES (50, 'israelg@sqreamtech.com');
INSERT INTO Emails VALUES (56, 'maayank@sqreamtech.com');
INSERT INTO Emails VALUES (55, 'almag@sqreamtech.com');
INSERT INTO Emails VALUES (48, 'slavi@sqreamtech.com');

DROP TABLE IF EXISTS mailing_lists CASCADE;
CREATE TABLE mailing_lists(
    id          SERIAL,
    environment TEXT,
    report      TEXT,
    to_user_id  INT,
    cc_user_id  INT
);

DROP TABLE IF EXISTS inventory CASCADE;
CREATE TABLE inventory (
    object_name     TEXT,
    object_type     TEXT,
    is_exist        BOOLEAN,
    is_empty        BOOLEAN         
);
INSERT INTO inventory (
            object_name,
            object_type
)
VALUES 
('api_log','table'),('db_log','table'),('issues','table'),('releases','table'),('sprints','table'),('tasks','table'),('userstories','table'),('users','table'),
('vw_users','view'),('vw_issues','view'),('vw_releases','view'),('vw_tasks','view'),('vw_sprints','view'),('vw_userstories','view'),
('vw_sprint_userstories','view'),('vw_sprints_headers','view'),('vw_tasks_tot','view'),('vw_sprint_effort','view'),('vw_capacity','view'),
('vw_release_headers','view'),('vw_release_effort','view'),('vw_releases','view'),
('vw_capacity_report','view'),('vw_sprint_userstories_report','view'),('vw_sprint_summary_report','view');


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
    TaskOwnerId       int,
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

DROP TABLE IF EXISTS Users CASCADE;
CREATE TABLE Users(
    Guid              text,
    Id                int,
    FirstName         text,
    LastName          text,
    FocusFactor       NUMERIC,
    is_rnd            boolean,
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

DROP TABLE IF EXISTS api_log CASCADE;
CREATE TABLE api_log(
    api_guid        uuid NOT NULL DEFAULT uuid_generate_v1(),
    transact_guid   uuid,
    http_req        TEXT,
    response_code   INT,
    response_text   TEXT,
    time_stamp      timestamp without time zone
);

DROP TABLE IF EXISTS db_log CASCADE;
CREATE TABLE db_log(
    db_guid         uuid NOT NULL DEFAULT uuid_generate_v1(),
    transact_guid   uuid,
    table_name      TEXT,
    action          TEXT,
    rows_effected   INT,
    time_stamp      timestamp without time zone
);

DROP TABLE IF EXISTS userstories_daily CASCADE;
CREATE TABLE userstories_daily 
(
    id                      SERIAL,
    date                    DATE,
    userstory_id            INT,
    userstory_title         TEXT,
    status                  TEXT,
    tasks_total             INT,
    total_tasks_unplanned   INT,
    total_tasks_progress    INT,   
    tasks_completed         INT,        
    task_comp_ratio         REAL, 
    estimate_total          REAL,         
    logged_total            REAL,           
    remainig_total          REAL        
);


--Update focufactor
UPDATE users SET focusfactor = 0.5 WHERE firstname IN ('Ben','Ofer','Gil','Yuval');
UPDATE users SET focusfactor = 0.75 WHERE firstname NOT IN ('Ben','Ofer','Gil','Yuval');
--Update is_rnd
UPDATE users SET is_rnd = true WHERE id=11;
UPDATE users SET is_rnd = true WHERE id=25;
UPDATE users SET is_rnd = true WHERE id=36;
UPDATE users SET is_rnd = true WHERE id=4;
UPDATE users SET is_rnd = true WHERE id=17;
UPDATE users SET is_rnd = true WHERE id=18;
UPDATE users SET is_rnd = true WHERE id=19;
UPDATE users SET is_rnd = true WHERE id=28;
UPDATE users SET is_rnd = true WHERE id=47;
UPDATE users SET is_rnd = true WHERE id=51;
UPDATE users SET is_rnd = true WHERE id=53;
UPDATE users SET is_rnd = true WHERE id=54;
DROP VIEW IF EXISTS vw_users CASCADE;
CREATE VIEW vw_users AS
        SELECT  t1.Id                              AS user_id,
                t1.FirstName                       AS first_name,
                t1.LastName                        AS last_name,
                t1.FirstName || ' ' || LastName    AS full_name,
                t1.is_rnd                          AS is_rnd,
                t2.email                           AS email,
                t1.UpdatedOn                       AS updated_on,
                t1.CreatedOn                       AS created_on,
                t1.FocusFactor                     AS focus_factor
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

DROP VIEW IF EXISTS vw_releases CASCADE;
CREATE VIEW vw_releases AS
WITH Status AS 
(
    SELECT  Id,
            Title,
            Status                  AS release_status,
            CreatedById             AS created_by_id,
            CAST(UpdatedOn AS DATE) AS updated_on,
            CAST(CreatedOn AS DATE) AS created_on,
            CAST(StartDate AS DATE) AS start_date,
            CAST(EndDate AS DATE)   AS end_date,
            CreatedById,
            UpdatedOn,
            CreatedOn,
            StartDate,
            EndDate
    FROM Releases
)
SELECT  Id                      AS release_id,
        Title                   AS release_title,
        updated_on,
        created_on,
        start_date,
        end_date,
        CASE 
            WHEN start_date > current_date                       THEN 'Planned'
            WHEN current_date BETWEEN start_date AND end_date    THEN 'Active'
            WHEN current_date > end_date                         THEN 'Closed'
        END AS Status,
        CASE 
            WHEN current_date BETWEEN start_date AND end_date    THEN True
            ELSE False
        END AS is_active
FROM Status;


DROP VIEW IF EXISTS vw_tasks CASCADE;
CREATE VIEW vw_tasks AS
SELECT  T1.guid,
        T1.taskid       AS task_id,
        T1.taskownerid  AS task_owner_id,
        T1.userstoryid  AS userstory_id,
        T1.title,
        T1.createdbyid              AS created_by,
        CAST(T1.updatedon AS DATE)  AS updated_on,
        T1.updatedbyid              AS updated_by,
        CAST(T1.createdon AS DATE)  AS created_on,
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
                CreatedById                 AS created_by_id,
                CAST(UpdatedOn AS DATE)     AS updated_on,
                CAST(CreatedOn AS DATE)     AS created_on,
                CAST(StartDate AS DATE)     AS start_date,
                CAST(EndDate AS DATE)       AS end_date
        FROM Sprints
    )
    SELECT  t1.sprint_id                                AS sprint_id,
            t1.sprint_title                             AS sprint_title,
            CASE 
                    WHEN start_date > current_date                      THEN 'Planned'
                    WHEN current_date BETWEEN start_date AND end_date   THEN 'Active'
                    WHEN current_date > end_date                        THEN 'Closed'
            END                                         AS status,
            t1.created_by_id                            AS created_by_id,
            t2.full_name                                AS created_by,
            t1.updated_on                               AS updated_on,
            t1.created_on                               AS created_on,
            t1.start_date                               AS start_date,
            t1.end_date                                 AS end_date,
            CASE 
                WHEN current_date BETWEEN start_date AND end_date THEN True
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

DROP VIEW IF EXISTS vw_inventory_tot CASCADE;
CREATE VIEW vw_inventory_tot AS
SELECT  T1.object_name,
        T1.object_type,
        CASE 
            WHEN L1.table_name IS NULL THEN 'False'
            ELSE 'True'
        END AS is_exist,
        L2.row_count
FROM inventory AS T1
LEFT JOIN LATERAL (     
                    SELECT P1.table_name
                    FROM information_schema.tables AS P1
                    WHERE P1.table_name   = T1.object_name AND table_schema='public'
                ) AS L1 ON TRUE
LEFT JOIN LATERAL (
            SELECT row_count 
            FROM  table_count(T1.object_name) AS t(row_count BIGINT)                            
) AS L2 ON TRUE;

DROP VIEW IF EXISTS vw_tasks_tot CASCADE;
CREATE VIEW vw_tasks_tot AS
SELECT  T1.task_id,
        T1.created_on   AS task_created_on,
        T2.userstory_id,
        T3.sprint_id,
        T3.sprint_title,
        T3.start_date   AS sprint_start_date
FROM vw_tasks       AS T1
JOIN vw_userstories AS T2 ON T2.userstory_id = T1.userstory_id
JOIN vw_sprints     AS T3 ON T3.sprint_id = T2.sprint_id;


DROP VIEW IF EXISTS vw_sprint_userstories CASCADE;
CREATE VIEW vw_sprint_userstories AS
        WITH total AS 
        (
        SELECT  T1.sprint_id,
                T1.sprint_title,
                T1.userstory_id,
                T1.userstory_title,
                L1.total_tasks_usersoty + L2.total_issues_userstory                     AS tasks_total,
                COALESCE(L3.tasks_added,0)                                              AS total_tasks_unplanned,
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
        --tasks opened after sprint started
        LEFT JOIN LATERAL (
                                SELECT  Q1.sprint_id, 
                                        COUNT(Q1.*) AS total_tasks,
                                        L1.tasks_added
                                FROM vw_tasks_tot AS Q1
                                LEFT JOIN LATERAL       (
                                                                SELECT P1.userstory_id,count(P1.*) AS tasks_added
                                                                FROM vw_tasks_tot P1
                                                                WHERE P1.task_created_on > P1.sprint_start_date AND P1.userstory_id = Q1.userstory_id
                                                                GROUP BY 1
                                                        ) AS L1 ON TRUE 
                                WHERE Q1.userstory_id = T1.userstory_id
                                GROUP BY 1,3
                        ) AS L3 ON TRUE
        WHERE T1.is_active
        )
        SELECT  sprint_title,
                userstory_id,           
                userstory_title,        
                case
                     when task_comp_ratio = 100 then 'Done'
                     when total_tasks_progress > 0 or tasks_completed > 0 then 'In Progress'
                     when task_comp_ratio > 0  and task_comp_ratio < 100 and total_tasks_blocked > 0 then 'Blocked'
                     when total_tasks_progress = 0 and tasks_completed = 0 then 'Not Started'
                     else 'err'
                end                     AS "status",
                tasks_total,   
                total_tasks_unplanned,          
                total_tasks_progress,    
                tasks_completed,         
                task_comp_ratio, 
                estimate_total,          
                logged_total,            
                remainig_total          
        FROM total
        ORDER BY        sprint_title,
                        4,
                        task_comp_ratio DESC;

DROP VIEW IF EXISTS vw_sprints_headers CASCADE;
CREATE VIEW vw_sprints_headers AS
SELECT  T1.sprint_id,
        T1.sprint_title,
        T2.full_name                            AS responsible,
        T2.email                                AS responsible_email,
        T1.start_date,
        T1.end_date,
        T1.end_date - T1.start_date +1          AS total_days,
        current_date - T1.start_date + 1        AS day_number, 
        T1.end_date - current_date              AS remaining_days
FROM vw_sprints AS T1
JOIN vw_users   AS T2 ON T2.user_id = T1.created_by_id
WHERE T1.is_active;

DROP VIEW IF EXISTS vw_release_headers CASCADE;
CREATE VIEW vw_release_headers AS
        SELECT  T1.release_id,
                T1.release_title,
                T1.start_date,
                T1.end_date,
                T1.end_date - T1.start_date + 1         AS total_days,
                current_date - T1.start_date + 1        AS day_number, 
                T1.end_date - current_date              AS remaining_days
        FROM vw_releases AS T1
        WHERE T1.is_active;

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

DROP VIEW IF EXISTS vw_capacity CASCADE;
CREATE VIEW vw_capacity AS
        SELECT  T4.sprint_title,
                T2.full_name,
                COALESCE(COUNT(T1.task_id),0)                   AS tot_assigned_tasks,
                COALESCE(SUM(T1.effort_estimate),0)             AS sum_effort_estimate,
                COALESCE(SUM(T1.effort_logged),0)               AS sum_effort_logged,
                COALESCE(SUM(T1.effort_remaining),0)            AS sum_effort_remaining,
                T5.remaining_days                               AS days_remaining,
                T5.remaining_days * 8.5 * T2.focus_factor       AS estimated_remaining_capacity
        FROM vw_tasks           AS T1
        RIGHT JOIN vw_users      AS T2 ON T2.user_id = T1.task_owner_id
        LEFT JOIN vw_userstories     AS T3 ON T3.userstory_id = T1.userstory_id
        LEFT JOIN vw_sprints         AS T4 ON T4.sprint_id = T3.sprint_id
        LEFT JOIN vw_sprints_headers AS T5 ON T5.sprint_id = T4.sprint_id
        WHERE T2.is_rnd
        GROUP BY 1,2,7,8;     


DROP VIEW IF EXISTS vw_capacity_report CASCADE;
CREATE VIEW vw_capacity_report AS
    SELECT  sprint_title                    AS "Sprint Title",
            full_name                       AS "Full Name",
            tot_assigned_tasks              AS "#Assigned Tasks",
            sum_effort_estimate             AS "#Effort Estimate",
            sum_effort_logged               AS "#Effort Spent",
            sum_effort_remaining            AS "#Effort Remaining",
            days_remaining                  AS "Days Remaining", 
            estimated_remaining_capacity    AS "Estimated Remaining Capacity",
            CASE 
                    WHEN sum_effort_remaining > estimated_remaining_capacity    THEN 'Overload' 
                    WHEN sum_effort_estimate = 0                                THEN 'Idle'
                    WHEN estimated_remaining_capacity/sum_effort_estimate > 3   THEN 'Idle'                        
                    ELSE 'Balanced' 
            END                             AS "Capacity Allocation"
    FROM vw_capacity
    ORDER BY 9 DESC ,1,4;

DROP VIEW IF EXISTS vw_sprint_userstories_report CASCADE;
CREATE VIEW vw_sprint_userstories_report AS
SELECT  sprint_title,
        userstory_id            AS "id",
        userstory_title         AS "Userstory Title",
        status                  AS "Status",
        tasks_total             AS "Tasks Total",
        total_tasks_unplanned   AS "Tasks Unplanned",
        total_tasks_progress    AS "Tasks In Progress",
        tasks_completed         AS "Tasks Completed",
        task_comp_ratio || '%'  AS "Tasks Completion Ratio",
        estimate_total          AS "Effort Estimate",
        logged_total            AS "Effort Spent",
        remainig_total          AS "Effort Remaining"
FROM vw_sprint_userstories
ORDER BY        sprint_title,
                4,
                task_comp_ratio DESC;

DROP VIEW IF EXISTS vw_release_summary_report CASCADE;
CREATE VIEW vw_release_summary_report AS
SELECT  "Category",
        "Total",
        "#Completed",
        "%Completed"
FROM    (
            select  'Release Days'              AS "Category",
                    total_days                  AS "Total",
                    day_number                  AS "#Completed",
                    remaining_days              AS "Remaining",
                    1                           AS "Sort",
                    round(day_number*100/total_days) || '%' AS "%Completed"
            from vw_release_headers
            UNION
            --effort
            select  'Release Effort'            AS "Category",
                    total_effort_estimate       AS "Total",
                    total_effort_spent          AS "#Completed",
                    total_effort_remaining      AS "Remaining",
                    2                           AS "Sort",
                    effort_completion_ratio || '%' as "%Completed"
            from vw_release_effort
            UNION
            --userstories
            select      'Userstories'                       AS "Category",
                        count(userstory_id)                 AS "Total",
                        sum(case when "status" = 'Done' then 1 else 0 end)  AS "#Completed",
                        NULL                                AS "Remaining",
                        3                                   AS "Sort",
                        cast(round(cast(sum(case when "status" = 'Done' then 1 else 0 end) as numeric) / cast(count(userstory_id) as numeric) * 100) as text) || '%' AS "%Completed"
            from vw_sprint_userstories
    order by 6
    ) AS T;


DROP VIEW IF EXISTS vw_sprint_summary_report CASCADE;
CREATE VIEW vw_sprint_summary_report AS
SELECT  "sprint_title",
        "Category",
        "Total",
        "#Completed",
        "%Completed"
FROM    (
            --tasks opened after sprint started
            -- with items as
            -- (
            --     select T1.sprint_title, count(T1.*) as total_items,L1.items_added
            --     from vw_tasks_tot as T1
            --     LEFT JOIN LATERAL   (
            --                 select P1.sprint_title,count(P1.*) as items_added
            --                 from vw_tasks_tot P1
            --                 WHERE P1.task_created_on > P1.sprint_start_date and P1.sprint_title=T1.sprint_title
            --                 group by 1
            --     ) AS L1 ON TRUE 
            --     group by 1,3
            -- )
            -- select  sprint_title                AS "sprint_title",
            --         'Tasks Added During Sprint' AS "Category",
            --         total_items                 AS "Total",
            --         items_added                 AS "#Completed",
            --         total_items - items_added   AS "Remaining",
            --         4                           AS "Sort",
            --         round(items_added*100/total_items) || '%' as "%Completed"
            -- from items
            -- UNION
            --days elapsed
            select  sprint_title                AS "sprint_title",
                    'Sprint Days'               AS "Category",
                    total_days                  AS "Total",
                    day_number                  AS "#Completed",
                    remaining_days              AS "Remaining",
                    1                           AS "Sort",
                    round(day_number*100/total_days) || '%' AS "%Completed"
            from vw_sprints_headers
            UNION
            --effort
            select  sprint_title                AS "sprint_title",
                    'Sprint Effort'             AS "Category",
                    total_effort_estimate       AS "Total",
                    total_effort_spent          AS "#Completed",
                    total_effort_remaining      AS "Remaining",
                    2                           AS "Sort",
                    effort_completion_ratio || '%' as "%Completed"
            from vw_sprint_effort
            UNION
            --userstories
            select      sprint_title                 AS "sprint_title",
                        'Userstories'                       AS "Category",
                        count(userstory_id)                           AS "Total",
                        sum(case when "status" = 'Done' then 1 else 0 end)  AS "#Completed",
                        NULL                                AS "Remaining",
                        3                                   AS "Sort",
                        cast(round(cast(sum(case when "status" = 'Done' then 1 else 0 end) as numeric) / cast(count(userstory_id) as numeric) * 100) as text) || '%' AS "%Completed"
            from vw_sprint_userstories 
            group by 1
    order by 6
    ) AS T;
/*
select  sprint_title,
        Blocked,
        Not_Started,
        In_Progress,
        Done
from crosstab
('
    SELECT  sprint_title,
            "status",
            COUNT(id)::INT 
    FROM vw_sprints_sub_tot 
    GROUP BY 1,2 
    ORDER BY 1,2
')
as final(
            sprint_title    TEXT,
             In_Progress  INT,
             NotStarted  INT,
             Done         INT,
             Blocked      INT
);
*/


DROP VIEW IF EXISTS vw_release_userstories_report CASCADE;
CREATE VIEW vw_release_userstories_report AS
SELECT * 
FROM vw_sprint_userstories_report 
ORDER BY CAST(split_part("Tasks Completion Ratio",'%',1) AS INT) DESC;

