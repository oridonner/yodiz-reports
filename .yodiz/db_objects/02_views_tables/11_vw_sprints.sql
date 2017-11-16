DROP VIEW IF EXISTS vw_sprints CASCADE;
CREATE VIEW vw_sprints AS
    WITH status AS 
    (
        SELECT  Id                          AS sprint_id,
                Title                       AS sprint_title,
                CASE 
                    WHEN StartDate > current_date                       THEN 'Planned'
                    WHEN current_date BETWEEN StartDate AND EndDate     THEN 'Active'
                    WHEN current_date > EndDate                         THEN 'Closed'
                END                         AS status,
                CreatedById                 AS created_by_id,
                CAST(UpdatedOn AS DATE)     AS updated_on,
                CAST(CreatedOn AS DATE)     AS created_on,
                CAST(StartDate AS DATE)     AS start_date,
                CAST(EndDate AS DATE)       AS end_date
        FROM Sprints
    )
    SELECT  t1.sprint_id                                AS sprint_id,
            t1.sprint_title                             AS sprint_title,
            t1.status                                   AS status,
            t1.created_by_id                            AS created_by_id,
            t2.full_name                                AS created_by,
            t1.updated_on                               AS updated_on,
            t1.created_on                               AS created_on,
            t1.start_date                               AS start_date,
            t1.end_date                                 AS end_date,
            CASE 
                WHEN Status = 'Active'     THEN True
                ELSE False
            END                                         AS is_active
    FROM status     AS t1
    JOIN vw_users   AS t2 on t2.user_id = t1.created_by_id;
