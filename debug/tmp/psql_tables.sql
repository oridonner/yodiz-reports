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

DROP TABLE IF EXISTS Issues;
CREATE TABLE Issues(
    Guid              text,
    Id                int,
    Title             text,
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

DROP TABLE IF EXISTS Severity;
CREATE TABLE Severity(
    Severity          text,
    Value              int
);

INSERT INTO Severity VALUES 
            ('Blocker',1),
            ('Critical',2),
            ('Major',3),
            ('Normal',4),
            ('Minor',5),
            ('Not in Use',6);

DROP TABLE IF EXISTS Users;
CREATE TABLE Users(
    Id                int,
    FirstName         text,
    LastName          text,
    UpdatedOn         timestamp without time zone,
    CreatedOn         timestamp without time zone
);