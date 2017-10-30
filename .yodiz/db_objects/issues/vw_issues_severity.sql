-- Open issues severity pivoted by OpenIssueCategory
DROP VIEW IF EXISTS vw_open_issues_severity;
CREATE VIEW vw_open_issues_severity AS
    SELECT  Severity , 
            Open , 
            InProgress , 
            Approved , 
            Blocked 
    FROM crosstab
    ('
        SELECT  Severity, 
                OpenIssueCategory, 
                COUNT(Id)::int AS ct
        FROM vw_issues
        WHERE IsOpen
        GROUP BY 1,2 
        ORDER BY 1,2
    ') 
    AS final_results(   
                        Severity    TEXT, 
                        Approved    INT, 
                        Blocked     INT,
                        InProgress  INT, 
                        Open INT
                    );