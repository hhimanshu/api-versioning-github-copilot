import logging

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from services.api_version import ApiVersion


logger = logging.getLogger(__name__)


def custom_openapi(app: FastAPI):
    def custom_openapi_func():
        try:
            logger.debug("Generating custom OpenAPI schema")
            if app.openapi_schema:
                logger.debug("Returning cached OpenAPI schema")
                return app.openapi_schema

            openapi_schema = get_openapi(
                title="Your API",
                version="1.0.0",
                description="Your API description",
                routes=app.routes,
            )

            logger.debug("Adding version parameter to all endpoints")
            # Define the version parameter once at the components level
            openapi_schema["components"] = openapi_schema.get("components", {})
            openapi_schema["components"]["parameters"] = {
                "ApiVersionHeader": {
                    "name": "x-api-version",
                    "in": "header",
                    "required": True,
                    "schema": {
                        "type": "string",
                        "enum": [v.value for v in ApiVersion],
                        "default": ApiVersion.LATEST.value,
                    },
                    "description": "API Version to use",
                }
            }

            # Reference the parameter in all paths
            for path in openapi_schema["paths"].values():
                for method in path.values():
                    # Remove any existing x-api-version parameters
                    if "parameters" in method:
                        method["parameters"] = [
                            param
                            for param in method["parameters"]
                            if param.get("name", "").lower() != "x-api-version"
                        ]

                    # Add the reference to our component parameter
                    method["parameters"] = [
                        {"$ref": "#/components/parameters/ApiVersionHeader"}
                    ] + (method.get("parameters", []))

            # Modify the servers to include the /api prefix (not needed)
            # openapi_schema["servers"] = [{"url": "/"}]

            app.openapi_schema = openapi_schema

            return app.openapi_schema
        except Exception as e:
            logger.error(f"Error generating OpenAPI schema: {str(e)}")
            raise

    return custom_openapi_func
