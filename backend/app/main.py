import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from .config import get_settings
from .routes import auth, events

settings = get_settings()

is_debug = False if settings.ENV != 'development' else True
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info('✅ Application started')
    yield
    logger.info('✅ Application stopped')


app = FastAPI(
    title='tasker',
    version='1.0.0',
    docs_url='/api/docs' if settings.ENV == 'development' else None,
    redoc_url='/api/redoc' if settings.ENV == 'development' else None,
    openapi_url='/api/openapi.json',
    lifespan=lifespan,
)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    from fastapi import HTTPException

    if isinstance(exc, HTTPException):
        if isinstance(exc.detail, dict):
            return JSONResponse(
                status_code=exc.status_code,
                content=exc.detail,
            )
        return JSONResponse(
            status_code=exc.status_code,
            content={'detail': exc.detail},
        )

    logger.error(f'Unhandled error: {exc}', exc_info=True)
    return JSONResponse(
        status_code=500,
        content={'detail': 'Внутренняя ошибка сервера'},
    )


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS.split(','),
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
    expose_headers=['Set-Cookie'],
)

app.include_router(auth.router, prefix='/api')
app.include_router(events.router, prefix='/api')


@app.get('/api/health')
async def health():
    return {'status': 'ok'}
