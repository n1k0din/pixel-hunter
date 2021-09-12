import aiohttp_jinja2
import asyncpgsa
import jinja2
from aiohttp import web

from .routes import setup_routes

MB = 1024 ** 2
MAX_POST_SIZE = 10 * MB


async def create_app(config=None):
    app = web.Application(client_max_size=MAX_POST_SIZE)
    app['config'] = config
    aiohttp_jinja2.setup(
        app,
        loader=jinja2.PackageLoader('pixel_hunter', 'templates'),
    )
    setup_routes(app)
    app.on_startup.append(on_start)
    app.on_cleanup.append(on_shutdown)
    return app


async def on_start(app):
    config = app['config']
    app['db'] = await asyncpgsa.create_pool(dsn=config['db_uri'])


async def on_shutdown(app):
    await app['db'].close()
