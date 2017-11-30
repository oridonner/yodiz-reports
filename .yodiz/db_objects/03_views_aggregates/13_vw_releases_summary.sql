SELECT  T1.*,
        L1.*
FROM vw_releases_headers AS T1
LEFT JOIN LATERAL ( 
                    SELECT  "Category",
                            SUM("Total") AS "Total",
                            SUM("#Completed") AS "#Completed"

                    FROM vw_sprint_summary_report
                    GROUP BY 1
                    ) AS L1 ON TRUE;
