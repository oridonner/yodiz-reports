-- Open issues severity pivoted by OpenIssueCategory
DROP VIEW IF EXISTS vw_open_issues_severity;
CREATE VIEW vw_open_issues_severity AS
    SELECT  severity , 
            open , 
            in_progress , 
            approved , 
            blocked 
    FROM crosstab
    ('
        SELECT  severity, 
                open_issue_category, 
                COUNT(issue_id)::int AS ct
        FROM vw_issues
        WHERE is_open
        GROUP BY 1,2 
        ORDER BY 1,2
    ') 
    AS final_results(   
                        severity    TEXT, 
                        approved    INT, 
                        blocked     INT,
                        in_progress INT, 
                        open        INT
                    );