import hashlib
import io
import json
from collections import defaultdict

from PIL import Image
from aiohttp_jinja2 import template, render_template
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

    colors_counter = defaultdict(int)

    for x in range(width):
        for y in range(height):
            rgb = rgb_image.getpixel((x, y))
            hex_rgb = rgb_to_hex(rgb)
            colors_counter[hex_rgb] += 1

    return colors_counter


async def process_image(request, image):
    if image:
        image_content = image.file.read()
        hash = hashlib.sha224(image_content).hexdigest()

        async with request.app['db'].acquire() as conn:
            query = select([db.image_color]).where(db.image_color.c.id == hash)
            result = await conn.fetch(query)

            if result:
                return json.loads(dict(result[0])['colors'])

        colors = count_colors(image_content)

        statement = insert(db.image_color).values({'id': hash, 'colors': colors})

        async with request.app['db'].acquire() as conn:
            await conn.execute(statement, hash, str(colors))
            return colors


async def upload_image_get_colors(request):
    post = await request.post()
    image = post.get('image')

    if not image:
        return render_template('index.html', request, context={'error': 'Image is required!'})

    colors_counter = await process_image(request, image)

    context = {}

    if colors_counter:
        context['is_submited'] = True

    bw = post.get('bw')
    color = post.get('color')

    if bw:
        context['blacks_or_whites'] = get_blacks_or_whites_more(colors_counter)

    if color:
        color_key = color.lstrip('#').lower()        
        context['color_amount'] = {
            'color': color,
            'amount': get_hex_color_amount(colors_counter, color_key),
        }

    return render_template('index.html', request, context=context)


def get_blacks_or_whites_more(colors_counter, black='000000', white='ffffff'):
    if colors_counter.get(black, 0) == colors_counter.get(white, 0):
        return 'same'

    return 'blacks' if colors_counter[black] > colors_counter[white] else 'whites'


def get_hex_color_amount(colors_counter, color):
    return colors_counter.get(color, 0)
