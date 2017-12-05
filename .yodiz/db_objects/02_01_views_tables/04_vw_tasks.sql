DROP VIEW IF EXISTS vw_tasks CASCADE;
CREATE VIEW vw_tasks AS
SELECT  T1.guid,
        T1.taskid       AS task_id,
        T1.taskownerid  AS task_owner_id,
        T1.userstoryid  AS userstory_id,
        T1.title,
        T1.createdbyid              AS created_by,
        CAST(T1.updatedon AS DATE)  AS updated_on,
        T1.updatedbyid              AS updated_by,
        CAST(T1.createdon AS DATE)  AS created_on,
        CASE
            WHEN T1.status ~~ '%10%'::text THEN 'new'::text
            WHEN T1.status ~~ '%20%'::text THEN 'in progress'::text
            WHEN T1.status ~~ '%30%'::text THEN 'done'::text
            WHEN T1.status ~~ '%40%'::text THEN 'blocked'::text
            ELSE 'unknown'::text
        END AS status,
        T1.effortestimate   AS effort_estimate,
        T1.effortremaining  AS effort_remaining,
        T1.effortlogged     AS effort_logged
   FROM tasks AS T1;