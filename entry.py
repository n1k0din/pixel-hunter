import aiohttp
import argparse
import asyncio

try:
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except ImportError:
    print('uvloop is not available')

from pixel_hunter import create_app


parser = argparse.ArgumentParser()
parser.add_argument('--host', help='Hostname', default='0.0.0.0')
parser.add_argument('--port', help='Port', default=8080)
parser.add_argument('--reload', action='store_true', help='Reload parameters')

args = parser.parse_args()

app = create_app()

if args.reload:
    print('Start with code reload')
    import aioreloader
    aioreloader.start()


if __name__ == '__main__':
    aiohttp.web.run_app(app, host=args.host, port=args.port)
