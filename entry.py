import asyncio
import aiohttp

try:
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except ImportError:
    print('uvloop is not available')


from pixel_hunter import create_app


app = create_app()

if __name__ == '__main__':
    aiohttp.web.run_app(app)
