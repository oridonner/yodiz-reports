SELECT MtdCategory ,closed_last_month,opened_current_month,opened_last_month from crosstab 
('
    with 
    categories as (
        select  id,
                status,
                UpdatedOn,
                CreatedOn,
                case 
                    when CreatedOn>=last_month_trunc(current_date) and CreatedOn<last_month(current_date)                          THEN ''opened_last_month''
                    when Status=''Closed'' AND UpdatedOn>=last_month_trunc(current_date) and UpdatedOn<last_month(current_date)    THEN ''closed_last_month''
                    when CreatedOn>=date_trunc(''month'',current_date)                                                             THEN ''opened_current_month''
                    when Status=''Closed'' AND UpdatedOn>=date_trunc(''month'',current_date)                                       THEN ''closed_current_month''
                end as MtdCategory
        from vw_issues
    )
    select  ''MTD Report'',
            MtdCategory,
            count(id)::int as Ids
    from categories
    where categories is not null
    group by 1,2
    order by 1,2',
    
    'select ''opened_last_month'',''closed_last_month'',''opened_current_month'',''closed_current_month'' order by 1'
) 
AS final_results(MtdCategory TEXT, opened_last_month INT, closed_last_month INT, opened_current_month INT, closed_current_month INT);

