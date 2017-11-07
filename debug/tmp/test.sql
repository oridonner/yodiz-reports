merge into temp.sprints target
using (select * from extr.sprints) as source
on target




select t1.id,t1.updatedon,t2.updatedon
from temp.sprints t1
join extr.sprints t2 on t2.id = t1.id
where t2.updatedon<>t1.updatedon;
