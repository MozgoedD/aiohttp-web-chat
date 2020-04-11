from aiohttp import web
from aiohttp_session import session_middleware
from aiohttp_session.cookie_storage import EncryptedCookieStorage
import aiohttp_jinja2
import jinja2

from routes import setup_routes
from middleware import authorize


async def on_shutdown(app):
    for ws in app['websockets']:
        await ws.close(code=1001, message='Server shutdown')

async def init_app():
    app = web.Application(middlewares=[
        session_middleware(EncryptedCookieStorage(b'Thirty  two  length  bytes  key.')),
        authorize,
    ])
    aiohttp_jinja2.setup(
        app, loader=jinja2.FileSystemLoader('templates'))

    setup_routes(app)
    app['static_root_url'] = '/static'
    app.router.add_static('/static', 'static', name='static')
    app.on_cleanup.append(on_shutdown)
    app['websockets'] = []

    return app

def main():
    app = init_app()
    web.run_app(app)

if __name__ == '__main__':
    main()