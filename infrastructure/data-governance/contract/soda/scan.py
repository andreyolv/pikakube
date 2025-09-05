from soda.contracts.data_contract_translator import DataContractTranslator
from soda.scan import Scan
import logging

# Read your data contract file as a Python str
with open("contract.yml") as f:
    data_contract_yaml_str: str = f.read()

# Translate the data contract into SodaCL
data_contract_parser = DataContractTranslator()
sodacl_yaml_str = data_contract_parser.translate_data_contract_yaml_str(data_contract_yaml_str)

# Logging or saving the SodaCL YAMl file will help with debugging potential scan execution issues
logging.debug(sodacl_yaml_str)

# Execute the contract SodaCL in a scan
scan = Scan()
scan.set_data_source_name("my_postgres")
scan.add_configuration_yaml_file(file_path="/home/andreyolv/projects/big-data-platform-on-k8s/infrastructure/data-governance/contract/configuration.yml")
scan.add_sodacl_yaml_str(sodacl_yaml_str)
scan.execute()
scan.assert_all_checks_pass()