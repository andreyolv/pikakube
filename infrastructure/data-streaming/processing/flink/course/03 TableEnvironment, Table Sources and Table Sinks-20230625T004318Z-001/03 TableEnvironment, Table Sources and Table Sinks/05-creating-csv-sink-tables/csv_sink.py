from pyflink.table import (
    DataTypes, TableEnvironment, EnvironmentSettings, 
    CsvTableSource, CsvTableSink, WriteMode
)


def main():
    env_settings = EnvironmentSettings.new_instance()\
                        .in_batch_mode()\
                        .use_blink_planner()\
                        .build()
    tbl_env = TableEnvironment.create(env_settings)

    # all data to one output file
    tbl_env.get_config().get_configuration().set_string("parallelism.default", "1")

    in_field_names = ['seller_id', 'product', 'quantity', 'product_price', 'sales_date']
    in_field_types = [DataTypes.STRING(), DataTypes.STRING(), DataTypes.INT(), DataTypes.DOUBLE(), DataTypes.DATE()]
    source = CsvTableSource(
        './csv-input',
        in_field_names,
        in_field_types,
        ignore_first_line=True
    )
    tbl_env.register_table_source('product_locale_sales', source)

    tbl = tbl_env.from_path('product_locale_sales')

    print('\nProduct Sales Schema')
    tbl.print_schema()

    out_field_names = ['seller_id', 'product', 'quantity', 'product_price', 'sales_date']
    out_field_types = [DataTypes.STRING(), DataTypes.STRING(), DataTypes.INT(), DataTypes.DOUBLE(), DataTypes.DATE()]
    sink = CsvTableSink(
        out_field_names,
        out_field_types,
        './csv-output/revenue.csv',
        num_files=1,
        write_mode=WriteMode.OVERWRITE
    )
    tbl_env.register_table_sink('locale_revenue', sink)

    tbl.insert_into('locale_revenue')

    tbl_env.execute('source-demo')

if __name__ == '__main__':
    main()
