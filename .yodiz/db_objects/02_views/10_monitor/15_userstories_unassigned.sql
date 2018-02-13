DROP VIEW IF EXISTS vw_userstories_unassigned CASCADE;
CREATE VIEW vw_userstories_unassigned AS
    SELECT  T1.Id                                       AS userstory_id,
            T1.Title                                    AS userstory_title,
            T1.ReleaseId                                AS release_id,
            T1.SprintId                                 AS sprint_id,
            T2.Title                                    AS sprint_title,            
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
    LEFT JOIN Sprints        T2 ON T2.Id = T1.SprintId
    JOIN vw_releases    T3 ON T3.release_id = T1.ReleaseId
    WHERE T3.is_active AND T1.SprintId  IS NULL;