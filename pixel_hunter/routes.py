from aiohttp import web

from .views import frontend


def setup_routes(app):
    config = app['config']

    app.router.add_route('GET', '/', frontend.index)
    app.router.add_route('POST', '/', frontend.upload_image_get_colors)
    if 'static_dir' in config:
        app.add_routes([web.static('/static', config['static_dir'])])
