CREATE OR REPLACE FUNCTION html_table(query text)
  RETURNS SETOF text AS
$BODY$
declare
    rec record;
    header boolean := true;
begin
    return next '<html><head><style>h1 {color: green;text-align: center;}label {color: darkgreen;}table {border-collapse: collapse;width: 100%;}th {text-align: left;padding: 8px;background-color:cornflowerblue;color:white;}.tdErr {color:red;}.tdOk {color:green;}</style></head><body><h1></h1><table>';
    for rec in
        execute format($q$
            select row_to_json(q) json_row
            from (%s) q
            $q$, query)
    loop
        if header then
            return query select
                format ('<tr><th>%s</th></tr>', string_agg(key, '</th><th>'))
            from json_each(rec.json_row);
            header := false;
        end if;
        return query select
            format ('<tr><td>%s</td></tr>', string_agg(value, '</td><td>'))
        from json_each_text(rec.json_row);
    end loop;
    return next '</table></body></html>';
end $BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100
  ROWS 1000;
ALTER FUNCTION html_table(text)
  OWNER TO postgres;

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
