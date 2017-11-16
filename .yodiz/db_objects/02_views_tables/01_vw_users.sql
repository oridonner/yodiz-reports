DROP VIEW IF EXISTS vw_users CASCADE;
CREATE VIEW vw_users AS
        SELECT  t1.Id                              AS user_id,
                t1.FirstName                       AS first_name,
                t1.LastName                        AS last_name,
                t1.FirstName || ' ' || LastName    AS full_name,
                t2.email                           AS email,
                t1.UpdatedOn                       AS updated_on,
                t1.CreatedOn                       AS created_on
        FROM Users              AS t1
        LEFT JOIN Emails        AS t2 ON t2.user_id = t1.Id;
