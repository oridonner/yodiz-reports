select  T1.id,
        T1.status,
        T1.createdon,
        T1.updatedon,
        T2.MtdCategory
from vw_issues T1
left join lateral
(
    select  id,
        status,
        UpdatedOn,
        CreatedOn,
        case 
            when CreatedOn>=last_month_trunc(current_date) and CreatedOn<last_month(current_date)                          THEN 'opened_last_month'
            when Status='Closed' AND UpdatedOn>=last_month_trunc(current_date) and UpdatedOn<last_month(current_date)    THEN 'closed_last_month'
            when CreatedOn>=date_trunc('month',current_date)                                                             THEN 'opened_current_month'
            when Status='Closed' AND UpdatedOn>=date_trunc('month',current_date)                                       THEN 'closed_current_month'
        end as MtdCategory
    from vw_issues
) T2 ON True;