import duckdb

df = duckdb.read_csv("flights.csv")

duckdb.sql("SELECT * FROM df").show() 