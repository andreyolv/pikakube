from pyflink.table import EnvironmentSettings, TableEnvironment, DataTypes


def main():
    settings = EnvironmentSettings.new_instance()\
                  .in_batch_mode()\
                  .use_blink_planner()\
                  .build()
    tbl_env = TableEnvironment.create(settings)

    products = [
        ('Toothbrush',   3.99),
        ('Dental Floss', 1.99),
        ('Toothpaste',   4.99)
    ]

    tbl1 = tbl_env.from_elements(products)
    print('\ntbl1 schema')
    tbl1.print_schema()

    print('\ntbl1 data')
    print(tbl1.to_pandas())

    col_names = ['product', 'price']
    tbl2 = tbl_env.from_elements(products, col_names)
    print('\ntbl2 schema')
    tbl2.print_schema()

    print('\ntbl2 data')
    print(tbl2.to_pandas())

    schema = DataTypes.ROW([
        DataTypes.FIELD('product', DataTypes.STRING()),
        DataTypes.FIELD('price', DataTypes.DOUBLE())
    ])
    tbl3 = tbl_env.from_elements(products, schema)
    print('\ntbl3 schema')
    tbl3.print_schema()

    print('\ntbl3 data')
    print(tbl3.to_pandas())



if __name__ == '__main__':
    main()
