-- open mtd , close mtd , open lmtd , close lmtd
DROP VIEW IF EXISTS vw_issues_mtd;
CREATE VIEW vw_issues_mtd AS
SELECT  MtdCategory ,
        opened_current_month,
        closed_current_month,
        opened_last_month,
        closed_last_month
FROM crosstab 
('
    WITH 
    categories AS (
        SELECT  Id,
                Status,
                UpdatedOn,
                CreatedOn,
                CASE 
                    WHEN CreatedOn BETWEEN last_month_trunc(current_date) AND last_month(current_date)                          THEN ''opened_last_month''
                    WHEN Status=''Closed'' AND UpdatedOn BETWEEN last_month_trunc(current_date) AND last_month(current_date)    THEN ''closed_last_month''
                    WHEN CreatedOn>=date_trunc(''month'',current_date)                                                          THEN ''opened_current_month''
                    WHEN Status=''Closed'' AND UpdatedOn>=date_trunc(''month'',current_date)                                    THEN ''closed_current_month''
                END AS MtdCategory
        FROM vw_issues
    )
    SELECT  ''MTD Report'',
            MtdCategory,
            COUNT(Id)::INT AS Ids
    FROM categories
    WHERE categories IS NOT NULL
    GROUP BY 1,2
    ORDER BY 1,2
') AS final_results(
                        MtdCategory             TEXT, 
                        closed_last_month       INT, 
                        opened_last_month       INT, 
                        opened_current_month    INT, 
                        closed_current_month    INT
                    );