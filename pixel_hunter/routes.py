from .views import frontend


def setup_routes(app):
    app.router.add_route('GET', '/', frontend.index)
    app.router.add_route('POST', '/upload_image', frontend.upload_image)
    app.router.add_route('GET', '/is_black_or_white_more/{hash}', frontend.is_black_or_white_more)
