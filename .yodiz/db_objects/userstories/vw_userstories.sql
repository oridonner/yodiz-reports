DROP VIEW IF EXISTS vw_userstories;
CREATE VIEW vw_userstories AS
SELECT  T1.Id              ,
        T1.Title           ,
        T1.CreatedById     ,
        T1.UpdatedOn       ,
        T1.UpdatedById     ,
        T1.CreatedOn       ,
        T1.ResponsibleId   ,
        T1.Status          ,
        T1.ReleaseId       ,
        T1.SprintId        ,
        T2.Status AS SprintStatus,
        CASE 
            WHEN T2.Status = 'Active'     THEN True
            ELSE False
        END AS IsActive,
        T1.EffortEstimate  ,
        T1.EffortRemaining ,
        T1.EffortLogged 
FROM UserStories    T1
JOIN Sprints         T2 ON T2.Id = T1.SprintId; 