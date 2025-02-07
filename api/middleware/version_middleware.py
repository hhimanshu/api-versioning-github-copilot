from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response, JSONResponse
from services.api_version import ApiVersion, DeprecatedVersionError


class APIVersionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        try:
            # Extract API version from header
            version_str = request.headers.get("X-API-Version", "").strip().strip('"\'')

            # Set version
            if not version_str:
                version = ApiVersion.LATEST
            else:
                # Check if it's the LATEST version
                if version_str == str(ApiVersion.LATEST):
                    version = ApiVersion.LATEST
                else:
                    # Validate version string
                    if not ApiVersion.is_valid_version(version_str):
                        return JSONResponse(
                            status_code=400,
                            content={
                                "detail": f"Invalid version: {version_str}",
                                "valid_versions": [v.value for v in ApiVersion]
                            }
                        )
                    version = ApiVersion.from_string(version_str)

            try:
                # Set version in request state before validation
                request.state.api_version = version
                # Validate version (may raise DeprecatedVersionError)
                version.validate()
                
                # Process the request
                response = await call_next(request)
                response.headers['X-API-Version'] = str(version)
                return response

            except DeprecatedVersionError as de:
                return JSONResponse(
                    status_code=de.status_code,
                    content={"detail": de.detail}
                )

        except Exception as e:
            return JSONResponse(
                status_code=400,
                content={
                    "detail": str(e),
                    "valid_versions": [str(v) for v in ApiVersion]
                }
            )
