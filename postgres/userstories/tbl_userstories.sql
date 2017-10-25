DROP TABLE IF EXISTS UserStories;
CREATE TABLE UserStories(
    Guid              text,
    Id                int,
    Title             text,
    CreatedById       int,
    UpdatedOn         timestamp without time zone,
    UpdatedById       int,
    CreatedOn         timestamp without time zone,
    ResponsibleId     int, 
    Status            text,
    ReleaseId         int,
    SprintId          int,
    EffortEstimate    real,
    EffortRemaining   real,
    EffortLogged      real
);