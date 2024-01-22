{{
	config(
		materielized='table'
		)
}}

SELECT * FROM {{ source('data_lake_raw', 'atomic_events') }}