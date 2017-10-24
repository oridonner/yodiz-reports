DROP VIEW IF EXISTS total_open_bugs;

CREATE VIEW total_open_bugs AS 
    SELECT COUNT(Id) AS open_bugs 
    FROM issues 
    WHERE status NOT IN ('Ignored','Closed','Duplicate');