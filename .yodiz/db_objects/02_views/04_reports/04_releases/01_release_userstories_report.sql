DROP VIEW IF EXISTS vw_release_userstories_report CASCADE;
CREATE VIEW vw_release_userstories_report AS
SELECT * 
FROM vw_sprint_userstories_report 
ORDER BY CAST(split_part("Tasks Completion Ratio",'%',1) AS INT) DESC, "Status" ASC;