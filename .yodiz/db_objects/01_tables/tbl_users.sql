DROP TABLE IF EXISTS Users CASCADE;
CREATE TABLE Users(
    Guid              text,
    Id                int,
    FirstName         text,
    LastName          text,
    FocusFactor       NUMERIC,
    UpdatedOn         timestamp without time zone,
    CreatedOn         timestamp without time zone
);