from fastapi import Request, FastAPI, status
from uvicorn import run
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
import logging

#from .dependencies import get_query_token, get_token_header
from .routers import contents

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(dependencies=[])

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://127.0.0.1:8000",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "HEAD", "OPTIONS", "DELETE", "PUT", "PATCH"],
    allow_headers=[
        "Origin",
        "Content-Type",
        "Accept",
        "Accept-Encoding",
        "Connection",
        "Host",
        "Priority",
        "Referer",
        "Sec-GPC",
        "User-Agent",
        "Access-Control-Allow-Headers",
        "Authorization",
        "Access-Control-Allow-Origin",
        "Set-Cookie"
        ],
    expose_headers=["*"],
)

app.include_router(contents.router)

@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
	exc_str = f'{exc}'.replace('\n', ' ').replace('   ', ' ')
	logging.error(f"{request}: {exc_str}")
	content = {'status_code': 10422, 'message': exc_str, 'data': None}
	return JSONResponse(content=content, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)

if __name__ == '__main__':
    run(
        "app.main:app", 
        host="0.0.0.0", 
        port=int("8085"),  
        reload=True,
        http="h11",
        forwarded_allow_ips="*",
        log_level="debug"
        )