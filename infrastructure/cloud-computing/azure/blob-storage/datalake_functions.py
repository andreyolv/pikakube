def get_datalake_client(storage_account_name, tenant_id, client_id, client_secret):
    from azure.identity import ClientSecretCredential
    from azure.storage.filedatalake import DataLakeServiceClient

    # Use ClientSecretCredential to authenticate with SPN
    credential = ClientSecretCredential(
                    tenant_id=tenant_id,
                    client_id=client_id,
                    client_secret=client_secret
                )

    # Create a DataLakeServiceClient
    service_client = DataLakeServiceClient(
                        account_url=f"https://{storage_account_name}.dfs.core.windows.net",
                        credential=credential
                    )
    
    return service_client

def get_file_size(container_name, file_path):
    # Get a DataLakeFileClient for the specified file
    file_system_client = service_client.get_file_system_client(container_name)
    file_client = file_system_client.get_file_client(file_path)

    # Get file properties and retrieve file size
    file_properties = file_client.get_file_properties()
    
    return file_properties.size

def generate_relative_directory_list_level(root_path, directory_path, level):
    # Verifique se o root_path está presente no início do directory_path
    if not directory_path.startswith(root_path):
        return "Erro: O root_path não está presente no início do directory_path."
    
    # Remova o root_path do início do directory_path
    relative_path = directory_path.split(root_path, 1)[1].lstrip('/')
    
    # Use split para dividir o caminho do diretório em partes
    list_path = relative_path.split('/')
    
    # Retorne o resultado com base no nível especificado
    list_level = '/'.join(list_path[:level])
    
    return list_level

def generate_absolute_directory_list_level(root_path, directory_path, level):
    # Verifique se o root_path está presente no início do directory_path
    if not directory_path.startswith(root_path):
        return "Erro: O root_path não está presente no início do directory_path."
       
    # Use split para dividir o caminho do diretório em partes
    list_path = directory_path.split('/')
    
    # Retorne o resultado com base no nível especificado
    list_level = '/'.join(list_path[:len(root_path.split('/'))-1+level])
    
    return list_level

def get_directory_size(container_name, directory_path):
    file_system_client = service_client.get_file_system_client(container_name)
    paths = file_system_client.get_paths(directory_path)
    
    total_size = 0
    
    for path in paths:
        file_size = get_file_size(container_name, path)
        
        total_size += file_size
    
    return total_size

def list_subdirectories(container_name, root_path, level_path):
    file_system_client = service_client.get_file_system_client(container_name)
    paths = file_system_client.get_paths(root_path)

    subdirectories = [item.name for item in paths if item.is_directory]

    filtered_list = set(generate_absolute_directory_list_level(root_path, subdirectory, level_path) for subdirectory in subdirectories)

    return sorted(list(filtered_list))

def get_subdirectories_size(container_name, root_path, level_path):
    import pandas as pd

    list_sub = list_subdirectories(container_name, root_path, level_path)
    
    # Inicialize listas para armazenar os resultados
    subdirectory_dict = {}

    for subdirectory in list_sub:
        subdirectory_name = generate_relative_directory_list_level(root_path, subdirectory, level_path)
        subdirectory_size = get_directory_size(container_name, subdirectory)
                
        subdirectory_dict[subdirectory_name] = subdirectory_size
        
    df = pd.DataFrame(list(subdirectory_dict.items()), columns=['Subdirectory', 'Size'])

    return df

##--------------------------------------------
def list_subdirectories_airflow(storage_account_name, tenant_id, client_id, client_secret, container_name, root_path, level_path):
    service_client = get_datalake_client(storage_account_name, tenant_id, client_id, client_secret)

    file_system_client = service_client.get_file_system_client(container_name)
    paths = file_system_client.get_paths(root_path)

    subdirectories = [item.name for item in paths if item.is_directory]

    filtered_list = set(generate_absolute_directory_list_level(root_path, subdirectory, level_path) for subdirectory in subdirectories)

    return sorted(list(filtered_list))

def get_subdirectories_size_airflow(container_name, root_path, sub_path, level_path):
    import pandas as pd
   
    # Inicialize listas para armazenar os resultados
    subdirectory_dict = {}

    subdirectory_name = generate_relative_directory_list_level(root_path, sub_path, level_path)
    subdirectory_size = get_directory_size(container_name, sub_path)
                
    subdirectory_dict[subdirectory_name] = subdirectory_size
        
    df = pd.DataFrame(list(subdirectory_dict.items()), columns=['Subdirectory', 'Size'])

    return df