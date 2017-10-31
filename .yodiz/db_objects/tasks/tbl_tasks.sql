DROP TABLE IF EXISTS Tasks CASCADE;
CREATE TABLE Tasks(
    Guid              text,
    TaskId            int,
    UserStoryId       int,
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