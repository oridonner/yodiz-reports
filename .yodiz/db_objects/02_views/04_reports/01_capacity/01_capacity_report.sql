DROP VIEW IF EXISTS vw_capacity_report CASCADE;
CREATE VIEW vw_capacity_report AS
    SELECT  sprint_title                    AS "Sprint Title",
            full_name                       AS "Full Name",
            tot_assigned_tasks              AS "#Assigned Tasks",
            sum_effort_estimate             AS "#Effort Estimate",
            sum_effort_logged               AS "#Effort Spent",
            sum_effort_remaining            AS "#Effort Remaining",
            days_remaining                  AS "Days Remaining", 
            estimated_remaining_capacity    AS "Estimated Remaining Capacity",
            CASE 
                    WHEN sum_effort_remaining > estimated_remaining_capacity    THEN 'Overload' 
                    WHEN sum_effort_estimate = 0                                THEN 'Idle'
                    WHEN estimated_remaining_capacity/sum_effort_estimate > 3   THEN 'Idle'                        
                    ELSE 'Balanced' 
            END                             AS "Capacity Allocation"
    FROM vw_capacity
    ORDER BY 9 DESC ,1,4;