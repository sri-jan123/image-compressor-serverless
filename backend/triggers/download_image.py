import os
import json
import logging

from datetime import datetime, timedelta

import azure.functions as func

from azure.storage.blob import (
    generate_blob_sas,
    BlobSasPermissions
)

from function_app import app


@app.route(
    route="downloadImage",
    auth_level=func.AuthLevel.ANONYMOUS
)
def downloadImage(req: func.HttpRequest) -> func.HttpResponse:

    try:

        file_name = req.params.get("fileName")

        if not file_name:

            return func.HttpResponse(
                "fileName parameter missing",
                status_code=400
            )

        account_name = "imgcompressor123"

        account_key = os.environ["StorageAccountKey"]

        sas_token = generate_blob_sas(
            account_name=account_name,
            container_name="compressed-images",
            blob_name=file_name,
            account_key=account_key,
            permission=BlobSasPermissions(read=True),
            expiry=datetime.utcnow() + timedelta(hours=1)
        )

        download_url = (
            f"https://{account_name}.blob.core.windows.net/"
            f"compressed-images/{file_name}?{sas_token}"
        )

        return func.HttpResponse(
            body=json.dumps({
                "downloadUrl": download_url
            }),
            mimetype="application/json",
            status_code=200
        )

    except Exception as e:

        logging.exception(str(e))

        return func.HttpResponse(
            f"Error: {str(e)}",
            status_code=500
        )