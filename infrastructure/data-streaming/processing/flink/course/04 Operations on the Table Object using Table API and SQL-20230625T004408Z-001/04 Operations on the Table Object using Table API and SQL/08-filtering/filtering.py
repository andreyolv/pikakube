from pyflink.table import (
    DataTypes,
    TableEnvironment,
    EnvironmentSettings,
    CsvTableSource
)
from pyflink.table.expressions import col


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

    # Use Table API to calculate the product sales for each day
    # and filter down to just those with sales of $80 or better
    high_sales = tbl.select(tbl.sales_date,
                              tbl.seller_id,
                              tbl.product,
                              (tbl.product_price * tbl.quantity).alias('sales'))\
                        .distinct()\
                        .where(col('sales') >= 80)

    print('\nhigh_sales data')
    print(high_sales.to_pandas())


    # Use SQL to calculate the product sales for each day
    # and filter down to just those with sales of $80 or better
    high_sales2 = tbl_env.sql_query("""
        SELECT * FROM (
            SELECT DISTINCT sales_date, seller_id, product,
                product_price * quantity AS sales
            FROM product_locale_sales) t
        WHERE t.sales >= 80
    """)

    print('\nhigh_sales2 data')
    print(high_sales2.to_pandas())

    # Use table API to select all high sales products (at least $80)
    # for July 1, 2021
    july1_high_sales = tbl.select(tbl.sales_date,
                              tbl.seller_id,
                              tbl.product,
                              (tbl.product_price * tbl.quantity).alias('sales'))\
                        .distinct()\
                        .where("sales >= 80 && sales_date = '2021-07-01'.toDate")

    print('\njuly1_high_sales data')
    print(july1_high_sales.to_pandas())


    # Use SQL to select all high sales products (at least $80)
    # for July 1, 2021
    july1_high_sales2 = tbl_env.sql_query("""
        SELECT * FROM (
            SELECT DISTINCT sales_date, seller_id, product,
                product_price * quantity AS sales
            FROM product_locale_sales) t
        WHERE t.sales >= 80 AND t.sales_date = '2021-07-01'
    """)

    print('\njuly1_high_sales2 data')
    print(july1_high_sales2.to_pandas())


if __name__ == '__main__':
    main()
