\i postgres_lib/users_lib/users_tabe.sql

select Severity::text, OpenIssueCategory::text, count(id)::int as ct from vw_open_issues where isopen group by 1,2 order by 1,2;

select * from crosstab('select Severity::text, OpenIssueCategory::text, count(id)::int as ct from vw_open_issues where isopen group by 1,2 order by 1,2') as final_results(Severity TEXT, Approved NUMERIC, Blocked NUMERIC, InProgress NUMERIC, Open NUMERIC);


