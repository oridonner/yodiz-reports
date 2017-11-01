DROP VIEW IF EXISTS vw_users CASCADE;
CREATE VIEW vw_users AS
        SELECT  Id                              AS user_id,
                FirstName                       AS first_name,
                LastName                        AS last_name,
                FirstName || ' ' || LastName    AS full_name,
                UpdatedOn                       AS updated_on,
                CreatedOn                       AS created_on 
        FROM Users;
