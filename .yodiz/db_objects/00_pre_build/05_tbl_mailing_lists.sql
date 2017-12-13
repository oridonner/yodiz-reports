DROP TABLE IF EXISTS mailing_lists CASCADE;
CREATE TABLE mailing_lists(
    id          SERIAL,
    environment TEXT,
    report      TEXT,
    to_user_id  INT,
    cc_user_id  INT
);