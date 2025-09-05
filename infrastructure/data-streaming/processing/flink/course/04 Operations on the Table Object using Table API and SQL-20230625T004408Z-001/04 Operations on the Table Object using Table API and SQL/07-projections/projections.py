from pyflink.table import (
    DataTypes, TableEnvironment, EnvironmentSettings, 
    CsvTableSource
)


def main():
    env_settings = EnvironmentSettings.new_instance()\
                        .in_batch_mode()\
                        .use_blink_planner()\
                        .build()
    tbl_env = TableEnvironment.create(env_settings)

    field_names = ['seller_id', 'product', 'quantity', 'product_price', 'sales_date']
    field_types = [DataTypes.STRING(), DataTypes.STRING(), DataTypes.INT(), DataTypes.DOUBLE(), DataTypes.DATE()]
    source = CsvTableSource(
        './csv-input',
        field_names,
        field_types,
        ignore_first_line=True
    )
    tbl_env.register_table_source('product_locale_sales', source)

    tbl = tbl_env.from_path('product_locale_sales')

    # important to note that operations will be parallelized over
    # task slots across system cores so output will appear randomly
    # ordered and differ from run to run

    # Use Table API to select the product and product_price aliased as price
    redundant_prices = tbl.select(tbl.product,
                                  tbl.product_price.alias('price'))

    print('\nredundant_prices data')
    print(redundant_prices.to_pandas())


    # Use SQL to select the product and product_price aliased as price
    redundant_prices2 = tbl_env.sql_query("""
        SELECT product, product_price AS price
        FROM product_locale_sales
    """)
    print('\nredundant_prices2 data')
    print(redundant_prices2.to_pandas())


    # Use Table API to select the product and product_price aliased as price
    # trimmed down to distinct results
    distinct_prices = tbl.select(tbl.product,
                                tbl.product_price.alias('price'))\
                          .distinct()
    print('\ndistinct_prices data')
    print(distinct_prices.to_pandas())


    # Use SQL to select the product and product_price aliased as price
    # trimmed down to distinct results
    distinct_prices2 = tbl_env.sql_query("""
        SELECT DISTINCT product, product_price AS price
        FROM product_locale_sales
    """)
    print('\ndistinct_prices2 data')
    print(distinct_prices2.to_pandas())


    # Use Table API to calculate the product sales for each day
    product_sales = tbl.select(tbl.sales_date,
                              tbl.seller_id,
                              tbl.product,
                              (tbl.product_price * tbl.quantity).alias('sales'))\
                        .distinct()

    print('\nproduct_sales schema')
    product_sales.print_schema()

    print('\nproduct_sales data')
    print(product_sales.to_pandas())


    # Use SQL to calculate the product sales for each day
    product_sales2 = tbl_env.sql_query("""
        SELECT DISTINCT sales_date, seller_id, product,
            product_price * quantity AS sales
        FROM product_locale_sales
    """)

    print('\nproduct_sales2 schema')
    product_sales2.print_schema()

    print('\nproduct_sales2 data')
    print(product_sales2.to_pandas())


if __name__ == '__main__':
    main()
