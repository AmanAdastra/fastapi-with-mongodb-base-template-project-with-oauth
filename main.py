from fastapi import FastAPI
from routers import user_authentication_router
from fastapi_jwt_auth import AuthJWT
from schemas import common_schema
from fastapi_jwt_auth.exceptions import AuthJWTException
from fastapi import Request
from fastapi.responses import JSONResponse
from http import HTTPStatus
app = FastAPI()



app.include_router(user_authentication_router.router)


@AuthJWT.load_config
def get_config():
    return common_schema.Settings()


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code= HTTPStatus.UNAUTHORIZED,
        content={"detail": exc.message}
    )