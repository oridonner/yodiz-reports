--Added fields: IsOpen boolean, SeverityVal int  
DROP VIEW IF EXISTS vw_issues CASCADE;
CREATE VIEW vw_issues as
    SELECT  Guid            ,
            Id              AS issue_id,
            Title           AS issue_title,
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