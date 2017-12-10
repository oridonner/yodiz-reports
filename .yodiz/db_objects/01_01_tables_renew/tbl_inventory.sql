DROP TABLE IF EXISTS inventory CASCADE;
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
('vw_sprint_userstories','view'),('vw_sprints_headers','view'),('vw_tasks_headers','view'),('vw_sprint_effort','view'),('vw_capacity','view'),
('vw_release_headers','view'),('vw_release_effort','view'),('vw_releases','view'),('vw_userstories_unassigned','view'),
('vw_capacity_report','view'),('vw_sprint_userstories_report','view'),('vw_sprint_summary_report','view'),('vw_capacity_unassigned','view');

