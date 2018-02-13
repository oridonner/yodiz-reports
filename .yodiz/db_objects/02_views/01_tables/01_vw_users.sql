--Update focufactor
UPDATE users SET focusfactor = 0.5 WHERE firstname IN ('Ben','Ofer','Gil','Yuval');
UPDATE users SET focusfactor = 0.75 WHERE firstname NOT IN ('Ben','Ofer','Gil','Yuval');
--Update is_rnd
UPDATE users SET is_rnd = true WHERE id=11;
UPDATE users SET is_rnd = true WHERE id=25;
UPDATE users SET is_rnd = true WHERE id=36;
UPDATE users SET is_rnd = true WHERE id=4;
UPDATE users SET is_rnd = true WHERE id=17;
UPDATE users SET is_rnd = true WHERE id=18;
UPDATE users SET is_rnd = true WHERE id=19;
UPDATE users SET is_rnd = true WHERE id=28;
UPDATE users SET is_rnd = true WHERE id=47;
UPDATE users SET is_rnd = true WHERE id=51;
UPDATE users SET is_rnd = true WHERE id=53;
UPDATE users SET is_rnd = true WHERE id=54;


DROP VIEW IF EXISTS vw_users CASCADE;
CREATE VIEW vw_users AS
        SELECT  t1.Id                              AS user_id,
                t1.FirstName                       AS first_name,
                t1.LastName                        AS last_name,
                t1.FirstName || ' ' || LastName    AS full_name,
                t1.is_rnd                          AS is_rnd,
                t2.email                           AS email,
                t1.UpdatedOn                       AS updated_on,
                t1.CreatedOn                       AS created_on,
                t1.FocusFactor                     AS focus_factor
        FROM Users              AS t1
        LEFT JOIN Emails        AS t2 ON t2.user_id = t1.Id;
