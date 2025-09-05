{{ config(materialized='table')}}

SELECT * FROM {{ source('mysql_raw', 'customers')}}