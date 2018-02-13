DROP VIEW IF EXISTS vw_sprint_burndown CASCADE;
CREATE VIEW vw_sprint_burndown AS
        SELECT  T1.sprint_id,
                to_char(T1.sprint_date, 'DD/MM') as sprint_date ,
                T1.is_work_day,
                T1.sprint_day,
                T1.remaining_days,
                ROUND(CAST(T3.remaining_total AS NUMERIC),0)              AS remaining_effort,
                ROUND((T2.total_effort_estimate/T1.total_days) * T1.remaining_days,0) as trend_line
        FROM vw_sprint_calendar         AS T1
        LEFT JOIN vw_sprint_effort           AS T2 ON T2.sprint_id = T1.sprint_id
        LEFT JOIN vw_sprints_daily           AS T3 ON T3.sprint_id = T1.sprint_id AND T3.date = T1.sprint_date;