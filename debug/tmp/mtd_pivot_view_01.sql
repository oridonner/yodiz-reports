SELECT MtdCategory ,closed_last_month,opened_current_month,opened_last_month
from crosstab ('
with 
dates as (
    select  id,
            status,
            UpdatedOn,
            CreatedOn,
            last_month_trunc(current_date) AS LastMonthStart,
            date_trunc(''month'',current_date) AS CurrentMonthStart,
            last_month(current_date) AS LastMonthDate
    from vw_issues
),
categories as (
    select  id,
            status,
            UpdatedOn,
            CreatedOn,
            case 
                when CreatedOn>=LastMonthStart and CreatedOn<LastMonthDate                          THEN ''opened_last_month''
                when Status=''Closed'' AND UpdatedOn>=LastMonthStart and UpdatedOn<LastMonthDate    THEN ''closed_last_month''
                when CreatedOn>=CurrentMonthStart                                                   THEN ''opened_current_month''
                when Status=''Closed'' AND UpdatedOn>=CurrentMonthStart                             THEN ''closed_current_month''
            end as MtdCategory
    from dates
)
select  ''MTD Report'',
        MtdCategory,
        count(id)::int as Ids
from categories
where categories is not null
group by 1,2
order by 1,2')
AS final_results(MtdCategory TEXT, closed_last_month INT, opened_current_month INT, opened_last_month INT);


