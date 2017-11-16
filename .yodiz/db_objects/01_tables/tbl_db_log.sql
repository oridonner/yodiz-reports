DROP TABLE IF EXISTS db_log CASCADE;
CREATE TABLE db_log(
    db_guid         uuid NOT NULL DEFAULT uuid_generate_v1(),
    transact_guid   uuid,
    table_name      TEXT,
    rows_inserted   INT,
    time_stamp      timestamp without time zone
);