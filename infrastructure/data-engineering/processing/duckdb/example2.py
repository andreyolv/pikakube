import duckdb as dd

con = dd.connect('my_database.db')

con.execute('''
CREATE OR REPLACE TABLE countries (
    country VARCHAR,
    code VARCHAR,
    region VARCHAR,
    sub_region VARCHAR,
    intermediate_region VARCHAR
);
''')

con.execute('''
INSERT INTO countries VALUES
('Australia', 'AUS', 'Oceania', 'Australia and New Zealand', ''),
('India', 'IND', 'Asia', 'Southern Asia', '');
''')

con.sql('SELECT * FROM countries').show()