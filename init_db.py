from config import dbconf
import asyncio
import aiopg


if __name__ == "__main__":
    async def init_db():
        connection = await aiopg.connect(**dbconf)
        cursor = await connection.cursor()

#         sql_query = """CREATE TABLE users(
#   id SERIAL PRIMARY KEY,
#   login VARCHAR(64),
#   password VARCHAR(64));
# """
#         await cursor.execute(sql_query)

#         sql_query = """CREATE TABLE messages(
#   id SERIAL PRIMARY KEY,
#   room_id SMALLINT,
#   user_login VARCHAR(64),
#   text TEXT,
#   datetime TIMESTAMP);
# """
#         await cursor.execute(sql_query)

#         sql_query = """CREATE TABLE rooms(
#   id SERIAL PRIMARY KEY,
#   name VARCHAR(64));
# """
#         await cursor.execute(sql_query)

        sql_query = """CREATE TABLE messages(
  id SERIAL PRIMARY KEY,
  room_id integer references rooms(id),
  user_id integer references users(id),
  text TEXT,
  datetime TIMESTAMP);
"""
        await cursor.execute(sql_query)
        

        
        print(f'SRV: db initializated')

    loop = asyncio.get_event_loop()
    loop.run_until_complete(init_db())


