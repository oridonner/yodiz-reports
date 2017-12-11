DROP VIEW IF EXISTS vw_sprint_summary_report CASCADE;
CREATE VIEW vw_sprint_summary_report AS
SELECT  "sprint_title",
        "Category",
        "Total",
        "#Completed",
        "%Completed"
FROM    (
            --tasks opened after sprint started
            -- with items as
            -- (
            --     select T1.sprint_title, count(T1.*) as total_items,L1.items_added
            --     from vw_tasks_tot as T1
            --     LEFT JOIN LATERAL   (
            --                 select P1.sprint_title,count(P1.*) as items_added
            --                 from vw_tasks_tot P1
            --                 WHERE P1.task_created_on > P1.sprint_start_date and P1.sprint_title=T1.sprint_title
            --                 group by 1
            --     ) AS L1 ON TRUE 
            --     group by 1,3
            -- )
            -- select  sprint_title                AS "sprint_title",
            --         'Tasks Added During Sprint' AS "Category",
            --         total_items                 AS "Total",
            --         items_added                 AS "#Completed",
            --         total_items - items_added   AS "Remaining",
            --         4                           AS "Sort",
            --         round(items_added*100/total_items) || '%' as "%Completed"
            -- from items
            -- UNION
            --days elapsed
            select  sprint_title                AS "sprint_title",
                    'Sprint Days'               AS "Category",
                    total_days                  AS "Total",
                    day_number                  AS "#Completed",
                    remaining_days              AS "Remaining",
                    1                           AS "Sort",
                    round(day_number*100/total_days) || '%' AS "%Completed"
            from vw_sprints_headers
            UNION
            --effort
            select  sprint_title                AS "sprint_title",
                    'Sprint Effort'             AS "Category",
                    total_effort_estimate       AS "Total",
                    total_effort_spent          AS "#Completed",
                    total_effort_remaining      AS "Remaining",
                    2                           AS "Sort",
                    effort_completion_ratio || '%' as "%Completed"
            from vw_sprint_effort
            UNION
            --userstories
            select      sprint_title                 AS "sprint_title",
                        'Userstories'                       AS "Category",
                        count(userstory_id)                           AS "Total",
                        sum(case when "status" = 'Done' then 1 else 0 end)  AS "#Completed",
                        NULL                                AS "Remaining",
                        3                                   AS "Sort",
                        cast(round(cast(sum(case when "status" = 'Done' then 1 else 0 end) as numeric) / cast(count(userstory_id) as numeric) * 100) as text) || '%' AS "%Completed"
            from vw_sprint_userstories 
            group by 1
            UNION
            --issues
            SELECT      sprint_title            AS "sprint_title",
                        'Issues'                AS "Category",
                        COUNT(issue_id)         AS "Total",
                        sum(case when "status" = 'Done' then 1 else 0 end)  AS "#Completed",
                        COUNT(issue_id) - sum(case when "status" = 'Done' then 1 else 0 end) AS "Remaining",
                        4                       AS "Sort",
                        cast(round(cast(sum(case when "status" = 'Done' then 1 else 0 end) as numeric) / cast(count(issue_id) as numeric) * 100) as text) || '%' AS "%Completed"
            FROM vw_sprint_issues
            group by 1
    order by 6
    ) AS T;

/*
select  sprint_title,
        Blocked,
        Not_Started,
        In_Progress,
        Done
from crosstab
('
    SELECT  sprint_title,
            "status",
            COUNT(id)::INT 
    FROM vw_sprints_sub_tot 
    GROUP BY 1,2 
    ORDER BY 1,2
')
as final(
            sprint_title    TEXT,
             In_Progress  INT,
             NotStarted  INT,
             Done         INT,
             Blocked      INT
);
*/
