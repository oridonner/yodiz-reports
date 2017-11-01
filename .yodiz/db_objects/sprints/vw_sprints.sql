DROP VIEW IF EXISTS vw_sprints CASCADE;
CREATE VIEW vw_sprints AS
    WITH Status AS 
    (
        SELECT  Id          AS sprint_id,
                Title       AS sprint_title,
                CASE 
                    WHEN StartDate > current_date                       THEN 'Planned'
                    WHEN current_date BETWEEN StartDate AND EndDate     THEN 'Active'
                    WHEN current_date > EndDate                         THEN 'Closed'
                END                         AS Status,
                CreatedById                 AS created_by,
                CAST(UpdatedOn AS DATE)     AS updated_on,
                CAST(CreatedOn AS DATE)     AS created_on,
                CAST(StartDate AS DATE)     AS start_date,
                CAST(EndDate AS DATE)       AS end_date
        FROM Sprints
    )
    SELECT  *,
            CASE 
                WHEN Status = 'Active'     THEN True
                ELSE False
            END             AS is_active
    FROM Status;
