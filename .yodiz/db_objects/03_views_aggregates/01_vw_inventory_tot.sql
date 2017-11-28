DROP VIEW IF EXISTS vw_inventory_tot CASCADE;
CREATE VIEW vw_inventory_tot AS
SELECT  T1.object_name,
        T1.object_type,
        CASE 
            WHEN L1.table_name IS NULL THEN 'False'
            ELSE 'True'
        END AS is_exist,
        L2.row_count
FROM inventory AS T1
LEFT JOIN LATERAL (     
                    SELECT P1.table_name
                    FROM information_schema.tables AS P1
                    WHERE P1.table_name   = T1.object_name AND table_schema='public'
                ) AS L1 ON TRUE
LEFT JOIN LATERAL (
            SELECT row_count 
            FROM  table_count(T1.object_name) AS t(row_count BIGINT)                            
) AS L2 ON TRUE;