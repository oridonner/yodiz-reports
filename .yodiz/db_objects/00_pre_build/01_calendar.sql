DROP TABLE IF EXISTS calendar CASCADE;
CREATE TABLE calendar (
  date DATE NOT NULL PRIMARY KEY,
  year SMALLINT NOT NULL, -- 2012 to 2038
  month SMALLINT NOT NULL, -- 1 to 12
  day SMALLINT NOT NULL, -- 1 to 31
  quarter SMALLINT NOT NULL, -- 1 to 4
  is_work_day BOOLEAN NOT NULL DEFAULT TRUE,
  day_of_week SMALLINT NOT NULL, -- 1 () to 7 ()
  day_of_year SMALLINT NOT NULL, -- 1 to 366
  week_of_year SMALLINT NOT NULL, -- 1 to 53
  CONSTRAINT con_month CHECK (month >= 1 AND month <= 31),
  CONSTRAINT con_day_of_year CHECK (day_of_year >= 1 AND day_of_year <= 366), -- 366 allows for leap years
  CONSTRAINT con_week_of_year CHECK (week_of_year >= 1 AND week_of_year <= 53)
);

INSERT INTO calendar (date, year, month, day, quarter, day_of_week, day_of_year, week_of_year)
(SELECT ts, 
  EXTRACT(YEAR FROM ts),
  EXTRACT(MONTH FROM ts),
  EXTRACT(DAY FROM ts),
  EXTRACT(QUARTER FROM ts),
  EXTRACT(DOW FROM ts) +1,
  EXTRACT(DOY FROM ts),
  EXTRACT(WEEK FROM ts)
  FROM generate_series('2012-01-01'::timestamp, '2038-01-01', '1day'::interval) AS t(ts));

UPDATE calendar SET is_work_day = False WHERE day_of_week = 6 OR day_of_week = 7;