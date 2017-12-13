DROP VIEW IF EXISTS vw_sprint_issues_report CASCADE;
CREATE VIEW vw_sprint_issues_report AS
SELECT  sprint_title,
        issue_id            AS "Issue Id",
        issue_title         AS "Issue Title",    
        status              AS "Status",
        effort_estimate     AS "Effort Estimate",
        effort_remaining    AS "Effort Remaining",
        effort_spent        AS "Effort Spent",
        is_done,
        effort_completion_ratio || '%' AS "Tasks Completion Ratio"
FROM vw_sprint_issues
ORDER BY    sprint_title,
            4,
            effort_completion_ratio DESC;