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
