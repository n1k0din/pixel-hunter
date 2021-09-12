import logging

import aiohttp
import argparse


from pixel_hunter import create_app
from pixel_hunter.settings import load_config


parser = argparse.ArgumentParser()
parser.add_argument('--host', help='Hostname', default='0.0.0.0')
parser.add_argument('--port', help='Port', default=8080)
parser.add_argument('-c', '--config', type=argparse.FileType('r'), help='Path to config file')

args = parser.parse_args()

app = create_app(config=load_config(args.config))

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')
    aiohttp.web.run_app(app, host=args.host, port=args.port, access_log=None)
