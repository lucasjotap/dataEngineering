{{
  config(
    materielized='table'
    )
}}

SELECT 
  user_domain_id || CAST(session_idx AS VARCHAR) AS session_id, 
  * 
FROM 
  {{ ref('new_session') }}