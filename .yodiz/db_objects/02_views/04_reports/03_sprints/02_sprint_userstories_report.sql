DROP VIEW IF EXISTS vw_sprint_userstories_report CASCADE;
CREATE VIEW vw_sprint_userstories_report AS
SELECT  sprint_title,
        userstory_id            AS "id",
        userstory_title         AS "Userstory Title",
        status                  AS "Status",
        tasks_total             AS "Tasks Total",
        total_tasks_unplanned   AS "Tasks Unplanned",
        total_tasks_progress    AS "Tasks In Progress",
        tasks_completed         AS "Tasks Completed",
        task_comp_ratio || '%'  AS "Tasks Completion Ratio",
        estimate_total          AS "Effort Estimate",
        logged_total            AS "Effort Spent",
        remaining_total          AS "Effort Remaining"
FROM vw_sprint_userstories
WHERE sprint_is_active
ORDER BY        sprint_title,
                4,
                task_comp_ratio DESC;