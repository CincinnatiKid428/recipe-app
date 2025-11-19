# Custom backend file from ChatGPT to get dev application to save 
# uploads to Azure Storage blob.

from storages.backends.azure_storage import AzureStorage
import os

class MediaStorage(AzureStorage):
    account_name = os.environ.get("AZURE_ACCOUNT_NAME")
    account_key = os.environ.get("AZURE_ACCOUNT_KEY")
    azure_container = os.environ.get("AZURE_CONTAINER", "media")
    expiration_secs = None