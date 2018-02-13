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