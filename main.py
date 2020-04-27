from aiohttp import web
from aiohttp_session import session_middleware
from aiohttp_session.cookie_storage import EncryptedCookieStorage
import aiohttp_jinja2
import jinja2

from routes import setup_routes
from middleware import authorize
from db import start_db, close_db
from chat.models import Room


async def on_shutdown(app):
    for ws in app['websockets']:
        await ws.close(code=1001, message='Server shutdown')

async def init_rooms(app):
    sql_query = f"""SELECT * FROM rooms;"""
    await app['db_cursor'].execute(sql_query)
    rooms_in_db = await app['db_cursor'].fetchall()
    for room in rooms_in_db:
        app['rooms'].append(Room(app['db_cursor'], room[1]))
        
    print('rooms has been initialized', app['rooms'])

async def init_app():
    app = web.Application(middlewares=[
        session_middleware(EncryptedCookieStorage(b'Thirty  two  length  bytes  key.')),
        authorize,
    ])
    aiohttp_jinja2.setup(
        app, loader=jinja2.FileSystemLoader('templates'))

    setup_routes(app)
    app['static_root_url'] = 'static'
    app.router.add_static('/static', 'static', name='static')
    app.on_cleanup.append(on_shutdown)
    app.on_cleanup.append(close_db)
    await start_db(app)
    app['websockets'] = []
    app['rooms'] = []
    await init_rooms(app)


    return app

def main():
    app = init_app()
    web.run_app(app)

if __name__ == '__main__':
    main()