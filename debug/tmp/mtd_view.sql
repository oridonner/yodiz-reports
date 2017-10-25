with 
dates as (
    select  id,
            status,
            UpdatedOn,
            CreatedOn,
            last_month_trunc(current_date) AS LastMonthStart,
            date_trunc('month',current_date) AS CurrentMonthStart,
            last_month(current_date) AS LastMonthDate
    from vw_issues
),
categories as (
    select  id,
            status,
            UpdatedOn,
            CreatedOn,
            case 
                when CreatedOn>=LastMonthStart and CreatedOn<LastMonthDate                      THEN 'opened_last_month'
                when Status='Closed' AND UpdatedOn>=LastMonthStart and UpdatedOn<LastMonthDate  THEN 'closed_last_month'
                when CreatedOn>=CurrentMonthStart                                               THEN 'opened_current_month'
                when Status='Closed' AND UpdatedOn>=CurrentMonthStart                           THEN 'closed_current_month'
            end as MtdCategory
    from dates
)
select  count(id) as Ids,
        MtdCategory
from categories
where categories is not null
group by 2
order by 2;

