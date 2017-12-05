DROP TABLE IF EXISTS Tasks CASCADE;
CREATE TABLE Tasks(
    Guid              text,
    TaskId            int,
    TaskOwnerId       int,
    UserStoryId       int,  --inserted by code, not custom api
    Title             text,
    CreatedById       int,
    UpdatedOn         timestamp without time zone,
    UpdatedById       int,
    CreatedOn         timestamp without time zone,
    Status            text,
    EffortEstimate    real,
    EffortRemaining   real,
    EffortLogged      real
);