DROP VIEW IF EXISTS vw_userstories CASCADE;
CREATE VIEW vw_userstories AS
    SELECT  T1.Id               AS userstory_id,
            T1.Title            AS userstory_title,
            T1.ReleaseId        AS release_id,
            T2.sprint_id        AS sprint_id,
            T2.sprint_title     AS sprint_title,            
            T1.CreatedById      AS created_by,
            T1.UpdatedOn        AS updated_on,
            T1.UpdatedById      aS updated_by,
            T1.CreatedOn        AS created_on,
            T1.ResponsibleId    AS responsible,
            T1.Status           AS status,
            CASE 
                WHEN T2.Status = 'Active'     THEN True
                ELSE False
            END                 AS is_active,
            T1.EffortEstimate   AS effort_estimate,
            T1.EffortRemaining  AS effort_remaining,
            T1.EffortLogged     AS effort_logged
    FROM UserStories    T1
    JOIN vw_sprints     T2 ON T2.sprint_id = T1.SprintId; 