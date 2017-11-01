-- open mtd , close mtd , open lmtd , close lmtd
DROP VIEW IF EXISTS vw_issues_mtd;
CREATE VIEW vw_issues_mtd AS
SELECT  mtd_category ,
        opened_current_month,
        closed_current_month,
        opened_last_month,
        closed_last_month
FROM crosstab 
('
    WITH 
    categories AS (
        SELECT  issue_id,
                status,
                updated_on,
                created_on,
                CASE 
                    WHEN created_on BETWEEN last_month_trunc(current_date) AND last_month(current_date)                         THEN ''opened_last_month''
                    WHEN status=''Closed'' AND updated_on BETWEEN last_month_trunc(current_date) AND last_month(current_date)    THEN ''closed_last_month''
                    WHEN created_on>=date_trunc(''month'',current_date)                                                         THEN ''opened_current_month''
                    WHEN status=''Closed'' AND updated_on>=date_trunc(''month'',current_date)                                   THEN ''closed_current_month''
                END AS mtd_category
        FROM vw_issues
    )
    SELECT  ''MTD Report'',
            mtd_category,
            COUNT(issue_id)::INT AS Ids
    FROM categories
    WHERE categories IS NOT NULL
    GROUP BY 1,2
    ORDER BY 1,2
') AS final_results(
                        mtd_category            TEXT, 
                        closed_last_month       INT, 
                        opened_last_month       INT, 
                        opened_current_month    INT, 
                        closed_current_month    INT
                    );