DROP TABLE IF EXISTS api_log CASCADE;
CREATE TABLE api_log(
    api_guid        uuid NOT NULL DEFAULT uuid_generate_v1(),
    transact_guid   uuid,
    http_req        TEXT,
    response_code   INT,
    time_stamp      timestamp without time zone
);