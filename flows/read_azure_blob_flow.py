from prefect import flow, task, get_run_logger
from prefect_azure import AzureBlobStorageCredentials
from azure.storage.blob import BlobServiceClient
from prefect.blocks.system import Secret

@task
def read_blob():
    # Specify the container and blob names
    container_name = "container1"
    blob_name = "source_dir/source1.csv"
        
    logger = get_run_logger()
    
    # Load the Azure Blob Storage credentials block
    #credentials = AzureBlobStorageCredentials.load("azure-blob-credentials")

    # Create a BlobServiceClient using the credentials
    #blob_service_client = credentials.get_client()

    # Load the connection string from a Prefect Secret block
    conn_str = Secret.load("azure-conn-string").get()
    blob_service_client = BlobServiceClient.from_connection_string(conn_str)

    # Access the blob
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
    
    # Read and decode the contents
    download_stream = blob_client.download_blob()
    content = download_stream.readall().decode("utf-8")

    # Log each line
    for line in content.splitlines():
        get_run_logger().info(line)

@flow
def azure_blob_flow():
    read_blob()

if __name__ == "__main__":
    azure_blob_flow()