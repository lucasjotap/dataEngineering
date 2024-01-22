{{
	config(
		materielized='ephemeral'
		)
}}

SELECT * FROM {{ source('data_lake_raw', 'atomic_events') }}