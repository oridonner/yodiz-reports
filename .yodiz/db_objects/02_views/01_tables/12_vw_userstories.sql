DROP VIEW IF EXISTS vw_userstories CASCADE;
CREATE VIEW vw_userstories AS
    SELECT  T1.ReleaseId                                AS release_id,
            T1.SprintId                                 AS sprint_id,
            T2.sprint_title                             AS sprint_title,   
            T2.is_active                                AS sprint_is_active,         
            T1.Id                                       AS userstory_id,
            T1.Title                                    AS userstory_title,
            T1.CreatedById                              AS created_by,
            T1.UpdatedOn                                AS updated_on,
            T1.UpdatedById                              AS updated_by,
            T1.CreatedOn                                AS created_on,
            T1.ResponsibleId                            AS responsible,
            T1.Status                                   AS status,
            T1.EffortEstimate                           AS effort_estimate,
            T1.EffortRemaining                          AS effort_remaining,
            T1.EffortLogged                             AS effort_logged
    FROM UserStories    T1
    JOIN vw_sprints     T2 ON T2.sprint_id = T1.SprintId
    WHERE T2.is_active;
















    /*
select distinct release_id,sprint_id,userstory_id from vw_userstories;
    */