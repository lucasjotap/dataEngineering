{{
	config(
		materielized='ephemeral'
		)
}}

  SELECT 
    user_domain_id, 
    timestamp, 
    previous_timestamp, 
    CASE WHEN date_diff(
      'minute', previous_timestamp, timestamp
    ) >= 30 THEN 1 ELSE 0 END AS new_session 
  FROM 
      {{ ref('previous_timestamp') }}