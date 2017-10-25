DROP TABLE IF EXISTS Users;
CREATE TABLE Users(
    Id                int,
    FirstName         text,
    LastName          text,
    UpdatedOn         timestamp without time zone,
    CreatedOn         timestamp without time zone
);