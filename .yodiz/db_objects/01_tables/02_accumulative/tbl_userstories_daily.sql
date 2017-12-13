DROP TABLE IF EXISTS userstories_daily CASCADE;
CREATE TABLE userstories_daily 
(
    id                      SERIAL,
    date                    DATE,
    userstory_id            INT,
    userstory_title         TEXT,
    status                  TEXT,
    tasks_total             INT,
    total_tasks_unplanned   INT,
    total_tasks_progress    INT,   
    tasks_completed         INT,        
    task_comp_ratio         REAL, 
    estimate_total          REAL,         
    logged_total            REAL,           
    remaining_total         REAL        
);