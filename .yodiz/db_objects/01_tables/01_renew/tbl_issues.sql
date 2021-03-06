DROP TABLE IF EXISTS Issues CASCADE;
CREATE TABLE Issues(
    Guid              text,
    Id                int,
    Title             text,
    UserStoryId       int,   -- inserted by code, not from custom api
    CreatedById       int,
    UpdatedOn         timestamp without time zone,
    UpdatedById       int,
    CreatedOn         timestamp without time zone,
    ResponsibleId     int, 
    Status            text,
    Severity          text,
    ReleaseId         int,
    SprintId          int,
    EffortEstimate    real,
    EffortRemaining   real,
    EffortLogged      real
);