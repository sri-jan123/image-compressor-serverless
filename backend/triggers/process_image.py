import os
import uuid
import logging

from io import BytesIO
from datetime import datetime

import azure.functions as func

from PIL import Image

from azure.cosmos import CosmosClient

from azure.storage.blob import (
    BlobServiceClient
)

from app_instance import app


@app.blob_trigger(
    arg_name="myblob",
    path="uploads/{name}",
    connection="AzureWebJobsStorage"
)
def processImage(myblob: func.InputStream):

    try:

        logging.info(
            f"Processing {myblob.name}"
        )

        image_bytes = myblob.read()

        image = Image.open(
            BytesIO(image_bytes)
        )

        image.thumbnail((1200, 1200))

        if image.mode in (
            "RGBA",
            "P"
        ):

            image = image.convert(
                "RGB"
            )

        output_stream = BytesIO()

        image.save(
            output_stream,
            format="JPEG",
            quality=60,
            optimize=True
        )

        compressed_bytes = (
            output_stream.getvalue()
        )

        blob_service_client = (
            BlobServiceClient
            .from_connection_string(
                os.environ[
                    "AzureWebJobsStorage"
                ]
            )
        )

        filename = os.path.basename(
            myblob.name
        )

        compressed_blob_client = (
            blob_service_client
            .get_blob_client(
                container="compressed-images",
                blob=filename
            )
        )

        compressed_blob_client.upload_blob(
            compressed_bytes,
            overwrite=True
        )

        original_size_kb = round(
            len(image_bytes) / 1024,
            2
        )

        compressed_size_kb = round(
            len(compressed_bytes)
            / 1024,
            2
        )

        compression_percentage = round(
            (
                (
                    original_size_kb
                    -
                    compressed_size_kb
                )
                /
                original_size_kb
            )
            *
            100,
            2
        )

        document = {

            "id":
            str(uuid.uuid4()),

            "fileName":
            filename,

            "originalSizeKB":
            original_size_kb,

            "compressedSizeKB":
            compressed_size_kb,

            "compressionPercentage":
            compression_percentage,

            "status":
            "Success",

            "timestamp":
            datetime.utcnow()
            .isoformat()
        }

        cosmos_client = (
            CosmosClient
            .from_connection_string(
                os.environ[
                    "CosmosDBConnectionString"
                ]
            )
        )

        database = (
            cosmos_client
            .get_database_client(
                "ImageDB"
            )
        )

        container = (
            database
            .get_container_client(
                "ProcessedImages"
            )
        )

        container.create_item(
            document
        )

        logging.info(
            "Metadata stored."
        )

    except Exception as e:

        logging.exception(
            str(e)
        )