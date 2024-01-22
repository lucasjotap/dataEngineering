{{
  config(
    materielized='ephemeral'
    )
}}

  SELECT 
    user_domain_id, 
    timestamp, 
    previous_timestamp, 
    new_session, 
    SUM(new_session) OVER (
      PARTITION BY user_domain_id 
      ORDER BY 
        timestamp ROWS BETWEEN UNBOUNDED PRECEDING 
        AND CURRENT ROW
    ) AS session_idx 
  FROM 
    {{ ref('new_session') }}