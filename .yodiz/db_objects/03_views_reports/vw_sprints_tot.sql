DROP VIEW IF EXISTS vw_sprints_tot CASCADE;
CREATE VIEW vw_sprints_tot AS
select sprint_title,title , value
from (
	select sprint_title,'Total Days' as title , total_days as value , 0 as sort from vw_sprints_headers
		union
	select sprint_title,'Day Number' as title , day_number as value  , 1 as sort from vw_sprints_headers
		union
	select sprint_title,'User Stories' as title , count(1)  as value , 2 as sort from vw_sprints_sub_tot group by 1,2,4
		union
	select sprint_title,'Sprint Effort Estimation' as title , sum("effort estimate") as value  , 3 as sort from vw_sprints_sub_tot group by 1,2,4
		union
	select sprint_title,'Sprint Effort Spent' as title , sum("effort spent") as value  , 4 as sort from vw_sprints_sub_tot group by 1,2,4
		union
	select sprint_title,'Sprint Effort remaining' as title , sum("effort remaining") as value  , 5 as sort from vw_sprints_sub_tot group by 1,2,4
order by 3
) a
;
