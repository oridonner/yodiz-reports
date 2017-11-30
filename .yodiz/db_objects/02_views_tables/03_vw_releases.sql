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
SELECT  Id                      AS release_id,
        Title                   AS release_title,
        Status                  AS release_status,
        CreatedById             AS created_by_id,
        CAST(UpdatedOn AS DATE) AS updated_on,
        CAST(CreatedOn AS DATE) AS created_on,
        CAST(StartDate AS DATE) AS start_date,
        CAST(EndDate AS DATE)   AS end_date,
        CASE 
            WHEN Status = 'Active'     THEN True
            ELSE False
        END AS is_active
FROM Status;
