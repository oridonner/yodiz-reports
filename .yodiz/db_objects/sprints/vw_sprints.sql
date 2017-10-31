DROP VIEW IF EXISTS vw_sprints;
CREATE VIEW vw_sprints AS
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
    FROM Sprints
)
SELECT  *,
        CASE 
            WHEN Status = 'Active'     THEN True
            ELSE False
        END AS IsActive
FROM Status;
