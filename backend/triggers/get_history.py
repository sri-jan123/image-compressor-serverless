import os
import json
import logging

import azure.functions as func

from azure.cosmos import CosmosClient

from function_app import app


@app.route(
    route="getHistory",
    auth_level=func.AuthLevel.ANONYMOUS
)
def getHistory(req: func.HttpRequest):

    try:

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

        query = """
        SELECT TOP 1 *
        FROM c
        ORDER BY c.timestamp DESC
        """

        items = list(

            container.query_items(

                query=query,

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