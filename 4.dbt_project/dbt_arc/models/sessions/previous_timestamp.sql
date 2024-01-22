{{
	config(
		materielized='ephemeral'
		)
}}

SELECT 
    user_domain_id, 
    date_parse(
      event_timestamp, '%Y-%m-%d %h:%i:%s.%f'
    ) as timestamp, 
    LAG(
      date_parse(
        event_timestamp, '%Y-%m-%d %h:%i:%s.%f'
      ), 
      1
    ) OVER (
      PARTITION BY user_domain_id 
      ORDER BY 
        event_timestamp
    ) AS previous_timestamp 
  FROM 
    {{ ref('stg__atomic_events') }}