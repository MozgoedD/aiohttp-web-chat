import asyncio
import aiopg
from config import dbconf


async def start_db(app):
    connection = await aiopg.connect(**dbconf)
    cursor = await connection.cursor()
    app['db_cursor'] = cursor
    app['db_connection'] = connection
    print(f'SRV: start db \n')



async def close_db(app):
    app['db_cursor'].close()
    app['db_connection'].close()