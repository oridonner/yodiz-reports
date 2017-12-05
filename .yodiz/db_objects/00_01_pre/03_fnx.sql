DROP FUNCTION IF EXISTS last_month(timestamp without time zone);
CREATE FUNCTION last_month(timestamp without time zone) RETURNS timestamp without time zone AS $$
    select $1 - interval '1' month
$$ LANGUAGE SQL;

DROP FUNCTION IF EXISTS last_month_trunc(timestamp without time zone);
CREATE FUNCTION last_month_trunc(timestamp without time zone) RETURNS timestamp without time zone AS $$
    select date_trunc('month',last_month($1))
$$ LANGUAGE SQL;

DROP FUNCTION IF EXISTS days_trunc(timestamp without time zone);
CREATE FUNCTION days_trunc(timestamp without time zone) RETURNS interval AS $$
    select date_trunc('day',$1 - date_trunc('month',$1)) + interval '1' day
$$ LANGUAGE SQL;

CREATE OR REPLACE FUNCTION public.table_count(table_name text) 
RETURNS SETOF RECORD
LANGUAGE plpgsql
AS $BODY$
BEGIN
    RETURN QUERY EXECUTE 'select count(*) from ' || table_name;
END
$BODY$;
