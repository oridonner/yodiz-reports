DROP VIEW IF EXISTS vw_capacity_unassigned CASCADE;
CREATE VIEW vw_capacity_unassigned AS
    SELECT  T1.full_name
    FROM vw_users AS T1 
    LEFT JOIN LATERAL (
                        SELECT DISTINCT P1.full_name 
                        FROM vw_capacity AS P1
                        WHERE P1.full_name = T1.full_name
                    ) AS L1 ON TRUE
    WHERE T1.is_rnd AND L1.full_name IS NULL;


