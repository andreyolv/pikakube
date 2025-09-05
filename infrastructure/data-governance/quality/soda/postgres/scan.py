from soda.scan import Scan

scan = Scan()
scan.set_data_source_name("my_postgres")

# Add configuration YAML files
scan.add_configuration_yaml_file(file_path="/home/andreyolv/projects/big-data-platform-on-k8s/infrastructure/data-governance/quality/soda/postgres/configuration.yml")

# Add variables
scan.add_variables({"date": "2024-01-28"})

# Add check YAML files 
scan.add_sodacl_yaml_file("/home/andreyolv/projects/big-data-platform-on-k8s/infrastructure/data-governance/quality/soda/postgres/checks.yml")
# scan.add_sodacl_yaml_file("./soda/checks/returned_orders.yml")

# Execute the scan
exit_code = scan.execute()
print(exit_code)

# Set logs to verbose mode, equivalent to CLI -V option
scan.set_verbose(True)

# Print results of scan
print(scan.get_logs_text())