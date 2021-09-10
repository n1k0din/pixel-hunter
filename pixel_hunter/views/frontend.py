import hashlib
import io

from PIL import Image
from aiohttp import web
from aiohttp_jinja2 import template
from sqlalchemy import select
from sqlalchemy import insert


from .. import db


@template('index.html')
async def index(request):
    return {}


def rgb_to_hex(rgb):
    r, g, b = rgb
    return '{:02x}{:02x}{:02x}'.format(r, g, b)


def count_colors(image_content):
    buffer = io.BytesIO(image_content)
    image = Image.open(buffer)
    width, height = image.size
    rgb_image = image.convert('RGB')

    colors_counter = {}

    for x in range(width):
        for y in range(height):
            rgb = rgb_image.getpixel((x, y))
            hex_rgb = rgb_to_hex(rgb)
            if hex_rgb in colors_counter:
                colors_counter[hex_rgb] += 1
            else:
                colors_counter[hex_rgb] = 0

    return colors_counter


async def upload_image(request):
    post = await request.post()
    image = post.get('image')

    if image:
        image_content = image.file.read()
        hash = hashlib.sha224(image_content).hexdigest()

        async with request.app['db'].acquire() as conn:
            query = select([db.image_color]).where(db.image_color.c.id == hash)
            result = await conn.fetch(query)

            if result:
                colors = dict(result[0])['colors']
                return web.Response(body=hash)

        colors = count_colors(image_content)
        stmt = insert(db.image_color).values({'id': hash, 'colors': colors})

        async with request.app['db'].acquire() as conn:
            await conn.execute(stmt, hash, str(colors))
            return web.Response(text=hash)

    return web.Response(text='Nothing happened')


async def is_black_or_white_more(request):
    hash = request.match_info['hash']

    async with request.app['db'].acquire() as conn:
        query = select(db.image_color).filter_by(id=hash)
        result = await conn.fetch(query)

        if result:
            colors = dict(result[0])['colors']
            return web.Response(body=str(colors))

    return web.Response(text='Not found!')
