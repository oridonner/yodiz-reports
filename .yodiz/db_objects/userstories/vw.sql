select
    c.title as sprint_title ,
    cast(c.startdate as date) sprint_start_date,
    cast(c.enddate as date) sprint_end_date,
    a.id as userstory_id,
    a.title ,
    a.releaseid ,
    a.sprintid ,
    count(b.taskid) as num_of_tasks,
    count(d.id) as num_of_issues,    
    sum(b.effortestimate) as effort_estimate,
    sum(b.effortremaining) as effort_remaining,
    sum(b.effortlogged) as effort_logged,
    round(  cast(sum(case when b.status != 'done' then 0 else 1 end) as numeric) / cast(count(b.taskid) as numeric) * 100 , 2)|| '%' as task_completion_ratio
from userstories a
    left join vw_tasks b on  a.id = b.userstoryid
    left join sprints c  on  a.sprintid = c.id
    left join vw_issues d on d.userstoryid = a.id
where 1=1
and now() between startdate and enddate
group by c.title ,cast(c.startdate as date) , cast(c.enddate as date) , a.id , a.title , a.releaseid , a.sprintid
having count(b.taskid) > 0
--order by c.title , a.id desc
order by c.title , round(  cast(sum(case when b.status != 'done' then 0 else 1 end) as numeric) / cast(count(b.taskid) as numeric) * 100 , 2) desc;