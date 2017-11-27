DROP TABLE IF EXISTS inventory;
CREATE TABLE inventory (
    object_name     TEXT,
    object_type     TEXT,
    is_exist        BOOLEAN,
    is_empty        BOOLEAN         
);

INSERT INTO inventory (
            object_name,
            object_type
)
VALUES 
('api_log','table'),('db_log','table'),('issues','table'),('releases','table'),('sprints','table'),('tasks','table'),('userstories','table'),('users','table'),
('vw_users','view'),('vw_issues','view'),('vw_releases','view'),('vw_tasks','view'),('vw_sprints','view'),('vw_userstories','view'),
('vw_sprints_headers','view'),('vw_sprints_sub_tot','view'),('vw_sprints_tot','view'),('vw_tasks_user','view');

