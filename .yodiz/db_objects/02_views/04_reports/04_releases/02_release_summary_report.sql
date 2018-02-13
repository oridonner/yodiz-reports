DROP VIEW IF EXISTS vw_release_summary_report CASCADE;
CREATE VIEW vw_release_summary_report AS
SELECT  "Category",
        "Total",
        "#Completed",
        "%Completed"
FROM    (
            select  'Release Days'              AS "Category",
                    total_days                  AS "Total",
                    day_number                  AS "#Completed",
                    remaining_days              AS "Remaining",
                    1                           AS "Sort",
                    round(day_number*100/total_days) || '%' AS "%Completed"
            from vw_release_headers
            UNION
            --effort
            select  'Release Effort'            AS "Category",
                    total_effort_estimate       AS "Total",
                    total_effort_spent          AS "#Completed",
                    total_effort_remaining      AS "Remaining",
                    2                           AS "Sort",
                    effort_completion_ratio || '%' as "%Completed"
            from vw_release_effort
            UNION
            --userstories
            select      'Userstories'                       AS "Category",
                        count(userstory_id)                 AS "Total",
                        sum(case when "status" = 'Done' then 1 else 0 end)  AS "#Completed",
                        NULL                                AS "Remaining",
                        3                                   AS "Sort",
                        cast(round(cast(sum(case when "status" = 'Done' then 1 else 0 end) as numeric) / cast(count(userstory_id) as numeric) * 100) as text) || '%' AS "%Completed"
            from vw_sprint_userstories
    order by 6
    ) AS T;
