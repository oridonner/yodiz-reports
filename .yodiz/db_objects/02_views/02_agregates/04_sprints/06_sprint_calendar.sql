DROP VIEW IF EXISTS vw_sprint_calendar CASCADE;
CREATE VIEW vw_sprint_calendar AS
    WITH calendar AS
    (
        SELECT  T1.sprint_id,
                RANK() OVER (PARTITION BY T1.sprint_id ORDER BY L1.date ASC) AS sprint_day,
                T1.total_days,
                L1.date AS sprint_date,
                L1.is_work_day
        FROM vw_sprints_headers AS T1
        LEFT JOIN LATERAL (   
                            SELECT  P1.date,
                                    P1.is_work_day
                            FROM calendar AS P1
                            WHERE P1.date >= T1.start_date AND P1.date <= T1.end_date
        ) AS L1 ON TRUE                   
    )
    SELECT  sprint_id,
            total_days,
            sprint_day,
            is_work_day,
            total_days - sprint_day +1 AS remaining_days,
            sprint_date
    FROM calendar;