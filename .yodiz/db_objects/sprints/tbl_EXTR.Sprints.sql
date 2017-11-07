DROP TABLE IF EXISTS EXTR.Sprints CASCADE;
CREATE TABLE EXTR.Sprints(
    Id                int,
    Title             text,
    CreatedById       int,
    UpdatedOn         timestamp without time zone,
    CreatedOn         timestamp without time zone,
    Status            text,
    StartDate         timestamp without time zone,
    EndDate           timestamp without time zone    
);