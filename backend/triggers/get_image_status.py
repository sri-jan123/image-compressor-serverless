import os
import json
import logging

from datetime import datetime, timedelta

import azure.functions as func

from azure.storage.blob import (
    generate_blob_sas,
    BlobSasPermissions
)

from azure.cosmos import CosmosClient

from app_instance import app

@app.route(
     route="getImageStatus",
     auth_level=func.AuthLevel.ANONYMOUS)

def getImageStatus(req: func.HttpRequest) -> func.HttpResponse:

     try:

         file_name = req.params.get("fileName")

         cosmos_client = CosmosClient.from_connection_string(
             os.environ["CosmosDBConnectionString"]
         )

         database = cosmos_client.get_database_client(
             "ImageDB"
         )

         container = database.get_container_client(
             "ProcessedImages"
         )

         query = """
         SELECT *
         FROM c
         WHERE c.fileName = @fileName
         """

         parameters = [
             {
                 "name": "@fileName",
                 "value": file_name
             }
         ]
         items = list(
             container.query_items(
                 query=query,
                 parameters=parameters,
                 enable_cross_partition_query=True
             )
         )

         return func.HttpResponse(
             body=json.dumps(items),
             mimetype="application/json",
             status_code=200
         )

     except Exception as e:

         logging.exception(str(e))

         return func.HttpResponse(
             str(e),
             status_code=500
         )