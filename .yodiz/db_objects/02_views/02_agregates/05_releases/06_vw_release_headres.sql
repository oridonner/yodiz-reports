DROP VIEW IF EXISTS vw_release_headers CASCADE;
CREATE VIEW vw_release_headers AS
        SELECT  T1.release_id,
                T1.release_title,
                T1.start_date,
                T1.end_date,
                T1.end_date - T1.start_date + 1         AS total_days,
                current_date - T1.start_date + 1        AS day_number, 
                T1.end_date - current_date              AS remaining_days
        FROM vw_releases AS T1
        WHERE T1.is_active;