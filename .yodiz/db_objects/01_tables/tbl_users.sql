DROP TABLE IF EXISTS Users;
CREATE TABLE Users(
    Guid              text,
    Id                int,
    FirstName         text,
    LastName          text,
    UpdatedOn         timestamp without time zone,
    CreatedOn         timestamp without time zone
);