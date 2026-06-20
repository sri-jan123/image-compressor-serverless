import os
import uuid
import json
import logging

import azure.functions as func

from azure.storage.blob import BlobServiceClient

from app_instance import app


@app.route(
    route="uploadImage",
    auth_level=func.AuthLevel.ANONYMOUS
)
def uploadImage(req: func.HttpRequest):

    try:

        logging.info(
            "Image upload function triggered."
        )

        image_bytes = req.get_body()

        if not image_bytes:

            return func.HttpResponse(
                "No image received.",
                status_code=400
            )

        filename = req.headers.get(
            "filename",
            "image.jpg"
        )

        unique_filename = (
            f"{uuid.uuid4()}_{filename}"
        )

        blob_service_client = (
            BlobServiceClient
            .from_connection_string(
                os.environ[
                    "AzureWebJobsStorage"
                ]
            )
        )

        blob_client = (
            blob_service_client
            .get_blob_client(
                container="uploads",
                blob=unique_filename
            )
        )

        blob_client.upload_blob(
            image_bytes,
            overwrite=True
        )

        return func.HttpResponse(
            body=json.dumps({
                "fileName":
                unique_filename
            }),
            mimetype="application/json",
            status_code=200
        )

    except Exception as e:

        logging.exception(str(e))

        return func.HttpResponse(
            str(e),
            status_code=500
        )